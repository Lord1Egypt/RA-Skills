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
import json, urllib.request, urllib.error, sys, datetime
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

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
    liveness_ok = False
    last_seen_ts = None
    try:
        req2 = urllib.request.Request(
            f"{api}/beak/spaceducks?duckling_id={did}",
            headers={'Accept': 'application/json', 'X-Beak-Key': bk}
        )
        with urllib.request.urlopen(req2, timeout=10) as r2:
            sd_data = json.loads(r2.read())
            spaceducks = sd_data.get('spaceducks', [])
            # Find own entry for last_seen
            for sd in spaceducks:
                if sd.get('spaceduck_id') == sdid:
                    ts = sd.get('last_seen')
                    if ts:
                        last_seen_ts = int(ts)
    except Exception:
        pass

    # Liveness comes from trust_tier T2+ (T2 requires liveness)
    tier = status_data.get('trust_tier', '')
    liveness_ok = tier in ('T2', 'T3', 'T4')

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

    # ── 5. Print ─────────────────────────────────────────────────────────────
    print('🦆 Space Duck Status')
    print(f"   Agent:       {cfg.get('agent_name','?')}  ({sdid or '?'})")
    print(f"   Duckling:    {did}")
    print(f"   Trust tier:  {tier or '?'}")
    print(f"   Cert status: {status_data.get('cert_status','?')}")
    print(f"   Plan:        {status_data.get('plan','?')}")
    print(f"   Liveness:    {'✅ verified' if liveness_ok else '⚠️  not verified'}")
    print(f"   Owned agents: {len(owned)}  |  Bonded agents: {len(bonded)}")
    print(f"   Last pulse:  {last_pulse_str}")

    return status_data

if __name__ == '__main__':
    cfg = load_config()
    get_status(cfg)
