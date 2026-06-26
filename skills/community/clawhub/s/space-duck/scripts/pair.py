#!/usr/bin/env python3
"""
Space Duck — Pair this agent with one of your ducks via browser confirm.

INTENT: Eliminate chat-pasted secrets. The agent generates a 6-digit code +
        URL, the user signs in (already typically signed in) and clicks
        Confirm in the browser, the agent polls and receives its long-lived
        identity bundle (spaceduck_id, duckling_id, bk_LIVE_…). Zero secrets
        flow through the chat surface.
CALLS:  POST <api>/beak/pair/start          (no auth — agent-initiated)
        GET  <api>/beak/pair/<code>         (no auth — single-shot bound read)
        POST <api>/beak/pulse               (register webhook after bound)
AUTH:   None on the agent side. The browser-side bind is auth-gated by the
        user's sd_token. The Beak Key arrives once, in the bound poll
        response, and is wiped from the server record after first read.

Usage:
  # One-shot interactive (foreground):
  python3 pair.py
  python3 pair.py --agent-name "claude on macbook-pro"
  python3 pair.py --webhook-url https://my-openclaw.example.com/peck

  # Wire Telegram forward at pair time (writes ~/.space-duck/forward.json):
  python3 pair.py \
      --forward-tg-token 8507764812:AAEo… \
      --forward-tg-chat  8592866150

  # Two-step (safe for agents that may background a process):
  python3 pair.py --start         # prints JSON {code,pair_url,...}, exits 0
  # ...user confirms in browser...
  python3 pair.py --confirm       # polls, writes config, exits 0

AGENT NOTE: pair.py is interactive. If you must background it, prefer the
two-step --start / --confirm flow — --start exits immediately with the
6-digit code in stdout JSON, so you can surface it to the user without
relying on a long-running process whose stdout you may not read.
"""
import argparse
import getpass
import hashlib
import json
import os
import platform
import secrets
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Line-buffer stdout so prints surface immediately even when backgrounded
# (default Python buffering is block-buffered when stdout isn't a TTY,
# which silently swallows the handshake until the process exits).
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

API_BASE = 'https://beak.spaceduckling.com'

POLL_INTERVAL_SEC = 3
POLL_TIMEOUT_SEC = 600  # matches code TTL

# Persistent path resolution — try in this order. Brief v0.1.7 §5.3.
# Docker volumes mount /data; OpenClaw runs at /data/.openclaw/workspace;
# bare hosts and dev machines fall back to ~/.space-duck. We attempt every
# writable path on write so a session that loses one mount still finds its
# config on the next start.
_CANDIDATE_DIRS = [
    Path('/data/.spaceduck'),
    Path('/data/.openclaw/workspace/.spaceduck'),
    Path.home() / '.space-duck',
]


def _writable_dirs():
    """Return the subset of candidate dirs we can create + write to."""
    out = []
    for d in _CANDIDATE_DIRS:
        try:
            d.mkdir(mode=0o700, parents=True, exist_ok=True)
            probe = d / '.write_test'
            probe.write_text('')
            probe.unlink()
            out.append(d)
        except (OSError, PermissionError):
            continue
    return out


def _primary_dir():
    """First writable dir — used for fingerprint + pending state.
    Falls back to ~/.space-duck unconditionally (legacy behaviour) so
    --init / cmd_pulse don't crash on a host with no writable path."""
    dirs = _writable_dirs()
    return dirs[0] if dirs else (Path.home() / '.space-duck')


def _config_paths():
    return [d / 'config.json' for d in _CANDIDATE_DIRS]


