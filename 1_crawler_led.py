# from webdriver_manager.chrome import ChromeDriverManager   #-------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
# from selenium import webdriver
from chromedriver_py import binary_path # This will get you the path variable
import undetected_chromedriver as uc
import time
from datetime import datetime
import json
from dateutil.relativedelta import *
import os
import configure
import sys
import csv
import requests
import pandas as pd

time.sleep(10)

TOKEN_GROUP_ALL = configure.TOKEN_GROUP_ALL


def find_maxdate(province):
    with open(f'../data/{province}_currentlink.json', 'r') as file:
        currentlink = json.load(file)

        return max(list(currentlink.keys()))

def currentstatus2csv(file_path,province,total,isgps):
    # current_date = datetime.now().date()
    current_date = find_maxdate(province)
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=['province', 'date','total','isgps'])

    df['date'] = df['date'].astype(str)
    df2 = df[(df['province']==province) & (df['date']==str(current_date))]

    if df2.shape[0] > 0:
        index  = df2.index[0]
        if total == -1:
            total = df.iloc[index]['total']
        elif isgps == -1:
            isgps = df.iloc[index]['isgps']

        df.iloc[index] = [province, str(current_date),total,isgps]

    else:
        new_row = {'province': province, 'date': current_date, 'total': total,'isgps':isgps}
        # df = df.append(new_row, ignore_index=True)
        try:
            df = df.append(new_row, ignore_index=True)
        except:
            new_row_df = pd.DataFrame([new_row])
            df = pd.concat([df, new_row_df], ignore_index=True)

    df.to_csv('../data/currentstatus.csv', index=False) 

    

# def line_noti(token,msg):
#     url = 'https://notify-api.line.me/api/notify'
#     headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
#     r = requests.post(url, headers=headers, data = {'message':msg})
#     return r.text

def scrolling_down(t):
    for i in range(t):
        driver.execute_script("window.scrollBy(0,2000)","")
        time.sleep(0.5)
        
def get_text(x):
    return driver.find_element(By.XPATH,x).text

def get_herf(x):
    attb = ['href','onclick','src','data-responsive']
    for a in attb:
        v = driver.find_element(By.XPATH,x).get_attribute(a)
        if v:
            break 
    return v

def click(x):
    try:
        driver.find_element(By.XPATH,x).click()
    except:
        # Wait for the <tr> element to be present
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, x)))
        tr_element = driver.find_element(By.XPATH, x)

        # Option 1: Scroll into view using JavaScript
        driver.execute_script("arguments[0].scrollIntoView(true);", tr_element)
        # time.sleep(1)  # Allow time for the scroll

        # Option 2: Try clicking a child element inside <tr> (e.g., <td>)
        child_element = tr_element.find_element(By.TAG_NAME, "td")  # Replace 'td' if the child element is different
        driver.execute_script("arguments[0].scrollIntoView(true);", child_element)
        # time.sleep(1)  # Allow time for the scroll
        child_element.click()



    
def sent_key(x,val):
    driver.find_element(By.XPATH, x).send_keys(val)
    
def clear(x):
    driver.find_element(By.XPATH, x).clear()

def isoDate(b,k):
    if k == 'bit_date':
        bb = b.split('/')
        iso_date = datetime(int(bb[2])-543, int(bb[1]), int(bb[0]), 0, 0, 0, 0)
        # iso_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return iso_date
    elif k == 'announce_date':
        bb = b.split('-')
        iso_date = datetime(int(bb[2])-543, int(bb[1]), int(bb[0]), 0, 0, 0, 0)
        # iso_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return iso_date
    elif k == 'timestamp_date':
        bb = b.split('-')
        iso_date = datetime(int(bb[0]), int(bb[1]), int(bb[2]), 0, 0, 0, 0)
        # iso_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return iso_date

#----------------------------------------------
def detail_row(r):
#     r = 3
    row = {}
    H = ['sell_order','case_id','type','size2','size1','size0','eva_price','tumbon','aumper','province']
    for c,h in enumerate(H):
        t = get_text(f'/html/body/table[3]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[{2+r}]/td[{c+1}]')
        t = t.strip().replace(',','')
        if t.isnumeric():
            t = int(t)
        elif t.replace(".", "").isnumeric():
            t = float(t)
        row[h] = t
    return row

