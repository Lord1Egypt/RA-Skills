#!/usr/bin/env python3
"""
Read/write JetEngine meta fields

JetEngine stores custom fields as postmeta. This script provides a convenient
interface for reading and writing JetEngine fields.

Usage:
    # Get all JetEngine fields for a post
    python3 jetengine_fields.py --post-id 123
    
    # Get specific field
    python3 jetengine_fields.py --post-id 123 --field my_jet_field
    
    # Set JetEngine fields (JSON)
    python3 jetengine_fields.py --post-id 123 --set '{"field1": "value1", "field2": "value2"}'
    
    # Set single field
    python3 jetengine_fields.py --post-id 123 --field my_field --value "my value"
    
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

def get_jetengine_fields(url, username, password, post_id, field_name=None):
    """Get JetEngine fields (stored as postmeta)"""
    
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
            
            # JetEngine fields can have various naming conventions
            # Common patterns: no prefix, 'jet_' prefix, or custom field group names
            # We'll return all meta that doesn't start with underscore (private meta)
            jetengine_fields = {k: v for k, v in meta.items() if not k.startswith('_')}
            
            if field_name:
                return {field_name: jetengine_fields.get(field_name)}
            return jetengine_fields
        else:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            return {"error": f"HTTP {response.status_code}", "details": error_data}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def set_jetengine_fields(url, username, password, post_id, fields_dict):
    """Set JetEngine fields (via postmeta)"""
    
    credentials = f"{username}:{password}"
    auth_header = 'Basic ' + b64encode(credentials.encode()).decode()
    headers = {
        'Authorization': auth_header,
        'Content-Type': 'application/json'
    }
    
    base_url = url.rstrip('/')
    
    try:
        payload = {'meta': fields_dict}
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
    parser = argparse.ArgumentParser(description='Read/write JetEngine fields')
    parser.add_argument('--url', default=os.getenv('WP_SITE_URL') or os.getenv('WP_URL'), 
                       help='WordPress site URL')
    parser.add_argument('--username', default=os.getenv('WP_USER') or os.getenv('WP_USERNAME'), 
                       help='WordPress username')
    parser.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'), 
                       help='Application Password')
    parser.add_argument('--post-id', required=True, type=int, 
                       help='Post ID')
    parser.add_argument('--field', 
                       help='Specific field name to get/set')
    parser.add_argument('--value', 
                       help='Field value (when setting single field with --field)')
    parser.add_argument('--set', dest='set_json',
                       help='Set fields from JSON string')
    parser.add_argument('--list-all', action='store_true',
                       help='List all meta fields (including private ones)')
    
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
        # Set operation
        if args.set_json:
            fields = json.loads(args.set_json)
            result = set_jetengine_fields(args.url, args.username, args.app_password, 
                                         args.post_id, fields)
            print(json.dumps(result, indent=2))
        elif args.field and args.value:
            fields = {args.field: args.value}
            result = set_jetengine_fields(args.url, args.username, args.app_password, 
                                         args.post_id, fields)
            print(json.dumps(result, indent=2))
        # Get operation
        else:
            result = get_jetengine_fields(args.url, args.username, args.app_password, 
                                         args.post_id, args.field)
            print(json.dumps(result, indent=2))
            
    except json.JSONDecodeError as e:
        print(json.dumps({"error": f"Invalid JSON: {e}"}), file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
