import csv
import sys
import json
from datetime import datetime,date
import pandas as pd
import configure

province = sys.argv[1]

# def find_maxdate(province):
#     with open(f'../data/{province}_currentlink.json', 'r') as file:
#         currentlink = json.load(file)

#         return max(list(currentlink.keys()))


def find_maxdate(province,fromLastCompleteStatus):
    if fromLastCompleteStatus:
        df = pd.read_csv('../data/currentstatus.csv')
        return str(max(list(df[df['province']==province]['date'])))

    else:
        with open(f'../data/{province}_currentlink.json', 'r') as file:
            currentlink = json.load(file)

            return max(list(currentlink.keys()))

def link2deed(l):
    print('l',l)
    if l != 'about:blank':
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

        return d
    else:
        return []
    
def find_last_sta(sell_table):
    dates = []
    stas = []
    discount_factor = 0
    for i in sell_table.keys():
        d = sell_table[i]['date']
        # print('\n\n\n\nd',d)
        a = d.split('/')
        # print('a',a)
        try:
            d = str(int(a[2])-543) + a[1] + a[0]
        
            # print(d,sell_table[i]['sta'])
            dates.append(d)
            stas.append(sell_table[i]['sta'])
        except:
            pass

        if 'ไม่มี' in sell_table[i]['sta']:
            discount_factor += 1
      
    today = date.today()
    today = today.strftime("%Y%m%d")
    
    b = [int(x)-int(today) for x in dates]
    
    print(dates)
    print(b)
    if not dates:
        return None,None,None,None,None
    try:
        idx = b.index(min([x for x in b if x >= 0]))
    except:
        idx = b.index(max(b))
    return dates[idx],stas[idx],dates,idx+1,discount_factor

# READY = False
# with open('../data/stage.csv', mode='r') as file:
#     csv_reader = csv.reader(file)
#     for row in csv_reader:
#         if row[0] == 'True':
#             READY = True

# print(READY)

with open(f'../data/{province}_currentlink.json', 'r') as file:
    currentlink = json.load(file)

with open(f'../data/{province}_led.json', 'r') as file:
    led_data = json.load(file)

df_gps = pd.read_csv(f'../data/{province}_gps.csv')
df_gps['deed'] = df_gps['deed'].astype(str)




# date_now = formatted_date = datetime.now().strftime("%Y%m%d")

# max_date = find_maxdate(province,True)
max_date = find_maxdate(province,False)

# print(date_now)


# print(led_data)

DATAS = []
for page in currentlink[max_date].keys():
    link = currentlink[max_date][page]

    D = led_data[link]
    D['link'] = link
    D['page'] = page
    

    deeds = link2deed(link)
    print(deeds)
    lat = None
    lon = None
    print(list(df_gps['deed']))
    for d in deeds:
        try:
            lat,lon = dict(df_gps[df_gps['deed']==str(d)].iloc[0])['gps'].split(',')
            break
        except:
            pass
            # lat = None
            # lon = None
    print(lat,lon)

    D['lat'] = lat
    D['lon'] = lon
    if 'sell_table' in D.keys():
        D['lastSta_date'], D['lastSta_detail'],D['bid_dates'],D['bid_time'],D['discount_factor'] = find_last_sta(D['sell_table'])
        if 'max_price' in D.keys():

            if D['discount_factor'] > 3:
                D['discount_factor'] = 3

            D['current_price'] = int(D['max_price']*(1-D['discount_factor']*0.1))

    if 'img' in D.keys():
        for  i,im in enumerate(D['img']):
            D[f'img{i}'] = im

    D['timestamp'] = str(datetime.now().strftime("%Y-%m-%d"))

    # print('-'*200)
    # print(D)

    DATAS.append(D)

df = pd.DataFrame(DATAS)
print(df)

df.to_csv(f'../data/df_{province}.csv', index=False)

configure.line_noti(configure.TOKEN_GROUP_ALL,f'[{province}] 3_data2csv.py complete!!!')




# ['sell_order', 'case_id', 'type', 'size2', 'size1', 'size0', 'eva_price', 'tumbon', 'aumper', 'province', 'deed_number', 'pay_down', 'sell_table', 'status', 'max_price', 'announce_date', 'img', 'link', 'page', 'lat', 'lon', 'lastSta_date', 'lastSta_detail', 'bid_dates', 'bid_time', 'discount_factor', 'img0', 'img1']

# sell_order,case_id,deed_number,type,size0,size1,size2,tumbon,aumper,province,pay_down,status,max_price,,lastSta_date,lastSta_detail,bid_dates,bid_time,discount_factor,,img0,img1,imgGP0,imgGP1,link
# # print(x)
# timestamp
# current_price
# print(dict(df_gps[df_gps['deed']=='84048'].iloc[0])['gps'].split(','))


# sell_order,case_id,deed_number,type,size0,size1,size2,tumbon,aumper,province,pay_down,
# lastSta_date,lastSta_detail,bid_dates,bid_time,discount_factor


# status,link

# ,max_price,
# timestamp,
# ,
# ,
# ,
# ,
# ,
# current_price,
# img0,
# img1,
# imgGP0,
# imgGP1,


# {'sell_order': '165 - 1', 'case_id': 'ผบE.750/2565', 'type': 'ห้องชุด', 'size2': 0, 'size1': 0, 'size0': 38.39, 'eva_price': 587367.0, 'tumbon': 'ปากเกร็ด(สีกัน)', 'aumper': 'ปากเกร็ด(ตลาดขวัญ)', 'province': 'นนทบุรี', 'deed_number': '134116, 9373', 'pay_down': 50000, 'sell_table': {'1': {'date': '31/08/2566', 'sta': 'งดขายไม่มีผู้สู้ราคา'}, '2': {'date': '21/09/2566', 'sta': '-'}, '3': {'date': '12/10/2566', 'sta': '-'}, '4': {'date': '02/11/2566', 'sta': '-'}, '5': {'date': '23/11/2566', 'sta': '-'}, '6': {'date': '14/12/2566', 'sta': '-'}}, 'status': 'ปลอดภาระผูกพัน', 'max_price': 587367, 'announce_date': '03-07-2566', 'img': ['https://asset.led.go.th/PPKPicture/2566/06-2566/16/c3-913p.jpg', 'https://asset.led.go.th/PPKPicture/2566/06-2566/16/c3-913j.jpg'], 'link': 'https://asset.led.go.th/newbid-old/asset_open.asp?law_suit_no=%BC%BAE.750&law_suit_year=2565&deed_no=134116,%209373&addrno=3/913', 'page': '33/35', 'lat': '13.90882980', 'lon': '100.55215100'}