#!/usr/bin/env python3
"""
Space Duck — Inbound Telegram listener for BYOB ducks (α verifier + Σ glue).

INTENT: Receive HMAC-signed Telegram forwards from the Space Duck Lambda
        (per α-layer, lambda v537+) and dispatch them to the local agent.
        Optionally auto-reply via the δ-lite `/beak/telegram/send-as`
        endpoint (lambda v539+) by piping stdout of an --on-message hook
        through `tg_send.py`.

CALLS:  Outbound only when --auto-reply: POST /beak/telegram/send-as via
        tg_send.send_as(). The receiver itself is inbound only.
AUTH:   Validates the forwarder's HMAC signature using the duck's beak_key
        (per-agent secret in ~/.space-duck/config.json, written by pair.py).
        Replays the canonical bytes (timestamp || nonce || raw_body) and
        verifies against the `X-SpaceDuck-Signature: sha256=…` header.
        Rejects payloads outside ±5min skew and de-dups nonces in a 24h
        in-memory LRU.

The platform-side forwarder ships these headers per v537+:
  X-SpaceDuck-Event:           telegram.message
  X-SpaceDuck-Timestamp:       <unix>
  X-SpaceDuck-Nonce:           <hex>
  X-SpaceDuck-Idempotency-Key: <hex>
  X-SpaceDuck-Signature:       sha256=<hmac-hex>
  X-SpaceDuck-Binding-State:   VERIFIED|DEGRADED|LEGACY

What it does:
  • Listens on --host:--port (default 0.0.0.0:8788)
  • POST /beak/telegram/forward   → verify HMAC → write to
        ~/.space-duck/tg-inbox/<idempotency_key>.json → optional hook
  • GET  /healthz                 → 200 OK (so the platform can see you're up)
  • Anything else                 → 404

Auto-reply mode (--auto-reply with --on-message <cmd>):
  • Pipes the verified inbound JSON to <cmd> on stdin
  • Reads <cmd> stdout — if non-empty, sends it back as a Telegram reply
    via tg_send.send_as, threaded to the original message_id

Usage:
  # Plain receive: just store inbound + audit
  python3 telegram_listener.py --port 8788

  # Verbose: print verified payloads to stdout
  python3 telegram_listener.py --verbose

  # With a reply hook (e.g. local Claude or any brain)
  python3 telegram_listener.py --on-message ./reply_with_claude.sh --auto-reply

  # Skip HMAC verify (debug only — DO NOT use in production)
  python3 telegram_listener.py --unsafe-skip-hmac

The --on-message script receives the full verified payload on stdin:
  {
    "event": "telegram.message",
    "telegram_update": {…full Telegram Update…},
    "spaceduck_id": "…",
    "token_hash": "…",
    "timestamp": <unix>,
    "idempotency_key": "…",
    "nonce": "…"
  }

If --auto-reply, the script's stdout is sent back via tg_send as a
threaded reply to telegram_update.message.message_id. Empty stdout =
no reply (e.g. the hook decided not to engage). Non-zero exit = error,
no reply sent.

For TLS termination, run behind nginx/caddy/CloudFront:
  Lambda → CloudFront *.spaceduck.bot (γ, future) → your nginx → this listener
  Or for quick testing: cloudflared tunnel → this listener.
"""
import argparse
import collections
import hashlib
import hmac
import json
import os
import shlex
import signal
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
INBOX_DIR = Path.home() / '.space-duck' / 'tg-inbox'
# 0.3.15 — mirror peck.received envelopes here so send_peck.py --reply-to
# can resolve the sender SDID. peck_listener.py canonically owns this
# directory; we only write to it for event=peck.received so the two
# listeners don't double-write identical data if both are running.
PECK_INBOX_DIR = Path.home() / '.space-duck' / 'inbox'
# 0.3.6 — signed-action consent UX state directory. Pending approvals
# live here until the owner taps Approve or Deny (or the TTL expires).
# 0600 perms; bash content + action_id only — no beak_key written.
PENDING_DIR = Path.home() / '.space-duck' / 'pending-approvals'
PENDING_TTL = 600  # 10 minutes; matches the MC dispatch window
# 0.3.7 — local pulse marker; doctor.py reads this for offline-detection.
PULSE_FILE = Path.home() / '.space-duck' / 'listener-pulse.json'
PULSE_INTERVAL = 90      # platform self-pulse every 90s
SKILL_VERSION = '0.3.11'
# 0.3.9 — Auto-approved-action memory. When the owner taps "Approve &
# remember" on action_kind X, X is added here with expires_at = now+24h.
# Future X dispatches auto-execute (with audit) until the entry expires.
AUTO_APPROVED_FILE = Path.home() / '.space-duck' / 'auto-approved.json'
AUTO_APPROVE_TTL = 86400  # 24 hours
DEFAULT_API_BASE = os.environ.get('SPACE_DUCK_API', 'https://beak.spaceduckling.com')
# 0.3.8 — TTL janitor sweep interval. Cleans stale pending-approval +
# orphaned `.claimed-*` files. Conservative — runs every 10 min.
JANITOR_INTERVAL = 600
# 0.3.8 — Read-only actions that the consent UX can auto-approve without
# inline-button friction. These are idempotent inspection commands;
# auto-approval is logged + audited but doesn't bother the owner.
# Owner can override with --strict-consent (every action needs tap).
READ_ONLY_ACTIONS = {'show_beak_key', 'show_tunnel'}
# 0.3.8 — Where the breadcrumb of owner-approved actions lives. Local
# only; the duck's brain reads this on startup so subsequent sessions
# know "Wayne restarted the bridge at 03:14 UTC". Best-effort write —
# any IO failure is swallowed.
MEMORY_CANDIDATES = [
    Path.home() / '.openclaw' / 'workspace' / 'MEMORY.md',
    Path('/data/.openclaw/workspace/MEMORY.md'),
    Path.home() / '.space-duck' / 'MEMORY.md',
]
import re as _re_owner  # avoid collision with any future `re` use

# 24h sliding FIFO of seen nonces. Sized large enough that 30 msg/sec/bot
# for 24h won't evict before TTL (30*86400 = 2.6M; cap at 100k as a soft
# memory ceiling — real rates are far lower). ThreadingHTTPServer dispatches
# each request on its own thread, so the dict needs a lock — concurrent
# reads + writes against OrderedDict can wedge the structure or let a
# replay slip through.
_NONCE_LRU = collections.OrderedDict()
_NONCE_LOCK = threading.Lock()
_NONCE_TTL = 86400  # 24h
_NONCE_MAX = 100_000
_TS_SKEW = 300  # 5 min


