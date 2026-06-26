#!/usr/bin/env python3
"""Get WordPress post via REST API"""
import argparse, json, os, sys, urllib.request
from base64 import b64encode
from security import warn_insecure_wp_url

parser = argparse.ArgumentParser(description='Get WordPress post')
parser.add_argument('--url', default=os.getenv('WP_URL'))
parser.add_argument('--username', default=os.getenv('WP_USERNAME'))
parser.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'))
parser.add_argument('--post-id', required=True, type=int)

args = parser.parse_args()
if not all([args.url, args.username, args.app_password]):
    print(json.dumps({"error": "Missing credentials"}), file=sys.stderr)
    sys.exit(1)
warn_insecure_wp_url(args.url)

api_url = f"{args.url.rstrip('/')}/wp-json/wp/v2/posts/{args.post_id}"
credentials = f"{args.username}:{args.app_password}".encode('utf-8')
auth_header = b64encode(credentials).decode('ascii')

request = urllib.request.Request(api_url)
request.add_header('Authorization', f'Basic {auth_header}')

try:
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode('utf-8'))
        print(json.dumps(result, indent=2))
except Exception as e:
    print(json.dumps({"error": str(e)}), file=sys.stderr)
    sys.exit(1)
