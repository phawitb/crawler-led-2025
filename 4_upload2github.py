from github import Github
import sys
import pandas as pd
from datetime import datetime
import os
import json
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
    
def currentstatus2csv(file_path,province,total,isgps):
    # current_date = datetime.now().date()
    # current_date = find_maxdate(province,True)
    current_date = find_maxdate(province,False)
    
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


def upload_file_to_github(file_path, repo_name, file_name, branch_name, github_token):
    g = Github(github_token)
    repo = g.get_repo(repo_name)

    try:
        existing_file = repo.get_contents(file_name, ref=branch_name)
        file_exists = True
        sha = existing_file.sha
    except:
        file_exists = False

    with open(file_path, 'rb') as file:
        content = file.read()

    if file_exists:
        repo.update_file(file_name, f'Update {file_name}', content, sha, branch_name)
        print(f'Successfully updated {file_name} in {repo_name}/{branch_name}')
    else:
        repo.create_file(file_name, f'Add {file_name}', content, branch_name)
        print(f'Successfully uploaded {file_name} to {repo_name}/{branch_name}')
        
# province = 'songkhla'
file_path = f'../data/df_{province}.csv'
repo_name = 'phawitb/crawler-led3-window'
file_name = f'df_{province}.csv'  
branch_name = 'main' 

github_token = 'xxxx' #-----------------------------------------------

upload_file_to_github(file_path, repo_name, file_name, branch_name, github_token)

df = pd.read_csv(file_path)
# print("df['lat'].isnull().sum()",df['lat'].isnull().sum())
# print('df.shape[0]',df.shape[0])
isgps = f"{df.shape[0] - df['lat'].isnull().sum()}/{df.shape[0]}"

configure.line_noti(configure.TOKEN_GROUP_ALL,f'[{province}] Finish! 2_find_gps>>>>>{isgps}')

file_path = '../data/currentstatus.csv'
file_name = f'currentstage.csv'

currentstatus2csv(file_path,province,-1,isgps)
upload_file_to_github(file_path, repo_name, file_name, branch_name, github_token)

configure.line_noti(configure.TOKEN_GROUP_ALL,f'[{province}] 4_upload2github.py complete!!!')