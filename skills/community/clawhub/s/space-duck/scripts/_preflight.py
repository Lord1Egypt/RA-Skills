#!/usr/bin/env python3
"""
Space Duck — pre-flight permission cache + check shared by send_peck.py and chat.py.

INTENT: Before any outbound peck, fetch the per-connection effective permissions
        and decide what to drop (attached files not in shared_files), whether the
        peer is muted, and whether topic/keyword filters apply. Returns a struct
        the caller acts on, plus user-visible warnings.

CALLS:  GET  <api>/beak/skill/permissions  (bulk; cached 60 min)
        POST <api>/beak/connection/permissions  (per-target live, fallback)
AUTH:   X-Beak-Key from ~/.space-duck/config.json.

Cache:  ~/.space-duck/permissions-cache.json   {fetched_at, defaults, by_target}
"""
import json, time, urllib.request, urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
CACHE_PATH  = Path.home() / '.space-duck' / 'permissions-cache.json'
CACHE_TTL   = 3600  # 60 min


def _load_config():
    if not CONFIG_PATH.exists():
        return {}
    try: return json.loads(CONFIG_PATH.read_text())
    except Exception: return {}


def _http_get(url, beak_key):
    req = urllib.request.Request(url, headers={'X-Beak-Key': beak_key, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read() or b'{}')


def _http_post(url, beak_key, body):
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method='POST',
        headers={'X-Beak-Key': beak_key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read() or b'{}')


def refresh_cache(cfg=None):
    """Pull bulk permissions and rewrite the cache file. Returns the cache dict."""
    cfg = cfg or _load_config()
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    bk  = cfg.get('beak_key', '')
    if not bk: return None
    try:
        data = _http_get(f'{api}/beak/skill/permissions', bk)
    except Exception:
        return None
    by_target = {}
    for c in data.get('connections', []) or []:
        tid = c.get('target_spaceduck_id') or c.get('spaceduck_id')
        if tid:
            by_target[tid] = c.get('permissions', {})
    cache = {
        'fetched_at': int(time.time()),
        'defaults':   data.get('defaults', {}),
        'by_target':  by_target,
    }
    try:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps(cache, indent=2))
    except Exception: pass
    return cache


def _load_cache():
    if not CACHE_PATH.exists(): return None
    try:
        c = json.loads(CACHE_PATH.read_text())
        if (int(time.time()) - int(c.get('fetched_at', 0))) > CACHE_TTL:
            return None
        return c
    except Exception:
        return None


def get_effective(target_id, cfg=None):
    """Return effective permissions dict for one target. Cache-first, live fallback."""
    cfg = cfg or _load_config()
    cache = _load_cache() or refresh_cache(cfg)
    if cache:
        merged = dict(cache.get('defaults') or {})
        merged.update(cache.get('by_target', {}).get(target_id) or {})
        if merged: return merged
    # Live fallback
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    bk  = cfg.get('beak_key', '')
    try:
        body = {'spaceduck_id': cfg.get('spaceduck_id', ''), 'target_id': target_id}
        d = _http_post(f'{api}/beak/connection/permissions', bk, body)
        return d.get('permissions') or {}
    except Exception:
        return {}


def preflight(target_id, attached_files=None, topic=None, text=None, cfg=None):
    """
    Pre-flight check before sending a peck.

    Returns: dict { allowed: bool, reason: str, allowed_files: [str],
                    dropped_files: [str], warnings: [str], perms: dict }
    """
    perms = get_effective(target_id, cfg)
    attached_files = list(attached_files or [])
    warnings = []
    out = {'allowed': True, 'reason': '', 'allowed_files': [],
           'dropped_files': [], 'warnings': warnings, 'perms': perms}

    # Mute (server-enforced too; here so we don't waste a call)
    if int(perms.get('muted_until') or 0) > int(time.time()):
        out['allowed'] = False
        out['reason'] = 'muted'
        warnings.append(f'Connection muted until {perms["muted_until"]} (epoch).')
        return out

    # File whitelist / blocklist
    shared = set(perms.get('shared_files') or [])
    never  = set(perms.get('never_share') or [])
    for f in attached_files:
        if f in never:
            out['dropped_files'].append(f)
            warnings.append(f'{f} is in never_share — dropped.')
        elif shared and f not in shared:
            out['dropped_files'].append(f)
            warnings.append(f'{f} not in shared_files for this peer — dropped.')
        else:
            out['allowed_files'].append(f)

    # Topic gates
    if topic:
        allowed = perms.get('allowed_topics') or []
        blocked = perms.get('blocked_topics') or []
        if blocked and topic in blocked:
            out['allowed'] = False
            out['reason'] = f'topic_blocked:{topic}'
            warnings.append(f'Topic "{topic}" is blocked for this peer.')
            return out
        if allowed and topic not in allowed:
            out['allowed'] = False
            out['reason'] = f'topic_not_allowed:{topic}'
            warnings.append(f'Topic "{topic}" not in allowed_topics for this peer.')
            return out

    # Stop keywords
    if text:
        stops = perms.get('stop_keywords') or []
        lt = text.lower()
        hit = [w for w in stops if w and w.lower() in lt]
        if hit:
            out['allowed'] = False
            out['reason'] = f'stop_keyword:{hit[0]}'
            warnings.append(f'Stop keyword matched: {hit[0]}')
            return out

    return out


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: _preflight.py <target_id> [file1 file2 ...]'); sys.exit(1)
    res = preflight(sys.argv[1], attached_files=sys.argv[2:])
    print(json.dumps(res, indent=2))
