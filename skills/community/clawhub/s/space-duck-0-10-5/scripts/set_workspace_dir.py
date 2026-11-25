#!/usr/bin/env python3
"""
Space Duck — Set the bridge's per-duck workspace_dir.

0.3.10 — addresses Wayne's case (msg 22261): the bridge picked
/data/.openclaw/workspace (shared workspace) because nothing told it
about the per-duck directory. This writes
~/.openclaw/credentials/clawhub-gateway.json's
`spaceduck.workspace_dir` field so the bridge's discovery chain
(precedence #3) picks up the right dir on next start.

Usage:
  # Inspect current setting
  python3 set_workspace_dir.py --show

  # Set explicit dir
  python3 set_workspace_dir.py --dir /data/.openclaw/agents/waynecollins_bot

  # Reset (back to auto-discovery)
  python3 set_workspace_dir.py --unset
"""
import argparse
import json
import os
import sys
from pathlib import Path

GATEWAY = Path.home() / '.openclaw' / 'credentials' / 'clawhub-gateway.json'


def _load():
    if not GATEWAY.exists():
        return {}
    try:
        return json.loads(GATEWAY.read_text())
    except Exception as e:
        sys.exit(f'error: gateway config unreadable: {e}')


def _save(d):
    GATEWAY.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    tmp = GATEWAY.with_suffix('.tmp')
    tmp.write_text(json.dumps(d, indent=2))
    os.chmod(tmp, 0o600)
    os.replace(str(tmp), str(GATEWAY))


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    p.add_argument('--show', action='store_true')
    p.add_argument('--dir', help='absolute path to per-duck workspace')
    p.add_argument('--unset', action='store_true',
                   help='Remove workspace_dir (re-enable discovery chain)')
    args = p.parse_args(argv)

    d = _load()
    sd = d.get('spaceduck', {}) if isinstance(d.get('spaceduck'), dict) else {}
    if args.show or not (args.dir or args.unset):
        cur = sd.get('workspace_dir', '(not set — bridge uses discovery)')
        print(f'current workspace_dir: {cur}')
        return 0

    if args.unset:
        sd.pop('workspace_dir', None)
        d['spaceduck'] = sd
        _save(d)
        print('✓ workspace_dir removed — restart bridge to pick up the change')
        return 0

    target = Path(args.dir).expanduser().resolve()
    if not target.exists():
        sys.exit(f'error: {target} does not exist. Create it first.')
    if not target.is_dir():
        sys.exit(f'error: {target} is not a directory.')
    sd['workspace_dir'] = str(target)
    d['spaceduck'] = sd
    _save(d)
    print(f'✓ workspace_dir set to {target}')
    print('  Restart bridge: pkill -f workspace_bridge.py; '
          '(your supervisor/cron/launchd restarts it automatically)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
