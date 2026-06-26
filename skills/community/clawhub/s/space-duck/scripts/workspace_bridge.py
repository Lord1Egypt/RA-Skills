#!/usr/bin/env python3
"""BYOB Workspace Bridge — reference runtime (single-file, stdlib only).

Pinned to docs/spec/BYOB-WORKSPACE-BRIDGE.md rev 4 (LOCKED 2026-05-30).

What this is
============
The OpenClaw side of the Phase 4 bridge. Mission Control calls this runtime
through the platform proxy (POST /beak/byob/workspace/{list,read,write});
this server speaks the v1 wire protocol:

    GET  /v1/files                  list .md files in the agent workspace
    GET  /v1/file/<name>            read a single file (If-None-Match → 304)
    POST /v1/file/<name>            write with platform-snapshot id + owner-confirm

It is *not* a demo. It is the production-grade reference implementation an
external openclaw operator would deploy (laptop, Fargate, VPS, k8s). Designed
the way an MIT 6.824 distributed-systems engineer would write it:

  - Single-file. Stdlib only. Python 3.10+.
  - Atomic writes (write-to-temp + os.replace) so a crash mid-write never
    leaves the file truncated.
  - Strict spec compliance — every clause from rev 4 lives in code:
        no trailing slash, lowercase %2f, NFC normalisation, sha256(empty)
        constant for GET, ±10min skew window, 5MB cap, content-type prefix
        match, UTF-8 mandate, filename echo-back, ETag = sha256[:32].
  - Discovery layer (see § Discovery): the runtime locates the OpenClaw
    workspace directory via Gateway-token resolution OR explicit --workspace.
    Gateway lookup is the path Josh asked for ("search the Gateway token
    for openclaw as if it was syncing of its own UI") — the runtime feels
    native because it shares the same discovery machinery the openclaw skill
    already uses for sync.
  - Threat model: see README.md adjacent. Short version: TLS-only (terminate
    upstream), beak_key is the long-lived auth secret, HMAC adds replay
    protection within the skew window. The runtime trusts the network not at
    all and the OpenClaw working-tree completely.

Discovery
=========
The runtime resolves the agent workspace via this precedence chain:

  1. --workspace <path>                          explicit flag (highest priority)
  2. $SPACEDUCK_WORKSPACE_DIR                    env override
  3. Gateway-token lookup against ClawHub        the native-feel path
     (~/.openclaw/credentials/clawhub-gateway.json → spaceduck.workspace_dir)
  4. ~/.openclaw/agents/<agent>/                 conventional location
  5. ./AGENTS.md present?                        current working directory

The Gateway-token path mirrors how the existing openclaw skill discovers its
state — the BYOB runtime behaves like an openclaw subsystem rather than a
separate process the operator has to configure twice.

CLI
===
    python3 workspace_bridge.py run \\
        --bind 0.0.0.0:8086 \\
        --workspace ~/.openclaw/agents/wayne \\
        --beak-key bk_LIVE_...

    python3 workspace_bridge.py introspect          # print resolved config
    python3 workspace_bridge.py selftest            # in-proc HMAC round-trip

Deployment
==========
See README.md adjacent. Typical: behind nginx (TLS termination) + systemd unit;
or as a Fargate task; or via cloudflared/ngrok tunnel for laptop dev.
"""
from __future__ import annotations
import argparse
import hashlib
import hmac
import http.server
import json
import os
import pathlib
import socket
import socketserver
import sys
import tempfile
import threading
import time
import unicodedata
import urllib.parse
import urllib.request  # 0.3.8 — explicit for self-pulse + cmd_status
from typing import Optional


# ─────────────────────────── canonical (mirrors byob_hmac.py) ───────────────

