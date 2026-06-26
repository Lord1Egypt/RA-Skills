#!/usr/bin/env python3
import json
import base64
import shutil
import argparse
import datetime as dt
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

try:
    import requests
except Exception:
    requests = None

REDACT_KEYS = {
    'access_token', 'refresh_token', 'id_token', 'token', 'api_key', 'apiKey', 'secret', 'appSecret'
}

DEFAULT_PROBE_URL = 'https://api.openai.com/v1/models'
CODEX_USAGE_URL = 'https://chatgpt.com/backend-api/wham/usage'
CODEX_UA = 'codex_cli_rs/0.76.0 (Debian 13.0.0; x86_64) WindowsTerminal'


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


def redact_value(key: str, value: Any) -> Any:
    if key in REDACT_KEYS and isinstance(value, str):
        return mask_token(value)
    if isinstance(value, dict):
        return {k: redact_value(k, v) for k, v in value.items()}
    if isinstance(value, list):
        return [redact_value(key, v) for v in value]
    return value


def find_candidate_files(root: Path) -> List[Path]:
    files = []
    for p in root.rglob('*'):
        if p.is_file():
            name = p.name.lower()
            if p.suffix.lower() == '.json' or 'token' in name or 'auth' in name or 'session' in name:
                files.append(p)
    return files


def read_json(path: Path):
    try:
        raw = path.read_text(encoding='utf-8', errors='replace').strip()
        if not raw:
            return None, 'empty'
        data = json.loads(raw)
        if not isinstance(data, dict):
            return None, 'json_not_object'
        return data, None
    except Exception as e:
        return None, f'read_error:{e}'


def classify_failure(report: Dict[str, Any]) -> str:
    issues = set(report.get('issues') or [])
    probe_detail = (report.get('probe_detail') or '').lower()
    probe_json = report.get('probe_json') or {}
    status_code = report.get('status_code')

    # Online result takes priority for codex configs
    if report.get('type') == 'codex' and report.get('online_checked'):
        if report.get('online_valid') is True:
            return 'online_valid'
        if status_code in (401, 403):
            return 'online_invalid_or_revoked'
        if 'token_invalidated' in probe_detail:
            return 'online_invalid_or_revoked'
        return 'online_probe_failed'

    if 'expired_field_past' in issues or 'access_token_expired' in issues:
        return 'token_expired'
    if 'not_jwt' in ' '.join(issues) or 'decode_error' in ' '.join(issues):
        return 'malformed_token'
    if 'missing_type' in issues or 'missing_email' in issues:
        return 'incomplete_config'

    code = ''
    message = ''
    if isinstance(probe_json, dict):
        code = str(((probe_json.get('error') or {}).get('code') or '')).lower()
        message = str(((probe_json.get('error') or {}).get('message') or '')).lower()

    if status_code in (401, 403):
        return 'online_invalid_or_revoked'
    if 'token_invalidated' in probe_detail or 'token_invalidated' in code:
        return 'online_invalid_or_revoked'
    if 'signing in again' in probe_detail or 'signing in again' in message:
        return 'online_invalid_or_revoked'
    if report.get('online_checked') and report.get('online_valid') is False:
        return 'online_probe_failed'
    if report.get('valid_offline'):
        return 'looks_valid_offline'
    return 'unknown_failure'


def detect_quota_state(report: Dict[str, Any]) -> Tuple[bool, bool]:
    text = (report.get('probe_detail') or '').lower()
    pj = report.get('probe_json')

    if classify_failure(report) == 'online_invalid_or_revoked':
        return False, False

    has_account_info = False
    no_quota = False

    if isinstance(pj, dict):
        flat = json.dumps(pj, ensure_ascii=False).lower()
        has_account_info = any(k in flat for k in [
            'quota', 'limit', 'balance', 'usage', 'remaining', 'plan',
            '套餐', '限额', '额度', '余额', '剩余', '代码审查', 'weekly'
        ])
        zero_signals = [
            '"remaining": 0', '"remaining":0', '"quota": 0', '"quota":0',
            '"balance": 0', '"balance":0', '"weekly": 0', '"weekly":0'
        ]
        no_quota = any(z in flat for z in zero_signals)
        return has_account_info, no_quota

    has_account_info = any(k in text for k in [
        'quota', 'limit', 'balance', 'usage', 'remaining', 'plan',
        '套餐', '限额', '额度', '余额', '剩余', '代码审查', 'weekly'
    ])
    zero_signals = ['"remaining":0', '"remaining": 0', '"quota":0', '"quota": 0', '余额为0', '额度为0', '剩余为0']
    no_quota = any(z in text for z in zero_signals)
    return has_account_info, no_quota