def detail_click(r,d):
#     r = 1
    # D = {}
    D = d
    click(f'/html/body/table[3]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[{2+r}]')
    
    driver.switch_to.window(driver.window_handles[1])
    url = driver.current_url
    # if url == 'about:blank':
    #     time.sleep(2)
    #     url = driver.current_url
    while url == 'about:blank':
        # time.sleep(2)
        url = driver.current_url


    # print('-'*100)
    print('url::',url,type(url))
    # print('='*100)
    
    try:
        element_order = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/b/font/font')))
    except:
        try:
            element_order = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[2]/td/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/b/font/font')))
        except:
            pass

    try:
        deed_number = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[5]/td/font')
        D['deed_number'] = deed_number
    except:
        pass
    try:
        pay_down = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[16]/td/font')
        pay_down = pay_down.replace(',','')
        D['pay_down'] = int(float(pay_down))
    except:
        pass
    try:
        sell_table = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[17]')
        # print(sell_table)
        sell_table
        sell_table = sell_table.split('\n')
        sell_table = [x.split() for x in sell_table]
        sell_table = [[x for x in x if x not in ['นัดที่','วันที่']] for x in sell_table]
        sell_table
        S = {}
        for s in sell_table:
            S[s[0]] = {
                'date' : s[1],
                'sta' : s[2]
            }
        D['sell_table'] = S
    except:
        pass
    try:
        D['status'] = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[18]/td/font')
    except:
        pass
    try:
        EVA_PRICE = ['/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[19]/td/font','/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[20]/td/font','/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[21]/td/font','/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[22]/td/font']
        max_price = []
        for e in EVA_PRICE:
            x = get_text(e)
            max_price.append(x)
        D['max_price'] = max([int(float(x.replace(',',''))) for x in max_price if x.replace(',','').replace('.','').isnumeric()] )
    except:
        pass
    try:
        announce_date = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[23]/td/font')
        D['announce_date'] = announce_date
#         D['announce_date'] = isoDate(announce_date,'announce_date')
    except:
        pass
    img = []
    try:
        img1 = get_herf('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[3]/table/tbody/tr[2]/td/div/a/img')
        img.append(img1)
    except:
        pass
    try:
        img2 = get_herf('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[3]/table/tbody/tr[4]/td/table[1]/tbody/tr/td')
        img2 = 'https://asset.led.go.th' + img2.split(",")[0].split('window.open(')[1].replace("'",'')
        img.append(img2)
    except:
        pass
    if img:
        D['img'] = img
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return url,D
    
def row_crawled(current_page):

    cc = []
    for k in C[dtn].keys():
        if C[dtn][k]:
            cc.append(k)

    # current_page = 2
    # c = [int(x.split('/')[0]) for x in C[dtn].keys() if x.split('/')[1] == str(current_page)]
    c = [int(x.split('/')[0]) for x in cc if x.split('/')[1] == str(current_page)]
    c = set(c)
    # r_crawled = list(set(range(1,51)) - c)
    r_crawled = list(c.intersection(set(range(1,51))))
    print(current_page,r_crawled)
    return r_crawled
#-----------------------------------------
print('start')


if not os.path.exists('../data'):
   os.makedirs('../data')


# Driver ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
chrome_headless = configure.chrome_headless
# driver = uc.Chrome(headless=False,use_subprocess=True)

options = webdriver.FirefoxOptions()
if chrome_headless:
    options.add_argument("--headless")  # Run Firefox in headless mode (no GUI)
driver = webdriver.Firefox(options=options)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


driver.maximize_window()
print('driver.get_window_size()',driver.get_window_size())

province = sys.argv[1]
iteration = sys.argv[2]

configure.line_noti(TOKEN_GROUP_ALL,f'[{province}]Start! 1_crawler_led.py')

configure.write_state('state.csv', province, False)
# province = 'nonthaburi'
search_province = configure.search_province[province][1]

# configure.line_noti(TOKEN_GROUP_ALL,f'process1 start!--->{province}')

#find lastpage
dtn = datetime.now().strftime("%Y%m%d")
# dtn = '20230413'
try:
    with open(f'../data/{province}_currentlink.json', 'r') as openfile:
        C = json.load(openfile)
except:
    C = {}
# print(C)
d = list(C.keys())

#------------------------------
if int(iteration) > 0:
    dtn = d[-1]
#------------------------------

if dtn in d:
    d = max([int(x) for x in d])
    p = C[str(d)].keys()
    last_page = max([int(x.split('/')[-1]) for x in p])
    start_page = last_page
else:
    start_page = 1
print('start_page',start_page)

if configure.START_FIRST_PAGE:
    start_page = 1

p = start_page
url_p = f'https://asset.led.go.th/newbid-old/asset_search_province.asp?search_asset_type_id=&search_tumbol=&search_ampur=&search_province={search_province}&search_sub_province=&search_price_begin=&search_price_end=&search_bid_date=&page={p}'   
driver.get(url_p)
u = '/html/body/table[3]/tbody/tr/td[1]/table[2]/tbody/tr/td[2]/div'
page = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, u)))
page = get_text(u)
current_page,max_page = [int(x) for x in page.split()[-1].split('/')]
total_propertys = int(get_text('/html/body/table[3]/tbody/tr/td[1]/table[2]/tbody/tr/td[2]/div/font'))
print('(current_page,max_page)',current_page,max_page)
print('total_propertys',total_propertys)

print('C.keys()',C.keys())
print('dtn',dtn)
CRAWLED = {}
for i in range(1,max_page+1):
    CRAWLED[i] = []
if dtn in C.keys():
    NEW_DATE = False
    for i in range(1,max_page+1):
        n = row_crawled(i)
        if n:   # and i !=  max_page:
            CRAWLED[i] = n
    print(CRAWLED)
else:
    NEW_DATE = True