def _load_beak_key():
    if not CONFIG_PATH.exists():
        return ''
    with open(CONFIG_PATH) as f:
        return json.load(f).get('beak_key', '')


def _load_spaceduck_id():
    if not CONFIG_PATH.exists():
        return ''
    with open(CONFIG_PATH) as f:
        return json.load(f).get('spaceduck_id', '')


def _byob_secret(beak_key):
    """Domain-separated secret for forward signing — must match
    lambda_v8.py:_byob_hmac_secret(beak_key)."""
    return hmac.new(beak_key.encode(), b'byob-hmac-v1', hashlib.sha256).digest()


def _verify_forward(beak_key, timestamp, nonce, raw_body, signature):
    """Return (ok: bool, reason: str). Constant-time comparison; checks
    skew + nonce replay + signature. Mirrors α-layer canonical bytes:
    f'{ts}.{nonce}.'.encode() + raw_body."""
    if not beak_key:
        return False, 'no beak_key loaded'
    if not signature:
        return False, 'missing signature header'
    sig = signature.removeprefix('sha256=')
    if not timestamp or not str(timestamp).isdigit():
        return False, 'missing/invalid timestamp'
    skew = abs(int(timestamp) - int(time.time()))
    if skew > _TS_SKEW:
        return False, f'timestamp skew {skew}s exceeds {_TS_SKEW}s'
    if not nonce:
        return False, 'missing nonce'
    # Verify signature BEFORE touching the nonce dict — no point spending
    # a critical section on a payload that's going to be rejected anyway.
    secret = _byob_secret(beak_key)
    sig_input = f'{timestamp}.{nonce}.'.encode() + raw_body
    expected = hmac.new(secret, sig_input, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        return False, 'signature mismatch'
    # Nonce replay check + eviction under a single lock so the
    # ThreadingHTTPServer worker threads can't race each other.
    now = int(time.time())
    with _NONCE_LOCK:
        # Evict expired entries (FIFO; insertion order == chronological).
        while _NONCE_LRU and (now - next(iter(_NONCE_LRU.values()))) > _NONCE_TTL:
            _NONCE_LRU.popitem(last=False)
        if nonce in _NONCE_LRU:
            return False, 'nonce already seen (replay)'
        # Record nonce only on full verify success.
        _NONCE_LRU[nonce] = now
        if len(_NONCE_LRU) > _NONCE_MAX:
            _NONCE_LRU.popitem(last=False)
    return True, 'ok'


# ── 0.3.6 — Owner-approval (signed-action consent UX) helpers ──
_SDA_MARKER_RE = _re_owner.compile(
    r'^sda:v1:([0-9a-f]+):(\d+):([0-9a-f]+)\s*$', _re_owner.MULTILINE)
_BASH_BLOCK_RE = _re_owner.compile(
    r'```bash\s*\n(.*?)```', _re_owner.DOTALL)


def _verify_owner_action(beak_key, text, return_reason=False):
    """Parse + verify a signed [OWNER-APPROVED] dispatch.

    Returns (action_id, action_kind, bash) on success, or None if the
    marker is missing/invalid or the signature doesn't match.

    If `return_reason=True`, returns (True, reason, (action_id, action_kind, bash))
    on success or (False, reason, None) on failure — for caller-side logging
    that distinguishes stale-state from signature-mismatch (0.4.5 — clearer
    owner-approval failure messaging per Sam-feedback).

    The Lambda dispatch path is _owner_action_sign(beak_key, action_id,
    ts, action_kind, bash). Canonical signed bytes:
        b'sda-v1:' + action_id + '|' + ts + '|' + action_kind + '|' +
        sha256_hex(bash)

    `action_kind` is the trigger_action from MC (restart_bridge,
    install_bridge_here, etc). The listener extracts it from the visible
    text (line 'Action: `kind`') because the marker only signs the hash.
    A tampered action_kind in the visible text fails the signature.
    """
    def _ret_ok(payload):
        return (True, 'ok', payload) if return_reason else payload
    def _ret_fail(reason):
        return (False, reason, None) if return_reason else None
    if not beak_key:
        return _ret_fail('no_beak_key')
    m = _SDA_MARKER_RE.search(text or '')
    if not m:
        return _ret_fail('marker_not_found')
    action_id, ts, sig = m.group(1), m.group(2), m.group(3)
    try:
        if abs(int(time.time()) - int(ts)) > PENDING_TTL:
            return _ret_fail('stale_ttl_exceeded')
    except (TypeError, ValueError):
        return _ret_fail('bad_timestamp')
    bash_match = _BASH_BLOCK_RE.search(text)
    if not bash_match:
        return _ret_fail('bash_block_missing')
    bash = bash_match.group(1).rstrip('\n')
    kind_match = _re_owner.search(r'Action:\s*`([^`]+)`', text)
    action_kind = kind_match.group(1) if kind_match else ''
    if not action_kind:
        return _ret_fail('action_kind_missing')
    bash_hash = hashlib.sha256(bash.encode()).hexdigest()
    canonical = (
        b'sda-v1:' + action_id.encode() + b'|' + ts.encode() +
        b'|' + action_kind.encode() + b'|' + bash_hash.encode()
    )
    secret = _byob_secret(beak_key)
    expected = hmac.new(secret, canonical, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, sig):
        # Signature mismatch — almost always beak_key rotation, very rarely tampering.
        return _ret_fail('signature_mismatch_likely_key_rotation')
    return _ret_ok((action_id, action_kind, bash))


def _write_pending(action_id, action_kind, bash, chat_id, message_id):
    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    p = PENDING_DIR / f'{action_id}.json'
    with open(p, 'w') as f:
        json.dump({
            'action_id': action_id,
            'action_kind': action_kind,
            'bash': bash,
            'chat_id': chat_id,
            'message_id': message_id,
            'expires_at': int(time.time()) + PENDING_TTL,
        }, f)
    os.chmod(p, 0o600)
    return p


def _read_pending(action_id):
    p = PENDING_DIR / f'{action_id}.json'
    if not p.exists():
        return None
    try:
        with open(p) as f:
            d = json.load(f)
        if int(d.get('expires_at', 0)) < int(time.time()):
            try: p.unlink()
            except Exception: pass
            return None
        return d
    except Exception:
        return None


def _claim_pending(action_id):
    """0.3.7 — POSIX-atomic single-tap guard. os.rename is atomic; second
    concurrent tap raises FileNotFoundError. Closes the double-execute
    race in the previous read-then-delete sequence."""
    src = PENDING_DIR / f'{action_id}.json'
    if not src.exists():
        return None
    dst = PENDING_DIR / f'{action_id}.json.claimed-{os.getpid()}-{int(time.time())}'
    try:
        os.rename(str(src), str(dst))
    except FileNotFoundError:
        return None
    try:
        with open(dst) as f:
            d = json.load(f)
    except Exception:
        try: os.unlink(str(dst))
        except Exception: pass
        return None
    if int(d.get('expires_at', 0)) < int(time.time()):
        try: os.unlink(str(dst))
        except Exception: pass
        return None
    d['_claim_path'] = str(dst)
    return d


def _release_claim(claim):
    """Delete the renamed claim file after exec finishes."""
    try:
        os.unlink(claim.get('_claim_path', ''))
    except Exception:
        pass


def _delete_pending(action_id):
    p = PENDING_DIR / f'{action_id}.json'
    try: p.unlink()
    except Exception: pass


def _post_approval_buttons(beak_key, spaceduck_id, chat_id, action_id,
                           action_kind, reply_to):
    """Render the inline 3-button consent prompt as a threaded reply.

    0.3.9 — three buttons:
      ✅ Approve & run         (this dispatch only)
      🔁 Approve & remember    (auto-approve this action_kind 24h)
      ❌ Deny                  (drop, audit)

    "Remember" persists to ~/.space-duck/auto-approved.json. Future
    dispatches of the same kind from the same duck skip the prompt and
    execute silently (with audit + breadcrumb) until expiry.
    """
    try:
        from tg_send import send_as
    except Exception as e:
        print(f'[OWNER-APPROVAL] tg_send import failed: {e}', file=sys.stderr)
        return False
    text = (
        f'🔐 Owner-approved action ready: `{action_kind}`.\n\n'
        f'• ✅ Approve — run this one\n'
        f'• 🔁 Run all — approve every `{action_kind}` for 24h\n'
        f'• ❌ Deny — ignore\n\n'
        f'(Signed by your platform key; expires in 10min.)'
    )
    reply_markup = {
        'inline_keyboard': [
            [
                {'text': '✅ Approve',
                 'callback_data': f'sda:a:{action_id}'},
                {'text': '🔁 Run all (24h)',
                 'callback_data': f'sda:r:{action_id}'},
            ],
            [
                {'text': '❌ Deny',
                 'callback_data': f'sda:d:{action_id}'},
            ],
        ]
    }
    status, resp = send_as(
        spaceduck_id, chat_id, text,
        beak_key=beak_key, reply_to=reply_to,
        parse_mode='Markdown', reply_markup=reply_markup,
        idempotency_key=f'sda-prompt-{action_id}',
    )
    if status != 200:
        print(f'[OWNER-APPROVAL] prompt-send failed status={status} '
              f'resp={resp}', file=sys.stderr)
        return False
    return True


def _load_auto_approved():
    """0.3.9 — Return {action_kind: expires_at} dict of unexpired entries.
    Expired entries are pruned on read. Empty dict if file doesn't
    exist."""
    if not AUTO_APPROVED_FILE.exists():
        return {}
    try:
        with open(AUTO_APPROVED_FILE) as f:
            d = json.load(f)
    except Exception:
        return {}
    now = int(time.time())
    live = {k: int(v) for k, v in d.items()
            if isinstance(v, (int, float)) and int(v) > now}
    if len(live) != len(d):
        _save_auto_approved(live)  # prune expired
    return live


def _save_auto_approved(d):
    try:
        AUTO_APPROVED_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = AUTO_APPROVED_FILE.with_suffix('.tmp')
        with open(tmp, 'w') as f:
            json.dump(d, f)
        os.chmod(tmp, 0o600)
        os.replace(str(tmp), str(AUTO_APPROVED_FILE))
    except Exception as e:
        print(f'[AUTO-APPROVED] save failed: {e}', file=sys.stderr)


def _remember_action_kind(action_kind):
    """0.3.9 — Record action_kind as auto-approved for 24h."""
    d = _load_auto_approved()
    d[action_kind] = int(time.time()) + AUTO_APPROVE_TTL
    _save_auto_approved(d)


def _is_action_remembered(action_kind):
    return action_kind in _load_auto_approved()


def _exec_pending(pending):
    """Run the approved bash with a 60s timeout. Capture combined output
    for the reply. Honest reporting — no stripping of stderr.

    0.3.11 — returns the FULL output now. Truncation + S3 offload is
    done downstream by the callback handler so the full text is
    available for upload to /beak/byob/workspace/action-log."""
    try:
        proc = subprocess.run(
            pending['bash'], shell=True, executable='/bin/bash',
            capture_output=True, timeout=60)
        out = (proc.stdout or b'').decode('utf-8', errors='replace')
        err = (proc.stderr or b'').decode('utf-8', errors='replace')
        body = out
        if err:
            body += ('\n--- stderr ---\n' + err)
        body = body.strip() or '(no output)'
        return proc.returncode, body
    except subprocess.TimeoutExpired:
        return 124, '(timeout after 60s)'
    except Exception as e:
        return 1, f'(exec error: {e})'


def _upload_action_log(beak_key, sd_id, api_base, action_id, action_kind,
                       output, exit_code):
    """0.3.11 — upload full output of a long-running action to S3 via
    Lambda's action-log endpoint. Returns viewer_url on success, '' on
    failure. Best-effort: caller falls back to plain truncated reply."""
    if not beak_key or not sd_id or not action_id:
        return ''
    try:
        payload = {
            'action_id': action_id, 'action_kind': action_kind,
            'output': output, 'exit_code': int(exit_code),
        }
        req = urllib.request.Request(
            f'{api_base.rstrip("/")}/beak/byob/workspace/action-log',
            data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json',
                     'Authorization': f'Bearer {beak_key}'},
            method='POST')
        with urllib.request.urlopen(req, timeout=15) as r:
            if r.status != 200:
                return ''
            d = json.loads(r.read())
            return d.get('viewer_url', '')
    except Exception as e:
        print(f'[ACTION-LOG] upload failed: {e}', file=sys.stderr)
        return ''


