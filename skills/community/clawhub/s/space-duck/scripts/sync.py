#!/usr/bin/env python3
"""
Space Duck — Sync MD files between this BYOB agent and the platform.

INTENT: Two-way sync for the duck's per-spaceduck MD files (MEMORY.md, SOUL.md,
HEARTBEAT.md, plus any user-created markdown). The agent reads/writes locally;
this script reconciles with the platform copy so Mission Control sees fresh
content and your edits in MC land back here on the next pull.

CALLS:  GET  <api>/beak/skill/files
        POST <api>/beak/skill/file   { filename, action: read|write|delete, ... }
AUTH:   Beak Key from ~/.space-duck/config.json (X-Beak-Key header).

Local layout: ~/.space-duck/workspace/<filename>
A snapshot of the platform-side ETag is stored in ~/.space-duck/sync-state.json
so subsequent pushes can pass if_match for safe overwrite.

Usage:
  python3 sync.py pull           # platform → local (overwrites local; backs up first)
  python3 sync.py push           # local → platform (uses if_match; prompts on conflict)
  python3 sync.py status         # show diffs (local vs platform)
  python3 sync.py pull --force   # ignore local edits since last sync
"""
import json, os, sys, time, hashlib, urllib.request, urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
STATE_PATH  = Path.home() / '.space-duck' / 'sync-state.json'
BACKUP_DIR  = Path.home() / '.space-duck' / 'workspace-backups'


def resolve_workspace_dir(cfg, argv):
    """Order of precedence: --dir flag > config.workspace_dir > $SPACE_DUCK_WORKSPACE > cwd."""
    for i, a in enumerate(argv):
        if a == '--dir' and i + 1 < len(argv):
            return Path(argv[i + 1]).expanduser().resolve()
        if a.startswith('--dir='):
            return Path(a.split('=', 1)[1]).expanduser().resolve()
    if cfg.get('workspace_dir'):
        return Path(cfg['workspace_dir']).expanduser().resolve()
    env = os.environ.get('SPACE_DUCK_WORKSPACE')
    if env:
        return Path(env).expanduser().resolve()
    return Path.cwd().resolve()


def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: ~/.space-duck/config.json missing. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())


def load_state():
    if STATE_PATH.exists():
        try: return json.loads(STATE_PATH.read_text())
        except Exception: pass
    return {'files': {}}


