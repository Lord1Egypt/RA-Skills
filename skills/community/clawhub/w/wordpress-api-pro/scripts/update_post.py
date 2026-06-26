#!/usr/bin/env python3
"""
Update WordPress post via REST API

Usage:
    python3 update_post.py --post-id 123 --content "New content" --title "New Title"
    
Environment variables:
    WP_URL - WordPress site URL
    WP_USERNAME - WordPress username  
    WP_APP_PASSWORD - Application Password
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from base64 import b64encode

from security import SafetyError, TEXT_MAX_BYTES, die_safety, validate_local_file, warn_insecure_wp_url, should_confirm_publish

def update_post(url, username, app_credential, post_id, **updates):
    """Update WordPress post via REST API"""
    
    # Build API endpoint
    api_url = f"{url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
    
    # Prepare auth header
    credentials = f"{username}:{app_credential}".encode('utf-8')
    auth_header = b64encode(credentials).decode('ascii')
    
    # Build request data
    data = {}
    if 'content' in updates and updates['content']:
        data['content'] = updates['content']
    if 'title' in updates and updates['title']:
        data['title'] = updates['title']
    if 'status' in updates and updates['status']:
        data['status'] = updates['status']
    if 'featured_media' in updates and updates['featured_media']:
        data['featured_media'] = int(updates['featured_media'])
    if 'meta' in updates and updates['meta']:
        data['meta'] = updates['meta']
    
    if not data:
        print(json.dumps({"error": "No updates provided"}), file=sys.stderr)
        sys.exit(1)
    
    # Make request
    request = urllib.request.Request(
        api_url,
        data=json.dumps(data).encode('utf-8'),
        method='POST'
    )
    request.add_header('Authorization', f'Basic {auth_header}')
    request.add_header('Content-Type', 'application/json')
    
    try:
        with urllib.request.urlopen(request) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(json.dumps(result, indent=2))
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_data = json.loads(error_body)
            print(json.dumps(error_data), file=sys.stderr)
        except:
            print(json.dumps({"error": error_body}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Update WordPress post')
    parser.add_argument('--url', default=os.getenv('WP_URL'), help='WordPress site URL')
    parser.add_argument('--username', default=os.getenv('WP_USERNAME'), help='WordPress username')
    parser.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'), help='Application Password')
    parser.add_argument('--post-id', required=True, type=int, help='Post ID to update')
    parser.add_argument('--content', help='Post content (HTML/Gutenberg)')
    parser.add_argument('--title', help='Post title')
    parser.add_argument('--status', choices=['publish', 'draft', 'pending', 'private'], help='Post status')
    parser.add_argument('--featured-media', type=int, help='Featured image ID')
    parser.add_argument('--content-file', help='Read content from file')
    parser.add_argument('--yes', '-y', action='store_true', help='Skip the interactive publish confirmation.')

    args = parser.parse_args()

    # Validate required args
    if not args.url:
        print(json.dumps({"error": "WordPress URL required (--url or WP_URL)"}), file=sys.stderr)
        sys.exit(1)
    warn_insecure_wp_url(args.url)
    if should_confirm_publish(args.status, args.yes, sys.stdin.isatty()):
        print("About to PUBLISH live content to %s. Type 'PUBLISH' to confirm:" % args.url, file=sys.stderr)
        if input("> ").strip() != "PUBLISH":
            print("Aborted: publish not confirmed.", file=sys.stderr)
            sys.exit(1)
    if not args.username:
        print(json.dumps({"error": "Username required (--username or WP_USERNAME)"}), file=sys.stderr)
        sys.exit(1)
    if not args.app_password:
        print(json.dumps({"error": "App password required (--app-password or WP_APP_PASSWORD)"}), file=sys.stderr)
        sys.exit(1)
    
    # Read content from file if specified. The safety helper restricts reads to
    # the current working directory by default; opt in to other roots with
    # WP_ALLOWED_FILE_ROOTS=/safe/path[:/another/path].
    content = args.content
    if args.content_file:
        try:
            content_path = validate_local_file(args.content_file, purpose="content file", max_bytes=TEXT_MAX_BYTES)
            with open(content_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except SafetyError as e:
            die_safety(e)
        except Exception as e:
            print(json.dumps({"error": f"Failed to read content file: {e}"}), file=sys.stderr)
            sys.exit(1)
    
    # Update post
    update_post(
        args.url,
        args.username,
        args.app_password,
        args.post_id,
        content=content,
        title=args.title,
        status=args.status,
        featured_media=args.featured_media
    )

if __name__ == '__main__':
    main()