def _format_long_output(output, viewer_url):
    """0.3.11 — when output exceeds TG's safe inline budget, return a
    head + tail snippet bracketing the omitted middle, with the viewer
    URL inline. Budget chosen so the full TG reply (with wrapper code-
    block + status line) stays under TG's 4096 ceiling."""
    HEAD = 800
    TAIL = 800
    if len(output) <= HEAD + TAIL + 200:
        return output
    omitted = len(output) - HEAD - TAIL
    head = output[:HEAD].rstrip()
    tail = output[-TAIL:].lstrip()
    middle = (
        f'\n\n…(omitted {omitted} chars — full log: {viewer_url})…\n\n'
        if viewer_url else
        f'\n\n…(omitted {omitted} chars — full log unavailable, '
        f'truncated for TG)…\n\n'
    )
    return head + middle + tail


def _answer_callback_query(beak_key, spaceduck_id, callback_query_id, text):
    """Best-effort answerCallbackQuery via /beak/telegram/send-as is not
    supported (send-as is sendMessage only). For now we skip the spinner
    ack — Telegram falls back gracefully (button shows a brief grey
    state). Real ack will land when /beak/telegram/answer-callback is
    added platform-side."""
    return  # intentional no-op for 0.3.6


def _handle_owner_approval_message(handler_cfg, payload):
    """If the inbound message is a signed [OWNER-APPROVED] dispatch,
    render Approve/Deny and return True. Otherwise return False so the
    listener falls through to its normal --on-message hook.

    0.3.8 changes:
      • Read-only actions (show_beak_key, show_tunnel) auto-approve and
        execute when --strict-consent is off (default). Owner can flip
        on --strict-consent to require tap for everything.
      • If text contains [OWNER-APPROVED but no signed marker, log loud
        so doctor.py can surface the broken dispatch (item 7).
    """
    tg = payload.get('telegram_update', {}) or {}
    msg = tg.get('message') or {}
    text = msg.get('text') or ''
    if 'sda:v1:' not in text:
        # Item 7 — silent-drop visibility. If the platform dispatched
        # [OWNER-APPROVED] but the marker was stripped, log it so the
        # downstream diagnosis isn't mystery dormancy.
        if '[OWNER-APPROVED' in text:
            print('[OWNER-APPROVAL] [OWNER-APPROVED] dispatch arrived '
                  'WITHOUT signed marker — TG/proxy may have stripped '
                  'the trailing line. Owner cannot consent without it.',
                  file=sys.stderr)
        return False
    beak_key = handler_cfg.get('beak_key', '')
    verified = _verify_owner_action(beak_key, text, return_reason=True)
    if not verified or (isinstance(verified, tuple) and verified[0] is False):
        # 0.4.5 — Sam-feedback fix: softer wording. The usual cause is stale
        # state (beak_key rotated, old marker; or dispatch arrived after TTL).
        # Phishing is the rare case. Log the actual reason so the user can
        # tell which one it is, without alarming wording front-and-center.
        reason = verified[1] if isinstance(verified, tuple) else 'unknown'
        print(f'[OWNER-APPROVAL] signed marker did not verify (reason={reason}) — '
              f'likely stale dispatch or key rotation; phishing is rare. '
              f'Action ignored.', file=sys.stderr)
        return False
    if isinstance(verified, tuple):
        verified = verified[2]
    action_id, action_kind, bash = verified
    chat_id = (msg.get('chat') or {}).get('id')
    message_id = msg.get('message_id')
    if not chat_id:
        return False
    sd_id = payload.get('spaceduck_id', '')
    strict = handler_cfg.get('strict_consent', False)
    # 0.3.9 — check the auto-approve memory (set by previous "Run all"
    # taps). If this action_kind has an unexpired grant, execute
    # immediately with audit + breadcrumb, no prompt.
    if _is_action_remembered(action_kind):
        if handler_cfg.get('verbose'):
            print(f'[OWNER-APPROVAL] auto-approving via 24h memory '
                  f'kind={action_kind} id={action_id[:8]}')
        pending = {
            'action_id': action_id, 'action_kind': action_kind,
            'bash': bash, 'chat_id': chat_id, 'message_id': message_id,
            'expires_at': int(time.time()) + 60, '_claim_path': '',
        }
        rc, out = _exec_pending(pending)
        _write_memory_breadcrumb(action_kind, action_id, rc, out)
        viewer_url = ''
        if len(out) > 1600:
            viewer_url = _upload_action_log(
                beak_key, sd_id, DEFAULT_API_BASE,
                action_id, action_kind, out, rc)
        display_out = _format_long_output(out, viewer_url)
        try:
            from tg_send import send_as
            reply = (f'{"✅" if rc == 0 else "⚠"} (🔁 remembered) '
                     f'`{action_kind}` exit={rc}\n```\n{display_out}\n```')
            send_as(sd_id, chat_id, reply[:4000],
                    beak_key=beak_key, reply_to=message_id,
                    parse_mode='Markdown')
        except Exception as e:
            print(f'[OWNER-APPROVAL] remembered reply failed: {e}',
                  file=sys.stderr)
        return True
    if (not strict) and action_kind in READ_ONLY_ACTIONS:
        # Item 10 — auto-approve idempotent read-only inspection.
        # Equivalent semantics to a tap, just no friction.
        if handler_cfg.get('verbose'):
            print(f'[OWNER-APPROVAL] auto-approving read-only action '
                  f'kind={action_kind} id={action_id[:8]}')
        # Synthesise a pending record; execute immediately; reply.
        pending = {
            'action_id': action_id,
            'action_kind': action_kind,
            'bash': bash,
            'chat_id': chat_id,
            'message_id': message_id,
            'expires_at': int(time.time()) + 60,
            '_claim_path': '',  # nothing to release
        }
        rc, out = _exec_pending(pending)
        _write_memory_breadcrumb(action_kind, action_id, rc, out)
        viewer_url = ''
        if len(out) > 1600:
            viewer_url = _upload_action_log(
                beak_key, sd_id, DEFAULT_API_BASE,
                action_id, action_kind, out, rc)
        display_out = _format_long_output(out, viewer_url)
        try:
            from tg_send import send_as
            reply = (f'{"✅" if rc == 0 else "⚠"} (auto-approved read-only) '
                     f'`{action_kind}` exit={rc}\n```\n{display_out}\n```')
            send_as(sd_id, chat_id, reply[:4000],
                    beak_key=beak_key, reply_to=message_id,
                    parse_mode='Markdown')
        except Exception as e:
            print(f'[OWNER-APPROVAL] auto-approve reply failed: {e}',
                  file=sys.stderr)
        return True
    _write_pending(action_id, action_kind, bash, chat_id, message_id)
    posted = _post_approval_buttons(
        beak_key, sd_id, chat_id,
        action_id, action_kind, message_id)
    if handler_cfg.get('verbose'):
        print(f'[OWNER-APPROVAL] action={action_kind} id={action_id} '
              f'posted={posted}')
    return True


