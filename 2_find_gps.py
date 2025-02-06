# from webdriver_manager.chrome import ChromeDriverManager   #-------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import json
from dateutil.relativedelta import *
import os
from selenium.webdriver.support.ui import Select
import configure
import sys
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests
import re
import pandas as pd
from chromedriver_py import binary_path
import random

import undetected_chromedriver as uc

time.sleep(10)

# TOKEN_GROUP_ALL = '1hZqXJ1UwUlSD2eIIMjnobPb5PkoQIKT70Y0IR5SAzt'
TOKEN_GROUP_ALL = configure.TOKEN_GROUP_ALL

def link2deed(l):
    try:
        print('l',l)
        d = l.split('deed_no=')[1].split('&')[0]
        print(d)
        d = d.replace('%20',',')
        d = d.replace('(',',')
        d = d.replace('.',',')
        d = d.split(',')
        # d = [x.replace('%20','') for x in d]
        d = [x.split('%')[0] for x in d]
        d = [x.replace('(','') for x in d]
        d = [x.split('-')[0] for x in d]
        d = [x for x in d if x and len(x)>2]

        d = [str(x) for x in d]

        return d
    except:
        return []
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
    attb = ['href','onclick','src']
    for a in attb:
        v = driver.find_element(By.XPATH,x).get_attribute(a)
        if v:
            break 
    return v

def click(x):
    driver.find_element(By.XPATH,x).click()
    
def sent_key(x,val):
    driver.find_element(By.XPATH, x).send_keys(val)
    
def clear(x):
    driver.find_element(By.XPATH, x).clear()
    

# def select_scroll(x,val):
#     #     x = '/html/body/nav/form[1]/div/select'
#         element= Select(driver.find_element(By.XPATH,x))
#         element.select_by_visible_text(val)   # ddelement.select_by_value('12')

def select_scroll(x, val):
    try:
        # Wait for the modal to disappear
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-backdrop"))
        )
        
        # Scroll into view
        element = driver.find_element(By.XPATH, x)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        
        # Interact with the dropdown
        select = Select(element)
        select.select_by_visible_text(val)
    except Exception as e:
        print(f"Error: {e}")
        
def list_aumphers(province):
    # //*[@id="cbprovince"]
    # //*[@id="cbprovince"]
    # /html/body/nav/form[1]/div
    x_select_provinces = '//*[@id="cbprovince"]' # '/html/body/nav/form[1]/div/select'
    provinces = get_text(x_select_provinces).split('\n')[1:]
    print('provinces',provinces)
    aumphers = []
    if province in provinces:
        print('provincezz',province)
        select_scroll(x_select_provinces,province)
        aumphers = get_text('/html/body/nav/form[2]/div/select').split('\n')[1:]
    return aumphers
        
def find_gps(thai_province,aumper,deed_no):
    def read_box():
        data = {}
        L = ['deed_id','page_explor','land_id','position','tumbon','aumpher','province','area','eva_price','gps']
        for i,l in enumerate(L):
            
            # driver.implicitly_wait(10)
            start = time.time()
            d = None
            while not d and time.time()-start < 10:
                d = get_text(f'/html/body/div[1]/div[3]/span/div/div[2]/div[2]/div/div[2]/div[{i+1}]/div[2]')
#                 print(d)
                data[l] = d

        return data

    thai_province = configure.search_province[province][0]  #++++++++++++++++++++

    if thai_province == 'กรุงเทพฯ':
        thai_province = 'กรุงเทพมหานคร'
    if 'เมือง' in aumper:
        aumper = 'เมือง'
    if '(' in aumper:
        aumper = aumper.replace('(',' ').replace(')','').split()
    else:
        aumper = [aumper]
    aumper = [x.strip() for x in aumper]
    print('aumper',aumper)

    if thai_province not in aumphers.keys():
        aumphers[thai_province] = list_aumphers(thai_province)
        
