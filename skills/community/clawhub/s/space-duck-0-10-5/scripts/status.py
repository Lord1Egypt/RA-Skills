#!/usr/bin/env python3
"""
Space Duck — Show this agent's live status on the network.

INTENT: Fetch trust tier, cert status, agent counts, and last-pulse time.
CALLS:  GET <api>/beak/status?duckling_id=...
        GET <api>/beak/spaceducks?duckling_id=...
        Space Duck's own backend only — no third-party hosts.
AUTH:   Beak Key from ~/.space-duck/config.json, sent as X-Beak-Key
        header to the Space Duck backend.

Usage: python3 status.py
"""
import json, urllib.request, urllib.error, sys, datetime, time
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    cfg = json.loads(CONFIG_PATH.read_text())
    from _apiguard import check_api_base  # [HARDEN-071]
    check_api_base(cfg)
    return cfg

def get_status(cfg):
    api   = cfg.get('api_base', 'https://beak.spaceduckling.com')
    did   = cfg.get('duckling_id', '')
    bk    = cfg.get('beak_key', '')
    sdid  = cfg.get('spaceduck_id', '')

    # ── 1. Core duckling status ──────────────────────────────────────────────
    status_data = {}
    try:
        req = urllib.request.Request(
            f"{api}/beak/status?duckling_id={did}",
            headers={'Accept': 'application/json', 'X-Beak-Key': bk}
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            status_data = json.loads(r.read())
    except Exception as e:
        print(f"  ⚠️  Status endpoint failed: {e}")

    # ── 2. Spaceducks list (agent count + liveness) ──────────────────────────
    spaceducks  = []
    identity_ok = False
    last_seen_ts = None
    try:
        req2 = urllib.request.Request(
            f"{api}/beak/spaceducks?duckling_id={did}",
            headers={'Accept': 'application/json', 'X-Beak-Key': bk}
        )
        with urllib.request.urlopen(req2, timeout=10) as r2:
            sd_data = json.loads(r2.read())
            spaceducks = sd_data.get('agents', sd_data.get('spaceducks', []))
            # Find own entry for last_seen (fallback only — this list is the
            # bond graph, so a solo duck never appears in it and last_seen stays
            # unset. Authoritative read is the identity-scoped call below.)
            for sd in spaceducks:
                if sd.get('spaceduck_id') == sdid:
                    ts = sd.get('last_seen')
                    if ts:
                        last_seen_ts = int(ts)
    except Exception:
        pass

    # ── 2b. Authoritative last_seen (identity-scoped) ─────────────────────────
    # PULSE-01: /beak/pulse persists last_seen on the duck's OWN spaceducks row,
    # but /beak/spaceducks lists only bonded ducks — a solo duck is never in it,
    # so it read "Last pulse: —" forever. Read our own row directly instead.
    if sdid:
        try:
            reqc = urllib.request.Request(
                f"{api}/beak/duck/{sdid}/capabilities",
                headers={'Accept': 'application/json'}
            )
            with urllib.request.urlopen(reqc, timeout=10) as rc:
                cap_data = json.loads(rc.read())
                ts = cap_data.get('last_seen')
                if ts:
                    last_seen_ts = int(ts)
        except Exception:
            pass

    # Identity/KYC liveness check (T2 requires face-verification liveness) —
    # this is the identity gate, NOT the runtime-pulse liveness printed below.
    tier = status_data.get('trust_tier', '')
    identity_ok = tier in ('T2', 'T3', 'T4')

    # ── 3. Agent counts ──────────────────────────────────────────────────────
    owned   = [s for s in spaceducks if s.get('relationship') == 'OWNER']
    bonded  = [s for s in spaceducks if s.get('relationship') == 'BOND']

    # ── 4. Last pulse ────────────────────────────────────────────────────────
    last_pulse_str = '—'
    if last_seen_ts:
        try:
            dt = datetime.datetime.fromtimestamp(last_seen_ts, datetime.UTC)
            last_pulse_str = dt.strftime('%d %b %Y %H:%M UTC')
        except Exception:
            last_pulse_str = str(last_seen_ts)
    if last_seen_ts:
        _delta = int(time.time()) - last_seen_ts
        if _delta < 600:
            runtime_str = '🟢 live'
        elif _delta < 1800:
            runtime_str = '🟡 stale'
        else:
            runtime_str = '🔴 offline'
    else:
        runtime_str = '⚪ no pulse yet'

    # ── 5. Print ─────────────────────────────────────────────────────────────
    print('🦆 Space Duck Status')
    print(f"   Agent:       {cfg.get('agent_name','?')}  ({sdid or '?'})")
    print(f"   Duckling:    {did}")
    print(f"   Trust tier:  {tier or '?'}")
    print(f"   Cert status: {status_data.get('cert_status','?')}")
    print(f"   Plan:        {status_data.get('plan','?')}")
    print(f"   Identity:    {'✅ verified' if identity_ok else '⚠️  not verified'}")
    print(f"   Owned agents: {len(owned)}  |  Bonded agents: {len(bonded)}")
    print(f"   Runtime:     {runtime_str}")
    print(f"   Last pulse:  {last_pulse_str}")

    return status_data

if __name__ == '__main__':
    cfg = load_config()
    get_status(cfg)
