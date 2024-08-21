from datetime import datetime, timedelta
import requests
import json
import pandas as pd

# a dictonary of your credentials and API key will need to be provided
# using the following format
# cred1 = {
#   "subdomain": "yourzdsubdomain",
#   "email": "ZDadmin@yourorg.com",
#   "api_token": "example_api_key"
#  }

# create active date variable
active_date = (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')

def get_inactive_users(credentials, active_date=active_date):

    subdomain, email, api_token = credentials["subdomain"], credentials["email"], credentials["api_token"]

    auth = (email + "/token", api_token)
    api_endpoint = f'https://{subdomain}.zendesk.com/api/v2/users'
    agent_endpoint = f'{api_endpoint}?role=agent'

    all_users = []

    while agent_endpoint:
        r = requests.get(agent_endpoint, auth=auth)
        
        if r.status_code != 200:
            print(f"Failed to fetch data: Status code {r.status_code}")
            print(r.text)  # Print the full response for debugging
            break
        
        data = r.json()

        if 'users' in data:
            all_users.extend(data['users'])
            agent_endpoint = data.get('next_page')
        else:
            print("Key 'users' not found in the response.")
            print(data)  # Print the full response for debugging
            break

    df = pd.DataFrame(all_users)
    df['last_login'] = pd.to_datetime(df['last_login_at'])

    # this section finds inactive users and users that have never logged in
    inactive_users = df[df['last_login'] < active_date]
    inactive_users = pd.concat([inactive_users, df[df['last_login'].isnull()]])
    inactive_users[['id','name','email','last_login']]

    print(f"Found {inactive_users.shape[0]} inactive users on subdomain {subdomain}")

    for user_id in inactive_users['id']:
        print(f"Downgrading user {api_endpoint}/{user_id}.json")
        r = requests.put(f'{api_endpoint}/{user_id}.json', auth=auth, data=json.dumps({'user': {'role': 'end-user'}}), headers={'content-type': 'application/json'})
        print(r.status_code, r.json())

#example over one set of credentials
#get_inactive_users(credentials)

#example over a list of dictionary credemtials 
#all_crednetials = [cred1, cred2, cred3]
#for credentials in all_credentials:
#    get_inactive_users(credentials)