#     print('aumphers[thai_province] ',aumphers[thai_province] )

    aums = []
    for a in aumper:
        aums += [x for x in aumphers[thai_province] if a in x]
    #     aums += 
    print('aums',aums)

    input_list = aumphers[thai_province]
    selected_elements = aums
    aums = [x for x in selected_elements if x in input_list] + [x for x in input_list if x not in selected_elements]

    for aumper in aums:
        print(thai_province,aumper)
        try:
            select_scroll('/html/body/nav/form[1]/div/select',thai_province)
            select_scroll('/html/body/nav/form[2]/div/select',aumper)

            clear('/html/body/nav/form[3]/span/input')
            sent_key('/html/body/nav/form[3]/span/input',deed_no)

            click('/html/body/nav/form[4]/button')
            time.sleep(2)
            box = read_box()
        #     click('/html/body/div[1]/div[3]/span/div/div[1]/button')
            return box
        except Exception as e:
            print('e',e)
            # pass
    return None


#---------------------------------------------------------------
# province = 'nonthaburi'
province = sys.argv[1]

configure.line_noti(TOKEN_GROUP_ALL,f'[{province}] 2_find_gps start!----')

thai_province = configure.search_province[province][0]



# Driver ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
chrome_headless = configure.chrome_headless
# driver = uc.Chrome(headless=False,use_subprocess=True)

options = webdriver.FirefoxOptions()
if chrome_headless:
    options.add_argument("--headless")  # Run Firefox in headless mode (no GUI)
driver = webdriver.Firefox(options=options)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


driver.maximize_window()

# driver.maximize_window()
print('driver.get_window_size()',driver.get_window_size())

driver.get('https://landsmaps.dol.go.th/')

try:
    # u = '/html/body/div[25]/div/div/div/div[1]/button/i'
    u = '/html/body/div[25]/div/div/div/div[3]/button'
    element_order = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,u)))
    # time.sleep()
    # driver.find_element(By.XPATH,u).click()
    time.sleep(10)
    click(u)
except:
    pass

print('thai_province',thai_province)
aumphers = {}
aumphers[thai_province] = list_aumphers(thai_province)
print('aumphers',aumphers)


with open(f"../data/{province}_led.json", 'r') as json_file:
    data = json.load(json_file)

try:
    df = pd.read_csv(f"../data/{province}_gps.csv")
    df['deed'] = df['deed'].astype(str)
    exist_gps = list(df['deed'])
except:
    exist_gps = []

print('exist_gps',len(exist_gps),exist_gps)


no_gps = []
for l in data.keys():
    if l != 'null':
        d = link2deed(l)

        print(d,data[l]['aumper'],data[l]['province'])
        print('nooooo',d)
        if not set(d).intersection(set(exist_gps)):
            # ag = {'thai_province':data[l]['province'],'aumper':data[l]['aumper'],'d':d}
            ag = {'thai_province':data[l]['province'],'aumper':data[l]['aumper'],'d':d,'size0':data[l]['size0'],'size1':data[l]['size1'],'size2':data[l]['size2'],'type':data[l]['type']}
            no_gps.append(ag)
# print(no_gps)
print('nogps',len(no_gps),no_gps)
# no_gps.reverse()
random.shuffle(no_gps)