def _handle_owner_approval_callback(handler_cfg, payload):
    """Handle a forwarded callback_query whose data is sda:a:<id> or
    sda:d:<id>. Returns True if it was an sda callback (so the listener
    skips the normal pipeline)."""
    tg = payload.get('telegram_update', {}) or {}
    cb = tg.get('callback_query') or {}
    data = cb.get('data') or ''
    if not (data.startswith('sda:a:') or data.startswith('sda:d:')):
        return False
    action_id = data.split(':', 2)[2]
    chat_id = ((cb.get('message') or {}).get('chat') or {}).get('id')
    message_id = (cb.get('message') or {}).get('message_id')
    cb_id = cb.get('id', '')
    beak_key = handler_cfg.get('beak_key', '')
    sd_id = payload.get('spaceduck_id', '')
    # 0.3.9 — three callback prefixes:
    #   sda:a:  → Approve & run this one
    #   sda:r:  → Approve & remember (run + 24h auto-approve action_kind)
    #   sda:d:  → Deny
    is_approve = data.startswith('sda:a:') or data.startswith('sda:r:')
    is_remember = data.startswith('sda:r:')
    # Atomic claim — only one tap wins. Double-tap on flaky network = 1 run.
    pending = _claim_pending(action_id)
    if not chat_id or not pending:
        # Expired, already handled, or unknown.
        _try_answer_cb(sd_id, beak_key, cb_id,
                       'Already handled' if cb_id else '', alert=False)
        try:
            from tg_send import send_as
            send_as(sd_id, chat_id, '⚠ Action expired or already handled.',
                    beak_key=beak_key, reply_to=message_id)
        except Exception:
            pass
        return True
    # Immediate ack so the spinner closes.
    _ack_text = 'Running…' if is_approve else 'Denied'
    if is_remember:
        _ack_text = 'Running + remembering 24h…'
    _try_answer_cb(sd_id, beak_key, cb_id, _ack_text, alert=False)
    if not is_approve:
        _release_claim(pending)
        try:
            from tg_send import send_as
            send_as(sd_id, chat_id,
                    f'❌ Denied: `{pending["action_kind"]}`. Nothing ran.',
                    beak_key=beak_key, reply_to=message_id,
                    parse_mode='Markdown')
        except Exception:
            pass
        return True
    if is_remember:
        # Persist the trust grant BEFORE exec so a crash during exec
        # still leaves the trust grant active for the next dispatch.
        _remember_action_kind(pending['action_kind'])
    rc, output = _exec_pending(pending)
    _release_claim(pending)
    # Item 8 — write a breadcrumb so the duck's brain sees recent
    # owner-approved actions next session.
    _write_memory_breadcrumb(pending['action_kind'], action_id, rc, output)
    # 0.3.11 — long-output offload. Upload full output, splice in link.
    viewer_url = ''
    if len(output) > 1600:
        viewer_url = _upload_action_log(
            beak_key, sd_id, DEFAULT_API_BASE,
            action_id, pending['action_kind'], output, rc)
    display_output = _format_long_output(output, viewer_url)
    _remember_note = ' (🔁 remembered 24h)' if is_remember else ''
    reply_text = (
        f'{"✅" if rc == 0 else "⚠"} `{pending["action_kind"]}` '
        f'exit={rc}{_remember_note}\n```\n{display_output}\n```'
    )
    try:
        from tg_send import send_as
        send_as(sd_id, chat_id, reply_text[:4000],
                beak_key=beak_key, reply_to=message_id,
                parse_mode='Markdown')
    except Exception as e:
        print(f'[OWNER-APPROVAL] result-reply failed: {e}', file=sys.stderr)
    return True