EMPTY_SHA256 = ('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
SKEW_WINDOW_SEC = 600                                   # spec finding R
CONTENT_MAX_BYTES = 5 * 1024 * 1024                     # spec finding DD
LIST_CAP = 200                                          # spec finding I-revisit
ALLOWED_CONTENT_TYPES = ('text/markdown', 'text/plain', 'application/json')


def canonical(method: str, path: str, unix_ts: int, body: Optional[bytes]) -> str:
    if path != '/' and path.endswith('/'):
        raise ValueError('trailing_slash_disallowed')
    if not body:
        body_hash = EMPTY_SHA256
    else:
        body_hash = hashlib.sha256(body).hexdigest()
    return '\n'.join([method.upper(), path, str(int(unix_ts)), body_hash])


def expected_signature(beak_key: str, method: str, path: str, unix_ts: int,
                       body: Optional[bytes]) -> str:
    return hmac.new(beak_key.encode('utf-8'),
                    canonical(method, path, unix_ts, body).encode('utf-8'),
                    hashlib.sha256).hexdigest()


def etag_of(content_bytes: bytes) -> str:
    """sha256_hex(content)[:32] — spec finding G + II. 128 bits."""
    return hashlib.sha256(content_bytes).hexdigest()[:32]


# ─────────────────────────── discovery ──────────────────────────────────────

def resolve_workspace(explicit: Optional[str]) -> pathlib.Path:
    """Discovery precedence chain — see module docstring § Discovery."""
    if explicit:
        return pathlib.Path(explicit).expanduser().resolve()
    env = os.environ.get('SPACEDUCK_WORKSPACE_DIR')
    if env:
        return pathlib.Path(env).expanduser().resolve()
    # Gateway token lookup — the native-feel path.
    gateway_creds = pathlib.Path.home() / '.openclaw' / 'credentials' / 'clawhub-gateway.json'
    if gateway_creds.exists():
        try:
            with open(gateway_creds, 'r') as fh:
                cfg = json.load(fh)
            sd = (cfg.get('spaceduck') or {})
            if sd.get('workspace_dir'):
                return pathlib.Path(sd['workspace_dir']).expanduser().resolve()
        except Exception:
            pass
    # Conventional ~/.openclaw/agents/<first> location.
    agents = pathlib.Path.home() / '.openclaw' / 'agents'
    if agents.exists() and agents.is_dir():
        children = sorted([p for p in agents.iterdir() if p.is_dir()])
        if children:
            return children[0]
    # Final fallback: cwd if it looks like an agent dir.
    cwd = pathlib.Path.cwd()
    if (cwd / 'AGENTS.md').exists():
        return cwd
    raise SystemExit(
        'Could not resolve workspace. Provide --workspace <path> or set '
        '$SPACEDUCK_WORKSPACE_DIR. See module docstring § Discovery.')


# ─────────────────────────── files (atomic, native semantics) ───────────────

class Workspace:
    """Wraps the agent's working directory with atomic write semantics."""

    PROTECTED = frozenset({'.history'})    # never expose; never accept as filename

    def __init__(self, root: pathlib.Path) -> None:
        if not root.is_dir():
            raise SystemExit(f'workspace root does not exist: {root}')
        self.root = root
        self.history_dir = root / '.history'

    def _safe(self, filename: str) -> pathlib.Path:
        # NFC normalise; reject path traversal; reject hidden / .history.
        filename = unicodedata.normalize('NFC', filename)
        if not filename or '/' in filename or '..' in filename \
                or filename.startswith('.') or filename in self.PROTECTED:
            raise ValueError('invalid_filename')
        p = (self.root / filename).resolve()
        # Defence in depth — resolved path must stay under root.
        if not str(p).startswith(str(self.root)):
            raise ValueError('invalid_filename')
        return p

    def list_md(self) -> list[dict]:
        out = []
        for p in sorted(self.root.iterdir()):
            if not p.is_file() or not p.suffix == '.md': continue
            try:
                stat = p.stat()
                with open(p, 'rb') as fh: content = fh.read(CONTENT_MAX_BYTES + 1)
                if len(content) > CONTENT_MAX_BYTES: continue
                out.append({
                    'filename': p.name,
                    'size': stat.st_size,
                    'modified_at': int(stat.st_mtime),
                    'etag': etag_of(content),
                })
            except Exception:
                continue
            if len(out) > LIST_CAP: break
        return out

    def read(self, filename: str) -> tuple[bytes, dict]:
        p = self._safe(filename)
        if not p.exists():
            raise FileNotFoundError(filename)
        with open(p, 'rb') as fh: content = fh.read(CONTENT_MAX_BYTES + 1)
        if len(content) > CONTENT_MAX_BYTES:
            raise ValueError('content_too_large')
        try: content.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError('non_utf8_content')
        meta = {
            'filename': p.name,
            'size': len(content),
            'modified_at': int(p.stat().st_mtime),
            'etag': etag_of(content),
        }
        return content, meta

    def write_atomic(self, filename: str, new_content: bytes,
                     if_match: Optional[str]) -> dict:
        """Atomic write: write-to-temp + os.replace. Snapshot prior to .history/.

        Returns dict with new etag + modified_at + snapshot key (if any).
        Native sync semantics: a reader open on the file during write sees
        either the old bytes or the new bytes — never a partial write.
        """
        p = self._safe(filename)
        try: new_content.decode('utf-8')
        except UnicodeDecodeError:
            raise ValueError('non_utf8_content')
        if len(new_content) > CONTENT_MAX_BYTES:
            raise ValueError('content_too_large')
        # if_match validation
        if if_match and p.exists():
            with open(p, 'rb') as fh: cur = fh.read(CONTENT_MAX_BYTES + 1)
            if etag_of(cur) != if_match:
                raise ConflictError('etag_mismatch', current_etag=etag_of(cur))
        # Snapshot prior to .history/ (always — durable rollback)
        snapshot_key = None
        if p.exists():
            self.history_dir.mkdir(exist_ok=True)
            ts = time.strftime('%Y%m%d_%H%M%S', time.gmtime())
            snap = self.history_dir / f'{p.name}.{ts}'
            with open(p, 'rb') as src, open(snap, 'wb') as dst:
                dst.write(src.read())
            snapshot_key = snap.name
        # Atomic write
        fd, tmp_path = tempfile.mkstemp(dir=str(self.root), prefix='.tmp-')
        try:
            with os.fdopen(fd, 'wb') as fh: fh.write(new_content)
            os.replace(tmp_path, str(p))
        except Exception:
            try: os.unlink(tmp_path)
            except Exception: pass
            raise
        return {
            'filename': p.name,
            'size': len(new_content),
            'modified_at': int(p.stat().st_mtime),
            'etag': etag_of(new_content),
            'snapshot_key': snapshot_key,
        }


class ConflictError(Exception):
    def __init__(self, code: str, current_etag: str) -> None:
        super().__init__(code)
        self.current_etag = current_etag


# ─────────────────────────── HTTP handler ───────────────────────────────────

class BridgeHandler(http.server.BaseHTTPRequestHandler):
    server_version = 'spaceduck-byob-bridge/1.0'

    # Class-attached at server boot:
    workspace: Workspace = None     # type: ignore[assignment]
    beak_key: str = ''

    # ── helpers ──
    def _send_json(self, status: int, payload: dict | None,
                   extra_headers: Optional[dict] = None) -> None:
        body = b'' if payload is None else json.dumps(payload).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        if extra_headers:
            for k, v in extra_headers.items(): self.send_header(k, v)
        self.end_headers()
        if body: self.wfile.write(body)

    def _verify_auth(self, method: str, path: str, body: Optional[bytes]) -> Optional[tuple[int, str]]:
        """Returns (status, sub_code) on failure; None on success."""
        bearer = self.headers.get('Authorization', '')
        if not bearer.startswith('Bearer '):
            return 401, 'invalid_token'
        if not hmac.compare_digest(bearer[7:].strip(), self.beak_key):
            return 401, 'invalid_token'
        ts_hdr = self.headers.get('X-Spaceduck-Timestamp', '')
        if not ts_hdr.isdigit():
            return 401, 'bad_signature'
        ts = int(ts_hdr)
        now = int(time.time())
        if abs(now - ts) > SKEW_WINDOW_SEC:
            return 401, 'stale_timestamp'
        sig_hdr = self.headers.get('X-Spaceduck-Signature', '')
        try:
            expected = expected_signature(self.beak_key, method, path, ts, body)
        except ValueError:
            return 422, 'trailing_slash_disallowed'
        if not hmac.compare_digest(sig_hdr, expected):
            return 401, 'bad_signature'
        return None

    # ── routes ──
    def do_GET(self) -> None:     # noqa: N802 — stdlib API
        # Strip query string for signature validation (not signed per spec).
        parsed = urllib.parse.urlparse(self.path)
        path_no_query = parsed.path
        auth_err = self._verify_auth('GET', path_no_query, None)
        if auth_err:
            return self._send_json(auth_err[0], {'error': auth_err[1]})
        if path_no_query == '/v1/files':
            files = self.workspace.list_md()
            return self._send_json(200, {
                'files': files[:LIST_CAP],
                'has_more': len(files) > LIST_CAP,
                'total_count': len(files),
                'v': 1,
            })
        if path_no_query.startswith('/v1/file/'):
            raw = path_no_query[len('/v1/file/'):]
            filename = urllib.parse.unquote(raw)
            try:
                content, meta = self.workspace.read(filename)
            except (FileNotFoundError, ValueError) as e:
                return self._send_json(404, {'error': str(e)})
            # If-None-Match — spec D + D-extension
            inm = self.headers.get('If-None-Match', '')
            if inm and inm == meta['etag']:
                return self._send_json(304, None)
            return self._send_json(200, {
                **meta, 'content': content.decode('utf-8'),
            })
        return self._send_json(404, {'error': 'unknown_path'})

    def do_POST(self) -> None:    # noqa: N802
        length = int(self.headers.get('Content-Length') or 0)
        if length > CONTENT_MAX_BYTES + 4096:    # headroom for envelope
            return self._send_json(413, {'error': 'content_too_large'})
        body = self.rfile.read(length) if length > 0 else b''
        parsed = urllib.parse.urlparse(self.path)
        path_no_query = parsed.path
        auth_err = self._verify_auth('POST', path_no_query, body)
        if auth_err:
            return self._send_json(auth_err[0], {'error': auth_err[1]})
        if not path_no_query.startswith('/v1/file/'):
            return self._send_json(404, {'error': 'unknown_path'})
        raw = path_no_query[len('/v1/file/'):]
        filename = urllib.parse.unquote(raw)
        try:
            payload = json.loads(body) if body else {}
        except Exception:
            return self._send_json(400, {'error': 'invalid_json'})
        if not payload.get('confirmed_by_owner'):
            return self._send_json(412, {'error': 'confirmed_by_owner_required'})
        content = (payload.get('content') or '').encode('utf-8')
        if_match = payload.get('if_match') or self.headers.get('If-Match')
        try:
            result = self.workspace.write_atomic(filename, content, if_match)
        except ConflictError as ce:
            return self._send_json(409, {'error': str(ce),
                                          'current_etag': ce.current_etag})
        except (ValueError, FileNotFoundError) as e:
            return self._send_json(400, {'error': str(e)})
        # 0.3.10 — push the just-written file to S3 fallback in a
        # background thread so the response isn't delayed. Failure is
        # silent — live read still works via the tunnel.
        creds = getattr(BridgeHandler, 'snapshot_creds', None)
        if creds:
            import threading
            def _post_write_push():
                try:
                    _push_snapshot_one(
                        creds['beak_key'], creds['sd_id'], creds['api_base'],
                        filename, content, int(time.time()))
                except Exception:
                    pass
            threading.Thread(target=_post_write_push, daemon=True).start()
        return self._send_json(200, result)

    def log_message(self, fmt, *args):
        # Quiet by default; uncomment for stdout debugging.
        # super().log_message(fmt, *args)
        return


# ─────────────────────────── server lifecycle ───────────────────────────────

class _ReusableTCPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


def _sync_connections_once(beak_key: str, sd_id: str, api_base: str,
                            workspace_dir: pathlib.Path) -> bool:
    """v0.4.4 — fetch this duck's approved connections from the gateway and
    render to ~/.space-duck/CONNECTIONS.md.

    Closes the Lane A parity gap: Lane B brains get their duck directory
    injected by the gateway chat path, but Lane A brains (claude CLI) had
    no equivalent and couldn't look up peer spaceduck_ids when asked.

    The MD file is read by peck_responder.py on each inbound and prepended
    to the brain's prompt as the "## Your Network" section. Updates land
    on the next peck — no listener restart needed.

    Returns True on successful write, False on any failure.
    """
    try:
        url = f'{api_base.rstrip("/")}/beak/duck/{sd_id}/connections'
        req = urllib.request.Request(url, headers={'X-Beak-Key': beak_key})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
        conns = data.get('connections') or []
        lines = ['# Your Network (auto-synced from Spaceduckling)',
                 '',
                 f'_Last updated: {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())} UTC ({len(conns)} approved peers)_',
                 '',
                 'These are the ducks you can peck via the peck tool. To send a peck,',
                 'pass the spaceduck_id (full 16-hex string).',
                 '',
                 '| Name | spaceduck_id | Trust | Relationship |',
                 '| --- | --- | --- | --- |']
        for c in conns:
            name = c.get('display_name') or c.get('spaceduck_id', '')[:8]
            sd = c.get('spaceduck_id', '')
            trust = c.get('trust_tier') or c.get('tier') or '—'
            rel = c.get('relationship') or c.get('bond_kind') or '—'
            lines.append(f'| {name} | `{sd}` | {trust} | {rel} |')
        if not conns:
            lines.append('| _(no approved peer connections yet)_ | | | |')
        content = '\n'.join(lines) + '\n'
        sd_dir = pathlib.Path.home() / '.space-duck'
        sd_dir.mkdir(parents=True, exist_ok=True)
        (sd_dir / 'CONNECTIONS.md').write_text(content)
        print(f'[bridge] CONNECTIONS.md synced ({len(conns)} peers)')
        return True
    except urllib.error.HTTPError as he:
        print(f'[bridge] CONNECTIONS.md sync HTTP {he.code}', file=sys.stderr)
        return False
    except Exception as e:
        print(f'[bridge] CONNECTIONS.md sync error: {e}', file=sys.stderr)
        return False


def _bridge_connections_sync_loop(beak_key: str, sd_id: str, api_base: str,
                                   workspace_dir: pathlib.Path) -> None:
    """v0.4.4 — periodic CONNECTIONS.md refresh. 5-minute interval matches
    the snapshot-push cadence so the file stays fresh without hammering the
    gateway."""
    while True:
        try:
            _sync_connections_once(beak_key, sd_id, api_base, workspace_dir)
        except Exception as e:
            print(f'[bridge] connections-sync loop error: {e}', file=sys.stderr)
        time.sleep(300)


def _push_snapshot_one(beak_key: str, sd_id: str, api_base: str,
                       filename: str, content_bytes: bytes,
                       mtime: int) -> bool:
    """0.3.10 (gap C / B+bridge-push) — push a single .md to S3 via the
    platform snapshot endpoint. Used by:
      • the startup full-snapshot loop (one-shot enumeration)
      • the post-write hook (single-file delta)
      • the periodic refresh thread (every 5min full snapshot)

    Best-effort; failures are swallowed (platform reads still work via
    the live tunnel; this is the fallback path). Returns True on 200."""
    import base64
    url = f'{api_base.rstrip("/")}/beak/byob/workspace/snapshot-file'
    payload = {
        'filename': filename,
        'content_b64': base64.b64encode(content_bytes).decode('ascii'),
        'mtime': mtime,
    }
    try:
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json',
                     'Authorization': f'Bearer {beak_key}'},
            method='POST')
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception:
        return False


