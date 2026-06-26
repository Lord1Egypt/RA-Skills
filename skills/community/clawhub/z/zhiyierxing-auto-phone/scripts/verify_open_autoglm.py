#!/usr/bin/env python3
import argparse
import json
import sys
import urllib.request


def post_json(url, payload, headers):
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = resp.read().decode('utf-8', errors='replace')
        return resp.status, body


def main():
    # This script should be executed from the repo-local .venv used by the skill.
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', required=True)
    p.add_argument('--model', required=True)
    p.add_argument('--apikey', default='')
    p.add_argument('--task', default='打开美团搜索附近的火锅店')
    args = p.parse_args()

    base = args.base_url.rstrip('/')
    url = base + '/chat/completions'
    headers = {'Content-Type': 'application/json'}
    if args.apikey:
        headers['Authorization'] = f'Bearer {args.apikey}'

    payload = {
        'model': args.model,
        'messages': [
            {'role': 'user', 'content': args.task}
        ],
        'temperature': 0.1,
        'max_tokens': 1024
    }

    try:
        status, body = post_json(url, payload, headers)
        print(f'[ok] HTTP {status}')
        print(body[:4000])
    except Exception as e:
        print(f'[error] endpoint verification failed: {e}')
        print('Check: base-url, model, apikey, service health, and OpenAI-compatible /v1 endpoint.')
        sys.exit(1)


if __name__ == '__main__':
    main()
