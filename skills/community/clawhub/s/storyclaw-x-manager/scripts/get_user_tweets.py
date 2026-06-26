#!/usr/bin/env python3
"""Get user tweets"""
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

def get_user_tweets(user_id, handle, count=10):
    creds = load_credentials(user_id)
    
    import requests
    
    headers = {"Authorization": f"Bearer {creds['bearer_token']}"}
    
    # Get user ID from handle
    user_url = f"https://api.twitter.com/2/users/by/username/{handle}"
    user_resp = requests.get(user_url, headers=headers)
    if user_resp.status_code != 200:
        raise Exception(f"User not found: {handle}")
    
    twitter_user_id = user_resp.json()['data']['id']
    
    # Get tweets
    tweets_url = f"https://api.twitter.com/2/users/{twitter_user_id}/tweets?max_results={count}"
    response = requests.get(tweets_url, headers=headers)
    
    if response.status_code == 200:
        return {"success": True, "tweets": response.json()}
    else:
        raise Exception(f"Failed to get tweets: {response.status_code} {response.text}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument('handle')
    parser.add_argument('--count', type=int, default=10)
    args = parser.parse_args()
    
    try:
        result = get_user_tweets(args.user_id, args.handle, args.count)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