def save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def http(method, url, beak_key, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={'X-Beak-Key': beak_key, 'Content-Type': 'application/json', 'Accept': 'application/json'},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status, json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        try: payload = json.loads(e.read() or b'{}')
        except Exception: payload = {'error': str(e)}
        return e.code, payload
    except Exception as e:
        return 0, {'error': str(e)}


def local_etag(text):
    # S3 single-part ETag = md5(content) hex. Matches what the platform stores.
    return hashlib.md5(text.encode('utf-8')).hexdigest()


def backup_local(name, text):
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime('%Y%m%d_%H%M%S', time.gmtime())
    (BACKUP_DIR / f'{name}.{ts}').write_text(text)


def cmd_pull(cfg, ws_dir, force=False):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    bk  = cfg.get('beak_key', '')
    print(f'workspace_dir = {ws_dir}')
    status, listing = http('GET', f'{api}/beak/skill/files', bk)
    if status != 200:
        print(f'ERROR: list failed ({status}): {listing}'); sys.exit(2)
    files = listing.get('files', [])
    state = load_state()
    ws_dir.mkdir(parents=True, exist_ok=True)
    pulled, skipped, conflicts = 0, 0, 0
    for f in files:
        name = f['name']
        local = ws_dir / name
        if local.exists() and not force:
            local_text = local.read_text()
            last_known = state['files'].get(name, {}).get('etag', '')
            if local_etag(local_text) != last_known and last_known:
                print(f'⚠ {name}: local edited since last sync — backup + overwrite (use --force to skip warn)')
                backup_local(name, local_text)
                conflicts += 1
        s2, payload = http('POST', f'{api}/beak/skill/file', bk, {'filename': name, 'action': 'read'})
        if s2 != 200:
            print(f'  skip {name} ({s2})'); skipped += 1; continue
        content = payload.get('content', '')
        etag = payload.get('etag', '')
        local.write_text(content)
        state['files'][name] = {'etag': etag, 'synced_at': int(time.time())}
        pulled += 1
        print(f'  ↓ {name} ({len(content)}B)')
    save_state(state)
    print(f'\npulled {pulled} · skipped {skipped} · conflicts backed up {conflicts}')
    # 2026-05-17 — also refresh the permissions cache so send_peck/chat preflight
    # has fresh data without an extra round-trip.
    try:
        from _preflight import refresh_cache
        c = refresh_cache(cfg)
        if c:
            print(f'  permissions cache refreshed ({len(c.get("by_target", {}))} peer overrides)')
    except Exception as e:
        print(f'  permissions cache refresh skipped: {e}')


def cmd_push(cfg, ws_dir):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    bk  = cfg.get('beak_key', '')
    state = load_state()
    print(f'workspace_dir = {ws_dir}')
    if not ws_dir.exists():
        print('No local workspace yet. Run `sync pull` first or point --dir at the agent dir.'); return
    pushed, skipped = 0, 0
    for path in sorted(ws_dir.iterdir()):
        if not path.is_file() or path.name.startswith('.'): continue
        if not (path.name.endswith('.md') or path.name.endswith('.txt')): continue
        name = path.name
        text = path.read_text()
        if_match = state['files'].get(name, {}).get('etag', '')
        s, payload = http('POST', f'{api}/beak/skill/file', bk, {
            'filename': name, 'action': 'write', 'content': text, 'if_match': if_match,
        })
        if s == 409:
            ans = input(f'⚠ {name}: platform copy changed since last pull. (o)verwrite / (s)kip ? ').strip().lower()
            if ans != 'o':
                print(f'  skip {name}'); skipped += 1; continue
            s, payload = http('POST', f'{api}/beak/skill/file', bk, {
                'filename': name, 'action': 'write', 'content': text,
            })
        if s != 200:
            print(f'  fail {name} ({s}): {payload}'); skipped += 1; continue
        state['files'][name] = {'etag': payload.get('etag', ''), 'synced_at': int(time.time())}
        pushed += 1
        print(f'  ↑ {name} ({len(text)}B)')
    save_state(state)
    print(f'\npushed {pushed} · skipped {skipped}')


def cmd_status(cfg, ws_dir):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    bk  = cfg.get('beak_key', '')
    state = load_state()
    print(f'workspace_dir = {ws_dir}')
    status, listing = http('GET', f'{api}/beak/skill/files', bk)
    if status != 200:
        print(f'ERROR: list failed ({status})'); return
    remote = {f['name']: f for f in listing.get('files', [])}
    local_names = set()
    if ws_dir.exists():
        for p in ws_dir.iterdir():
            if p.is_file() and not p.name.startswith('.') and (p.name.endswith('.md') or p.name.endswith('.txt')):
                local_names.add(p.name)
    all_names = sorted(set(remote) | local_names)
    for name in all_names:
        l = name in local_names
        r = name in remote
        last_etag = state['files'].get(name, {}).get('etag', '')
        if l and r:
            local_text = (ws_dir / name).read_text()
            local_e = local_etag(local_text)
            remote_e = remote[name].get('etag', '')
            if local_e == remote_e: tag = '=  in sync'
            elif local_e == last_etag: tag = '↓ remote ahead (pull)'
            elif remote_e == last_etag: tag = '↑ local ahead (push)'
            else: tag = '⚠ diverged (manual review)'
        elif l: tag = '↑ local only (push)'
        else:   tag = '↓ remote only (pull)'
        print(f'  {tag:<26} {name}')


def cmd_history(cfg, filename):
    """List prior versions of <filename> (skill-side, X-Beak-Key auth)."""
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    bk  = cfg.get('beak_key', '')
    status, payload = http('POST', f'{api}/beak/skill/file/history', bk, {'filename': filename})
    if status != 200:
        print(f'ERROR: history failed ({status}): {payload}'); sys.exit(2)
    versions = payload.get('history', [])
    if not versions:
        print(f'no prior versions for {filename} (every overwrite snapshots one)'); return
    print(f'{len(versions)} prior version(s) for {filename}:')
    for v in versions:
        ts = v['ts']
        pretty = f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}:{ts[13:15]} UTC" if len(ts) >= 15 else ts
        sz = v['size']
        sz_h = f'{sz}B' if sz < 1024 else f'{sz/1024:.1f}KB'
        print(f'  {ts}  {pretty}  {sz_h}')
    print('\nrestore one with:  python3 sync.py restore <filename> <ts>')


def cmd_restore(cfg, filename, history_ts):
    """Restore <filename> from its <history_ts> snapshot. Current version is snapshotted first."""
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    bk  = cfg.get('beak_key', '')
    status, payload = http('POST', f'{api}/beak/skill/file/restore', bk,
                           {'filename': filename, 'history_ts': history_ts})
    if status != 200:
        print(f'ERROR: restore failed ({status}): {payload}'); sys.exit(2)
    print(f'restored {payload.get("restored", filename)} from {payload.get("from_ts","?")} '
          f'({payload.get("size",0)}B). Current version was snapshotted first.')


def main():
    args = sys.argv[1:]
    if not args or args[0] in ('-h', '--help'):
        print(__doc__); return
    cmd = args[0]
    cfg = load_config()
    ws_dir = resolve_workspace_dir(cfg, args)
    if cmd == 'pull':   cmd_pull(cfg, ws_dir, force=('--force' in args))
    elif cmd == 'push': cmd_push(cfg, ws_dir)
    elif cmd == 'status': cmd_status(cfg, ws_dir)
    elif cmd == 'history':
        if len(args) < 2: print('Usage: sync.py history <filename>'); sys.exit(1)
        cmd_history(cfg, args[1])
    elif cmd == 'restore':
        if len(args) < 3: print('Usage: sync.py restore <filename> <history_ts>'); sys.exit(1)
        cmd_restore(cfg, args[1], args[2])
    else:
        print(f'Unknown command: {cmd}'); print(__doc__); sys.exit(1)


if __name__ == '__main__':
    main()