def _try_answer_cb(sd_id, beak_key, cb_id, text, alert=False):
    """0.3.7 — closes the grey-spinner gap. Calls Lambda's new
    /beak/telegram/answer-callback (v677) which proxies to Telegram's
    answerCallbackQuery. Best-effort: any failure here is swallowed
    silently — UX degrades to the 10s spinner timeout, no functional
    break."""
    if not cb_id or not sd_id or not beak_key:
        return
    try:
        from tg_send import answer_callback
        answer_callback(sd_id, cb_id, text=text[:200], show_alert=alert,
                        beak_key=beak_key)
    except Exception as e:
        if os.environ.get('SPACEDUCK_VERBOSE'):
            print(f'[ANSWER-CB] {e}', file=sys.stderr)


def _janitor_loop(verbose=False):
    """0.3.8 — Periodic sweep of PENDING_DIR. Deletes expired pending
    actions + orphan `.claimed-*` files left by crashed exec runs. Safe
    to run alongside live workflow because each file's expires_at is
    checked atomically. Doesn't touch fresh entries."""
    while True:
        try:
            now = int(time.time())
            if not PENDING_DIR.exists():
                time.sleep(JANITOR_INTERVAL)
                continue
            cleaned = 0
            for p in PENDING_DIR.iterdir():
                try:
                    if not p.is_file():
                        continue
                    # Orphan claim files older than 1h — exec definitely
                    # done (subprocess timeout is 60s).
                    if '.claimed-' in p.name:
                        if (now - p.stat().st_mtime) > 3600:
                            p.unlink()
                            cleaned += 1
                        continue
                    if p.suffix != '.json':
                        continue
                    with open(p) as f:
                        d = json.load(f)
                    if int(d.get('expires_at', 0)) < now:
                        p.unlink()
                        cleaned += 1
                except Exception:
                    pass
            if verbose and cleaned:
                print(f'[JANITOR] swept {cleaned} stale file(s)',
                      file=sys.stderr)
        except Exception as e:
            if verbose:
                print(f'[JANITOR-EXC] {e}', file=sys.stderr)
        time.sleep(JANITOR_INTERVAL)