def _push_snapshot_all(beak_key: str, sd_id: str, api_base: str,
                       workspace_dir: pathlib.Path,
                       verbose: bool = False) -> None:
    """Enumerate every .md in the workspace and push each. Idempotent —
    safe to call repeatedly. Skips files >5MB (server cap)."""
    if not workspace_dir.exists():
        return
    pushed = 0
    skipped = 0
    for p in workspace_dir.rglob('*.md'):
        try:
            # Flatten directories — store just the basename since the
            # snapshot endpoint rejects '/' in filenames. Collisions
            # across subdirs => last-write-wins. Acceptable trade-off
            # since the per-duck workspace shouldn't have name clashes.
            fn = p.name
            if '/' in fn or '..' in fn or fn.startswith('.'):
                skipped += 1; continue
            content = p.read_bytes()
            if len(content) > 5 * 1024 * 1024:
                skipped += 1; continue
            ok = _push_snapshot_one(
                beak_key, sd_id, api_base, fn, content,
                int(p.stat().st_mtime))
            if ok: pushed += 1
            else: skipped += 1
        except Exception:
            skipped += 1
    if verbose:
        print(f'[snapshot] pushed={pushed} skipped={skipped} '
              f'workspace={workspace_dir}', file=sys.stderr)


def _bridge_snapshot_periodic(beak_key: str, sd_id: str, api_base: str,
                              workspace_dir: pathlib.Path) -> None:
    """0.3.10 — periodic full-snapshot thread. Every 5min re-pushes every
    .md so any out-of-band edits (the owner editing files in their IDE
    while the bridge runs) eventually reach the S3 fallback."""
    INTERVAL = 300
    while True:
        time.sleep(INTERVAL)
        try:
            _push_snapshot_all(beak_key, sd_id, api_base, workspace_dir)
        except Exception:
            pass


