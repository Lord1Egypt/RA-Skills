#!/usr/bin/env python3
import argparse
import json
import os
import sys
import requests

GRAPH = 'https://graph.facebook.com/v23.0'


def main():
    ap = argparse.ArgumentParser(description='Publish a post to a Facebook Page')
    ap.add_argument('--message', required=True)
    ap.add_argument('--image-url')
    ap.add_argument('--image-file')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    page_id = os.getenv('FACEBOOK_PAGE_ID')
    token = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
    if not page_id or not token:
        print(json.dumps({'error': 'FACEBOOK_PAGE_ID or FACEBOOK_PAGE_ACCESS_TOKEN not set'}))
        sys.exit(1)

    if args.dry_run:
        print(json.dumps({
            'ok': True,
            'mode': 'dry-run',
            'page_id': page_id,
            'message': args.message,
            'image_url': args.image_url,
            'image_file': args.image_file,
        }, indent=2))
        return

    files = None
    if args.image_file:
        url = f'{GRAPH}/{page_id}/photos'
        data = {
            'caption': args.message,
            'access_token': token,
        }
        files = {
            'source': open(args.image_file, 'rb')
        }
    elif args.image_url:
        url = f'{GRAPH}/{page_id}/photos'
        data = {
            'url': args.image_url,
            'caption': args.message,
            'access_token': token,
        }
    else:
        url = f'{GRAPH}/{page_id}/feed'
        data = {
            'message': args.message,
            'access_token': token,
        }

    r = requests.post(url, data=data, files=files, timeout=30)
    try:
        payload = r.json()
    except Exception:
        payload = {'status_code': r.status_code, 'text': r.text}

    print(json.dumps(payload, indent=2))
    if r.status_code >= 400:
        sys.exit(1)


if __name__ == '__main__':
    main()
