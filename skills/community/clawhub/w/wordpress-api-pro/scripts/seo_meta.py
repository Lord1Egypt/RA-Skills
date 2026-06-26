#!/usr/bin/env python3
"""
Read/write Rank Math and Yoast SEO meta fields

Usage:
    # Auto-detect SEO plugin and get meta
    python3 seo_meta.py --post-id 123
    
    # Get specific plugin's meta
    python3 seo_meta.py --post-id 123 --plugin rankmath
    python3 seo_meta.py --post-id 123 --plugin yoast
    
    # Set SEO meta (JSON)
    python3 seo_meta.py --post-id 123 --set '{"title": "SEO Title", "description": "Meta desc"}'
    
    # Set with specific plugin
    python3 seo_meta.py --post-id 123 --plugin rankmath --set '{"title": "Title"}'
    
Environment variables:
    WP_SITE_URL or WP_URL - WordPress site URL
    WP_USER or WP_USERNAME - WordPress username  
    WP_APP_PASSWORD - Application Password
"""

import argparse
import json
import os
import sys
from base64 import b64encode
from security import warn_insecure_wp_url

# Meta key mappings
RANKMATH_KEYS = {
    'title': 'rank_math_title',
    'description': 'rank_math_description',
    'focus_keyword': 'rank_math_focus_keyword',
    'robots': 'rank_math_robots',
    'canonical_url': 'rank_math_canonical_url',
    'schema': 'rank_math_schema'
}

YOAST_KEYS = {
    'title': '_yoast_wpseo_title',
    'description': '_yoast_wpseo_metadesc',
    'focus_keyword': '_yoast_wpseo_focuskw',
    'canonical': '_yoast_wpseo_canonical',
    'meta_robots_noindex': '_yoast_wpseo_meta-robots-noindex',
    'meta_robots_nofollow': '_yoast_wpseo_meta-robots-nofollow'
}

def detect_seo_plugin(url, username, password, post_id):
    """Detect which SEO plugin is active"""
    import requests
    credentials = f"{username}:{password}"
    auth_header = 'Basic ' + b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }
    
    base_url = url.rstrip('/')
    
    try:
        response = requests.get(f"{base_url}/wp-json/wp/v2/posts/{post_id}", 
                              headers=headers, timeout=10)
        if response.status_code == 200:
            post_data = response.json()
            meta = post_data.get('meta', {})
            
            has_rankmath = any(key in meta for key in RANKMATH_KEYS.values())
            has_yoast = any(key in meta for key in YOAST_KEYS.values())
            
            if has_rankmath and has_yoast:
                return 'both'
            elif has_rankmath:
                return 'rankmath'
            elif has_yoast:
                return 'yoast'
            else:
                return None
    except:
        return None