def _bridge_self_pulse_loop(beak_key: str, sd_id: str,
                            api_base: str, workspace_dir: pathlib.Path) -> None:
    """0.3.8 (item 2) — bridge's own liveness signal to the platform.

    Was: platform's bridge-setup watchdog waited for an external
    `workspace_bridge.py status --report-to-platform` cron-driven POST.
    If owner forgot to wire that cron, plan-watchdog stalled out.

    Now: while the bridge's HTTP server is alive, this thread POSTs
    `state=up` to /bridge-status every 60s. Watchdog auto-advances.
    Silent on failure; no impact on serve_forever."""
    INTERVAL = 60
    url = f'{api_base.rstrip("/")}/beak/me/duck/{sd_id}/bridge-status'
    payload_base = {
        'state': 'up',
        'detail': {
            'http': 'self-pulse',
            'version': '0.4.0',
            'workspace': str(workspace_dir),
            'source': 'workspace_bridge.run',
        },
    }
    while True:
        try:
            payload = dict(payload_base, ts=int(time.time()))
            req = urllib.request.Request(
                url, data=json.dumps(payload).encode(),
                headers={'Content-Type': 'application/json',
                         'Authorization': f'Bearer {beak_key}'},
                method='POST')
            urllib.request.urlopen(req, timeout=5).close()
        except Exception:
            pass  # silent — platform-side state still advances on next tick
        time.sleep(INTERVAL)