def _preflight_bind_state(beak_key, sd_id, api_base, verbose=False):
    """0.3.8 — Verify that bind_telegram.py has completed binding before
    the listener accepts traffic. If state isn't VERIFIED, the listener
    pulse will still work but TG callbacks won't reach it (silent break
    of the consent UX). This makes that failure mode visible.

    Returns (ok: bool, state: str, remediation: str)."""
    if not beak_key or not sd_id:
        return False, 'NO_CREDS', 'Run pair.py first.'
    try:
        url = f'{api_base.rstrip("/")}/beak/agent/byob-status?spaceduck_id={sd_id}'
        req = urllib.request.Request(
            url, headers={'Authorization': f'Bearer {beak_key}'}, method='GET')
        with urllib.request.urlopen(req, timeout=8) as r:
            d = json.loads(r.read())
        state = (d.get('state') or '').upper()
        if state == 'VERIFIED':
            return True, state, ''
        if state in ('DEGRADED',):
            return True, state, (
                f'Binding is DEGRADED — TG forwards may be flaky. '
                f'Re-run: python3 bind_telegram.py')
        return False, state or 'UNKNOWN', (
            f'Binding state is {state or "UNKNOWN"}, not VERIFIED. '
            f'Run: python3 bind_telegram.py (full bind flow).')
    except urllib.error.HTTPError as he:
        # 0.4.5 — Sam-feedback fix: surface auth failures loudly. 401/403
        # from /beak/agent/byob-status means the BYOB binding side is not
        # authorized — TG webhook delivery is at risk. BUT direct TG
        # callbacks via inline buttons use HMAC (different auth path) and
        # may still work, so we log LOUD but still proceed. Doctor will
        # surface this same warning on review.
        if he.code in (401, 403):
            print(f'[PREFLIGHT-WARN] bind-verify auth failed ({he.code}) — '
                  f'beak_key not authorized for byob-status. Inbound webhook '
                  f'delivery is at risk; TG callbacks via inline buttons may '
                  f'still work (different auth path). Re-pair via The Inlet '
                  f'if forwards stop arriving.',
                  file=sys.stderr)
            return True, f'AUTH_{he.code}_PROCEED', (
                f'byob-status returned {he.code} — webhook forwards at risk. '
                f'Re-pair if traffic stops; listener still up for direct taps.')
        # Other HTTP codes are transient — warn but proceed.
        if verbose:
            print(f'[PREFLIGHT] byob-status probe HTTP {he.code}: {he}',
                  file=sys.stderr)
        return True, f'HTTP_{he.code}', (
            f'Bind-verify returned HTTP {he.code} (transient). '
            f'Proceeding; will re-probe in 24h.')
    except Exception as e:
        # Don't fail-loud on transient network — just warn.
        if verbose:
            print(f'[PREFLIGHT] byob-status probe failed: {e}',
                  file=sys.stderr)
        return True, 'PROBE_FAILED', (
            f'Could not reach platform to verify bind state ({e}). '
            f'Proceeding; will re-probe in 24h.')


def _bind_health_periodic(beak_key, sd_id, api_base, verbose=False):
    """0.3.8 — Daily re-probe of bind state. If a previously-VERIFIED
    binding rots (TG token rotation, webhook reset, etc), the periodic
    check surfaces the change. Pure best-effort; failure here is
    swallowed silently."""
    SLEEP_SEC = 86400  # 24h
    while True:
        time.sleep(SLEEP_SEC)
        try:
            ok, state, _ = _preflight_bind_state(beak_key, sd_id, api_base)
            if not ok and verbose:
                print(f'[BIND-PROBE] degraded — state={state}',
                      file=sys.stderr)
        except Exception:
            pass


def _write_memory_breadcrumb(action_kind, action_id, rc, output_summary):
    """0.3.8 — Append a one-line breadcrumb to the duck's MEMORY.md so
    its brain has context on the next session. Best-effort. Writes to
    whichever MEMORY.md candidate exists first; doesn't create one if
    none exist (would clutter installs that don't follow our convention)."""
    target = None
    for p in MEMORY_CANDIDATES:
        if p.exists():
            target = p
            break
    if target is None:
        return
    try:
        ts = time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())
        summary = (output_summary or '').strip().splitlines()[:1]
        summary_text = summary[0][:120] if summary else '(no output)'
        line = (
            f'\n- **owner-approved action** [{ts}] '
            f'`{action_kind}` (id `{action_id[:8]}`) exit={rc} — '
            f'`{summary_text}`'
        )
        with open(target, 'a') as f:
            f.write(line)
    except Exception:
        pass


def _send_shutdown_pulse(beak_key, sd_id, api_base):
    """0.3.8 — Final pulse on SIGTERM/SIGINT so MC flips to offline
    immediately instead of waiting the 240s stale window. Best-effort."""
    if not beak_key or not sd_id:
        return
    try:
        url = f'{api_base.rstrip("/")}/beak/me/duck/{sd_id}/listener-status'
        payload = {
            'skill_version': SKILL_VERSION,
            'owner_approval': True,
            'pid': os.getpid(),
            'started_at': int(time.time()),
            'ts': int(time.time()),
            'shutdown': True,
        }
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json',
                     'Authorization': f'Bearer {beak_key}'},
            method='POST')
        urllib.request.urlopen(req, timeout=3).close()
    except Exception:
        pass


def _pulse_loop(beak_key, sd_id, api_base, verbose=False):
    """0.3.7 — self-pulse so the platform knows the listener is alive.
    Mirrors workspace_bridge.py's `status --report-to-platform` pattern.
    Lambda's /beak/me/duck/<sd>/listener-status stamps spaceducks row
    with listener_state + listener_state_at; MC reads it to render
    'listener online' vs 'listener offline' banner."""
    payload = {
        'skill_version': SKILL_VERSION,
        'owner_approval': True,
        'pid': os.getpid(),
        'started_at': int(time.time()),
    }
    url = f'{api_base.rstrip("/")}/beak/me/duck/{sd_id}/listener-status'
    while True:
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps({**payload, 'ts': int(time.time())}).encode(),
                headers={'Content-Type': 'application/json',
                         'Authorization': f'Bearer {beak_key}'},
                method='POST')
            with urllib.request.urlopen(req, timeout=8) as r:
                if verbose:
                    print(f'[PULSE] HTTP {r.status} sd={sd_id[:8]}',
                          file=sys.stderr)
            # Write local pulse file so doctor.py can see freshness even
            # if it can't reach the platform itself.
            try:
                PULSE_FILE.parent.mkdir(parents=True, exist_ok=True)
                with open(PULSE_FILE, 'w') as f:
                    json.dump({**payload, 'last_pulse_at': int(time.time())}, f)
                os.chmod(PULSE_FILE, 0o600)
            except Exception:
                pass
        except Exception as e:
            if verbose:
                print(f'[PULSE-FAIL] {e}', file=sys.stderr)
        time.sleep(PULSE_INTERVAL)