def get_seo_meta(url, username, password, post_id, plugin=None):
    """Get SEO meta fields"""
    import requests
    credentials = f"{username}:{password}"
    auth_header = 'Basic ' + b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }
    
    base_url = url.rstrip('/')
    
    try:
        response = requests.get(f"{base_url}/wp-json/wp/v2/posts/{post_id}", 
                              headers=headers, timeout=10)
        if response.status_code == 200:
            post_data = response.json()
            meta = post_data.get('meta', {})
            
            # Auto-detect if not specified
            if not plugin:
                plugin = detect_seo_plugin(url, username, password, post_id)
            
            result = {'plugin': plugin, 'meta': {}}
            
            if plugin == 'rankmath' or plugin == 'both':
                rankmath_meta = {}
                for friendly_name, meta_key in RANKMATH_KEYS.items():
                    if meta_key in meta:
                        rankmath_meta[friendly_name] = meta[meta_key]
                if rankmath_meta:
                    result['meta']['rankmath'] = rankmath_meta
            
            if plugin == 'yoast' or plugin == 'both':
                yoast_meta = {}
                for friendly_name, meta_key in YOAST_KEYS.items():
                    if meta_key in meta:
                        yoast_meta[friendly_name] = meta[meta_key]
                if yoast_meta:
                    result['meta']['yoast'] = yoast_meta
            
            return result
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            return {"error": f"HTTP {response.status_code}", "details": error_data}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def _map_meta_keys(meta_dict, plugin, env=None):
    """Map friendly SEO key names to actual postmeta keys.

    Returns (payload_dict, raw_warnings) where payload_dict is ready to POST
    and raw_warnings is a list of (key, message) tuples for non-allowlisted keys.
    With WP_REQUIRE_ALLOWLIST=1, raises ValueError for the first raw key found.
    """
    if env is None:
        env = os.environ
    keys_map = RANKMATH_KEYS if plugin == 'rankmath' else YOAST_KEYS
    payload = {}
    raw_warnings = []
    for friendly_name, value in meta_dict.items():
        if friendly_name in keys_map:
            meta_key = keys_map[friendly_name]
            # Validate schema if it's Rank Math schema
            if friendly_name == 'schema' and plugin == 'rankmath':
                try:
                    if isinstance(value, str):
                        json.loads(value)
                except json.JSONDecodeError:
                    raise ValueError("Invalid JSON for schema field")
            payload[meta_key] = value
        else:
            # Raw (non-allowlisted) meta key. Allowed by default for flexibility,
            # but surfaced so it's never silent. WP_REQUIRE_ALLOWLIST=1 refuses.
            msg = (
                "SEO meta: '%s' is not in the %s allowlist — writing it as a raw "
                "postmeta key." % (friendly_name, plugin)
            )
            if env.get("WP_REQUIRE_ALLOWLIST") == "1":
                raise ValueError(msg + " (WP_REQUIRE_ALLOWLIST=1 set — refusing.)")
            raw_warnings.append((friendly_name, msg))
            payload[friendly_name] = value
    return payload, raw_warnings


def set_seo_meta(url, username, password, post_id, meta_dict, plugin='rankmath'):
    """Set SEO meta fields"""
    import requests
    credentials = f"{username}:{password}"
    auth_header = 'Basic ' + b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }

    base_url = url.rstrip('/')

    try:
        meta_payload, raw_warnings = _map_meta_keys(meta_dict, plugin)
    except ValueError as exc:
        return {"error": str(exc)}

    for _key, msg in raw_warnings:
        print("WARNING: " + msg, file=sys.stderr)
    
    try:
        payload = {'meta': meta_payload}
        response = requests.post(f"{base_url}/wp-json/wp/v2/posts/{post_id}", 
                               headers=headers, json=payload, timeout=10)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            return {"error": f"HTTP {response.status_code}", "details": error_data}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def main():
    parser = argparse.ArgumentParser(description='Read/write SEO meta (Rank Math + Yoast)')
    parser.add_argument('--url', default=os.getenv('WP_SITE_URL') or os.getenv('WP_URL'), 
                       help='WordPress site URL')
    parser.add_argument('--username', default=os.getenv('WP_USER') or os.getenv('WP_USERNAME'), 
                       help='WordPress username')
    parser.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'), 
                       help='Application Password')
    parser.add_argument('--post-id', required=True, type=int, 
                       help='Post ID')
    parser.add_argument('--plugin', choices=['rankmath', 'yoast', 'auto'],
                       help='SEO plugin to use (auto-detect if not specified)')
    parser.add_argument('--set', dest='set_json',
                       help='Set SEO meta from JSON string')
    parser.add_argument('--detect', action='store_true',
                       help='Only detect which SEO plugin is active')
    
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
        # Detect only
        if args.detect:
            plugin = detect_seo_plugin(args.url, args.username, args.app_password, args.post_id)
            print(json.dumps({"plugin": plugin}))
            return
        
        plugin = args.plugin if args.plugin and args.plugin != 'auto' else None
        
        # Set operation
        if args.set_json:
            meta = json.loads(args.set_json)
            if not plugin:
                plugin = detect_seo_plugin(args.url, args.username, args.app_password, args.post_id) or 'rankmath'
            result = set_seo_meta(args.url, args.username, args.app_password, 
                                 args.post_id, meta, plugin)
            print(json.dumps(result, indent=2))
        # Get operation
        else:
            result = get_seo_meta(args.url, args.username, args.app_password, 
                                 args.post_id, plugin)
            print(json.dumps(result, indent=2))
            
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
