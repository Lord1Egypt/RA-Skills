#!/usr/bin/env python3
"""
Space Duck — Inbound peck listener (webhook receiver stub).

INTENT: Run a tiny HTTP server that the Space Duck backend can POST
        peck.received events to, so the agent actually receives messages
        instead of dead-ending.
CALLS:  Outbound only when --forward-to is set (OS notifier and/or a
        user-supplied Telegram bot). Otherwise listens locally only.
AUTH:   The backend identifies itself with X-SpaceDuck-Event:
        peck.received header. There is no inbound HMAC today (per
        SKILL.md §Important — "best-effort, 10s timeout, no retry").
        For production, terminate behind a reverse proxy with TLS and
        firewall to the Beak edge IPs.

What it does:
  • Listens on --host:--port (default 0.0.0.0:8787)
  • POST /peck       → save body to ~/.space-duck/inbox/<peck_id>.json
  • POST /peck       → if --forward-to given, push to local channel(s)
  • POST /peck       → if --on-peck given, exec it with the JSON on stdin
  • GET  /healthz    → 200 OK (so the backend can see you're up)
  • Anything else    → 404

To register this as your inbound URL, run:
  python3 setup.py --webhook-url https://<public-host>/peck

Forward channels (--forward-to, repeatable):
  os         OS-native notification (osascript / notify-send / msg)
  telegram   USER-side Telegram bot (separate from the per-agent enc_token).
             Read SPACEDUCK_FWD_TG_TOKEN + SPACEDUCK_FWD_TG_CHAT from env,
             or {"telegram":{"bot_token":"…","chat_id":"…"}} from
             ~/.space-duck/forward.json. This rail bypasses the per-duck bot
             entirely — outages there don't break local delivery.
  slack      Slack incoming-webhook URL. SPACEDUCK_FWD_SLACK_WEBHOOK env, or
             {"slack":{"webhook_url":"https://hooks.slack.com/…"}} in
             forward.json.
  discord    Discord webhook URL. SPACEDUCK_FWD_DISCORD_WEBHOOK env, or
             {"discord":{"webhook_url":"https://discord.com/api/webhooks/…"}}
             in forward.json.
  email      SMTP. SPACEDUCK_FWD_SMTP_HOST/PORT/USER/PASS + EMAIL_FROM/TO env,
             or {"email":{"smtp_host":"…","smtp_port":587,"smtp_user":"…",
             "smtp_pass":"…","from_addr":"…","to_addr":"…","use_tls":true}}
             in forward.json.

Lambda variant (drop-in handler) — sketch at the bottom of this file.

Usage:
  python3 peck_listener.py                              # listen on 0.0.0.0:8787
  python3 peck_listener.py --port 9000
  python3 peck_listener.py --on-peck ./reply.sh

  # Autonomous responder (skill 0.3.2+): runs the local Claude Code CLI
  # to compose a reply, gated by the connection's auto_respond permission
  # and the session rotation cap. Closes the David ↔ Sam auto-conversation
  # loop without any platform-side change.
  python3 peck_listener.py --allow-shell-hook \
      --on-peck "python3 $(dirname $0)/peck_responder.py"
  python3 peck_listener.py --forward-to os
  python3 peck_listener.py --forward-to os --forward-to telegram
"""
import argparse, json, os, platform, shlex, subprocess, sys, time
import urllib.error, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

INBOX       = Path.home() / '.space-duck' / 'inbox'
# Legacy single-path constant — kept for back-compat with anyone importing it.
# Real lookup goes through _FORWARD_CFG_PATHS below so a forward.json that
# pair.py wrote to /data/.spaceduck (Docker mount) is still found.
FORWARD_CFG = Path.home() / '.space-duck' / 'forward.json'
_FORWARD_CFG_PATHS = [
    Path('/data/.spaceduck') / 'forward.json',
    Path('/data/.openclaw/workspace/.spaceduck') / 'forward.json',
    Path.home() / '.space-duck' / 'forward.json',
]

# Poll-mode state files. Same dir as INBOX so a paired agent finds them
# without extra config. Both are best-effort — losing them just means a
# slightly larger replay window on next start.
POLL_STATE  = Path.home() / '.space-duck' / 'poll_state.json'   # {latest_timestamp_ms}
SEEN_IDS    = Path.home() / '.space-duck' / 'seen_peck_ids'     # newline ids, last 1000
LISTENER_PID = Path.home() / '.space-duck' / 'listener.pid'
LISTENER_LOG = Path.home() / '.space-duck' / 'listener.log'