class _Handler(BaseHTTPRequestHandler):
    # Filled in by main() before serve_forever.
    config = None

    def _json(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        # Quiet default access log; let --verbose handle visibility.
        if self.config and self.config.get('verbose'):
            super().log_message(format, *args)

    def do_GET(self):
        if self.path == '/healthz':
            return self._json(200, {'ok': True, 'service': 'space-duck-telegram-listener'})
        return self._json(404, {'error': 'not_found'})

    def do_POST(self):
        if self.path != '/beak/telegram/forward':
            return self._json(404, {'error': 'not_found'})

        length = int(self.headers.get('Content-Length') or 0)
        raw = self.rfile.read(length) if length else b''
        ts = self.headers.get('X-SpaceDuck-Timestamp', '')
        nonce = self.headers.get('X-SpaceDuck-Nonce', '')
        sig = self.headers.get('X-SpaceDuck-Signature', '')
        binding_state = self.headers.get('X-SpaceDuck-Binding-State', '')

        if self.config.get('skip_hmac'):
            ok, reason = True, 'unsafe-skip-hmac'
        else:
            ok, reason = _verify_forward(
                self.config['beak_key'], ts, nonce, raw, sig)
        if not ok:
            print(f'[REJECT] {reason} sig={sig[:24]} ts={ts} nonce={nonce[:8]}',
                  file=sys.stderr)
            # Return 401 so the platform marks this as a failed forward
            # (3 fails → state→DEGRADED, owner can see in byob-status).
            return self._json(401, {'error': 'verification_failed', 'reason': reason})

        try:
            payload = json.loads(raw or b'{}')
        except Exception as e:
            return self._json(400, {'error': 'invalid_json', 'detail': str(e)[:120]})

        idem = payload.get('idempotency_key') or nonce or str(int(time.time()))
        INBOX_DIR.mkdir(parents=True, exist_ok=True)
        inbox_path = INBOX_DIR / f'{idem}.json'
        try:
            with open(inbox_path, 'w') as f:
                json.dump({**payload, '_received_at': int(time.time()),
                           '_binding_state': binding_state}, f, indent=2)
            os.chmod(inbox_path, 0o600)
        except Exception as e:
            print(f'[INBOX-WRITE-FAIL] {e}', file=sys.stderr)

        # 0.3.15 — mirror peck.received envelopes to ~/.space-duck/inbox/
        # so send_peck.py --reply-to <peck_id> can resolve the sender SDID.
        # Pre-0.3.15 only the tg-inbox copy existed; send_peck reads from
        # inbox/ (matching peck_listener.py's contract) → silent exit 1 on
        # every reply attempt under the B7' (lambda v713) delivery
        # topology where platform → telegram_listener → peck_responder
        # → send_peck --reply-to all happens without peck_listener.py
        # ever running. Wayne diagnosed this 2026-06-10 msg 22571 after
        # the first end-to-end loop test.
        # Only mirror peck.received — telegram.message echoes don't carry
        # peck metadata and have nothing for send_peck to resolve.
        event_type = payload.get('event', '')
        peck_id_for_mirror = payload.get('peck_id') or ''
        if event_type == 'peck.received' and peck_id_for_mirror:
            try:
                PECK_INBOX_DIR.mkdir(parents=True, exist_ok=True)
                mirror_path = PECK_INBOX_DIR / f'{peck_id_for_mirror}.json'
                with open(mirror_path, 'w') as f:
                    json.dump({**payload, '_received_at': int(time.time()),
                               '_binding_state': binding_state}, f, indent=2)
                os.chmod(mirror_path, 0o600)
            except Exception as e:
                print(f'[INBOX-MIRROR-FAIL] {e}', file=sys.stderr)

        if self.config.get('verbose'):
            tg = payload.get('telegram_update', {}) or {}
            text_preview = (((tg.get('message') or {}).get('text')) or '')[:80]
            chat = ((tg.get('message') or {}).get('chat') or {}).get('id', '?')
            print(f'[RECV] sd={payload.get("spaceduck_id","?")[:8]} '
                  f'state={binding_state} idem={idem[:8]} '
                  f'chat={chat} text={text_preview!r}')

        # 0.3.6 — owner-approval interception. Runs BEFORE the generic
        # --on-message hook so signed [OWNER-APPROVED] dispatches go
        # through the consent UX instead of being silently executed by a
        # brain hook. Returns True if it claimed the update.
        if self.config.get('owner_approval'):
            try:
                if _handle_owner_approval_callback(self.config, payload):
                    return self._json(200, {'received': True,
                                            'idempotency_key': idem,
                                            'handled_by': 'owner_approval_callback'})
                if _handle_owner_approval_message(self.config, payload):
                    return self._json(200, {'received': True,
                                            'idempotency_key': idem,
                                            'handled_by': 'owner_approval_prompt'})
            except Exception as e:
                print(f'[OWNER-APPROVAL-EXC] {e}', file=sys.stderr)

        reply_text = ''
        on_message = self.config.get('on_message')
        if on_message:
            try:
                # 0.3.14 — shlex-split the hook string so multi-token forms
                # like `python3 /path/to/peck_responder.py` work. Pre-0.3.14
                # subprocess.run(on_message, ...) without shell=True treated
                # the whole string as a single binary path on POSIX, which
                # silently `FileNotFoundError`'d every inbound and the
                # platform got a 200 → no reply ever fired.
                # argv parsed via shlex (no shell, no injection risk).
                # If shlex.split fails or yields empty, fall back to the
                # raw string so we don't make things worse for users
                # already relying on the single-token form.
                argv = on_message
                try:
                    _argv_split = shlex.split(on_message)
                    if _argv_split:
                        argv = _argv_split
                except Exception:
                    pass
                proc = subprocess.run(
                    argv, input=json.dumps(payload).encode(),
                    capture_output=True, timeout=self.config.get('hook_timeout', 60))
                if proc.returncode != 0:
                    print(f'[HOOK-FAIL] rc={proc.returncode} stderr={proc.stderr[:200]!r}',
                          file=sys.stderr)
                else:
                    reply_text = proc.stdout.decode('utf-8', errors='replace').rstrip('\n')
            except Exception as e:
                print(f'[HOOK-EXC] {e}', file=sys.stderr)

        # Auto-reply via send-as if enabled + hook produced output.
        if self.config.get('auto_reply') and reply_text:
            try:
                # Lazy import — only needed when auto-replying.
                from tg_send import send_as
                tg = payload.get('telegram_update', {}) or {}
                msg = (tg.get('message') or {})
                chat_id = (msg.get('chat') or {}).get('id')
                reply_to = msg.get('message_id')
                if chat_id:
                    status, resp = send_as(
                        payload.get('spaceduck_id', ''),
                        chat_id, reply_text,
                        beak_key=self.config['beak_key'],
                        reply_to=reply_to,
                        idempotency_key=f'reply-{idem}',
                    )
                    if status != 200:
                        print(f'[AUTOREPLY-FAIL] status={status} resp={resp}',
                              file=sys.stderr)
                    elif self.config.get('verbose'):
                        print(f'[AUTOREPLY] sd={payload.get("spaceduck_id","?")[:8]} '
                              f'message_id={resp.get("message_id")}')
            except Exception as e:
                print(f'[AUTOREPLY-EXC] {e}', file=sys.stderr)

        return self._json(200, {'received': True, 'idempotency_key': idem})


def main(argv=None):
    p = argparse.ArgumentParser(
        description='Listen for HMAC-signed Telegram forwards from the Space Duck platform.')
    p.add_argument('--host', default='0.0.0.0')
    p.add_argument('--port', type=int, default=8788)
    p.add_argument('--on-message',
                   help='Shell command to run per inbound (full JSON on stdin)')
    p.add_argument('--auto-reply', action='store_true',
                   help='Pipe --on-message stdout back as a threaded Telegram reply')
    p.add_argument('--hook-timeout', type=int, default=60,
                   help='Seconds before the --on-message subprocess is killed')
    p.add_argument('--verbose', action='store_true')
    p.add_argument('--unsafe-skip-hmac', action='store_true',
                   help='DEBUG ONLY: accept unsigned payloads')
    p.add_argument('--owner-approval', action='store_true',
                   help='Enable signed [OWNER-APPROVED] consent UX: '
                        'verify HMAC marker, render Approve/Deny inline '
                        'buttons, execute on owner tap. Runs before any '
                        '--on-message hook.')
    p.add_argument('--no-pulse', action='store_true',
                   help='Disable the 90s self-pulse to '
                        '/beak/me/duck/<sd>/listener-status. Default is '
                        'on; disable only for local/offline debug.')
    p.add_argument('--strict-consent', action='store_true',
                   help='Require explicit Approve/Deny tap for every '
                        'action including read-only ones (show_beak_key, '
                        'show_tunnel). Default auto-approves read-only.')
    p.add_argument('--skip-preflight', action='store_true',
                   help='Skip the bind-state preflight probe at startup. '
                        'Useful for local debug.')
    p.add_argument('--no-janitor', action='store_true',
                   help='Disable the 10-min pending-approvals TTL janitor.')
    args = p.parse_args(argv)

    beak_key = _load_beak_key()
    if not beak_key and not args.unsafe_skip_hmac:
        print(f'ERR: no beak_key in {CONFIG_PATH}. Run pair.py first '
              f'(or pass --unsafe-skip-hmac for local debug).', file=sys.stderr)
        return 1

    _Handler.config = {
        'beak_key': beak_key,
        'on_message': args.on_message,
        'auto_reply': args.auto_reply,
        'hook_timeout': args.hook_timeout,
        'verbose': args.verbose,
        'skip_hmac': args.unsafe_skip_hmac,
        'owner_approval': args.owner_approval,
        'strict_consent': args.strict_consent,
    }
    sd_id = _load_spaceduck_id()

    # 0.3.8 — Item 4 — bind preflight. Fail-loud (with continue option)
    # if binding isn't VERIFIED. Owner sees the real problem instead of
    # mystery dormancy when they tap Approve and nothing executes.
    if args.owner_approval and not args.skip_preflight and beak_key and sd_id:
        ok, state, remediation = _preflight_bind_state(
            beak_key, sd_id, DEFAULT_API_BASE, verbose=args.verbose)
        if not ok:
            print(f'[PREFLIGHT-FAIL] bind_state={state}\n  {remediation}\n'
                  f'  (override with --skip-preflight)', file=sys.stderr)
            return 2
        elif state != 'VERIFIED':
            print(f'[PREFLIGHT-WARN] bind_state={state} — {remediation}',
                  file=sys.stderr)

    # 0.3.7 — start the self-pulse thread when we have credentials.
    if beak_key and sd_id and not args.no_pulse:
        t = threading.Thread(
            target=_pulse_loop,
            args=(beak_key, sd_id, DEFAULT_API_BASE, args.verbose),
            daemon=True)
        t.start()
        print(f'[PULSE] thread started — {DEFAULT_API_BASE}/beak/me/duck/'
              f'{sd_id[:8]}…/listener-status every {PULSE_INTERVAL}s')
    # 0.3.8 — Item 3 — TTL janitor for pending-approvals.
    if not args.no_janitor:
        tj = threading.Thread(target=_janitor_loop,
                              args=(args.verbose,), daemon=True)
        tj.start()
        print(f'[JANITOR] thread started — sweep every {JANITOR_INTERVAL}s')
    # 0.3.8 — Item 12 — daily bind health re-probe.
    if args.owner_approval and beak_key and sd_id and not args.skip_preflight:
        tb = threading.Thread(
            target=_bind_health_periodic,
            args=(beak_key, sd_id, DEFAULT_API_BASE, args.verbose),
            daemon=True)
        tb.start()

    # 0.4.5 — Sam-feedback fix: SO_REUSEADDR so supervisord restart doesn't
    # collide with the still-bound socket (Errno 98 spam).
    ThreadingHTTPServer.allow_reuse_address = True
    srv = ThreadingHTTPServer((args.host, args.port), _Handler)
    # 0.3.8 — Item 6 — graceful shutdown sends a final 'down' pulse so
    # MC flips offline immediately instead of waiting the 240s stale
    # window. SIGTERM/SIGINT both honored. Installed AFTER srv is bound
    # so the handler closure can call srv.shutdown() safely.
    def _on_signal(signum, _frame):
        print(f'\n[STOP] signal {signum} — sending shutdown pulse',
              file=sys.stderr)
        _send_shutdown_pulse(beak_key, sd_id, DEFAULT_API_BASE)
        try:
            srv.shutdown()
        except Exception:
            pass
        sys.exit(0)
    try:
        signal.signal(signal.SIGTERM, _on_signal)
        signal.signal(signal.SIGINT, _on_signal)
    except (ValueError, OSError):
        # Signal can't be set when not in main thread — skip silently.
        pass

    print(f'[LISTEN] http://{args.host}:{args.port}/beak/telegram/forward '
          f'(auto_reply={args.auto_reply}, on_message={bool(args.on_message)}, '
          f'owner_approval={args.owner_approval}, '
          f'strict_consent={args.strict_consent}, '
          f'hmac={"OFF" if args.unsafe_skip_hmac else "ON"})')
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\n[STOP] interrupt')
    return 0


if __name__ == '__main__':
    sys.exit(main())