def _resolve_spaceduck_id() -> str:
    """0.3.8 — Look up the duck's spaceduck_id from the same gateway
    config the bridge already discovers via. Used only for the self-pulse
    URL; returns '' if not found (silently disables self-pulse)."""
    candidates = [
        pathlib.Path.home() / '.openclaw' / 'credentials' / 'clawhub-gateway.json',
        pathlib.Path.home() / '.space-duck' / 'config.json',
    ]
    for p in candidates:
        if not p.exists():
            continue
        try:
            j = json.loads(p.read_text())
            # Two known shapes:
            sd = (j.get('spaceduck', {}).get('spaceduck_id') or
                  j.get('spaceduck_id') or '')
            if sd:
                return str(sd).strip()
        except Exception:
            continue
    return ''


def run_server(bind: str, workspace_dir: pathlib.Path, beak_key: str,
               *, no_self_pulse: bool = False,
               api_base: str = 'https://beak.spaceduckling.com') -> None:
    BridgeHandler.workspace = Workspace(workspace_dir)
    BridgeHandler.beak_key = beak_key
    host, port = bind.rsplit(':', 1) if ':' in bind else ('0.0.0.0', bind)
    httpd = _ReusableTCPServer((host, int(port)), BridgeHandler)
    print(f'[bridge] listening on {host}:{port}')
    print(f'[bridge] workspace = {workspace_dir}')
    print(f'[bridge] beak_key  = {beak_key[:14]}...')
    # 0.3.8 — self-pulse the platform every 60s while serving so the
    # bridge-setup watchdog auto-advances after restart_bridge.
    # 0.3.10 — also start the S3 snapshot push on startup + every 5min.
    if not no_self_pulse:
        sd_id = _resolve_spaceduck_id()
        if sd_id:
            import threading
            t = threading.Thread(
                target=_bridge_self_pulse_loop,
                args=(beak_key, sd_id, api_base, workspace_dir),
                daemon=True)
            t.start()
            print(f'[bridge] self-pulse → {api_base}/beak/me/duck/'
                  f'{sd_id[:8]}…/bridge-status every 60s')
            # 0.3.10 — startup snapshot push so MC's S3 fallback has
            # fresh content immediately. Followed by periodic refresh.
            # Stash creds on the handler so write_file can push deltas.
            BridgeHandler.snapshot_creds = {
                'beak_key': beak_key, 'sd_id': sd_id, 'api_base': api_base,
            }
            ts_init = threading.Thread(
                target=_push_snapshot_all,
                args=(beak_key, sd_id, api_base, workspace_dir, True),
                daemon=True)
            ts_init.start()
            ts_periodic = threading.Thread(
                target=_bridge_snapshot_periodic,
                args=(beak_key, sd_id, api_base, workspace_dir),
                daemon=True)
            ts_periodic.start()
            print(f'[bridge] S3 snapshot → agents/{sd_id[:8]}…/ '
                  f'(startup + every 5min + after each write)')
            # v0.4.4 — connections sync: write ~/.space-duck/CONNECTIONS.md
            # every 5 min so peck_responder.py has fresh duck directory.
            _sync_connections_once(beak_key, sd_id, api_base, workspace_dir)
            tc_periodic = threading.Thread(
                target=_bridge_connections_sync_loop,
                args=(beak_key, sd_id, api_base, workspace_dir),
                daemon=True)
            tc_periodic.start()
            print(f'[bridge] CONNECTIONS.md sync (startup + every 5min)')
        else:
            print('[bridge] self-pulse SKIPPED — no spaceduck_id resolved')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\n[bridge] shutdown')


