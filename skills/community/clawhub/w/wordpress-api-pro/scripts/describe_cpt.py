#!/usr/bin/env python3
"""Describe a custom post type: rest_base, taxonomies, and discovered field keys.

Read-only. Samples the newest existing entry to surface ACF/meta keys so a caller
knows what to populate when seeding.

Usage:
    python3 describe_cpt.py --post-type projects
Env: WP_URL/WP_SITE_URL, WP_USERNAME/WP_USER, WP_APP_PASSWORD
"""
import argparse, json, os, sys, urllib.request
from base64 import b64encode


def _auth(u, p): return 'Basic ' + b64encode(f"{u}:{p}".encode()).decode()


def _get(url, auth):
    req = urllib.request.Request(url, method='GET')
    req.add_header('Authorization', auth)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def describe_cpt(base_url, username, password, post_type):
    auth = _auth(username, password)
    base = base_url.rstrip('/')
    info = _get(f"{base}/wp-json/wp/v2/types/{post_type}", auth)
    rest_base = info.get('rest_base') or post_type
    taxonomies = info.get('taxonomies', [])

    field_keys, sampled_id = [], None
    try:
        entries = _get(f"{base}/wp-json/wp/v2/{rest_base}?per_page=1&orderby=date", auth)
        if entries:
            sampled_id = entries[0].get('id')
            meta = entries[0].get('meta', {}) or {}
            acf = entries[0].get('acf', {}) or {}
            keys = set(k for k in meta if not k.startswith('_')) | set(acf.keys())
            field_keys = sorted(keys)
    except Exception:
        pass

    return {
        'post_type': post_type, 'rest_base': rest_base,
        'taxonomies': taxonomies, 'field_keys': field_keys,
        'sampled_entry_id': sampled_id,
        'note': '' if field_keys else 'No entries to sample; supply field keys manually.',
    }


def main():
    p = argparse.ArgumentParser(description='Describe a CPT for seeding')
    p.add_argument('--url', default=os.getenv('WP_URL') or os.getenv('WP_SITE_URL'))
    p.add_argument('--username', default=os.getenv('WP_USERNAME') or os.getenv('WP_USER'))
    p.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'))
    p.add_argument('--post-type', required=True)
    a = p.parse_args()
    if not all([a.url, a.username, a.app_password]):
        print(json.dumps({"error": "Missing required credentials"}), file=sys.stderr); sys.exit(1)
    try:
        print(json.dumps(describe_cpt(a.url, a.username, a.app_password, a.post_type), indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr); sys.exit(1)


if __name__ == '__main__':
    main()
