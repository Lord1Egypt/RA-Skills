#!/usr/bin/env python3
"""Retweet a tweet"""
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

def retweet(user_id, tweet_id):
    creds = load_credentials(user_id)
    
    import requests
    
    # Get user ID
    me_url = "https://api.twitter.com/2/users/me"
    headers = {"Authorization": f"Bearer {creds['bearer_token']}"}
    me_resp = requests.get(me_url, headers=headers)
    user_id_twitter = me_resp.json()['data']['id']
    
    url = f"https://api.twitter.com/2/users/{user_id_twitter}/retweets"
    data = {"tweet_id": tweet_id}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        return {"success": True}
    else:
        raise Exception(f"Failed to retweet: {response.status_code} {response.text}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument('tweet_id')
    args = parser.parse_args()
    
    try:
        result = retweet(args.user_id, args.tweet_id)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
