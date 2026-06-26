#!/usr/bin/env python3
"""Search tweets"""
import sys
import os
import json
import argparse
import urllib.parse

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

def search_tweets(user_id, query, count=10):
    creds = load_credentials(user_id)
    
    import requests
    
    headers = {"Authorization": f"Bearer {creds['bearer_token']}"}
    
    # Search tweets (requires Premium/Enterprise)
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.twitter.com/2/tweets/search/recent?query={encoded_query}&max_results={count}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return {"success": True, "results": response.json()}
    elif response.status_code == 403:
        raise Exception("Search requires Premium/Enterprise API. Please upgrade your Twitter API plan.")
    else:
        raise Exception(f"Failed to search: {response.status_code} {response.text}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('user_id')
    parser.add_argument('query')
    parser.add_argument('--count', type=int, default=10)
    args = parser.parse_args()
    
    try:
        result = search_tweets(args.user_id, args.query, args.count)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"success": False, "error": str(e)}))
        sys.exit(1)

if __name__ == '__main__':
    main()
