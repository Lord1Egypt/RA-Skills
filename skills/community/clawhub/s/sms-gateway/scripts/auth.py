#!/usr/bin/env python3
"""JWT authentication helper for sms-gate.app."""
import os
import sys
import json
import time
import base64
import urllib.request
import urllib.error

# Cache token next to .env in skill root
_SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TOKEN_CACHE = os.path.join(_SKILL_ROOT, '.token.json')

def _load_env():
    """Load .env from the skill root directory."""
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k, v)

def _get_config():
    """Return (base_url, username, password) from environment, loading .env if needed."""
    _load_env()
    base_url = os.environ.get('SMS_GATE_URL', '').rstrip('/')
    username = os.environ.get('SMS_GATE_USER', '')
    password = os.environ.get('SMS_GATE_PASS', '')
    if not base_url or not username or not password:
        print("Error: SMS_GATE_URL, SMS_GATE_USER, and SMS_GATE_PASS must be set", file=sys.stderr)
        sys.exit(1)
    return base_url, username, password

def _read_cached_token():
    """Read cached token if still valid (with 60s margin)."""
    if not os.path.exists(_TOKEN_CACHE):
        return None
    try:
        with open(_TOKEN_CACHE) as f:
            data = json.load(f)
        if data.get('expires_epoch', 0) > time.time() + 60:
            return data['access_token']
    except Exception:
        pass
    return None

def _write_cached_token(token_data):
    """Cache the token response to disk."""
    from datetime import datetime
    expires_at = token_data.get('expires_at', '')
    try:
        # Parse ISO 8601 with timezone
        dt = datetime.fromisoformat(expires_at)
        expires_epoch = dt.timestamp()
    except Exception:
        expires_epoch = time.time() + 3600
    cache = {
        'access_token': token_data['access_token'],
        'expires_epoch': expires_epoch,
        'id': token_data.get('id', '')
    }
    with open(_TOKEN_CACHE, 'w') as f:
        json.dump(cache, f)

def get_token():
    """Get a valid JWT token, using cache or requesting a new one."""
    cached = _read_cached_token()
    if cached:
        return cached

    base_url, username, password = _get_config()
    creds = base64.b64encode(f"{username}:{password}".encode()).decode()

    req = urllib.request.Request(
        f"{base_url}/auth/token",
        data=json.dumps({'ttl': 3600, 'scopes': ['messages:send', 'messages:read']}).encode(),
        headers={
            'Authorization': f'Basic {creds}',
            'Content-Type': 'application/json'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            _write_cached_token(data)
            return data['access_token']
    except urllib.error.HTTPError as e:
        print(f"Auth error: HTTP {e.code} - {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Auth error: {e}", file=sys.stderr)
        sys.exit(1)

def api_request(path, method='GET', data=None):
    """Make an authenticated API request using JWT."""
    base_url = _get_config()[0]
    token = get_token()

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }

    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers['Content-Type'] = 'application/json'

    req = urllib.request.Request(
        f"{base_url}{path}",
        data=body,
        headers=headers,
        method=method
    )

    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())
