#!/usr/bin/env python3
"""Get home timeline"""
import sys
import os
import json
import argparse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_credentials(user_id):
    cred_path = os.path.join(SKILL_DIR, 'credentials', f'{user_id}.json')
    if not os.path.exists(cred_path):
        raise Exception(f"No credentials found for user {user_id}. Configure Twitter credentials first.")
    
    with open(cred_path, 'r') as f:
        creds = json.load(f)
    
    if 'twitter' not in creds:
        raise Exception("Twitter credentials not found")
    
    return creds['twitter']

def get_timeline(user_id, count=20):
    creds = load_credentials(user_id)
    
    import requests
    
    headers = {"Authorization": f"Bearer {creds['bearer_token']}"}
    
    # Get user ID
    me_url = "https://api.twitter.com/2/users/me"
    me_resp = requests.get(me_url, headers=headers)
    user_id_twitter = me_resp.json()['data']['id']
    
    # Get timeline
    url = f"https://api.twitter.com/2/users/{user_id_twitter}/timelines/reverse_chronological?max_results={count}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return {"success": True, "tweets": response.json()}
    else:
        raise Exception(f"Failed to get timeline: {response.status_code} {response.text}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument('--count', type=int, default=20)
    args = parser.parse_args()
    
    try:
        result = get_timeline(args.user_id, args.count)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