print('NEW_DATE',NEW_DATE)
for p in range(1,max_page+1):

    # print(CRAWLED[p])

    if len(CRAWLED[p]) != 50 or NEW_DATE:
        driver.switch_to.window(driver.window_handles[0])
        driver.get(f'https://asset.led.go.th/newbid-old/asset_search_province.asp?search_asset_type_id=&search_tumbol=&search_ampur=&search_province={search_province}&search_sub_province=&search_price_begin=&search_price_end=&search_bid_date=&page={p}')
        
        u = '/html/body/table[3]/tbody/tr/td[1]/table[2]/tbody/tr/td[2]/div'
        page = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, u)))
        page = get_text(u)
        current_page,max_page = [int(x) for x in page.split()[-1].split('/')]
        total_page = int(page.split()[2])
        print(f"\n\n\ncurrent_page {current_page}/max_page {max_page}")

        if current_page%10 == 0:
            configure.line_noti(TOKEN_GROUP_ALL,f'[{province}]current_page:{current_page}/max_page:{max_page}')

        scrolling_down(5)

        for r in range(1,51):
            if r not in CRAWLED[p] or NEW_DATE:
                try:

                    # print(r,'/',p,'-'*20,C[dtn][f'{r}/{p}'])
                    #read exist data
                    try:
                        with open(f'../data/{province}_led.json', 'r') as openfile:
                            D = json.load(openfile)
                    except:
                        D = {} 
                    try:
                        with open(f'../data/{province}_currentlink.json', 'r') as openfile:
                            C = json.load(openfile)
                    except:
                        C = {}
                        
                    #--------------------
                    d = detail_row(r)

                    print(f'\n\n[{r}/50 Page:{p}/{max_page}]' ,'='*100)
                    print(f'detail_row: {d}')

                    url,d = detail_click(r,d)
                    page = f"{r}/{p}"
                    
                    D[url] = d
                    #     'link' : url,
                    #     'data' : d
                    # }
                    
                    print('Detail Property::',D[url])
                    
            #         dtn = datetime.now().strftime("%Y%m%d")
                    if dtn in C.keys():
                        C[dtn][page] = url
                    else:
                        C[dtn] = {
                            page : url
                        }
                    #--------------------
                    #write data
                    with open(f"../data/{province}_led.json", "w") as outfile:
                        outfile.write(json.dumps(D, indent=4))
                    with open(f"../data/{province}_currentlink.json", "w") as outfile:
                        outfile.write(json.dumps(C, indent=4))
                    
                except Exception as  e: 
                    # with open(f"../data/{province}_led.json", "w") as outfile:
                    #     outfile.write(json.dumps(D, indent=4))
                    # with open(f"../data/{province}_currentlink.json", "w") as outfile:
                    #     outfile.write(json.dumps(C, indent=4))

                    print(f'Error : row:{r}/page:{current_page}')
                    # line_noti(TOKEN_GROUP_ALL,f'Error : row:{r}/page:{current_page}')
                    driver.switch_to.window(driver.window_handles[0])

            else:
                pass
                # print(f'row {r}/{p} complete crawl in {dtn}...')
                
    else:
        print(f'page {p} complete crawl in {dtn}...')
# configure.line_noti(TOKEN_GROUP_ALL,f'Finish process1 {province} {page}')
        
        
with open(f'../data/{province}_currentlink.json', 'r') as openfile:
    C = json.load(openfile)

#check if crawl data > 95%
# if len(list(C[dtn].keys())) > (int(max_page)-1)*40:
if len(list(C[dtn].keys())) == total_page:
    configure.write_state('state.csv', province, 'complete')
    configure.line_noti(TOKEN_GROUP_ALL,f'[{province}]Complete! 1_crawler_led={len(list(C[dtn].keys()))}/{total_page}')

    #update current stage
    file_path = '../data/currentstatus.csv'
    # currentstatus2csv(file_path,province,total_propertys,-1)
    currentstatus2csv(file_path,province,f"{len(list(C[dtn].keys()))}/{total_page}",-1)
    
elif (len(list(C[dtn].keys())) / total_page) > 0.95:
    # print('cccc')
    # with open('../data/stage.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['True'])
    configure.write_state('state.csv', province, True)
    configure.line_noti(TOKEN_GROUP_ALL,f'[{province}]Complete! 1_crawler_led={len(list(C[dtn].keys()))}/{total_page}')
    


    #update current stage
    file_path = '../data/currentstatus.csv'
    # currentstatus2csv(file_path,province,total_propertys,-1)
    currentstatus2csv(file_path,province,f"{len(list(C[dtn].keys()))}/{total_page}",-1)

else:
    # print('nnnn')
    configure.write_state('state.csv', province, False)
    configure.line_noti(TOKEN_GROUP_ALL,f'[{province}]Fail! 1_crawler_led={len(list(C[dtn].keys()))}/{total_page}')
            
        

    # with open('../data/stage.csv', 'w', newline='') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['False'])
    #     # line_noti(TOKEN_GROUP_ALL,f'Error : row:{r}/page:{current_page}')
    #     line_noti(TOKEN_GROUP_ALL,f'Write complate stage= False crawler_data={len(list(C[dtn].keys()))} from total={total_page}')
            
        
