#!/usr/bin/env python3
"""Opt-in live duplicate verification. Never collected by unit-test discovery.

Requires an existing, authorized 8h ordinary-work record on the exact date.
Only cached authentication is used: no login/cache refresh, no OA writes.
"""
import argparse
import contextlib
from datetime import datetime
from decimal import Decimal
import io
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import requests
import oa_utils as oa
import submit_time_entry as cli
from personal_settings import DEFAULT_SETTINGS


LAST_REQUEST = None


def main():
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--date', default='2026-10-10')
    parser.add_argument('--project', required=True)
    parser.add_argument('--job-desc', required=True)
    parser.add_argument('--credentials', default=cli.DEFAULT_CREDS)
    parser.add_argument('--proof', required=True)
    args = parser.parse_args()
    account, password, host = oa.load_credentials(args.credentials, require_project=False)
    token = oa.load_cached_token(host, account, ttl_seconds=86400)
    if not token:
        parser.exit(1, 'Live verification blocked: no reusable cached token. No login or write attempted.\n')
    paths = [DEFAULT_SETTINGS, Path.home()/'.cache/sn-oa/token.enc', Path.home()/'.cache/sn-oa/token.json',
             Path(args.credentials).expanduser(), Path(str(Path(args.credentials).expanduser())+'.enc')]
    snapshots = {path: path.read_bytes() if path.exists() else None for path in paths}
    origin = urlsplit(host)
    allowed = {('POST','/sn/project/timeFeeDropDownPageList'),
               ('POST','/sn/system/dict/data/typeList'),
               ('POST','/sn/timeEntry/findEveryDayList')}
    requests_seen = []
    responses_seen = []
    denied = []
    original = requests.Session.request

    def read_only(session, method, url, **kwargs):
        global LAST_REQUEST
        parsed = urlsplit(url)
        key = (method.upper(), parsed.path)
        if (parsed.scheme, parsed.netloc) != (origin.scheme, origin.netloc) or key not in allowed:
            denied.append(key)
            raise AssertionError('Nonallowlisted request denied before network')
        requests_seen.append(key)
        LAST_REQUEST = key
        kwargs['allow_redirects'] = False
        try:
            response = original(session, method, url, **kwargs)
        except Exception as exc:
            responses_seen.append(dict(path=parsed.path, error_type=type(exc).__name__))
            raise
        responses_seen.append(dict(path=parsed.path, http_status=response.status_code))
        return response

    output, error = io.StringIO(), io.StringIO()
    with patch.object(requests.Session, 'request', read_only):
        session = oa.build_session(token)
        before, _ = oa.query_time_entries(session, host, args.date)
        assert len(before) == 1, 'Expected exactly one authorized existing record'
        row = before[0]
        assert row['projectName'] == args.project, 'Baseline project differs from authorized input'
        assert row['jobDesc'] == args.job_desc, 'Baseline description differs from authorized input'
        assert Decimal(row['manHour']) == Decimal(8), 'Baseline hours differ from authorized input'
        assert str(row['state']) == '20' and str(row['isDeleted']) == '0', 'Baseline state/deletion flag mismatch'
        argv = ['submit_time_entry.py', args.date, '--project', args.project,
                '--fill-type','工作','--project-phase','研发/交付','--work-type','开发',
                '--man-hour','8','--job-desc',args.job_desc,'--credentials',args.credentials,
                '--token',token,'--json']
        exit_code = 0
        with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(output), contextlib.redirect_stderr(error):
            try:
                cli.main()  # Real CLI, real option lookup, real low-level precheck.
            except SystemExit as exc:
                exit_code = exc.code
        after, _ = oa.query_time_entries(session, host, args.date)
    if exit_code != 0:
        diagnostic_tokens = ['节假日','缺少已确认','未知或歧义','同日存在','提交会话','自动重试','OA 地址','OA 查询','历史未核实','草稿','属性','绑定','权限','目录']
        print(json.dumps({'cli_exit_code':exit_code, 'diagnostic_tokens':[word for word in diagnostic_tokens if word in error.getvalue()],
                          'actual_requests':[list(key) for key in requests_seen], 'responses':responses_seen, 'denied_requests':len(denied)}, ensure_ascii=False))
    assert exit_code == 0, 'Actual CLI failed; no writes were allowed'
    result = json.loads(output.getvalue())
    assert result == {'code':200,'submission_status':'skipped-existing','verified':True}, 'Duplicate was not positively confirmed'
    assert before == after, 'Existing date records changed'
    assert not denied, 'A prohibited request was attempted'
    assert all(key in allowed for key in requests_seen)
    unchanged = all((path.read_bytes() if path.exists() else None) == value for path, value in snapshots.items())
    assert unchanged, 'Personal settings or authentication files changed'
    proof = dict(verified_at=datetime.now().astimezone().isoformat(), date=args.date,
                 execution='actual submit_time_entry.main, real Chinese choice resolution and common API precheck',
                 inputs=dict(project_name='<redacted verified project name>', fill_type='工作',
                             project_phase='研发/交付', work_type='开发', man_hour=8,
                             job_desc='<matched authorized existing description; redacted>'),
                 cli_exit_code=exit_code, cli_result=result,
                 baseline_record_count=len(before), final_record_count=len(after),
                 existing_records_exactly_unchanged=before==after,
                 personal_settings_and_auth_files_unchanged=unchanged,
                 network_allowlist=[list(key) for key in sorted(allowed)],
                 actual_requests=[list(key) for key in requests_seen],
                 denied_requests=len(denied), time_entry_write_requests=0,
                 request_redirects_disabled=True, actual_new_write_verified=False,
                 mocks='only transport allowlist interception and in-process CLI argv/output capture; no fake OA responses')
    Path(args.proof).write_text(json.dumps(proof, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(proof, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'live_verified':False, 'error_type':type(exc).__name__, 'last_allowlisted_request':LAST_REQUEST,
                          'assertion':str(exc) if isinstance(exc, AssertionError) else None}, ensure_ascii=False))
        raise SystemExit('Live verification blocked or assertion failed; no nonallowlisted requests permitted. No private exception details exported.') from None
