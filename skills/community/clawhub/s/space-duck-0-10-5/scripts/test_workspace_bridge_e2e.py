#!/usr/bin/env python3
"""End-to-end test for the BYOB workspace bridge reference runtime.

Spawns `workspace_bridge.py run` in-process on a free port pointing at a
temp directory; issues every endpoint as a real HTTP client; asserts
spec rev 4 wire behaviour. No mocks.

Exit non-zero on any failure.

Usage:
    python3 test_workspace_bridge_e2e.py
"""
import hashlib
import hmac
import json
import os
import pathlib
import secrets
import shutil
import socket
import sys
import tempfile
import threading
import time
import urllib.request, urllib.error

# Import the runtime as a module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import workspace_bridge as wb


BEAK_KEY = 'bk_LIVE_test_' + secrets.token_urlsafe(16)


def free_port() -> int:
    s = socket.socket(); s.bind(('127.0.0.1', 0)); p = s.getsockname()[1]; s.close(); return p


def start_server(workspace: pathlib.Path, port: int) -> threading.Thread:
    wb.BridgeHandler.workspace = wb.Workspace(workspace)
    wb.BridgeHandler.beak_key = BEAK_KEY
    httpd = wb._ReusableTCPServer(('127.0.0.1', port), wb.BridgeHandler)
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    # wait until ready
    for _ in range(20):
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.2): break
        except OSError:
            time.sleep(0.05)
    return httpd


def signed_req(method: str, port: int, path: str, body=None,
               if_none_match=None, if_match=None):
    body_bytes = json.dumps(body).encode() if body is not None else b''
    ts = int(time.time())
    sig = wb.expected_signature(BEAK_KEY, method, path, ts,
                                  body_bytes if body is not None else None)
    headers = {
        'Authorization': 'Bearer ' + BEAK_KEY,
        'X-Spaceduck-Timestamp': str(ts),
        'X-Spaceduck-Signature': sig,
    }
    if body is not None:
        headers['Content-Type'] = 'application/json'
    if if_none_match: headers['If-None-Match'] = if_none_match
    if if_match: headers['If-Match'] = if_match
    req = urllib.request.Request(
        f'http://127.0.0.1:{port}{path}',
        data=body_bytes if body is not None else None,
        method=method, headers=headers)
    try:
        r = urllib.request.urlopen(req, timeout=5)
        return r.getcode(), json.loads(r.read() or b'null')
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read() or b'null')
        except Exception: return e.code, {}


def ok(n): print(f'  ✓ {n}')
def fail(n, m): print(f'  ✗ {n}: {m}'); sys.exit(1)


