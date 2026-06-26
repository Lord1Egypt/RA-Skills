#!/usr/bin/env python3
"""Reply to a tweet"""
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

def reply_tweet(user_id, tweet_id, content):
    creds = load_credentials(user_id)
    
    import requests
    
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {creds['bearer_token']}",
        "Content-Type": "application/json"
    }
    
    data = {
        "text": content,
        "reply": {"in_reply_to_tweet_id": tweet_id}
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return {"success": True, "tweet_id": response.json()['data']['id']}
    else:
        raise Exception(f"Failed to reply: {response.status_code} {response.text}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument('tweet_id')
    parser.add_argument('content')
    args = parser.parse_args()
    
    try:
        result = reply_tweet(args.user_id, args.tweet_id, args.content)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