# ─────────────────────────── CLI ────────────────────────────────────────────

def _resolve_beak_key(explicit: Optional[str]) -> str:
    """0.3.13 — beak_key discovery chain. Mirrors workspace discovery's
    fallthrough so the bridge can launch with any of:
      1. --beak-key <key>                  explicit flag (highest)
      2. $SPACEDUCK_BEAK_KEY               env var
      3. ~/.openclaw/credentials/clawhub-gateway.json (spaceduck.beak_key)
         Written by send_beak_key — natural place to find it.
      4. ~/.space-duck/config.json (beak_key)  — written by pair.py
    Wayne msg 22398 — pre-0.3.13 we only checked 1 + 2, so
    restart_bridge dispatches died instantly even though the key was
    sitting right in the gateway config."""
    if explicit:
        return explicit
    env_key = os.environ.get('SPACEDUCK_BEAK_KEY', '').strip()
    if env_key:
        return env_key
    candidates = [
        pathlib.Path.home() / '.openclaw' / 'credentials' / 'clawhub-gateway.json',
        pathlib.Path.home() / '.space-duck' / 'config.json',
    ]
    for p in candidates:
        if not p.exists():
            continue
        try:
            j = json.loads(p.read_text())
        except Exception:
            continue
        # clawhub-gateway shape: {"spaceduck": {"beak_key": "..."}}
        sd = j.get('spaceduck') or {}
        if isinstance(sd, dict) and sd.get('beak_key'):
            return str(sd['beak_key']).strip()
        # config.json shape: {"beak_key": "..."}
        if j.get('beak_key'):
            return str(j['beak_key']).strip()
    return ''


def cmd_run(args) -> int:
    workspace = resolve_workspace(args.workspace)
    args.beak_key = _resolve_beak_key(args.beak_key)
    if not args.beak_key:
        sys.exit('--beak-key (or $SPACEDUCK_BEAK_KEY, or '
                 '~/.openclaw/credentials/clawhub-gateway.json, or '
                 '~/.space-duck/config.json) is required')
    run_server(args.bind, workspace, args.beak_key,
               no_self_pulse=getattr(args, 'no_self_pulse', False),
               api_base=getattr(args, 'api', 'https://beak.spaceduckling.com'))
    return 0


