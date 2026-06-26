#!/usr/bin/env python3
"""
Detect installed WordPress plugins (ACF, Rank Math, Yoast, JetEngine)

Usage:
    python3 detect_plugins.py
    python3 detect_plugins.py --verbose
    
Environment variables:
    WP_SITE_URL or WP_URL - WordPress site URL
    WP_USER or WP_USERNAME - WordPress username  
    WP_APP_PASSWORD - Application Password
"""

import argparse
import json
import os
import sys
import requests
from base64 import b64encode
from security import warn_insecure_wp_url

def detect_plugins(url, username, password, verbose=False):
    """Detect WordPress plugins via REST API"""
    
    # Prepare auth
    credentials = f"{username}:{password}"
    auth_header = 'Basic ' + b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }
    
    base_url = url.rstrip('/')
    plugins = {
        'acf': {'name': 'Advanced Custom Fields', 'detected': False, 'endpoint': None},
        'rank_math': {'name': 'Rank Math SEO', 'detected': False, 'endpoint': None},
        'yoast': {'name': 'Yoast SEO', 'detected': False, 'endpoint': None},
        'jetengine': {'name': 'JetEngine', 'detected': False, 'endpoint': None}
    }
    
    # Test ACF REST endpoint
    try:
        response = requests.get(f"{base_url}/wp-json/acf/v3/posts/1", headers=headers, timeout=10)
        if response.status_code in [200, 404]:  # Endpoint exists (404 means post not found, not plugin missing)
            plugins['acf']['detected'] = True
            plugins['acf']['endpoint'] = '/wp-json/acf/v3'
            if verbose:
                print(f"✓ ACF REST API endpoint found", file=sys.stderr)
    except:
        pass
    
    # Check for Rank Math via meta keys (get a sample post and check meta)
    try:
        response = requests.get(f"{base_url}/wp-json/wp/v2/posts?per_page=1", headers=headers, timeout=10)
        if response.status_code == 200:
            posts = response.json()
            if posts and len(posts) > 0:
                post_id = posts[0]['id']
                # Get post meta
                post_response = requests.get(f"{base_url}/wp-json/wp/v2/posts/{post_id}", headers=headers, timeout=10)
                if post_response.status_code == 200:
                    post_data = post_response.json()
                    meta = post_data.get('meta', {})
                    if any(key.startswith('rank_math_') for key in meta.keys()):
                        plugins['rank_math']['detected'] = True
                        plugins['rank_math']['endpoint'] = '/wp-json/wp/v2 (postmeta)'
                        if verbose:
                            print(f"✓ Rank Math detected via meta keys", file=sys.stderr)
    except:
        pass
    
    # Check for Yoast via meta keys
    try:
        response = requests.get(f"{base_url}/wp-json/wp/v2/posts?per_page=1", headers=headers, timeout=10)
        if response.status_code == 200:
            posts = response.json()
            if posts and len(posts) > 0:
                post_id = posts[0]['id']
                post_response = requests.get(f"{base_url}/wp-json/wp/v2/posts/{post_id}", headers=headers, timeout=10)
                if post_response.status_code == 200:
                    post_data = post_response.json()
                    meta = post_data.get('meta', {})
                    if any(key.startswith('_yoast_wpseo_') for key in meta.keys()):
                        plugins['yoast']['detected'] = True
                        plugins['yoast']['endpoint'] = '/wp-json/wp/v2 (postmeta)'
                        if verbose:
                            print(f"✓ Yoast SEO detected via meta keys", file=sys.stderr)
    except:
        pass
    
    # Check for JetEngine (usually via postmeta, no specific REST endpoint)
    # JetEngine stores fields as postmeta, so we look for common patterns
    try:
        response = requests.get(f"{base_url}/wp-json/wp/v2/posts?per_page=5", headers=headers, timeout=10)
        if response.status_code == 200:
            posts = response.json()
            for post in posts:
                post_response = requests.get(f"{base_url}/wp-json/wp/v2/posts/{post['id']}", headers=headers, timeout=10)
                if post_response.status_code == 200:
                    post_data = post_response.json()
                    meta = post_data.get('meta', {})
                    # JetEngine fields often prefixed or in specific patterns
                    # This is a heuristic - may need refinement
                    if any('jet_' in key.lower() for key in meta.keys()):
                        plugins['jetengine']['detected'] = True
                        plugins['jetengine']['endpoint'] = '/wp-json/wp/v2 (postmeta)'
                        if verbose:
                            print(f"✓ JetEngine detected via meta keys", file=sys.stderr)
                        break
    except:
        pass
    
    return plugins

def main():
    parser = argparse.ArgumentParser(description='Detect WordPress plugins')
    parser.add_argument('--url', default=os.getenv('WP_SITE_URL') or os.getenv('WP_URL'), 
                       help='WordPress site URL')
    parser.add_argument('--username', default=os.getenv('WP_USER') or os.getenv('WP_USERNAME'), 
                       help='WordPress username')
    parser.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'), 
                       help='Application Password')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Verbose output')
    
    args = parser.parse_args()
    
    # Validate required args
    if not args.url:
        print(json.dumps({"error": "WordPress URL required (--url or WP_SITE_URL/WP_URL env var)"}),
              file=sys.stderr)
        sys.exit(1)
    if not args.username:
        print(json.dumps({"error": "Username required (--username or WP_USER/WP_USERNAME env var)"}),
              file=sys.stderr)
        sys.exit(1)
    if not args.app_password:
        print(json.dumps({"error": "App password required (--app-password or WP_APP_PASSWORD env var)"}),
              file=sys.stderr)
        sys.exit(1)
    warn_insecure_wp_url(args.url)

    try:
        plugins = detect_plugins(args.url, args.username, args.app_password, args.verbose)
        print(json.dumps(plugins, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