# Config search order — matches pair.py CANDIDATE_DIRS so a Docker-mounted
# /data/.spaceduck and a bare-host ~/.space-duck both work. HOME-first so
# we match send_peck.py priority; OTP rekeys reach ~/.space-duck first and
# Docker-mounted copies may carry a stale key after a partial rotate.
_POLL_CONFIG_PATHS = [
    Path.home() / '.space-duck' / 'config.json',
    Path('/data/.spaceduck') / 'config.json',
    Path('/data/.openclaw/workspace/.spaceduck') / 'config.json',
]


# ── Forward adapters: skill-side delivery rails ──
# Each adapter takes the peck event dict and returns (ok: bool, info: str).
# Failures are logged and swallowed — one bad channel never breaks others.

def _load_forward_config():
    """Return the merged forward config from the first existing candidate
    path (Docker /data mount or bare-host home). Same search order pair.py
    writes to, so a paired agent always finds its own forward.json no
    matter which mount was writable at pair time.
    """
    for path in _FORWARD_CFG_PATHS:
        if not path.exists():
            continue
        try:
            return json.loads(path.read_text())
        except Exception:
            continue
    return {}


def _peck_summary(event):
    sender = event.get('sender_name') or event.get('sender_spaceduck_id') or 'duck'
    title  = f'🦆 Peck from {sender}'
    msg    = (event.get('message') or '').strip()
    shared = event.get('shared_mds') or []
    if shared:
        names = [(r.get('filename') or '?') for r in shared if isinstance(r, dict)]
        msg = msg + f'\n\n📎 {len(shared)} shared MD(s): {", ".join(names[:3])}' + ('…' if len(names) > 3 else '')
    return title, sender, msg