def offline_check(data: Dict[str, Any]) -> Dict[str, Any]:
    result = {
        'type': data.get('type'),
        'email': data.get('email'),
        'account_id': data.get('account_id'),
        'valid_offline': True,
        'issues': [],
        'times': {},
        'tokens': {},
        'bucket': 'unknown'
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
                # For codex, id_token expiry is informational only; access_token may still be refreshed/usable in panel flow
                if exp_dt <= now and not (result['type'] == 'codex' and key == 'id_token'):
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


def build_codex_panel_payload(data: Dict[str, Any], auth_index: str = 'dd2b5cfe06a6586b') -> Dict[str, Any]:
    token = data.get('access_token', '')
    account_id = data.get('account_id', '')
    return {
        'authIndex': auth_index,
        'method': 'GET',
        'url': CODEX_USAGE_URL,
        'header': {
            'Authorization': f'Bearer {token}',
            'Chatgpt-Account-Id': account_id,
            'Content-Type': 'application/json',
            'User-Agent': CODEX_UA,
        }
    }


def online_probe_codex_panel(data: Dict[str, Any], probe_url: str, timeout: int = 15) -> Dict[str, Any]:
    out = {'online_checked': False, 'online_valid': None, 'probe': probe_url, 'probe_detail': None, 'probe_json': None}
    if requests is None:
        out['probe_detail'] = 'requests_not_installed'
        return out
    access_token = data.get('access_token')
    if not isinstance(access_token, str) or not access_token:
        out['probe_detail'] = 'no_access_token'
        return out
    if not data.get('account_id'):
        out['probe_detail'] = 'no_account_id'
        return out

    payload = build_codex_panel_payload(data)
    headers = {
        'Authorization': 'Bearer ab87036181',
        'Content-Type': 'application/json',
    }
    try:
        out['online_checked'] = True
        r = requests.post(probe_url, json=payload, headers=headers, timeout=timeout)
        out['status_code'] = r.status_code
        out['probe_detail'] = r.text[:5000]
        try:
            out['probe_json'] = r.json()
        except Exception:
            out['probe_json'] = None

        if r.status_code == 200:
            pj = out['probe_json']
            if isinstance(pj, dict):
                inner_status = pj.get('status_code') or pj.get('status')
                inner_body = pj.get('body')
                inner_header = pj.get('header') or {}
                code = ''
                msg = ''
                parsed_body = None
                if isinstance(inner_body, str):
                    try:
                        parsed_body = json.loads(inner_body)
                    except Exception:
                        parsed_body = None
                if isinstance(parsed_body, dict):
                    code = str(((parsed_body.get('error') or {}).get('code') or '')).lower()
                    msg = str(((parsed_body.get('error') or {}).get('message') or '')).lower()
                ide_error = ''
                if isinstance(inner_header, dict):
                    ide = inner_header.get('X-Openai-Ide-Error-Code') or inner_header.get('x-openai-ide-error-code')
                    if isinstance(ide, list) and ide:
                        ide_error = str(ide[0]).lower()
                    elif isinstance(ide, str):
                        ide_error = ide.lower()
                if inner_status in (401, 403) or code == 'token_invalidated' or 'invalidated' in msg or ide_error == 'token_invalidated':
                    out['online_valid'] = False
                else:
                    out['online_valid'] = True
            else:
                out['online_valid'] = False
        else:
            out['online_valid'] = False
    except Exception as e:
        out['online_checked'] = True
        out['online_valid'] = False
        out['probe_detail'] = str(e)
    return out


def online_probe_generic(data: Dict[str, Any], probe_url: str, timeout: int = 12) -> Dict[str, Any]:
    out = {'online_checked': False, 'online_valid': None, 'probe': probe_url, 'probe_detail': None, 'probe_json': None}
    if requests is None:
        out['probe_detail'] = 'requests_not_installed'
        return out
    access_token = data.get('access_token')
    if not isinstance(access_token, str) or not access_token:
        out['probe_detail'] = 'no_access_token'
        return out

    headers = {'Authorization': f'Bearer {access_token}'}
    try:
        out['online_checked'] = True
        r = requests.get(probe_url, headers=headers, timeout=timeout)
        out['status_code'] = r.status_code
        out['probe_detail'] = r.text[:5000]
        try:
            out['probe_json'] = r.json()
        except Exception:
            out['probe_json'] = None
        out['online_valid'] = 200 <= r.status_code < 300
    except Exception as e:
        out['online_checked'] = True
        out['online_valid'] = False
        out['probe_detail'] = str(e)
    return out


def online_probe(data: Dict[str, Any], probe_url: str, timeout: int = 12) -> Dict[str, Any]:
    if 'management/api-call' in probe_url:
        return online_probe_codex_panel(data, probe_url, timeout=timeout)
    return online_probe_generic(data, probe_url, timeout=timeout)


def decide_bucket(report: Dict[str, Any], use_probe: bool) -> str:
    if not report.get('valid_offline') and report.get('type') != 'codex':
        return 'invalid'
    if not use_probe:
        return 'valid'
    if report.get('online_valid') is True:
        has_account_info, no_quota = detect_quota_state(report)
        if no_quota:
            return 'no_quota'
        return 'valid'
    return 'invalid'


def render_text_report(path: Path, report: Dict[str, Any]) -> str:
    lines = []
    lines.append(f'FILE: {path}')
    lines.append(f"  type: {report.get('type')}")
    lines.append(f"  email: {report.get('email')}")
    lines.append(f"  account_id: {report.get('account_id')}")
    lines.append(f"  valid_offline: {report.get('valid_offline')}")
    if 'online_checked' in report:
        lines.append(f"  online_checked: {report.get('online_checked')}")
        lines.append(f"  online_valid: {report.get('online_valid')}")
        if report.get('status_code') is not None:
            lines.append(f"  status_code: {report.get('status_code')}")
    lines.append(f"  failure_class: {classify_failure(report)}")
    lines.append(f"  bucket: {report.get('bucket')}")
    for k, v in (report.get('times') or {}).items():
        lines.append(f'  {k}: {v}')
    if report.get('issues'):
        lines.append('  issues:')
        for issue in report['issues']:
            lines.append(f'    - {issue}')
    if report.get('probe_detail'):
        preview = report.get('probe_detail')[:300].replace('\n', ' ')
        lines.append(f"  probe_preview: {preview}")
    lines.append('')
    return '\n'.join(lines)


def safe_copy(src: Path, dst_dir: Path, group_name: Optional[str], index: List[Dict[str, Any]], report: Dict[str, Any], label: str):
    target_dir = dst_dir / group_name if group_name else dst_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    dst = target_dir / src.name
    base = src.stem
    suffix = src.suffix
    n = 1
    while dst.exists():
        dst = target_dir / f'{base}_{n}{suffix}'
        n += 1
    shutil.copy2(src, dst)
    index.append({
        'source': str(src),
        'saved_to': str(dst),
        'bucket': label,
        'type': report.get('type'),
        'email': report.get('email'),
        'account_id': report.get('account_id'),
        'valid_offline': report.get('valid_offline'),
        'online_valid': report.get('online_valid'),
        'failure_class': classify_failure(report),
        'saved_at': utc_now().isoformat(),
    })


def main():
    ap = argparse.ArgumentParser(description='批量检测 token/config 文件有效性（三分类：有效 / 无额度 / 无效）')
    ap.add_argument('path', nargs='?', default='.')
    ap.add_argument('--probe', action='store_true', help='在线探测 access_token 是否有效')
    ap.add_argument('--probe-url', default=DEFAULT_PROBE_URL)
    ap.add_argument('--save-valid-dir', help='把有效配置复制到这个目录')
    ap.add_argument('--save-no-quota-dir', help='把有效但没额度的配置复制到这个目录')
    ap.add_argument('--save-invalid-dir', help='把无效配置复制到这个目录')
    ap.add_argument('--group-by-type', action='store_true', help='按 type 分类保存')
    ap.add_argument('--index-file', default='index.json')
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--out')
    ap.add_argument('--redact-dump', action='store_true')
    args = ap.parse_args()

    target = Path(args.path).expanduser().resolve()
    files = [target] if target.is_file() else find_candidate_files(target)
    if not files:
        print('No candidate files found.')
        return 0

    reports_text = []
    any_bad = False
    saved_index = []
    valid_count = 0
    no_quota_count = 0
    invalid_count = 0

    for f in files:
        data, err = read_json(f)
        if err:
            rep = {
                'type': None,
                'email': None,
                'account_id': None,
                'valid_offline': False,
                'issues': [err],
                'times': {},
                'tokens': {},
                'bucket': 'invalid'
            }
        else:
            rep = offline_check(data)
            if args.probe:
                rep.update(online_probe(data, args.probe_url))
            if args.redact_dump:
                rep['redacted_config'] = redact_value('root', data)
            rep['bucket'] = decide_bucket(rep, args.probe)

        bucket = rep['bucket']
        if bucket == 'valid':
            valid_count += 1
        elif bucket == 'no_quota':
            no_quota_count += 1
        else:
            invalid_count += 1
            any_bad = True

        if args.save_valid_dir and bucket == 'valid':
            safe_copy(f, Path(args.save_valid_dir).expanduser().resolve(), rep.get('type') if args.group_by_type else None, saved_index, rep, 'valid')
        if args.save_no_quota_dir and bucket == 'no_quota':
            safe_copy(f, Path(args.save_no_quota_dir).expanduser().resolve(), rep.get('type') if args.group_by_type else None, saved_index, rep, 'no_quota')
        if args.save_invalid_dir and bucket == 'invalid':
            safe_copy(f, Path(args.save_invalid_dir).expanduser().resolve(), rep.get('type') if args.group_by_type else None, saved_index, rep, 'invalid')

        if args.json:
            print(json.dumps({'file': str(f), **rep}, ensure_ascii=False))
        else:
            reports_text.append(render_text_report(f, rep))
            if args.redact_dump and rep.get('redacted_config') is not None:
                reports_text.append('  redacted_config:')
                reports_text.append(json.dumps(rep['redacted_config'], ensure_ascii=False, indent=2))
                reports_text.append('')

    if not args.json:
        summary = [
            '=== Summary ===',
            f'total: {len(files)}',
            f'valid: {valid_count}',
            f'no_quota: {no_quota_count}',
            f'invalid: {invalid_count}',
            ''
        ]
        final = '\n'.join(summary + reports_text)
        if args.out:
            Path(args.out).write_text(final, encoding='utf-8')
            print(f'报告已写入: {args.out}')
        else:
            print(final)

    target_dirs = []
    if args.save_valid_dir:
        d = Path(args.save_valid_dir).expanduser().resolve()
        d.mkdir(parents=True, exist_ok=True)
        target_dirs.append(d)
    if args.save_no_quota_dir:
        d = Path(args.save_no_quota_dir).expanduser().resolve()
        d.mkdir(parents=True, exist_ok=True)
        target_dirs.append(d)
    if args.save_invalid_dir:
        d = Path(args.save_invalid_dir).expanduser().resolve()
        d.mkdir(parents=True, exist_ok=True)
        target_dirs.append(d)

    if target_dirs:
        index_root = target_dirs[0]
        index_path = index_root / args.index_file
        index_path.write_text(json.dumps(saved_index, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'索引文件: {index_path}')
        if args.save_valid_dir:
            print(f'有效配置目录: {Path(args.save_valid_dir).expanduser().resolve()}')
        if args.save_no_quota_dir:
            print(f'无额度配置目录: {Path(args.save_no_quota_dir).expanduser().resolve()}')
        if args.save_invalid_dir:
            print(f'无效配置目录: {Path(args.save_invalid_dir).expanduser().resolve()}')

    return 1 if any_bad else 0


if __name__ == '__main__':
    raise SystemExit(main())
