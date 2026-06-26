#!/usr/bin/env python3
import os
import sys
import json
import base64
import argparse
import datetime as dt
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
except Exception:
    requests = None


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def parse_iso(s: str) -> Optional[dt.datetime]:
    try:
        if s.endswith('Z'):
            s = s[:-1] + '+00:00'
        return dt.datetime.fromisoformat(s).astimezone(dt.timezone.utc)
    except Exception:
        return None


def b64url_decode(data: str) -> bytes:
    pad = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + pad)


def decode_jwt_noverify(token: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None, 'not_jwt'
        payload = json.loads(b64url_decode(parts[1]).decode('utf-8', errors='replace'))
        return payload, None
    except Exception as e:
        return None, f'decode_error:{e}'


def mask_token(s: str, keep: int = 6) -> str:
    if not isinstance(s, str) or not s:
        return ''
    if len(s) <= keep * 2:
        return s[:keep] + '...'
    return s[:keep] + '...' + s[-keep:]


def find_json_files(root: Path) -> List[Path]:
    files = []
    for p in root.rglob('*'):
        if p.is_file():
            name = p.name.lower()
            if p.suffix.lower() == '.json' or 'token' in name or 'auth' in name or 'session' in name:
                files.append(p)
    return files


def read_json(p: Path):
    try:
        raw = p.read_text(encoding='utf-8', errors='replace').strip()
        if not raw:
            return None, 'empty'
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None, 'json_not_object'
        return data, None
    except Exception as e:
        return None, f'read_error:{e}'


def offline_check(data: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        'type': data.get('type'),
        'email': data.get('email'),
        'account_id': data.get('account_id'),
        'valid_offline': True,
        'issues': [],
        'times': {},
        'tokens': {},
    }
    now = utc_now()

    expired = data.get('expired')
    if isinstance(expired, str):
        exp_dt = parse_iso(expired)
        result['times']['expired_field'] = expired
        if exp_dt:
            result['times']['expired_field_utc'] = exp_dt.isoformat()
            if exp_dt <= now:
                result['valid_offline'] = False
                result['issues'].append('expired_field_past')
        else:
            result['issues'].append('expired_field_parse_failed')

    for key in ('id_token', 'access_token'):
        tok = data.get(key)
        if isinstance(tok, str):
            result['tokens'][key] = mask_token(tok)
            payload, err = decode_jwt_noverify(tok)
            if err:
                result['issues'].append(f'{key}_{err}')
                continue
            exp = payload.get('exp')
            iat = payload.get('iat')
            if exp:
                exp_dt = dt.datetime.fromtimestamp(exp, tz=dt.timezone.utc)
                result['times'][f'{key}_exp_utc'] = exp_dt.isoformat()
                if exp_dt <= now:
                    result['valid_offline'] = False
                    result['issues'].append(f'{key}_expired')
            if iat:
                result['times'][f'{key}_iat_utc'] = dt.datetime.fromtimestamp(iat, tz=dt.timezone.utc).isoformat()
        elif key in data:
            result['issues'].append(f'{key}_not_string')

    rt = data.get('refresh_token')
    if isinstance(rt, str):
        result['tokens']['refresh_token'] = mask_token(rt)

    if not data.get('email'):
        result['issues'].append('missing_email')
    if not data.get('type'):
        result['issues'].append('missing_type')

    return result


def online_probe(data: Dict[str, Any], timeout: int = 12) -> Dict[str, Any]:
    out = {'online_checked': False, 'online_valid': None, 'probe': None, 'probe_detail': None}
    if requests is None:
        out['probe_detail'] = 'requests_not_installed'
        return out
    access_token = data.get('access_token')
    if not isinstance(access_token, str) or not access_token:
        out['probe_detail'] = 'no_access_token'
        return out
    probe_url = 'https://api.openai.com/v1/models'
    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        out['online_checked'] = True
        out['probe'] = probe_url
        r = requests.get(probe_url, headers=headers, timeout=timeout)
        out['status_code'] = r.status_code
        out['online_valid'] = 200 <= r.status_code < 300
        if not out['online_valid']:
            out['probe_detail'] = r.text[:300]
    except Exception as e:
        out['online_checked'] = True
        out['online_valid'] = False
        out['probe_detail'] = str(e)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('path', nargs='?', default='.')
    ap.add_argument('--probe', action='store_true')
    args = ap.parse_args()

    target = Path(args.path).expanduser().resolve()
    files = [target] if target.is_file() else find_json_files(target)
    if not files:
        print('No candidate files found.')
        return 0

    bad = 0
    for f in files:
        data, err = read_json(f)
        if err:
            print(f'FILE: {f}\n  valid_offline: False\n  issues:\n    - {err}\n')
            bad += 1
            continue
        report = offline_check(data)
        if args.probe:
            report.update(online_probe(data))
        print(f'FILE: {f}')
        print(f"  type: {report.get('type')}")
        print(f"  email: {report.get('email')}")
        print(f"  account_id: {report.get('account_id')}")
        print(f"  valid_offline: {report.get('valid_offline')}")
        if args.probe:
            print(f"  online_valid: {report.get('online_valid')}")
            if report.get('status_code') is not None:
                print(f"  status_code: {report.get('status_code')}")
        if report.get('issues'):
            print('  issues:')
            for x in report['issues']:
                print(f'    - {x}')
        print()
        if not report.get('valid_offline') or (args.probe and report.get('online_valid') is False):
            bad += 1
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main())
