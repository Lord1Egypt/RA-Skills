#!/usr/bin/env python3
"""Read-only Technitium DNS Server health check.

Environment:
  TECHNITIUM_URL    Base URL, e.g. http://dns-server.example:5380
  TECHNITIUM_TOKEN  Technitium API/session token

Outputs JSON with keys: ok, checked, failures.
"""
import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

DEFAULT_TIMEOUT = int(os.environ.get('TECHNITIUM_TIMEOUT_SECONDS', '10'))


def require_config():
    base = os.environ.get('TECHNITIUM_URL', '').rstrip('/')
    token = os.environ.get('TECHNITIUM_TOKEN', '')
    if not base or not token:
        raise SystemExit('missing TECHNITIUM_URL or TECHNITIUM_TOKEN')
    return base, token


def api_get(base, token, path, params=None):
    qs = ('?' + urlencode(params)) if params else ''
    req = Request(base + path + qs, headers={'Authorization': 'Bearer ' + token})
    with urlopen(req, timeout=DEFAULT_TIMEOUT) as resp:
        body = resp.read().decode('utf-8', errors='replace')
    data = json.loads(body)
    if data.get('status') != 'ok':
        msg = data.get('errorMessage') or data.get('status') or 'unknown error'
        raise RuntimeError(f'{path}: {msg}')
    return data


def main():
    base, token = require_config()
    checked = []
    failures = []

    try:
        session = api_get(base, token, '/api/user/session/get')
        info = session.get('info') or {}
        checked.append({
            'service': 'technitium/session',
            'status': 'ok',
            'summary': f"user={session.get('username')} version={info.get('version')} domain={info.get('dnsServerDomain')}",
        })
    except Exception as e:
        failures.append({'service': 'technitium/session', 'summary': str(e)})
        print(json.dumps({'ok': False, 'checked': checked, 'failures': failures}, indent=2))
        return 2

    try:
        settings = api_get(base, token, '/api/settings/get')
        r = settings.get('response') or {}
        checked.append({
            'service': 'technitium/settings',
            'status': 'ok',
            'summary': f"version={r.get('version')} uptime={r.get('uptimestamp')}",
        })
    except Exception as e:
        failures.append({'service': 'technitium/settings', 'summary': str(e)})

    try:
        stats = api_get(base, token, '/api/dashboard/stats/get', {'type': 'LastHour', 'utc': 'true'})
        s = ((stats.get('response') or {}).get('stats') or {})
        total = int(s.get('totalQueries') or 0)
        servfail = int(s.get('totalServerFailure') or 0)
        refused = int(s.get('totalRefused') or 0)
        dropped = int(s.get('totalDropped') or 0)
        bad = servfail + refused + dropped
        checked.append({
            'service': 'technitium/stats',
            'status': 'ok',
            'summary': f'lastHour queries={total} servfail={servfail} refused={refused} dropped={dropped}',
        })
        if total >= 50 and bad / max(total, 1) > 0.05:
            failures.append({'service': 'technitium/stats', 'summary': f'High DNS error ratio: {bad}/{total} in last hour'})
        elif total < 50 and bad >= 25:
            failures.append({'service': 'technitium/stats', 'summary': f'High absolute DNS errors: {bad} in last hour with low traffic baseline'})
    except Exception as e:
        failures.append({'service': 'technitium/stats', 'summary': str(e)})

    try:
        zones = api_get(base, token, '/api/zones/list')
        zlist = ((zones.get('response') or {}).get('zones') or [])
        bad_zones = [z for z in zlist if z.get('disabled') or z.get('isExpired') or z.get('syncFailed')]
        checked.append({
            'service': 'technitium/zones',
            'status': 'ok',
            'summary': f'zones={len(zlist)} bad={len(bad_zones)}',
        })
        for z in bad_zones[:10]:
            failures.append({'service': 'technitium/zones', 'summary': f"zone={z.get('name')} disabled={z.get('disabled')} expired={z.get('isExpired')} syncFailed={z.get('syncFailed')}"})
    except Exception as e:
        failures.append({'service': 'technitium/zones', 'summary': str(e)})

    try:
        leases = api_get(base, token, '/api/dhcp/leases/list')
        llist = ((leases.get('response') or {}).get('leases') or [])
        checked.append({'service': 'technitium/dhcp', 'status': 'ok', 'summary': f'leases={len(llist)}'})
    except Exception as e:
        checked.append({'service': 'technitium/dhcp', 'status': 'warn', 'summary': f'not checked: {e}'})

    result = {'ok': not failures, 'checked': checked, 'failures': failures}
    print(json.dumps(result, indent=2))
    return 0 if not failures else 1


if __name__ == '__main__':
    raise SystemExit(main())