def _existing_config():
    """Return (path, parsed_config) for the first valid config we find,
    or (None, None). 'Valid' means all three identity fields populated."""
    for cfg_path in _config_paths():
        if not cfg_path.exists():
            continue
        try:
            cfg = json.loads(cfg_path.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        if cfg.get('beak_key') and cfg.get('spaceduck_id') and cfg.get('duckling_id'):
            return cfg_path, cfg
    return None, None


# Legacy module-level paths — preserved so other scripts that import these
# names keep working. Resolved against the primary writable dir at import.
CONFIG_DIR = _primary_dir()
CONFIG_PATH = CONFIG_DIR / 'config.json'
FINGERPRINT_PATH = CONFIG_DIR / 'fingerprint'
PENDING_PATH = CONFIG_DIR / 'pending_pair.json'
PRIVATE_KEY_FILENAME = 'private_key.pem'
PUBLIC_KEY_FILENAME = 'public_key.pem'
CERT_FILENAME = 'birth_cert.json'

# Listener auto-spawn (poll mode) — co-located with pair.py so we don't have
# to resolve install location across ClawHub vs dev paths.
LISTENER_SCRIPT = Path(__file__).resolve().parent / 'peck_listener.py'
LISTENER_PID_PATH = Path.home() / '.space-duck' / 'listener.pid'
LISTENER_LOG_PATH = Path.home() / '.space-duck' / 'listener.log'
# 0.3.8 — telegram_listener.py auto-spawn target. Separate process from
# peck_listener; opt-in via --telegram-listener.
TG_LISTENER_SCRIPT = Path(__file__).resolve().parent / 'telegram_listener.py'
TG_LISTENER_PID_PATH = Path.home() / '.space-duck' / 'tg-listener.pid'
TG_LISTENER_LOG_PATH = Path.home() / '.space-duck' / 'tg-listener.log'


def _generate_keypair():
    """RSA-4096 keypair (private_pem, public_pem) bytes, or (None, None).

    Brief v0.1.7 §4.1 — every paired agent gets its own keypair so Pond can
    sign a per-duck cert tying the public key to the SDID. Returns (None,
    None) if `cryptography` isn't installed; caller falls back to legacy
    HMAC-only pairing which the lambda still accepts.
    """
    try:
        from cryptography.hazmat.primitives.asymmetric import rsa
        from cryptography.hazmat.primitives import serialization
    except ImportError:
        return None, None
    priv = rsa.generate_private_key(public_exponent=65537, key_size=4096)
    private_pem = priv.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    public_pem = priv.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return private_pem, public_pem


def _ensure_keypair():
    """Return (public_pem_str, private_path) — generate + cache on first run."""
    primary = _primary_dir()
    priv_path = primary / PRIVATE_KEY_FILENAME
    pub_path = primary / PUBLIC_KEY_FILENAME
    if priv_path.exists() and pub_path.exists():
        try:
            return pub_path.read_text(), priv_path
        except OSError:
            pass
    private_pem, public_pem = _generate_keypair()
    if private_pem is None:
        return '', None
    primary.mkdir(mode=0o700, parents=True, exist_ok=True)
    priv_path.write_bytes(private_pem)
    priv_path.chmod(0o600)
    pub_path.write_bytes(public_pem)
    pub_path.chmod(0o644)
    return public_pem.decode('ascii'), priv_path


def _write_forward_config(tg_token, tg_chat):
    """Persist Telegram forward config so peck_listener picks it up without
    env vars on next start. Merges with any existing forward.json (preserves
    slack/discord/email blocks). Writes to every writable candidate dir so a
    Docker /data mount and a host ~/.space-duck both stay in sync — mirrors
    the config.json multi-write strategy.
    Returns the list of written paths (empty if nothing to write)."""
    if not (tg_token or tg_chat):
        return []
    existing = {}
    for d in _CANDIDATE_DIRS:
        fwd = d / 'forward.json'
        if fwd.exists():
            try:
                existing = json.loads(fwd.read_text())
                break
            except (OSError, json.JSONDecodeError):
                continue
    tg = existing.get('telegram') or {}
    if tg_token:
        tg['bot_token'] = tg_token
    if tg_chat:
        tg['chat_id'] = tg_chat
    existing['telegram'] = tg
    body = json.dumps(existing, indent=2)
    written = []
    for d in _writable_dirs():
        fwd = d / 'forward.json'
        try:
            fwd.write_text(body)
            fwd.chmod(0o600)
            written.append(fwd)
        except (OSError, PermissionError):
            continue
    return written


def _persist_birth_cert(bound):
    """Save signed birth cert + payload to every writable dir. Returns paths."""
    jws = bound.get('cert_signed_jws')
    payload = bound.get('cert_payload')
    if not jws or not payload:
        return []
    body = json.dumps({'jws': jws, 'payload': payload}, indent=2)
    written = []
    for d in _writable_dirs():
        cert_path = d / CERT_FILENAME
        try:
            cert_path.write_text(body)
            cert_path.chmod(0o600)
            written.append(cert_path)
        except (OSError, PermissionError):
            continue
    return written


def _stable_fingerprint(hostname, username):
    """Short stable per-host id, salted by a random value persisted on disk.

    Salt persistence means reruns produce the same fingerprint, so the user
    can recognise the agent across pair attempts without re-confirming.
    """
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    if FINGERPRINT_PATH.exists():
        salt = FINGERPRINT_PATH.read_text().strip()
    else:
        salt = secrets.token_hex(16)
        FINGERPRINT_PATH.write_text(salt)
        FINGERPRINT_PATH.chmod(0o600)
    return hashlib.sha256(f'{hostname}|{username}|{salt}'.encode()).hexdigest()[:12]


def _build_descriptor(agent_name_override):
    hostname = socket.gethostname() or 'unknown-host'
    try:
        username = getpass.getuser()
    except Exception:
        username = 'unknown'
    name = agent_name_override or f'{username} on {hostname}'
    host_hint = f'{hostname} / {platform.system()}'
    return {
        'name': name,
        'host_hint': host_hint,
        'fingerprint': _stable_fingerprint(hostname, username),
    }


def _post(path, body):
    req = urllib.request.Request(
        f'{API_BASE}{path}',
        data=json.dumps(body).encode(),
        method='POST',
        headers={'Content-Type': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read())
        except Exception:
            err_body = {'error': f'HTTP {e.code}'}
        return e.code, err_body


def _get(path):
    req = urllib.request.Request(f'{API_BASE}{path}', method='GET')
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read())
        except Exception:
            err_body = {'error': f'HTTP {e.code}'}
        return e.code, err_body


def _start_pair(descriptor, webhook_url):
    body = {'agent_descriptor': descriptor}
    if webhook_url:
        body['webhook_url'] = webhook_url
    pubkey_pem, _priv_path = _ensure_keypair()
    if pubkey_pem:
        body['pubkey_pem'] = pubkey_pem
    status, resp = _post('/beak/pair/start', body)
    if status != 200:
        print(f'❌ Pair start failed: {resp.get("error", "unknown")}')
        sys.exit(1)
    return resp


def _print_handshake(resp, descriptor):
    pair_url = resp['pair_url']
    code = resp['code']
    expires_min = max(1, int(resp.get('expires_in_seconds', 600)) // 60)
    print()
    print('🦆 Open this in your browser to bind this agent:')
    print()
    print(f'    {pair_url}')
    print()
    print(f'   Or visit https://spaceduckling.com/pair and enter code: {code}')
    print()
    print(f'   Agent: {descriptor["name"]}  ({descriptor["host_hint"]}, fp {descriptor["fingerprint"][:8]})')
    print()
    print(f'   Waiting for confirm (expires in {expires_min} min)...')
    print()


def _poll_until_bound(code):
    deadline = time.time() + POLL_TIMEOUT_SEC
    last_status = None
    while time.time() < deadline:
        status, resp = _get(f'/beak/pair/{code}')
        if status == 200:
            s = resp.get('status')
            if s == 'bound':
                return resp
            if s in ('expired', 'cancelled', 'consumed'):
                print(f'❌ Pair {s}. Re-run pair.py to start a fresh handshake.')
                sys.exit(1)
            if s != last_status:
                last_status = s
        elif status == 404:
            print('❌ Pair code not found (already expired). Re-run pair.py.')
            sys.exit(1)
        time.sleep(POLL_INTERVAL_SEC)
    print('⏰ Timed out waiting for browser confirm. Re-run pair.py to retry.')
    sys.exit(1)


def _write_config(bound, webhook_url, workspace_dir=''):
    # 2026-05-17 — capture workspace_dir at pair time so sync.py
    # defaults to the agent's actual working directory instead of cwd
    # wherever the user runs it next. Falls back to the cwd we paired in,
    # which is almost always the agent's working dir.
    if not workspace_dir:
        try:
            workspace_dir = str(Path.cwd().resolve())
        except Exception:
            workspace_dir = ''
    config = {
        'beak_key': bound['beak_key'],
        'spaceduck_id': bound['spaceduck_id'],
        'duckling_id': bound['duckling_id'],
        'agent_name': bound.get('agent_name') or 'Agent',
        'api_base': API_BASE,
        'openclaw_webhook_url': webhook_url or bound.get('webhook_url', ''),
        'workspace_dir': workspace_dir,
    }
    body = json.dumps(config, indent=2)
    written = []
    for d in _writable_dirs():
        cfg_path = d / 'config.json'
        try:
            cfg_path.write_text(body)
            cfg_path.chmod(0o600)
            written.append(cfg_path)
        except (OSError, PermissionError):
            continue
    if not written:
        # Legacy fallback: try the home path even if probe failed earlier.
        Path.home().joinpath('.space-duck').mkdir(mode=0o700, parents=True, exist_ok=True)
        legacy = Path.home() / '.space-duck' / 'config.json'
        legacy.write_text(body)
        legacy.chmod(0o600)
        written.append(legacy)
    config['_written_paths'] = [str(p) for p in written]
    return config


def _pulse(spaceduck_id, beak_key, webhook_url=''):
    """Send a presence pulse so the directory flips this duck to ALIVE.

    The webhook URL was already persisted server-side at bind time
    (lambda /beak/pair/<code>/confirm writes spaceducks.openclaw_webhook_url
    from the pair record). /beak/pulse only updates last_seen + health_state;
    the webhook field is harmless noise but kept for forward-compat.
    """
    payload = {
        'spaceduck_id': spaceduck_id,
        'beak_key': beak_key,
        'status': 'ACTIVE',
    }
    if webhook_url:
        payload['openclaw_webhook_url'] = webhook_url
    status, resp = _post('/beak/pulse', payload)
    return status == 200, resp


def _write_pending(started, descriptor, webhook_url, tg_token='', tg_chat='', workspace_dir=''):
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    expires_in = int(started.get('expires_in_seconds', 600))
    payload = {
        'code': started['code'],
        'pair_url': started['pair_url'],
        'expires_in_seconds': expires_in,
        'expires_at': int(time.time()) + expires_in,
        'descriptor': descriptor,
        'webhook_url': webhook_url or '',
        'forward_tg_token': tg_token or '',
        'forward_tg_chat': tg_chat or '',
        'workspace_dir': workspace_dir or '',
    }
    PENDING_PATH.write_text(json.dumps(payload, indent=2))
    PENDING_PATH.chmod(0o600)
    return payload


def _read_pending():
    if not PENDING_PATH.exists():
        print('❌ No pending pair found. Run: python3 pair.py --start')
        sys.exit(1)
    return json.loads(PENDING_PATH.read_text())


def _clear_pending():
    try:
        PENDING_PATH.unlink()
    except FileNotFoundError:
        pass


def _listener_already_running():
    """Return PID if a listener is alive for this user, else None.

    Poll-mode listener writes its PID to ~/.space-duck/listener.pid on
    startup. If the file exists but the process is gone, treat as stale
    and remove it so the next spawn isn't blocked.
    """
    if not LISTENER_PID_PATH.exists():
        return None
    try:
        pid = int(LISTENER_PID_PATH.read_text().strip())
    except Exception:
        try:
            LISTENER_PID_PATH.unlink()
        except Exception:
            pass
        return None
    try:
        os.kill(pid, 0)  # signal 0 = liveness probe
        return pid
    except (ProcessLookupError, PermissionError):
        try:
            LISTENER_PID_PATH.unlink()
        except Exception:
            pass
        return None
    except Exception:
        return pid  # uncertain — assume alive, don't double-spawn


def _detect_forward_channels():
    """Return the list of forward channels with config persisted on disk.

    Used by _spawn_listener so the auto-launched poller actually fans out to
    whatever forward.json has set up — without this, we'd write forward.json
    during pair but the freshly-spawned listener would never hit those rails.
    Currently scoped to telegram (the only channel pair.py knows how to
    write); slack/discord/email config is still external + manual.
    """
    channels = []
    for d in _CANDIDATE_DIRS:
        fwd = d / 'forward.json'
        if not fwd.exists():
            continue
        try:
            cfg = json.loads(fwd.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        tg = cfg.get('telegram') or {}
        if tg.get('bot_token') and tg.get('chat_id'):
            channels.append('telegram')
        break
    return channels


def _spawn_listener(forward_channels=None):
    """Best-effort: start peck_listener.py --poll detached in background.

    Fail soft on any error — pairing already succeeded, the listener is a
    convenience layer. Worst case we print the manual command and move on.
    Returns (pid_or_None, message).
    """
    if not LISTENER_SCRIPT.exists():
        return None, f'listener script not found at {LISTENER_SCRIPT}'

    existing = _listener_already_running()
    if existing:
        return existing, f'already running (pid {existing})'

    try:
        LISTENER_LOG_PATH.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        log_fh = open(LISTENER_LOG_PATH, 'ab')  # append; survives multi-launch
    except Exception as e:
        return None, f'could not open log {LISTENER_LOG_PATH}: {e}'

    cmd = [sys.executable, str(LISTENER_SCRIPT), '--poll']
    for ch in (forward_channels or []):
        cmd += ['--forward-to', ch]

    try:
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL, stdout=log_fh, stderr=log_fh,
            start_new_session=True,  # detach from this terminal session
            cwd=str(Path.home()),
        )
        # peck_listener writes its own PID file on startup; we record this
        # one too so even if the listener crashes pre-PID-write we have a
        # trail. The listener's own write will overwrite this on success.
        try:
            LISTENER_PID_PATH.write_text(str(proc.pid))
            LISTENER_PID_PATH.chmod(0o600)
        except Exception:
            pass
        return proc.pid, f'spawned (pid {proc.pid}, log: {LISTENER_LOG_PATH})'
    except Exception as e:
        try:
            log_fh.close()
        except Exception:
            pass
        return None, f'spawn failed: {type(e).__name__}: {e}'


def _tg_listener_already_running():
    """0.3.8 — best-effort check for an existing telegram_listener.py
    process so we don't double-spawn. Returns pid if alive else None."""
    if not TG_LISTENER_PID_PATH.exists():
        return None
    try:
        pid = int(TG_LISTENER_PID_PATH.read_text().strip())
        os.kill(pid, 0)
        return pid
    except Exception:
        return None


def _spawn_tg_listener(strict_consent=False):
    """0.3.8 — mirror of _spawn_listener but for telegram_listener.py
    --owner-approval. Opt-in via pair.py --telegram-listener flag. Fail
    soft — pairing already succeeded by the time we get here."""
    if not TG_LISTENER_SCRIPT.exists():
        return None, f'tg listener not found at {TG_LISTENER_SCRIPT}'
    existing = _tg_listener_already_running()
    if existing:
        return existing, f'already running (pid {existing})'
    try:
        TG_LISTENER_LOG_PATH.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        log_fh = open(TG_LISTENER_LOG_PATH, 'ab')
    except Exception as e:
        return None, f'could not open log {TG_LISTENER_LOG_PATH}: {e}'
    cmd = [sys.executable, str(TG_LISTENER_SCRIPT), '--owner-approval']
    if strict_consent:
        cmd.append('--strict-consent')
    try:
        proc = subprocess.Popen(
            cmd, stdin=subprocess.DEVNULL, stdout=log_fh, stderr=log_fh,
            start_new_session=True, cwd=str(Path.home()))
        try:
            TG_LISTENER_PID_PATH.write_text(str(proc.pid))
            TG_LISTENER_PID_PATH.chmod(0o600)
        except Exception:
            pass
        return proc.pid, (f'spawned (pid {proc.pid}, '
                          f'log: {TG_LISTENER_LOG_PATH})')
    except Exception as e:
        try: log_fh.close()
        except Exception: pass
        return None, f'spawn failed: {type(e).__name__}: {e}'


def _finalise(bound, webhook_url, spawn_listener=False, tg_token='', tg_chat='', workspace_dir=''):
    config = _write_config(bound, webhook_url, workspace_dir=workspace_dir)
    paths = config.pop('_written_paths', [str(CONFIG_PATH)])
    if len(paths) == 1:
        print(f'💾 Config saved to {paths[0]}')
    else:
        print(f'💾 Config saved to {len(paths)} paths:')
        for p in paths:
            print(f'   • {p}')

    cert_paths = _persist_birth_cert(bound)
    if cert_paths:
        suffix = 's' if len(cert_paths) > 1 else ''
        print(f'📜 Birth cert saved to {len(cert_paths)} path{suffix}')

    fwd_paths = _write_forward_config(tg_token, tg_chat)
    if fwd_paths:
        suffix = 's' if len(fwd_paths) > 1 else ''
        masked_chat = tg_chat or '(unchanged)'
        print(f'📨 Forward → Telegram (chat {masked_chat}) saved to {len(fwd_paths)} path{suffix}')
        print('   Listener will pick this up on next start. Add `--forward-to telegram` to your listener invocation.')

    # Always pulse. Pairing writes identity; presence is a separate signal.
    # Without this, /ducks.html keeps showing "Connect your duck" until some
    # other tool pulses on this duck's behalf.
    ok, resp = _pulse(
        config['spaceduck_id'],
        config['beak_key'],
        config.get('openclaw_webhook_url', ''),
    )
    if ok:
        print('💓 Pulse sent — duck is ALIVE in the directory.')
    else:
        err = resp.get('error', 'unknown') if isinstance(resp, dict) else str(resp)
        print(f'⚠️  Pulse failed ({err}) — pair succeeded, but duck won\'t show online until a pulse goes through.')

    if config.get('openclaw_webhook_url'):
        print(f'🔗 Webhook on file → {config["openclaw_webhook_url"]}')

    # Auto-spawn the polling listener so a freshly paired laptop actually
    # receives pecks without the user having to remember a second command.
    # Push-mode (HTTP webhook) is the right path for hosts with a public URL,
    # but the laptop default is poll. Best-effort — failure does not break
    # pairing (see DESIGN-POLLING-LISTENER-2026-05-09.md).
    if spawn_listener:
        channels = _detect_forward_channels()
        pid, msg = _spawn_listener(forward_channels=channels)
        if pid:
            extra = f' (forward → {",".join(channels)})' if channels else ''
            print(f'👂 Listener {msg}{extra}')
        else:
            print(f'⚠️  Listener not started: {msg}')
            extra = ' '.join(f'--forward-to {ch}' for ch in channels)
            manual = f'python3 {LISTENER_SCRIPT} --poll' + (f' {extra}' if extra else '')
            print(f'   Run manually: {manual}')

    print()
    print(f'✅ Paired as {config["agent_name"]}')
    print(f'   Spaceduck ID: {config["spaceduck_id"]}')
    print(f'   Duckling:     {config["duckling_id"]}')
    print(f'   Beak Key:     {config["beak_key"][:10]}…')

    duckling_id = config['duckling_id']
    has_webhook = bool(config.get('openclaw_webhook_url'))
    print()
    print('Next steps:')
    print(f'  1. Add a brain    → https://spaceduckling.com/the-inlet.html?duckling={duckling_id}')
    if not has_webhook:
        print(f'  2. Add a channel  → https://spaceduckling.com/hatch.html?duckling={duckling_id}')
        print('Until both are done, this duck cannot receive messages.')
    else:
        print('Channel is wired (OpenClaw webhook on file). Add a brain to start receiving.')
    return config


def pair(agent_name, webhook_url, tg_token='', tg_chat='', spawn_listener=False, workspace_dir=''):
    """One-shot interactive flow: start + poll + save in a single foreground run."""
    descriptor = _build_descriptor(agent_name)
    started = _start_pair(descriptor, webhook_url)
    # Persist pending state so a backgrounded run can be recovered with --confirm.
    _write_pending(started, descriptor, webhook_url, tg_token, tg_chat, workspace_dir=workspace_dir)
    _print_handshake(started, descriptor)
    bound = _poll_until_bound(started['code'])
    _clear_pending()
    return _finalise(bound, webhook_url, spawn_listener=spawn_listener,
                     tg_token=tg_token, tg_chat=tg_chat, workspace_dir=workspace_dir)


def cmd_start(agent_name, webhook_url, tg_token='', tg_chat='', workspace_dir=''):
    """Non-blocking start: POST /beak/pair/start, persist pending state, exit 0.

    Designed for agent callers that may background long-running processes —
    --start exits immediately with the 6-digit code on stdout (JSON), so the
    agent can surface it to the user without relying on a process whose
    stdout it may never read.
    """
    descriptor = _build_descriptor(agent_name)
    started = _start_pair(descriptor, webhook_url)
    pending = _write_pending(started, descriptor, webhook_url, tg_token, tg_chat, workspace_dir=workspace_dir)

    # Machine-readable on stdout so callers can parse deterministically.
    out = {
        'code': started['code'],
        'pair_url': started['pair_url'],
        'expires_in_seconds': pending['expires_in_seconds'],
        'expires_at': pending['expires_at'],
        'pending_path': str(PENDING_PATH),
        'next_step': 'After the user confirms in the browser, run: python3 pair.py --confirm',
    }
    print(json.dumps(out, indent=2))

    # Human hint on stderr so a person running this in a terminal still sees it.
    expires_min = max(1, pending['expires_in_seconds'] // 60)
    sys.stderr.write(
        f'\n🦆 Pair code {started["code"]}  ({started["pair_url"]})  '
        f'— expires in {expires_min} min. Run `pair.py --confirm` after browser confirm.\n\n'
    )


def cmd_confirm(spawn_listener=False):
    """Resume a previously started pair: poll until bound, save config."""
    pending = _read_pending()
    if time.time() > pending.get('expires_at', 0):
        print('❌ Pending pair has expired. Run: python3 pair.py --start')
        _clear_pending()
        sys.exit(1)
    bound = _poll_until_bound(pending['code'])
    _clear_pending()
    return _finalise(
        bound,
        pending.get('webhook_url') or '',
        spawn_listener=spawn_listener,
        tg_token=pending.get('forward_tg_token') or '',
        tg_chat=pending.get('forward_tg_chat') or '',
        workspace_dir=pending.get('workspace_dir') or '',
    )


def cmd_init():
    """Idempotent boot check: exit 0 if a valid config already exists.

    Brief v0.1.7 §5.3 — agents that re-enter pair.py on every session reset
    waste the user's time and burn pair codes. --init reads any persistent
    path and exits 0 silently when identity is already on disk. Skill
    install scripts (post_install hook) should call this before --start.

    Exit codes:
      0 → valid config found; agent is paired, no action needed
      1 → no config; caller should run pair.py --start
      2 → unexpected error
    """
    cfg_path, cfg = _existing_config()
    if cfg:
        sd = cfg.get('spaceduck_id', '')
        out = {
            'status': 'paired',
            'config_path': str(cfg_path),
            'spaceduck_id': sd,
            'duckling_id': cfg.get('duckling_id', ''),
            'agent_name': cfg.get('agent_name', ''),
        }
        print(json.dumps(out, indent=2))
        sys.stderr.write(f'\n✅ Already paired. Spaceduck ID: {sd}. No re-pairing required.\n\n')
        sys.exit(0)
    out = {'status': 'unpaired', 'next_step': 'python3 pair.py --start'}
    print(json.dumps(out, indent=2))
    sys.stderr.write('\nℹ️  No existing config found. Run: python3 pair.py --start\n\n')
    sys.exit(1)


def cmd_pulse():
    """Pulse using existing config — recovery for paired-but-dormant ducks.

    Reads ~/.space-duck/config.json and POSTs /beak/pulse so the directory
    flips this duck to ALIVE. Use when pairing succeeded but /ducks.html
    still shows "Connect your duck" (typical for ducks paired by an older
    pair.py that only pulsed when --webhook-url was supplied).
    """
    cfg_path, cfg = _existing_config()
    if not cfg:
        searched = ', '.join(str(p) for p in _config_paths())
        print(f'❌ No config found. Searched: {searched}. Run: python3 pair.py')
        sys.exit(1)
    sd = cfg.get('spaceduck_id', '')
    bk = cfg.get('beak_key', '')
    if not sd or not bk:
        print('❌ Config missing spaceduck_id or beak_key. Re-pair: python3 pair.py')
        sys.exit(1)
    ok, resp = _pulse(sd, bk, cfg.get('openclaw_webhook_url', ''))
    if ok:
        print(f'💓 Pulse OK — {sd[:10]}… is ALIVE')
    else:
        err = resp.get('error', 'unknown') if isinstance(resp, dict) else str(resp)
        print(f'❌ Pulse failed: {err}')
        sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Pair this agent with one of your ducks via browser confirm')
    parser.add_argument('--agent-name', default='', help='Friendly name for this agent (e.g. "claude on macbook-pro")')
    parser.add_argument('--webhook-url', default='', help='OpenClaw webhook URL for receiving pecks')
    parser.add_argument('--forward-tg-token', default='', help='Telegram bot token for the listener forward rail (writes ~/.space-duck/forward.json)')
    parser.add_argument('--forward-tg-chat', default='', help='Telegram chat_id to receive forwarded pecks (paired with --forward-tg-token)')
    parser.add_argument('--start', action='store_true', help='Start a pair handshake and exit 0 (non-blocking; outputs JSON on stdout)')
    parser.add_argument('--confirm', action='store_true', help='Resume a previously started pair: poll until bound, save config')
    parser.add_argument('--pulse', action='store_true', help='Send a presence pulse using existing config (recovery for paired-but-dormant ducks)')
    parser.add_argument('--init', action='store_true', help='Idempotent boot check: exit 0 if already paired, exit 1 if no config exists (call before --start in install hooks)')
    parser.add_argument('--telegram-listener', dest='telegram_listener',
                        action='store_true',
                        help=('0.3.8 — opt-in auto-spawn telegram_listener.py '
                              '--owner-approval after bind. Provides the MC '
                              'consent UX for BYOA ducks. Idempotent (no '
                              'double-spawn).'))
    parser.add_argument('--strict-consent', dest='strict_consent',
                        action='store_true',
                        help=('Forwarded to telegram_listener: require tap '
                              'for read-only actions too. Implies '
                              '--telegram-listener.'))
    parser.add_argument('--listener', dest='listener', action='store_true',
                        help=('Opt-in: also auto-spawn peck_listener.py --poll after bind. '
                              'OFF by default — _listener_already_running() only detects '
                              'PID-file listeners (poll mode), so users running a push-mode '
                              'listener under systemd/launchd would otherwise get '
                              'double-fanout to Telegram/Slack/email.'))
    parser.add_argument('--workspace-dir', dest='workspace_dir', default='',
                        help=('Absolute path to the agent\'s working directory. '
                              'Saved to config so sync.py defaults there instead of cwd. '
                              'Omit to use the directory you ran pair.py from.'))
    args = parser.parse_args()

    if sum(bool(x) for x in (args.start, args.confirm, args.pulse, args.init)) > 1:
        print('❌ --start, --confirm, --pulse, and --init are mutually exclusive.')
        sys.exit(2)
    spawn = args.listener
    # 0.3.8 — telegram listener auto-spawn. Decoupled from peck listener
    # (--listener) because they're separate processes serving separate
    # transports. --strict-consent implies --telegram-listener.
    tg_spawn = args.telegram_listener or args.strict_consent
    if args.init:
        cmd_init()
    elif args.pulse:
        cmd_pulse()
    elif args.start:
        cmd_start(args.agent_name, args.webhook_url,
                  args.forward_tg_token, args.forward_tg_chat,
                  workspace_dir=args.workspace_dir)
    elif args.confirm:
        cmd_confirm(spawn_listener=spawn)
    else:
        pair(args.agent_name, args.webhook_url,
             args.forward_tg_token, args.forward_tg_chat,
             spawn_listener=spawn, workspace_dir=args.workspace_dir)
    # Fire-and-forget after the pair command completes — does nothing if
    # already running (idempotent pid check). Strictly additive — does
    # not affect peck listener behavior.
    if tg_spawn:
        pid, msg = _spawn_tg_listener(strict_consent=args.strict_consent)
        if pid:
            print(f'🔔 telegram_listener.py --owner-approval {msg}')
        else:
            print(f'⚠ telegram_listener.py NOT started: {msg}')
            print(f'   You can run it manually: python3 '
                  f'{TG_LISTENER_SCRIPT} --owner-approval')
