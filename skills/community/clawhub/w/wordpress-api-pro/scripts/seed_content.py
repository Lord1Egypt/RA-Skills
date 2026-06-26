#!/usr/bin/env python3
"""Seed a dataset of CPT entries with ACF/Jet fields, taxonomies, and images.

Dry-run by default — validates and prints a per-entry plan with NO writes.
Pass --execute to perform writes. Reuses create_post / acf_fields /
jetengine_fields / upload_media.

Usage:
    python3 seed_content.py --dataset data.json            # dry-run (default)
    python3 seed_content.py --dataset data.json --execute  # write
Env: WP_URL/WP_SITE_URL, WP_USERNAME/WP_USER, WP_APP_PASSWORD
"""
import argparse, json, os, sys
from security import warn_insecure_wp_url

# NB: the write-path modules (acf_fields/jetengine_fields) import `requests`, and
# the image path needs upload_media. They are imported lazily inside seed() so the
# dry-run / planning path (and tests / CI smoke) need only the stdlib.


def plan_seed(dataset):
    """Pure planning — no network. Returns a list of per-entry plan dicts."""
    plan = []
    for i, e in enumerate(dataset):
        fi = e.get('featured_image')
        kind = None
        if isinstance(fi, int) or (isinstance(fi, str) and str(fi).isdigit()):
            kind = 'media_id'
        elif isinstance(fi, str) and fi:
            kind = 'url' if fi.lower().startswith(('http://', 'https://')) else 'path'
        will_set = []
        if e.get('acf'): will_set.append('acf')
        if e.get('jet'): will_set.append('jet')
        if e.get('terms'): will_set.append('terms')
        if fi is not None: will_set.append('featured_image')
        plan.append({
            'index': i, 'title': e.get('title', '(no title)'),
            'post_type': e.get('post_type', 'post'),
            'status': e.get('status', 'draft'),
            'will_set': will_set, 'featured_image_kind': kind,
        })
    return plan


def _resolve_image(url, user, pw, fi, allow_remote):
    if isinstance(fi, int) or (isinstance(fi, str) and str(fi).isdigit()):
        return int(fi)
    import upload_media as _media
    res = _media.upload_media(url, user, pw, fi, allow_remote_url=allow_remote)
    return res.get('id') if isinstance(res, dict) else None


def seed(url, user, pw, dataset, allow_remote=False):
    """Execute the seed. Returns {created: [...], failed: [...]}."""
    import create_post as _cp
    import acf_fields as _acf
    import jetengine_fields as _jet
    import upload_media as _media
    created, failed = [], []
    for e in dataset:
        try:
            post = _cp.create_post(
                url, user, pw, e['title'], e.get('content', ''),
                e.get('status', 'draft'), post_type=e.get('post_type', 'post'),
                terms=e.get('terms'))
            pid = post['id']
            if e.get('acf'):
                _acf.set_acf_fields(url, user, pw, pid, e['acf'])
            if e.get('jet'):
                _jet.set_jetengine_fields(url, user, pw, pid, e['jet'])
            if e.get('featured_image') is not None:
                mid = _resolve_image(url, user, pw, e['featured_image'], allow_remote)
                if mid:
                    _media.set_featured_image(url, user, pw, pid, mid)
            created.append({'id': pid, 'title': e['title']})
        except Exception as ex:
            failed.append({'title': e.get('title', '(no title)'), 'error': str(ex)})
    return {'created': created, 'failed': failed}


def main():
    p = argparse.ArgumentParser(description='Seed CPT entries from a JSON dataset')
    p.add_argument('--url', default=os.getenv('WP_URL') or os.getenv('WP_SITE_URL'))
    p.add_argument('--username', default=os.getenv('WP_USERNAME') or os.getenv('WP_USER'))
    p.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'))
    p.add_argument('--dataset', required=True, help='Path to JSON array of entries')
    p.add_argument('--execute', action='store_true', help='Perform writes (default: dry-run)')
    p.add_argument('--allow-remote-url', action='store_true', help='Permit remote image fetches')
    a = p.parse_args()

    with open(a.dataset) as f:
        dataset = json.load(f)
    if not isinstance(dataset, list):
        print(json.dumps({"error": "dataset must be a JSON array"}), file=sys.stderr); sys.exit(1)

    if not a.execute:
        print(json.dumps({"dry_run": True, "plan": plan_seed(dataset)}, indent=2))
        return

    if not all([a.url, a.username, a.app_password]):
        print(json.dumps({"error": "Missing required credentials"}), file=sys.stderr); sys.exit(1)
    warn_insecure_wp_url(a.url)
    result = seed(a.url, a.username, a.app_password, dataset, allow_remote=a.allow_remote_url)
    print(json.dumps(result, indent=2))
    if result['failed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