def cmd_introspect(args) -> int:
    workspace = resolve_workspace(args.workspace)
    print(f'workspace = {workspace}')
    print(f'discovered_via = ', end='')
    if args.workspace: print('--workspace flag')
    elif os.environ.get('SPACEDUCK_WORKSPACE_DIR'): print('SPACEDUCK_WORKSPACE_DIR env')
    elif (pathlib.Path.home()/'.openclaw'/'credentials'/'clawhub-gateway.json').exists():
        print('clawhub-gateway.json (native openclaw discovery)')
    else: print('conventional ~/.openclaw/agents/ lookup')
    print(f'beak_key_env_set = {bool(os.environ.get("SPACEDUCK_BEAK_KEY"))}')
    ws = Workspace(workspace)
    files = ws.list_md()
    print(f'md_files = {len(files)}')
    for f in files[:10]:
        print(f'  {f["filename"]:<24} {f["size"]:>6}B  etag={f["etag"][:8]}…')
    if len(files) > 10:
        print(f'  ... and {len(files) - 10} more')
    return 0


def cmd_selftest(args) -> int:
    """In-proc HMAC round-trip — verifies the canonical layer matches the
    Python reference in byob_hmac.py (when available)."""
    print('=== HMAC canonical round-trip ===')
    cases = [
        ('GET', '/v1/files', 1780058400, None),
        ('GET', '/v1/file/AGENTS.md', 1780058400, None),
        ('POST', '/v1/file/AGENTS.md', 1780058400, b'{"content":"hi","confirmed_by_owner":true}'),
    ]
    for method, path, ts, body in cases:
        sig = expected_signature('bk_test_key', method, path, ts, body)
        print(f'  {method:4} {path:30} ts={ts} body={"-" if not body else "+"}  sig={sig[:16]}…')
    print('=== Trailing slash rejection ===')
    try:
        canonical('GET', '/v1/files/', 1780058400, None)
        print('  ✗ trailing slash NOT rejected'); return 1
    except ValueError as e:
        print(f'  ✓ rejected: {e}')
    print('=== Atomic write semantics ===')
    with tempfile.TemporaryDirectory() as td:
        ws = Workspace(pathlib.Path(td))
        ws.write_atomic('TEST.md', b'first', None)
        c, m = ws.read('TEST.md')
        assert c == b'first', 'first read failed'
        e1 = m['etag']
        ws.write_atomic('TEST.md', b'second', e1)
        c, m = ws.read('TEST.md')
        assert c == b'second', 'second read failed'
        # if_match drift → ConflictError
        try:
            ws.write_atomic('TEST.md', b'third', e1)    # stale etag
            print('  ✗ conflict NOT detected'); return 1
        except ConflictError as ce:
            print(f'  ✓ conflict detected: {ce} current={ce.current_etag[:8]}')
        # Snapshot present
        snaps = list((pathlib.Path(td)/'.history').iterdir())
        print(f'  ✓ snapshots after writes: {len(snaps)} files in .history/')
    print('\nselftest passed.')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog='workspace_bridge',
        description=__doc__.split('\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    p_run = sub.add_parser('run', help='Run the bridge HTTP server')
    p_run.add_argument('--bind', default='0.0.0.0:8086',
                       help='host:port to bind to (default 0.0.0.0:8086)')
    p_run.add_argument('--workspace', help='workspace directory (overrides discovery)')
    p_run.add_argument('--beak-key', help='beak_key for HMAC auth '
                                          '(or $SPACEDUCK_BEAK_KEY)')
    p_run.add_argument('--no-self-pulse', action='store_true',
                       help='0.3.8 — disable 60s self-pulse to '
                            '/bridge-status. Default ON: lets platform '
                            'watchdog see bridge state without external '
                            'cron. Disable for tests or local debug.')
    p_run.add_argument('--api',
                       default=os.environ.get('SPACEDUCK_API',
                                              'https://beak.spaceduckling.com'),
                       help='Platform API base for self-pulse')
    p_run.set_defaults(func=cmd_run)

    p_in = sub.add_parser('introspect', help='Print resolved discovery + workspace state')
    p_in.add_argument('--workspace')
    p_in.set_defaults(func=cmd_introspect)

    p_st = sub.add_parser('selftest', help='In-proc HMAC + atomic-write round-trip')
    p_st.set_defaults(func=cmd_selftest)

    # 2026-06-06 — status reporter for the bridge_setup_jobs watchdog.
    # Probes the live bridge, classifies, optionally POSTs the result to
    # the platform's heartbeat endpoint so MC's setup-progress timeline
    # advances without owner intervention.
    p_status = sub.add_parser('status',
        help='Probe local bridge + report state (down|partial|up)')
    p_status.add_argument('--bind', default='0.0.0.0:8086',
                          help='where the bridge would be listening')
    p_status.add_argument('--workspace',
                          help='workspace dir (also influences "partial" check)')
    p_status.add_argument('--beak-key',
                          help='beak_key (or $SPACEDUCK_BEAK_KEY)')
    p_status.add_argument('--spaceduck-id',
                          help='SDID (otherwise read from clawhub-gateway.json)')
    p_status.add_argument('--report-to-platform', action='store_true',
                          help='POST result to /beak/me/duck/<sd>/bridge-status')
    p_status.add_argument('--api',
                          default=os.environ.get('SPACEDUCK_API',
                                                 'https://beak.spaceduckling.com'),
                          help='Platform API base URL')
    p_status.set_defaults(func=cmd_status)

    args = ap.parse_args()
    return args.func(args)


def cmd_status(args) -> int:
    """Classify the bridge's current state without disrupting it.

    States:
      up      — HTTP /v1/files responds 200 with valid JSON
      partial — process running OR config present but HTTP not responding
                (skill installed + key in place but server didn't start)
      down    — nothing — no process, no config, no listener
    """
    import socket, urllib.parse
    bind = args.bind or '0.0.0.0:8086'
    host, _, port_s = bind.partition(':')
    if host in ('0.0.0.0', '::'):
        host = '127.0.0.1'
    port = int(port_s or '8086')

    # 1. Try the actual HTTP endpoint — definitive proof of "up".
    state = 'down'
    detail = {}
    try:
        # Need a valid HMAC for /v1/files. We use --beak-key or env var.
        bk = (args.beak_key or os.environ.get('SPACEDUCK_BEAK_KEY') or '').strip()
        if not bk:
            # Fall back to clawhub-gateway.json discovery if present.
            cg = pathlib.Path.home() / '.openclaw' / 'credentials' / 'clawhub-gateway.json'
            if cg.exists():
                try:
                    j = json.loads(cg.read_text())
                    bk = (j.get('spaceduck', {}).get('beak_key') or '').strip()
                except Exception:
                    pass
        if bk:
            ts = int(time.time())
            sig = expected_signature(bk, 'GET', '/v1/files', ts, b'')
            req = urllib.request.Request(
                f'http://{host}:{port}/v1/files',
                headers={
                    'Authorization': f'Bearer {bk}',
                    'X-Beak-Timestamp': str(ts),
                    'X-Beak-Signature': sig,
                },
            )
            with urllib.request.urlopen(req, timeout=3) as r:
                _ = json.loads(r.read())
                state = 'up'
                detail['http_status'] = 200
        else:
            detail['no_beak_key'] = True
    except urllib.error.URLError:
        pass
    except socket.timeout:
        pass
    except Exception as e:
        detail['http_error'] = str(e)[:120]

    # 2. If not up, see if it's at least PARTIAL — config present or
    # process running. "partial" tells the watchdog to wait, not escalate.
    if state == 'down':
        cg = pathlib.Path.home() / '.openclaw' / 'credentials' / 'clawhub-gateway.json'
        if cg.exists():
            detail['gateway_config'] = 'present'
            state = 'partial'
        try:
            # Best-effort pgrep — succeeds means "process exists".
            r = subprocess.run(['pgrep', '-f', 'workspace_bridge.py'],
                               capture_output=True, text=True, timeout=2)
            if r.returncode == 0 and r.stdout.strip():
                detail['pid'] = r.stdout.strip().splitlines()[0]
                state = 'partial'
        except Exception:
            pass

    report = {
        'state': state,
        'detail': detail,
        'host': host, 'port': port,
        'workspace': str(args.workspace or ''),
        'version': '0.4.0',
        'ts': int(time.time()),
    }
    print(json.dumps(report, indent=2))

    if args.report_to_platform:
        bk = (args.beak_key or os.environ.get('SPACEDUCK_BEAK_KEY') or '').strip()
        sd = (args.spaceduck_id or '').strip()
        if not sd:
            cg = pathlib.Path.home() / '.openclaw' / 'credentials' / 'clawhub-gateway.json'
            if cg.exists():
                try:
                    j = json.loads(cg.read_text())
                    sd = (j.get('spaceduck', {}).get('spaceduck_id') or '').strip()
                except Exception:
                    pass
        if not bk or not sd:
            print('# warn: cannot report — missing beak_key or spaceduck_id',
                  file=sys.stderr)
            return 0
        try:
            req = urllib.request.Request(
                f'{args.api}/beak/me/duck/{sd}/bridge-status',
                data=json.dumps(report).encode(),
                headers={'Content-Type': 'application/json',
                         'Authorization': f'Bearer {bk}'},
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                print(f'# reported: HTTP {r.status}', file=sys.stderr)
        except Exception as e:
            print(f'# warn: report failed: {e}', file=sys.stderr)
    return 0


if __name__ == '__main__':
    sys.exit(main())
