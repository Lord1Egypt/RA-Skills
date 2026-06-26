#!/usr/bin/env python3
import argparse
import os
from pathlib import Path
import requests


API_URL = 'https://api.ltx.video/v1/text-to-video'


def main():
    ap = argparse.ArgumentParser(description='Generate vertical video with LTX text-to-video API')
    ap.add_argument('--prompt', required=True)
    ap.add_argument('--output', required=True)
    ap.add_argument('--model', default='ltx-2-3-fast')
    ap.add_argument('--duration', type=int, default=8, choices=[6, 8, 10, 12, 14, 16, 18, 20])
    ap.add_argument('--resolution', default='1080x1920')
    args = ap.parse_args()

    api_key = os.getenv('LTX_API_KEY')
    if not api_key:
        raise SystemExit('Missing LTX_API_KEY in environment')

    payload = {
        'prompt': args.prompt,
        'model': args.model,
        'duration': args.duration,
        'resolution': args.resolution,
    }
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    r = requests.post(API_URL, json=payload, headers=headers, timeout=600)
    if r.status_code != 200:
        raise SystemExit(f'LTX request failed: {r.status_code} {r.text}')

    out = Path(args.output)
    out.write_bytes(r.content)
    print(str(out))


if __name__ == '__main__':
    main()
