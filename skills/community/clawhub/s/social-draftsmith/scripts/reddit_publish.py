#!/usr/bin/env python3
import argparse
import json
import mimetypes
import os
import sys
import requests
from requests.auth import HTTPBasicAuth

TOKEN_URL = 'https://www.reddit.com/api/v1/access_token'
API_BASE = 'https://oauth.reddit.com'


def get_token():
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    username = os.getenv('REDDIT_USERNAME')
    password = os.getenv('REDDIT_PASSWORD')
    user_agent = os.getenv('REDDIT_USER_AGENT')
    missing = [
        name for name, value in [
            ('REDDIT_CLIENT_ID', client_id),
            ('REDDIT_CLIENT_SECRET', client_secret),
            ('REDDIT_USERNAME', username),
            ('REDDIT_PASSWORD', password),
            ('REDDIT_USER_AGENT', user_agent),
        ] if not value
    ]
    if missing:
        raise RuntimeError('Missing Reddit credentials: ' + ', '.join(missing))

    r = requests.post(
        TOKEN_URL,
        auth=HTTPBasicAuth(client_id, client_secret),
        data={'grant_type': 'password', 'username': username, 'password': password},
        headers={'User-Agent': user_agent},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()['access_token'], user_agent


def main():
    ap = argparse.ArgumentParser(description='Publish to a Reddit subreddit')
    ap.add_argument('--title', required=True)
    ap.add_argument('--text')
    ap.add_argument('--url')
    ap.add_argument('--image-file')
    ap.add_argument('--subreddit')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    subreddit = args.subreddit or os.getenv('REDDIT_DEFAULT_SUBREDDIT')
    if not subreddit:
        print(json.dumps({'error': 'No subreddit provided and REDDIT_DEFAULT_SUBREDDIT not set'}))
        sys.exit(1)

    kind = 'self'
    if args.url:
        kind = 'link'
    elif args.image_file:
        kind = 'image'

    if args.dry_run:
        print(json.dumps({
            'ok': True,
            'mode': 'dry-run',
            'subreddit': subreddit,
            'title': args.title,
            'kind': kind,
            'text': args.text,
            'url': args.url,
            'image_file': args.image_file,
        }, indent=2))
        return

    token, user_agent = get_token()
    headers = {
        'Authorization': f'bearer {token}',
        'User-Agent': user_agent,
    }
    if kind == 'image':
        mime = mimetypes.guess_type(args.image_file)[0] or 'image/jpeg'
        filename = os.path.basename(args.image_file)
        asset_req = requests.post(
            f'{API_BASE}/api/media/asset.json',
            headers=headers,
            data={'filepath': filename, 'mimetype': mime},
            timeout=30,
        )
        asset_req.raise_for_status()
        asset_data = asset_req.json()
        upload_args = asset_data['args']
        asset_id = asset_data['asset']['asset_id']
        upload_url = 'https:' + upload_args['action'] if upload_args['action'].startswith('//') else upload_args['action']
        upload_fields = {item['name']: item['value'] for item in upload_args['fields']}
        with open(args.image_file, 'rb') as f:
            upload_resp = requests.post(upload_url, data=upload_fields, files={'file': f}, timeout=60)
        upload_resp.raise_for_status()

        # Step 1: create a self post
        submit_data = {
            'sr': subreddit,
            'title': args.title,
            'kind': 'self',
            'resubmit': True,
            'api_type': 'json',
            'text': args.text or '',
        }
        submit_resp = requests.post(f'{API_BASE}/api/submit', headers=headers, data=submit_data, timeout=60)
        submit_resp.raise_for_status()
        submit_json = submit_resp.json()

        thing_id = None
        try:
            thing_id = submit_json['json']['data']['name']
        except Exception:
            pass
        if not thing_id:
            print(json.dumps(submit_json, indent=2))
            sys.exit(1)

        # Step 2: replace body with richtext that includes the uploaded image inline
        rtjson = {
            'document': [
                {'e': 'par', 'c': [{'e': 'text', 't': args.text or ''}]},
                {'e': 'img', 'id': asset_id},
            ]
        }
        edit_data = {
            'api_type': 'json',
            'thing_id': thing_id,
            'richtext_json': json.dumps(rtjson),
            'validate_on_submit': 'true',
        }
        r = requests.post(f'{API_BASE}/api/editusertext', headers=headers, data=edit_data, timeout=60)
    else:
        data = {
            'sr': subreddit,
            'title': args.title,
            'kind': kind,
            'resubmit': True,
            'api_type': 'json',
        }
        if kind == 'self':
            data['text'] = args.text or ''
        else:
            data['url'] = args.url
        r = requests.post(f'{API_BASE}/api/submit', headers=headers, data=data, timeout=30)
    try:
        payload = r.json()
    except Exception:
        payload = {'status_code': r.status_code, 'text': r.text}
    print(json.dumps(payload, indent=2))
    if r.status_code >= 400:
        sys.exit(1)


if __name__ == '__main__':
    main()