# ── shared_mds attachment fetch (Gap D-client) ──
# Envelope shape (lambda_v8.py:2377-2384): list of
#   {'filename': str, 'access_level': 'read', 'fetch_url': str}
# Server endpoint /beak/agent/files/shared/{filename} returns {'content': str, …}.
# Today the GET requires a Cognito JWT (_require_auth at lambda_v8.py:18716). The
# skill only has beak_key, so until the server adds a beak-key auth-bridge to that
# endpoint, the GET will 401 — we still surface the metadata (count + filenames)
# so the receiver isn't blind to attached files.
def _fetch_shared_mds_for_peck(event, listener_cfg):
    refs = event.get('shared_mds') or []
    if not refs:
        return None
    peck_id = event.get('peck_id') or f'peck_{int(time.time()*1000)}'
    files_dir = INBOX / f'{peck_id}.files'
    try:
        files_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        return {'count': len(refs), 'fetched': 0, 'failed': len(refs),
                'dir': str(files_dir), 'reason': f'mkdir_failed:{type(e).__name__}'}
    cfg = listener_cfg or _load_poll_config() or {}
    beak_key = cfg.get('beak_key', '')
    sdid     = cfg.get('spaceduck_id', '')
    fetched, failed, errors = 0, 0, []
    # Write a manifest with the metadata regardless of fetch outcome — this is
    # the receiver's record of what was attached, useful even when content fetch
    # 401s pending the server-side auth bridge.
    try:
        (files_dir / '_manifest.json').write_text(json.dumps(refs, indent=2))
    except Exception:
        pass
    if not beak_key or not sdid:
        return {'count': len(refs), 'fetched': 0, 'failed': len(refs),
                'dir': str(files_dir), 'reason': 'no_beak_key_or_sdid_in_config'}
    for ref in refs:
        if not isinstance(ref, dict):
            failed += 1; continue
        fn  = (ref.get('filename') or '').strip()
        url = (ref.get('fetch_url') or '').strip()
        if not fn or not url or '..' in fn or '/' in fn:
            failed += 1; errors.append(f'{fn}: bad ref')
            continue
        try:
            req = urllib.request.Request(
                url, method='GET',
                headers={'X-Beak-Key': beak_key, 'X-Spaceduck-ID': sdid},
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            content = data.get('content', '')
            (files_dir / fn).write_text(content)
            fetched += 1
        except urllib.error.HTTPError as e:
            failed += 1
            errors.append(f'{fn}: http_{e.code}')
        except Exception as e:
            failed += 1
            errors.append(f'{fn}: {type(e).__name__}')
    return {'count': len(refs), 'fetched': fetched, 'failed': failed,
            'dir': str(files_dir), 'errors': errors[:3]}


def _forward_os(event):
    """Pop an OS-native notification. Auto-detects platform."""
    title, _, msg = _peck_summary(event)
    body = msg[:200]
    sysname = platform.system()
    try:
        if sysname == 'Darwin':
            t = title.replace('"', "'").replace('\\', '')
            b = body.replace('"', "'").replace('\\', '')
            subprocess.run(['osascript', '-e',
                            f'display notification "{b}" with title "{t}"'],
                           check=False, timeout=5)
            return True, 'osascript'
        if sysname == 'Linux':
            r = subprocess.run(['notify-send', title, body],
                               check=False, timeout=5,
                               stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            if r.returncode == 0:
                return True, 'notify-send'
            return False, f'notify-send_rc{r.returncode}'
        if sysname == 'Windows':
            subprocess.run(['msg', '*', f'{title}: {body}'],
                           check=False, timeout=5)
            return True, 'msg'
        return False, f'unsupported_platform:{sysname}'
    except FileNotFoundError as e:
        return False, f'binary_missing:{e.filename}'
    except Exception as e:
        return False, f'os_err:{type(e).__name__}'


def _forward_telegram(event):
    """Push to a user-side Telegram bot. Decoupled from the per-agent enc_token."""
    cfg     = _load_forward_config().get('telegram') or {}
    token   = os.environ.get('SPACEDUCK_FWD_TG_TOKEN', cfg.get('bot_token', ''))
    chat_id = os.environ.get('SPACEDUCK_FWD_TG_CHAT',  cfg.get('chat_id', ''))
    if not token or not chat_id:
        return False, 'no_token_or_chat (set SPACEDUCK_FWD_TG_TOKEN/CHAT or ~/.space-duck/forward.json)'
    title, _, msg = _peck_summary(event)
    text = f'{title}\n\n{msg}'[:4000]
    payload = urllib.parse.urlencode({'chat_id': chat_id, 'text': text}).encode()
    req = urllib.request.Request(
        f'https://api.telegram.org/bot{token}/sendMessage',
        data=payload, method='POST',
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return (True, 'sent') if r.status == 200 else (False, f'http_{r.status}')
    except urllib.error.HTTPError as e:
        snippet = e.read()[:120].decode('utf-8', 'ignore')
        return False, f'http_{e.code}:{snippet}'
    except Exception as e:
        return False, f'tg_err:{type(e).__name__}'


def _post_json(url, body):
    """Tiny shared JSON POST. Returns (ok, info)."""
    data = json.dumps(body).encode()
    req  = urllib.request.Request(
        url, data=data, method='POST',
        headers={'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return (True, 'sent') if 200 <= r.status < 300 else (False, f'http_{r.status}')
    except urllib.error.HTTPError as e:
        snippet = e.read()[:120].decode('utf-8', 'ignore')
        return False, f'http_{e.code}:{snippet}'
    except Exception as e:
        return False, f'err:{type(e).__name__}'


def _forward_slack(event):
    """Push to a Slack incoming-webhook URL."""
    cfg = _load_forward_config().get('slack') or {}
    url = os.environ.get('SPACEDUCK_FWD_SLACK_WEBHOOK', cfg.get('webhook_url', ''))
    if not url:
        return False, 'no_webhook (set SPACEDUCK_FWD_SLACK_WEBHOOK or ~/.space-duck/forward.json)'
    title, _, msg = _peck_summary(event)
    return _post_json(url, {'text': f'*{title}*\n{msg[:3500]}'})


def _forward_discord(event):
    """Push to a Discord webhook URL."""
    cfg = _load_forward_config().get('discord') or {}
    url = os.environ.get('SPACEDUCK_FWD_DISCORD_WEBHOOK', cfg.get('webhook_url', ''))
    if not url:
        return False, 'no_webhook (set SPACEDUCK_FWD_DISCORD_WEBHOOK or ~/.space-duck/forward.json)'
    title, _, msg = _peck_summary(event)
    text = f'**{title}**\n{msg}'[:1900]
    return _post_json(url, {'content': text})


def _forward_email(event):
    """Send the peck as an email via SMTP."""
    import smtplib
    from email.message import EmailMessage
    cfg = _load_forward_config().get('email') or {}
    host = os.environ.get('SPACEDUCK_FWD_SMTP_HOST',  cfg.get('smtp_host', ''))
    port = int(os.environ.get('SPACEDUCK_FWD_SMTP_PORT', cfg.get('smtp_port', 587)) or 587)
    user = os.environ.get('SPACEDUCK_FWD_SMTP_USER',  cfg.get('smtp_user', ''))
    pwd  = os.environ.get('SPACEDUCK_FWD_SMTP_PASS',  cfg.get('smtp_pass', ''))
    fro  = os.environ.get('SPACEDUCK_FWD_EMAIL_FROM', cfg.get('from_addr', user))
    to   = os.environ.get('SPACEDUCK_FWD_EMAIL_TO',   cfg.get('to_addr', ''))
    use_tls = cfg.get('use_tls', True)
    if not host or not to or not fro:
        return False, 'no_smtp_config (set SPACEDUCK_FWD_SMTP_HOST + EMAIL_FROM/TO or ~/.space-duck/forward.json)'
    title, sender_name, msg = _peck_summary(event)
    em = EmailMessage()
    em['Subject'] = title
    em['From']    = fro
    em['To']      = to
    em.set_content(f'{title}\n\n{msg}\n\n— peck_id: {event.get("peck_id", "?")}')
    try:
        with smtplib.SMTP(host, port, timeout=10) as s:
            if use_tls:
                s.starttls()
            if user and pwd:
                s.login(user, pwd)
            s.send_message(em)
        return True, f'sent_to:{to}'
    except Exception as e:
        return False, f'smtp_err:{type(e).__name__}'


FORWARDERS = {
    'os':       _forward_os,
    'telegram': _forward_telegram,
    'slack':    _forward_slack,
    'discord':  _forward_discord,
    'email':    _forward_email,
}

class PeckHandler(BaseHTTPRequestHandler):
    on_peck_cmd = None  # set by main()
    forward_to  = None  # set by main(), list[str]

    def log_message(self, fmt, *args):
        ts = time.strftime('%H:%M:%S')
        sys.stdout.write(f'[{ts}] {self.address_string()} — {fmt % args}\n')
        sys.stdout.flush()

    def _send_json(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        try:
            self.wfile.flush()
        except Exception:
            pass

    def do_GET(self):
        if self.path == '/healthz':
            self._send_json(200, {'ok': True}); return
        self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path != '/peck':
            self.send_response(404); self.end_headers(); return

        n = int(self.headers.get('Content-Length') or 0)
        raw = self.rfile.read(n) if n else b''
        try:
            event = json.loads(raw)
        except Exception:
            self._send_json(400, {'error': 'invalid_json'}); return

        evt_hdr = self.headers.get('X-SpaceDuck-Event', '?')
        peck_id = event.get('peck_id') or f'peck_{int(time.time()*1000)}'
        sender  = event.get('sender_name') or event.get('sender_spaceduck_id') or '?'
        msg     = (event.get('message') or '')[:140]
        print(f'📩 peck.received  evt={evt_hdr}  from={sender}  id={peck_id}')
        print(f'   "{msg}"')

        # Persist to inbox before any side-effects.
        try:
            INBOX.mkdir(parents=True, exist_ok=True)
            (INBOX / f'{peck_id}.json').write_text(json.dumps(event, indent=2))
        except Exception as e:
            print(f'   warn: could not write inbox: {e}')

        # Surface + fetch any inbound shared MDs (Gap D-client). Manifest is
        # written regardless; content fetch is best-effort.
        sm = _fetch_shared_mds_for_peck(event, None)
        if sm:
            print(f'   📎 shared_mds: {sm["fetched"]}/{sm["count"]} fetched → {sm["dir"]}')
            if sm.get('errors'):
                print(f'      err: {"; ".join(sm["errors"])}')

        # Acknowledge first — backend has a 10s deadline. Forwarders + on-peck
        # run after the ack so a slow Telegram push or shell script can't time
        # the backend out.
        self._send_json(200, {'received': True, 'peck_id': peck_id})

        # 2026-05-17 — receiver-side mute filter. The connection record's
        # muted_until is a SINGLE field that silences both directions: outbound
        # is blocked at the send path (server 403 connection_muted); inbound is
        # filtered here. Audit trail still kept (we persisted above) so muted
        # pecks aren't lost — just not surfaced via forwarders / on-peck.
        sender_sd = event.get('sender_spaceduck_id') or ''
        if sender_sd:
            try:
                from _preflight import get_effective
                perms = get_effective(sender_sd) or {}
                muted_until = int(perms.get('muted_until') or 0)
                if muted_until > int(time.time()):
                    print(f'   🔇 sender muted (until epoch {muted_until}) — '
                          'forwarders + on-peck suppressed (peck still in inbox)')
                    return
            except Exception as e:
                # Fail-open: if preflight can't reach the server we still
                # forward, so a network blip doesn't silence pecks unexpectedly.
                print(f'   warn: mute check skipped ({e})')

        # Local-side fanout to user-preferred channels. Resilient to per-agent
        # bot-token outages (the dead Xero_Spaceduck_bot class of bug).
        for ch in (self.forward_to or []):
            fn = FORWARDERS.get(ch)
            if not fn:
                print(f'   warn: unknown forward channel "{ch}"')
                continue
            try:
                ok, info = fn(event)
            except Exception as e:
                ok, info = False, f'adapter_crash:{type(e).__name__}'
            print(f'   {"✅" if ok else "⚠️"} forward[{ch}]: {info}')

        # Optional handler script (gets the peck JSON on stdin)
        if self.on_peck_cmd:
            try:
                # argv is parsed with shlex; subprocess runs without shell
                # interpretation. Gated upstream by --allow-shell-hook.
                argv = shlex.split(self.on_peck_cmd)
                subprocess.Popen(
                    argv,
                    stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                ).communicate(input=raw, timeout=8)
            except Exception as e:
                print(f'   warn: --on-peck handler failed: {e}')

# ─────────────────────────────────────────────────────────────────────────
# Poll mode — drop-in alternative to the HTTP server for laptops with no
# public URL. Reuses every forwarder + the same INBOX path; only the
# transport changes. See coordination/DESIGN-POLLING-LISTENER-2026-05-09.md.
# ─────────────────────────────────────────────────────────────────────────

def _load_poll_config():
    # Collect every valid-shape candidate, then pick the one whose beak_key
    # actually authenticates. Solves the "stale-key in one path, fresh-key
    # in another" class of bug (Sam diagnosed 2026-06-16, Wayne re-hit
    # 2026-06-17) where pair.py wrote to all three paths but a subsequent
    # OTP rekey only landed on one — listener historically picked the
    # first path-on-disk and 403'd in silence.
    candidates = []
    for p in _POLL_CONFIG_PATHS:
        if not p.exists():
            continue
        try:
            cfg = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if cfg.get('beak_key') and cfg.get('spaceduck_id'):
            cfg['_path'] = str(p)
            candidates.append(cfg)
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]
    # Multiple candidates — probe each against /beak/peck/inbox and pick
    # the first that returns 200. Falls through to first valid-shape with
    # a warning if all probes fail (network down, all keys stale, etc.).
    for cfg in candidates:
        api_base = cfg.get('api_base', 'https://beak.spaceduckling.com').rstrip('/')
        url = (f'{api_base}/beak/peck/inbox'
               f'?spaceduck_id={urllib.parse.quote(cfg["spaceduck_id"])}'
               f'&since=0&limit=1')
        try:
            status, _body, _hdrs = _http_get_json(
                url, {'X-Beak-Key': cfg['beak_key']}, timeout=5)
        except Exception:
            status = 0
        if status == 200:
            return cfg
    # All probes failed — return first valid-shape; the poll loop will
    # surface the auth error visibly.
    chosen = candidates[0]
    paths = ', '.join(c['_path'] for c in candidates)
    print(f'⚠️  beak_key auth probe failed for all {len(candidates)} configs ({paths}); '
          f'falling back to {chosen["_path"]} — re-pair or rotate the OTP if 403 persists.')
    return chosen


def _load_poll_state():
    if not POLL_STATE.exists():
        return {'latest_timestamp_ms': 0}
    try:
        return json.loads(POLL_STATE.read_text())
    except Exception:
        return {'latest_timestamp_ms': 0}


def _save_poll_state(latest_ms):
    try:
        POLL_STATE.parent.mkdir(parents=True, exist_ok=True)
        POLL_STATE.write_text(json.dumps({'latest_timestamp_ms': int(latest_ms)}))
    except Exception:
        pass  # best-effort; restart just replays from cold floor


def _load_seen_ids():
    if not SEEN_IDS.exists():
        return set(), []
    try:
        lines = [ln.strip() for ln in SEEN_IDS.read_text().splitlines() if ln.strip()]
    except Exception:
        return set(), []
    return set(lines), lines


def _append_seen_id(peck_id, seen_set, seen_list, cap=1000):
    if peck_id in seen_set:
        return
    seen_set.add(peck_id)
    seen_list.append(peck_id)
    if len(seen_list) > cap:
        # drop oldest 100 at a time so we're not rewriting on every peck
        drop = len(seen_list) - cap
        for old in seen_list[:drop]:
            seen_set.discard(old)
        del seen_list[:drop]
    try:
        SEEN_IDS.parent.mkdir(parents=True, exist_ok=True)
        SEEN_IDS.write_text('\n'.join(seen_list) + '\n')
    except Exception:
        pass  # dedupe degrades to "rely on ack"; ack still prevents most dupes


def _http_get_json(url, headers, timeout=15):
    req = urllib.request.Request(url, method='GET', headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read()), dict(r.headers)
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read())
        except Exception:
            body = {'error': f'HTTP {e.code}'}
        return e.code, body, dict(e.headers or {})
    except Exception as e:
        return 0, {'error': f'{type(e).__name__}: {e}'}, {}


def _http_post_json(url, headers, body, timeout=15):
    req = urllib.request.Request(
        url, method='POST', headers={**headers, 'Content-Type': 'application/json'},
        data=json.dumps(body).encode(),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {'error': f'HTTP {e.code}'}
    except Exception as e:
        return 0, {'error': f'{type(e).__name__}: {e}'}


def _deliver(event, forward_to, on_peck_cmd):
    """Run the same fanout as the HTTP push handler. Reused verbatim from
    PeckHandler.do_POST so push and poll mode behave identically."""
    peck_id = event.get('peck_id') or f'peck_{int(time.time()*1000)}'
    sender  = event.get('sender_name') or event.get('sender_spaceduck_id') or '?'
    msg     = (event.get('message') or '')[:140]
    print(f'📩 peck.received  from={sender}  id={peck_id}')
    print(f'   "{msg}"')

    try:
        INBOX.mkdir(parents=True, exist_ok=True)
        (INBOX / f'{peck_id}.json').write_text(json.dumps(event, indent=2))
    except Exception as e:
        print(f'   warn: could not write inbox: {e}')

    # Surface + fetch any inbound shared MDs (Gap D-client). Manifest is
    # written regardless; content fetch is best-effort and uses beak_key
    # auth — server-side bridge to that endpoint is the remaining gap.
    sm = _fetch_shared_mds_for_peck(event, None)
    if sm:
        print(f'   📎 shared_mds: {sm["fetched"]}/{sm["count"]} fetched → {sm["dir"]}')
        if sm.get('errors'):
            print(f'      err: {"; ".join(sm["errors"])}')

    for ch in (forward_to or []):
        fn = FORWARDERS.get(ch)
        if not fn:
            print(f'   warn: unknown forward channel "{ch}"')
            continue
        try:
            ok, info = fn(event)
        except Exception as e:
            ok, info = False, f'adapter_crash:{type(e).__name__}'
        print(f'   {"✅" if ok else "⚠️"} forward[{ch}]: {info}')

    if on_peck_cmd:
        try:
            argv = shlex.split(on_peck_cmd)
            subprocess.Popen(
                argv,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).communicate(input=json.dumps(event).encode(), timeout=8)
        except Exception as e:
            print(f'   warn: --on-peck handler failed: {e}')


def _write_pid_file():
    try:
        LISTENER_PID.parent.mkdir(parents=True, exist_ok=True)
        LISTENER_PID.write_text(str(os.getpid()))
    except Exception:
        pass


def _clear_pid_file():
    try:
        LISTENER_PID.unlink()
    except FileNotFoundError:
        pass
    except Exception:
        pass


def run_poll(interval, forward_to, on_peck_cmd, cold_start_floor_sec=86400):
    """Long-running poll loop. Replaces the HTTP server for laptops that
    have no public URL. Backend endpoints already shipped (lambda v421+).

    Loop:
      GET  /beak/peck/inbox?spaceduck_id=&since=  (auth: X-Beak-Key)
      → fanout via _deliver()
      → POST /beak/peck/inbox/ack {spaceduck_id, up_to_timestamp}
      → save latest_timestamp_ms to poll_state.json
      → sleep interval (with backoff on 429/5xx)
    """
    cfg = _load_poll_config()
    if not cfg:
        searched = ', '.join(str(p) for p in _POLL_CONFIG_PATHS)
        print(f'❌ No paired config found. Searched: {searched}')
        print('   Run: python3 pair.py')
        sys.exit(1)

    api_base    = cfg.get('api_base', 'https://beak.spaceduckling.com').rstrip('/')
    sd_id       = cfg['spaceduck_id']
    beak_key    = cfg['beak_key']
    agent_name  = cfg.get('agent_name', 'agent')

    state = _load_poll_state()
    seen_set, seen_list = _load_seen_ids()

    # Cold start floor: if poll_state has no timestamp, start from now-24h so
    # we don't replay days of stale pecks on first launch.
    cold_floor_ms = (int(time.time()) - cold_start_floor_sec) * 1000
    since_ms = max(int(state.get('latest_timestamp_ms', 0)), cold_floor_ms)

    headers = {'X-Beak-Key': beak_key}
    INBOX.mkdir(parents=True, exist_ok=True)
    _write_pid_file()

    print(f'🦆 peck_listener (poll)  agent={agent_name}  duck={sd_id[:10]}…')
    print(f'    api: {api_base}')
    print(f'    config: {cfg["_path"]}')
    print(f'    interval: {interval}s   since: {since_ms}ms ({"cold floor" if since_ms == cold_floor_ms else "resumed"})')
    if forward_to:
        print(f'    forward-to: {", ".join(forward_to)}')
    if on_peck_cmd:
        print(f'    on-peck: {on_peck_cmd}')

    backoff = interval
    try:
        while True:
            url = (f'{api_base}/beak/peck/inbox'
                   f'?spaceduck_id={urllib.parse.quote(sd_id)}'
                   f'&since={since_ms}&limit=20')
            status, body, resp_headers = _http_get_json(url, headers)

            if status == 200:
                backoff = interval  # reset on success
                pecks = body.get('pecks') or []
                # backend sorts newest-first; we want oldest-first for ordered fanout
                pecks.sort(key=lambda p: int(p.get('timestamp', 0) or 0))
                processed_max_ts = since_ms
                delivered = 0
                for peck in pecks:
                    pid = peck.get('peck_id') or ''
                    pts = int(peck.get('timestamp', 0) or 0)
                    if pid and pid in seen_set:
                        # already delivered locally — backend ack was lost; skip fanout
                        # but still advance the watermark so we ack it next round
                        if pts > processed_max_ts:
                            processed_max_ts = pts
                        continue
                    _deliver(peck, forward_to, on_peck_cmd)
                    if pid:
                        _append_seen_id(pid, seen_set, seen_list)
                    if pts > processed_max_ts:
                        processed_max_ts = pts
                    delivered += 1

                if pecks and processed_max_ts > since_ms:
                    # Ack runs after fanout — best-effort, same as forwarders.
                    # Backend stores ms; pass ms straight through.
                    a_status, a_body = _http_post_json(
                        f'{api_base}/beak/peck/inbox/ack', headers,
                        {'spaceduck_id': sd_id, 'up_to_timestamp': int(processed_max_ts)},
                    )
                    if a_status == 200:
                        print(f'   ✅ ack {a_body.get("acked", 0)} up_to={processed_max_ts}'
                              + (f' (delivered {delivered})' if delivered else ' (already-seen)'))
                    else:
                        print(f'   ⚠️ ack failed: http_{a_status} {a_body}')
                    since_ms = processed_max_ts
                    _save_poll_state(since_ms)
            elif status in (429, 500, 502, 503, 504):
                ra = resp_headers.get('Retry-After', '') or resp_headers.get('retry-after', '')
                try:
                    ra_sec = int(ra) if ra else 0
                except Exception:
                    ra_sec = 0
                backoff = min(60, max(backoff * 2, ra_sec or interval))
                print(f'   ⚠️ inbox http_{status}; backing off {backoff}s')
            elif status == 0:
                # network error
                backoff = min(60, max(backoff * 2, interval))
                print(f'   ⚠️ inbox network err: {body.get("error", "?")}; backing off {backoff}s')
            else:
                # 4xx other than rate-limit — likely auth or schema mismatch.
                # Surface and keep trying at base interval; this isn't fatal.
                print(f'   ⚠️ inbox http_{status}: {body}')
                backoff = interval

            time.sleep(backoff)
    except KeyboardInterrupt:
        print('\nbye.')
    finally:
        _clear_pid_file()


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Run a peck.received listener (HTTP push or polling)')
    p.add_argument('--poll', action='store_true',
                   help='Polling mode — long-running loop against /beak/peck/inbox. '
                        'Use this on laptops with no public URL.')
    p.add_argument('--interval', type=float, default=3.0,
                   help='Poll interval in seconds (poll mode only; default 3)')
    p.add_argument('--host', default='0.0.0.0',
                   help='HTTP server bind host (push mode only)')
    p.add_argument('--port', type=int, default=8787,
                   help='HTTP server bind port (push mode only)')
    p.add_argument('--on-peck', dest='on_peck',
                   help='Local handler command to run for each peck (JSON on stdin). '
                        "argv is parsed with shlex; no shell interpretation. "
                        'Requires --allow-shell-hook for explicit opt-in.')
    p.add_argument('--allow-shell-hook', dest='allow_shell_hook', action='store_true',
                   help='Explicit opt-in to execute the --on-peck handler. The listener refuses '
                        'to run an --on-peck command without this flag — so an inbound peck can '
                        'never silently fan out to a local process.')
    p.add_argument('--forward-to', dest='forward_to', action='append', default=[],
                   choices=sorted(FORWARDERS.keys()),
                   help='Forward inbound pecks to a built-in adapter (telegram / slack / discord / '
                        'email / os). Built-in Python adapters only — no shell exec, no opt-in flag needed.')
    args = p.parse_args()

    # --on-peck requires explicit opt-in.
    if args.on_peck and not args.allow_shell_hook:
        sys.stderr.write(
            "error: --on-peck was given without --allow-shell-hook.\n"
            "       The listener refuses to run a user-supplied handler command\n"
            "       without an explicit opt-in flag. Re-run with both:\n"
            "         python3 peck_listener.py --poll --on-peck '<cmd>' --allow-shell-hook\n"
        )
        sys.exit(2)

    if args.poll:
        run_poll(
            interval=max(1.0, float(args.interval)),
            forward_to=args.forward_to,
            on_peck_cmd=args.on_peck,
        )
        sys.exit(0)

    PeckHandler.on_peck_cmd = args.on_peck
    PeckHandler.forward_to  = args.forward_to
    INBOX.mkdir(parents=True, exist_ok=True)

    srv = ThreadingHTTPServer((args.host, args.port), PeckHandler)
    print(f'🦆 peck_listener  listening on {args.host}:{args.port}')
    print(f'    inbox: {INBOX}')
    print(f'    register: python3 setup.py --webhook-url '
          f'https://<public-host-mapped-to-{args.port}>/peck')
    if args.on_peck:
        print(f'    on-peck: {args.on_peck}')
    if args.forward_to:
        print(f'    forward-to: {", ".join(args.forward_to)}')
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print('\nbye.')


# -----------------------------------------------------------------------------
# AWS Lambda drop-in (paste into a Lambda with API Gateway / Function URL):
#
# import json, os, time
# def handler(event, context):
#     headers = {k.lower(): v for k, v in (event.get('headers') or {}).items()}
#     if event.get('requestContext', {}).get('http', {}).get('method') == 'GET':
#         return {'statusCode': 200, 'body': '{"ok":true}'}
#     try:
#         peck = json.loads(event.get('body') or '{}')
#     except Exception:
#         return {'statusCode': 400, 'body': '{"error":"invalid_json"}'}
#     # Forward to your bot / queue / DB here.
#     # e.g. boto3.client('sqs').send_message(QueueUrl=..., MessageBody=json.dumps(peck))
#     return {'statusCode': 200, 'body': json.dumps({'received': True,
#             'peck_id': peck.get('peck_id')})}
# -----------------------------------------------------------------------------
