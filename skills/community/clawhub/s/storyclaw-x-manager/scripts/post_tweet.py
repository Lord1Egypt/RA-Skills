#!/usr/bin/env python3
"""
X/Twitter Post Tweet Script
Usage: post_tweet.py <USER_ID> "<content>" [--media <path>]
"""
import sys
import os
import json
import argparse

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SKILL_DIR, 'scripts'))

def load_credentials(user_id):
    """Load Twitter credentials for user"""
    cred_path = os.path.join(SKILL_DIR, 'credentials', f'{user_id}.json')
    if not os.path.exists(cred_path):
        raise Exception(f"No credentials found for user {user_id}. Configure Twitter credentials first.")
    
    with open(cred_path, 'r') as f:
        creds = json.load(f)
    
    if 'twitter' not in creds:
        raise Exception("Twitter credentials not found. Please bind X account at storyclaw.com")
    
    return creds['twitter']

def post_tweet(user_id, content, media_path=None):
    """Post a tweet using Twitter API v2"""
    creds = load_credentials(user_id)
    
    # Check for twitter-api-v2 library
    try:
        from twitterv2 import Client
    except ImportError:
        # Fallback to direct API calls
        return post_tweet_direct(creds, content, media_path)
    
    client = Client(creds['bearer_token'], creds['api_key'], creds['api_secret'], 
                    creds['access_token'], creds['access_token_secret'])
    
    media = None
    if media_path and os.path.exists(media_path):
        media = client.create_media(media_path)
    
    tweet = client.create_tweet(text=content, media=media)
    return tweet

def post_tweet_direct(creds, content, media_path=None):
    """Direct API call fallback using requests"""
    import requests
    
    url = "https://api.twitter.com/2/tweets"
    headers = {
        "Authorization": f"Bearer {creds['bearer_token']}",
        "Content-Type": "application/json"
    }
    
    data = {"text": content}
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        raise Exception(f"Failed to post tweet: {response.status_code} {response.text}")

def main():
    parser = argparse.ArgumentParser(description='Post a tweet')
    parser.add_argument('user_id', help='Telegram user ID')
    parser.add_argument('content', help='Tweet content')
    parser.add_argument('--media', help='Media file path')
    
    args = parser.parse_args()
    
    try:
        result = post_tweet(args.user_id, args.content, args.media)
        print(json.dumps({"success": True, "tweet_id": result.get('data', {}).get('id')}))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