def main():
    print('=== Workspace Bridge end-to-end ===\n')
    tmp = tempfile.mkdtemp(prefix='wb-e2e-')
    workspace = pathlib.Path(tmp)
    # Seed with realistic agent MDs
    (workspace / 'AGENTS.md').write_bytes(b'# Agents\n\nFirst version.\n')
    (workspace / 'SOUL.md').write_bytes(b'# Soul\n\nyou are wayne.\n')
    (workspace / 'config.json').write_bytes(b'{}')  # non-md, should be filtered

    port = free_port()
    start_server(workspace, port)

    # T1 — list returns only .md files; etag/size/modified_at present
    code, d = signed_req('GET', port, '/v1/files')
    if code != 200: fail('T1 list', f'code={code} d={d}')
    files = d.get('files', [])
    names = sorted([f['filename'] for f in files])
    if names != ['AGENTS.md', 'SOUL.md']:
        fail('T1 list', f'unexpected files: {names}')
    if any(not f.get('etag') for f in files):
        fail('T1 list', 'missing etag in some files')
    ok('T1 list (md-only, sorted, with etag)')

    # T2 — read AGENTS.md returns content + etag
    code, d = signed_req('GET', port, '/v1/file/AGENTS.md')
    if code != 200: fail('T2 read', f'code={code}')
    agents_etag = d['etag']
    if d['filename'] != 'AGENTS.md': fail('T2 read', 'filename mismatch')
    if not d['content'].startswith('# Agents'): fail('T2 read', 'content mismatch')
    ok('T2 read (200 with content + etag)')

    # T3 — If-None-Match match → 304
    code, d = signed_req('GET', port, '/v1/file/AGENTS.md', if_none_match=agents_etag)
    if code != 304: fail('T3 304', f'expected 304 got {code}')
    ok('T3 If-None-Match → 304')

    # T4 — missing file → 404
    code, d = signed_req('GET', port, '/v1/file/NOPE.md')
    if code != 404: fail('T4 404', f'expected 404 got {code} {d}')
    ok('T4 missing file → 404')

    # T5 — write requires confirmed_by_owner: true
    code, d = signed_req('POST', port, '/v1/file/AGENTS.md',
                          body={'content': '# new', 'if_match': agents_etag})
    if code != 412: fail('T5 412', f'expected 412 got {code} {d}')
    ok('T5 write without confirm → 412')

    # T6 — write with confirm + correct if_match → 200, etag rotates
    new_body = '# Agents v2\nUpdated by e2e test.\n'
    code, d = signed_req('POST', port, '/v1/file/AGENTS.md',
                          body={'content': new_body, 'if_match': agents_etag,
                                'confirmed_by_owner': True})
    if code != 200: fail('T6 write', f'code={code} d={d}')
    if d['etag'] == agents_etag: fail('T6 write', 'etag did not rotate')
    new_etag = d['etag']
    if not d.get('snapshot_key'): fail('T6 write', 'no snapshot recorded')
    ok('T6 write (etag rotates, snapshot recorded)')

    # T7 — second write with stale if_match → 409
    code, d = signed_req('POST', port, '/v1/file/AGENTS.md',
                          body={'content': '# stale', 'if_match': agents_etag,
                                'confirmed_by_owner': True})
    if code != 409: fail('T7 409', f'expected 409 got {code} {d}')
    ok('T7 stale if_match → 409')

    # T8 — re-read returns the new etag + content
    code, d = signed_req('GET', port, '/v1/file/AGENTS.md')
    if code != 200 or d['etag'] != new_etag: fail('T8 re-read', f'{code} {d}')
    if not d['content'].startswith('# Agents v2'): fail('T8 re-read', 'content not updated')
    ok('T8 re-read after write')

    # T9 — invalid filename rejected
    code, d = signed_req('GET', port, '/v1/file/../etc-passwd')
    if code != 404: fail('T9 traversal', f'expected 404 got {code} {d}')
    ok('T9 path traversal blocked')

    # T10 — bad sig rejected as 401 invalid_token (we deliberately use wrong key)
    bad_ts = int(time.time())
    bad_sig = hmac.new(b'WRONG_KEY', f'GET\n/v1/files\n{bad_ts}\n{wb.EMPTY_SHA256}'.encode(),
                       hashlib.sha256).hexdigest()
    req = urllib.request.Request(
        f'http://127.0.0.1:{port}/v1/files', method='GET',
        headers={'Authorization': 'Bearer ' + BEAK_KEY,
                 'X-Spaceduck-Timestamp': str(bad_ts),
                 'X-Spaceduck-Signature': bad_sig})
    try:
        urllib.request.urlopen(req, timeout=2)
        fail('T10 bad-sig', 'expected 401')
    except urllib.error.HTTPError as e:
        if e.code != 401: fail('T10 bad-sig', f'expected 401 got {e.code}')
        body = json.loads(e.read() or b'{}')
        if body.get('error') != 'bad_signature':
            fail('T10 bad-sig', f'expected bad_signature sub-code got {body}')
    ok('T10 bad signature → 401 bad_signature')

    # T11 — stale timestamp rejected
    stale_ts = int(time.time()) - 700  # > 10 min
    sig = wb.expected_signature(BEAK_KEY, 'GET', '/v1/files', stale_ts, None)
    req = urllib.request.Request(
        f'http://127.0.0.1:{port}/v1/files', method='GET',
        headers={'Authorization': 'Bearer ' + BEAK_KEY,
                 'X-Spaceduck-Timestamp': str(stale_ts),
                 'X-Spaceduck-Signature': sig})
    try:
        urllib.request.urlopen(req, timeout=2)
        fail('T11 skew', 'expected 401')
    except urllib.error.HTTPError as e:
        body = json.loads(e.read() or b'{}')
        if e.code != 401 or body.get('error') != 'stale_timestamp':
            fail('T11 skew', f'expected 401 stale_timestamp got {e.code} {body}')
    ok('T11 stale timestamp → 401 stale_timestamp')

    # cleanup
    shutil.rmtree(tmp, ignore_errors=True)

    print(f'\n=== PHASE 4 reference runtime: 11/11 PASS ===')
    return 0


if __name__ == '__main__':
    sys.exit(main())