for i,x in enumerate(no_gps):
    if i % len(no_gps)==200:
        configure.line_noti(TOKEN_GROUP_ALL,f'[{province}] 2_find_gps>>>>>{i}/{len(no_gps)}')

    print(f"\n{i}/{len(no_gps)}",'#'*200)
    print(x['thai_province'],x['aumper'],x['d'])
    for dd in x['d']:
        a = find_gps(x['thai_province'],x['aumper'],dd)

        print(dd,'='*100)
        # print("x['aumper']",x['aumper'])
        # print('a',a)
        # print('x',x)
        # print('-='*10)

        if a:
            #find box_area, led_area
            box_area = a['area'].split()
            box_area = [box_area[0],box_area[2],box_area[4]]
            box_area = [float(x) for x in box_area]
        
            led_area = [x['size2'],x['size1'],x['size0']]
            led_area = [float(x) for x in led_area]
            # print('-'*100)
            print('-'*70)
            print('box_area,led_area',box_area,led_area)
            print("a['aumpher'], x['aumper'],x['type']",a['aumpher'], x['aumper'],x['type'])
            # print('led_area',led_area)
            

            # if box_area==led_area:
            # if (box_area==led_area and x['aumper']==a['aumpher']) or (x['type'] == 'ห้องชุด' and x['aumper']==a['aumpher']): #---------------------
            # if (box_area==led_area and a['aumpher'] in x['aumper']) or (x['type'] == 'ห้องชุด' and a['aumpher'] in x['aumper']): #---------------------
            if (box_area==led_area and a['aumpher'] in x['aumper']) or (box_area==led_area and x['aumper'] in a['aumpher']) or (x['type'] == 'ห้องชุด' and a['aumpher'] in x['aumper']) or (x['type'] == 'ห้องชุด' and x['aumper'] in a['aumpher']): #---------------------
            
                print('type',x['type'])
                print('match!',"+"*150)
                # try:
                #     with open(f'../data/{province}_gps_data.json', 'r') as openfile:
                #         gps_data = json.load(openfile)
                # except:
                #     gps_data = {}

                a['deed'] = str(dd)
                # print('='*20)
                # # print(x['d'])
                # print(a)

                # try:
                file_path = f"../data/{province}_gps.csv"
                if os.path.exists(file_path):
                    df = pd.read_csv(file_path)
                    print(df.shape)
                    
                    # Check if the row exists
                    deed_to_check = dd
                    aumpher_to_check = x['aumper']
                    print('deed_to_check,aumpher_to_check',deed_to_check,aumpher_to_check)
                    exists = df[(df['deed'].astype(str) == str(deed_to_check)) & (df['aumpher'] == aumpher_to_check)].shape[0] > 0

                    print('exists',exists)

                    if not exists:
                        
                        df.loc[len(df)] = a
                        df.to_csv(file_path, index=False)
                else:
                    df = pd.DataFrame([a])
                    df.to_csv(file_path, index=False)

                # print(len(gps_data.keys()))

                # # line_noti(TOKEN_GROUP_ALL,f'find GPS from website,{a}')
                # print(f'find GPS from website,{a}')
                # gps_data[str(d)] = a
                # with open(f"../data/{province}_gps_data.json", "w") as outfile:
                #     outfile.write(json.dumps(gps_data, indent=4))
            else:
                print('box_area!=led_area',box_area,led_area)
                # line_noti(TOKEN_GROUP_ALL,f'Not find gps from website,{a}')
        else:
                print('NO BOX! Not find gps from website',a)
























# print('exist_gps',len(exist_gps))
# print('current_gps',len(current_gps))
# no_gps = set(current_gps)-set(exist_gps)
# no_gps = [str(x) for x in no_gps]
# no_gps = [x.split(' ')[0] for x in no_gps]
# no_gps = [x.split('(')[0] for x in no_gps]
# no_gps = [re.sub(r"\D", "", x) for x in no_gps]

# print(no_gps)
# print('no_gps',len(no_gps))

# for x in 



#             print(d)
#             if d in exist_gps:
#                 print('exist gps')
#             else:
#     #             print('not exist gps',province,d,data[p]['data']['aumper'])
#                 thai_province = data[k]['province'].strip()
#                 aumper = data[k]['aumper']
#                 print(d,'thai_province',thai_province,'aumper',aumper)
#                 a = find_gps(thai_province,aumper,d)
#                 if a:
#                     try:
#                         with open(f'../data/{province}_gps_data.json', 'r') as openfile:
#                             gps_data = json.load(openfile)
#                     except:
#                         gps_data = {}

#                     print('='*20)
#                     print(len(gps_data.keys()))

#                     # line_noti(TOKEN_GROUP_ALL,f'find GPS from website,{a}')
#                     print(f'find GPS from website,{a}')
#                     gps_data[str(d)] = a
#                     with open(f"../data/{province}_gps_data.json", "w") as outfile:
#                         outfile.write(json.dumps(gps_data, indent=4))
#                 else:
#                     print('Not find gps from website',a)
#                     # line_noti(TOKEN_GROUP_ALL,f'Not find gps from website,{a}')
#     else:
#         # line_noti(TOKEN_GROUP_ALL,f'Not have deed number {k}')
#         pass

        
# line_noti(TOKEN_GROUP_ALL,f'Finish process2')
