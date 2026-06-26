#!/usr/bin/env python3
"""Create a WordPress post or CPT entry via REST API (with taxonomy support)."""
import argparse, json, os, sys, urllib.request, urllib.parse
from base64 import b64encode
from security import warn_insecure_wp_url, should_confirm_publish


def _auth(username, password):
    return 'Basic ' + b64encode(f"{username}:{password}".encode()).decode()


def _get(url, auth):
    req = urllib.request.Request(url, method='GET')
    req.add_header('Authorization', auth)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def _post(url, auth, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method='POST')
    req.add_header('Authorization', auth)
    req.add_header('Content-Type', 'application/json')
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode())


def resolve_rest_base(base_url, auth, post_type):
    """Resolve a post type's REST base; fall back to the slug on any error."""
    try:
        info = _get(f"{base_url.rstrip('/')}/wp-json/wp/v2/types/{post_type}", auth)
        return info.get('rest_base') or post_type
    except Exception:
        return post_type


def resolve_terms(base_url, auth, terms_dict, create_missing=True):
    """Map {taxonomy: [name|id, ...]} -> {taxonomy: [id, ...]}.

    Names are resolved (and optionally created) via the taxonomy's REST base.
    Integer-like values pass through as ids.
    """
    base_url = base_url.rstrip('/')
    out = {}
    for taxonomy, values in (terms_dict or {}).items():
        tax_base = resolve_rest_base(base_url, auth, taxonomy)  # taxonomy rest_base
        ids = []
        for v in values:
            if isinstance(v, int) or (isinstance(v, str) and v.isdigit()):
                ids.append(int(v)); continue
            q = urllib.parse.quote(str(v))
            hits = _get(f"{base_url}/wp-json/wp/v2/{tax_base}?search={q}", auth)
            match = next((t for t in hits if str(t.get('name', '')).lower() == str(v).lower()), None)
            if match:
                ids.append(match['id'])
            elif create_missing:
                created = _post(f"{base_url}/wp-json/wp/v2/{tax_base}", auth, {'name': v})
                ids.append(created['id'])
            else:
                raise ValueError(f"Term '{v}' not found in '{taxonomy}'")
        out[taxonomy] = ids
    return out


def create_post(url, username, password, title, content, status='draft',
                post_type='post', featured_media=None, terms=None):
    """Create a post/CPT entry. Returns the created object dict. Raises on error."""
    auth = _auth(username, password)
    base = url.rstrip('/')
    rest_base = resolve_rest_base(base, auth, post_type)

    data = {'title': title, 'content': content, 'status': status}
    if featured_media:
        data['featured_media'] = int(featured_media)
    if terms:
        resolved = resolve_terms(base, auth, terms)
        for taxonomy, ids in resolved.items():
            data[taxonomy] = ids  # REST accepts the taxonomy key with term ids

    return _post(f"{base}/wp-json/wp/v2/{rest_base}", auth, data)


def main():
    p = argparse.ArgumentParser(description='Create WordPress post or CPT entry')
    p.add_argument('--url', default=os.getenv('WP_URL') or os.getenv('WP_SITE_URL'))
    p.add_argument('--username', default=os.getenv('WP_USERNAME') or os.getenv('WP_USER'))
    p.add_argument('--app-password', default=os.getenv('WP_APP_PASSWORD'))
    p.add_argument('--title', required=True)
    p.add_argument('--content', required=True)
    p.add_argument('--status', default='draft', choices=['publish', 'draft', 'pending'])
    p.add_argument('--post-type', default='post')
    p.add_argument('--featured-media', type=int)
    p.add_argument('--terms', help='JSON {"taxonomy": ["Name or id", ...]}')
    p.add_argument('--yes', '-y', action='store_true', help='Skip the interactive publish confirmation.')
    a = p.parse_args()
    if not all([a.url, a.username, a.app_password]):
        print(json.dumps({"error": "Missing required credentials"}), file=sys.stderr)
        sys.exit(1)
    warn_insecure_wp_url(a.url)
    if should_confirm_publish(a.status, a.yes, sys.stdin.isatty()):
        print("About to PUBLISH live content to %s. Type 'PUBLISH' to confirm:" % a.url, file=sys.stderr)
        if input("> ").strip() != "PUBLISH":
            print("Aborted: publish not confirmed.", file=sys.stderr)
            sys.exit(1)
    try:
        result = create_post(a.url, a.username, a.app_password, a.title, a.content,
                             a.status, post_type=a.post_type,
                             featured_media=a.featured_media,
                             terms=json.loads(a.terms) if a.terms else None)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
