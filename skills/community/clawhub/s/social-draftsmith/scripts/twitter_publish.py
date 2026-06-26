#!/usr/bin/env python3
import argparse
import json
import os
import sys
import requests
from requests_oauthlib import OAuth1

API_BASE = 'https://api.twitter.com/2'
UPLOAD_BASE = 'https://upload.twitter.com/1.1'


def main():
    ap = argparse.ArgumentParser(description='Publish a post to X/Twitter')
    ap.add_argument('--text', required=True)
    ap.add_argument('--image-file')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    api_key = os.getenv('TWITTER_API_KEY')
    api_secret = os.getenv('TWITTER_API_SECRET')
    access_token = os.getenv('TWITTER_ACCESS_TOKEN')
    access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
    missing = [
        name for name, value in [
            ('TWITTER_API_KEY', api_key),
            ('TWITTER_API_SECRET', api_secret),
            ('TWITTER_ACCESS_TOKEN', access_token),
            ('TWITTER_ACCESS_TOKEN_SECRET', access_token_secret),
        ] if not value
    ]
    if missing:
        print(json.dumps({'error': 'Missing X credentials', 'missing': missing}))
        sys.exit(1)

    if args.dry_run:
        print(json.dumps({
            'ok': True,
            'mode': 'dry-run',
            'text': args.text,
            'image_file': args.image_file,
            'auth': 'oauth1-user-context',
        }, indent=2))
        return

    auth = OAuth1(api_key, api_secret, access_token, access_token_secret)
    media_ids = []
    if args.image_file:
        with open(args.image_file, 'rb') as f:
            upload = requests.post(f'{UPLOAD_BASE}/media/upload.json', auth=auth, files={'media': f}, timeout=60)
        upload_data = upload.json()
        if upload.status_code >= 400 or 'media_id_string' not in upload_data:
            print(json.dumps(upload_data, indent=2))
            sys.exit(1)
        media_ids.append(upload_data['media_id_string'])

    payload = {'text': args.text}
    if media_ids:
        payload['media'] = {'media_ids': media_ids}
    r = requests.post(f'{API_BASE}/tweets', auth=auth, json=payload, timeout=30)
    try:
        data = r.json()
    except Exception:
        data = {'status_code': r.status_code, 'text': r.text}
    print(json.dumps(data, indent=2))
    if r.status_code >= 400:
        sys.exit(1)


if __name__ == '__main__':
    main()
