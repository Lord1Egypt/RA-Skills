#!/usr/bin/env python3
"""
Space Duck — Send a pulse (heartbeat) so this agent stays marked ACTIVE.

INTENT: One-shot heartbeat so Mission Control + the Pond know the duck is
        alive AND what it can actually do (auto-reply, owner-approval,
        workspace-bridge, etc).

v0.4.7 (2026-06-16) — Now declares `listener_capabilities`, probed live
from the local box state. Closes the diagnostic gap "delivery_state=pushed
but target never replies" by letting senders + MC know the target's
actual posture before assuming a response will come.

CALLS:  POST <api>/beak/pulse — Space Duck's own backend only.
AUTH:   Beak Key from ~/.space-duck/config.json over HTTPS.

Usage: python3 pulse.py
"""
import json, urllib.request, urllib.error, time, sys, os, subprocess, shutil
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
API_BASE = 'https://beak.spaceduckling.com'


def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())


def probe_capabilities():
    """v0.4.7 — Inspect the local box to determine what this duck can do.

    The truth here is what's RUNNING + what's REACHABLE — not what's
    documented. Pulse declares observed reality so MC + senders + doctor
    can all agree on posture.
    """
    caps = ['receive_peck', 'inbox_polling']  # baseline — anyone running this script

    # Check for telegram_listener.py running (= owner-approval marker path live)
    try:
        out = subprocess.run(['pgrep', '-fa', 'telegram_listener.py'],
                             capture_output=True, text=True, timeout=3)
        if out.returncode == 0 and 'telegram_listener.py' in out.stdout:
            caps.append('tg_forward_hmac')
            if '--owner-approval' in out.stdout:
                caps.append('owner_approval_marker')
    except Exception:
        pass

    # Check for peck_listener.py running with --on-peck (= auto-reply wired)
    try:
        out = subprocess.run(['pgrep', '-fa', 'peck_listener.py'],
                             capture_output=True, text=True, timeout=3)
        if out.returncode == 0 and 'peck_listener.py' in out.stdout:
            for line in out.stdout.splitlines():
                if '--on-peck' in line and 'peck_responder.py' in line:
                    caps.append('auto_respond_peck')
                    break
    except Exception:
        pass

    # Check for workspace_bridge.py running (= file sync live)
    try:
        out = subprocess.run(['pgrep', '-fa', 'workspace_bridge.py'],
                             capture_output=True, text=True, timeout=3)
        if out.returncode == 0 and 'workspace_bridge.py' in out.stdout:
            caps.append('workspace_bridge_sync')
    except Exception:
        pass

    # Check for claude CLI on PATH (= brain runtime available for auto-reply)
    if shutil.which('claude'):
        caps.append('claude_cli_available')

    # Dedup + sort
    return sorted(set(caps))


def check_byob_health(cfg):
    """Best-effort BYOB binding health surface. The server flips a binding
    VERIFIED→DEGRADED after 3 consecutive forward failures but never
    auto-revokes, so a dead tunnel can sit as a silent zombie. Pulse is the
    regular heartbeat — warn here so the owner notices. Never fails pulse."""
    sd = cfg.get('spaceduck_id', '')
    if not sd:
        return
    try:
        import urllib.parse
        url = (f"{API_BASE}/beak/agent/byob-status"
               f"?spaceduck_id={urllib.parse.quote(sd)}")
        req = urllib.request.Request(
            url, method='GET',
            headers={'x-beak-key': cfg.get('beak_key', '')})
        with urllib.request.urlopen(req, timeout=8) as r:
            d = json.loads(r.read())
    except Exception:
        return  # binding endpoint unavailable / not bound — stay quiet
    state = str(d.get('binding_state', d.get('state', ''))).upper()
    fails = d.get('failure_count', d.get('byob_failure_count', 0))
    if state == 'DEGRADED':
        print(f"[pulse] ⚠️  BYOB binding DEGRADED ({fails} consecutive "
              f"forward failures). Telegram forwards are not landing — check "
              f"your tunnel/listener, then re-bind: "
              f"bind_telegram.py --forward-url <URL>  "
              f"(or clear it: bind_telegram.py --revoke)")
    elif state == 'BINDING':
        print(f"[pulse] ⚠️  BYOB binding stuck in BINDING — verify handshake "
              f"never completed. Re-run bind_telegram.py to finish or revoke.")


def send_pulse(cfg):
    capabilities = probe_capabilities()
    payload = json.dumps({
        'spaceduck_id': cfg['spaceduck_id'],
        'beak_key': cfg['beak_key'],
        'status': 'ACTIVE',
        'timestamp': int(time.time()),
        # v0.4.7 — declare what we can do, so MC + senders know.
        'listener_capabilities': capabilities,
    }).encode()
    req = urllib.request.Request(
        f"{API_BASE}/beak/pulse",
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            recorded = ' caps✓' if data.get('capabilities_recorded') else ''
            print(f"[pulse] ✅ OK — {data.get('message','sent')} "
                  f"({data.get('trust_tier','?')}){recorded}")
            print(f"[pulse] capabilities declared: {', '.join(capabilities)}")
            return data
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"[pulse] ❌ HTTP {e.code}: {body}")
        return None
    except Exception as e:
        print(f"[pulse] ❌ Error: {e}")
        return None


if __name__ == '__main__':
    cfg = load_config()
    send_pulse(cfg)
    check_byob_health(cfg)
