#!/usr/bin/env python3
"""
Space Duck — Kick off a flock task (group chat with multiple ducks).

INTENT: Send one goal to many ducks at once. The backend creates a parent
        flock_task plus one peck_session per target and (for discussion mode)
        a shared thread.
CALLS:  POST <api>/beak/flock/task   — create a flock task
        GET  <api>/beak/flock/task   — read flock task state
AUTH:   X-Beak-Key header from ~/.space-duck/config.json (chmod 600).
        Internal kick-off pecks to each target are HMAC-signed by the server.

Modes:
  parallel    — all targets receive the goal at once, per-pair threads
  sequential  — first target starts, rest queued; next starts when prior ends
  discussion  — all targets share one thread (flock:FT-*) and can see each
                others' replies

Usage:
  # Parallel ask to three ducks
  python3 flock_task.py --goal "Review the PR" \\
      --targets duck_a,duck_b,duck_c --mode parallel --max-rounds 3

  # Discussion (round table)
  python3 flock_task.py --goal "Brainstorm Q2 themes" \\
      --targets duck_a,duck_b,duck_c --mode discussion

  # Inspect a flock
  python3 flock_task.py --show FT-abc123
"""
import argparse, json, sys, urllib.error, urllib.parse, urllib.request
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'

def load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run setup.py first.')
        sys.exit(1)
    return json.loads(CONFIG_PATH.read_text())

def _headers(cfg, extra=None):
    h = {'Content-Type': 'application/json',
         'X-Beak-Key': cfg.get('beak_key', '')}
    sdid = cfg.get('spaceduck_id')
    if sdid:
        h['X-Spaceduck-ID'] = sdid
    if extra:
        h.update(extra)
    return h

def _http_err(e):
    body = e.read().decode()
    print(f'ERROR: HTTP {e.code} — {body}')
    sys.exit(1)

def create_flock(cfg, goal, targets, mode='parallel', max_rounds=3):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    payload = {
        'spaceduck_id': cfg.get('spaceduck_id', ''),
        'beak_key':     cfg.get('beak_key', ''),
        'goal':         goal,
        'targets':      targets,
        'mode':         mode,
        'max_rounds':   max_rounds,
    }
    req = urllib.request.Request(
        f'{api}/beak/flock/task',
        data=json.dumps(payload).encode(),
        headers=_headers(cfg),
        method='POST',
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        _http_err(e)
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)

    ft = data.get('flock_task_id', '?')
    print(f'🦆🦆 Flock task created: {ft}')
    print(f'   Mode: {data.get("mode", mode)}')
    print(f'   Goal: {goal}')
    print(f'   Max rounds: {data.get("max_rounds", max_rounds)}')

    kicked = data.get('kicked', [])
    queued = data.get('queued', [])
    if kicked:
        print(f'   ✅ Kicked ({len(kicked)}):')
        for k in kicked:
            print(f'      • {k.get("target", "?")}  →  session {k.get("session_id", "?")}'
                  f'  [{k.get("status", "?")}]')
    if queued:
        print(f'   ⏳ Queued ({len(queued)}):')
        for q in queued:
            print(f'      • {q.get("target", "?")}  [{q.get("status", "QUEUED")}]')

    print()
    print(f'  → Inspect: python3 flock_task.py --show {ft}')
    return data

def show_flock(cfg, flock_task_id):
    api = cfg.get('api_base', 'https://beak.spaceduckling.com')
    qs  = urllib.parse.urlencode({'flock_task_id': flock_task_id})
    req = urllib.request.Request(f'{api}/beak/flock/task?{qs}', method='GET',
                                 headers=_headers(cfg))
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        _http_err(e)
    except Exception as e:
        print(f'ERROR: {e}')
        sys.exit(1)

    parent   = data.get('parent', {})
    children = data.get('children', [])
    print(f'🦆🦆 Flock {parent.get("session_id", flock_task_id)}')
    print(f'   Status:    {parent.get("status", "?")}')
    print(f'   Mode:      {parent.get("flock_mode", "?")}')
    print(f'   Initiator: {parent.get("initiator", "?")}')
    if parent.get('goal'):
        print(f'   Goal:      {parent["goal"]}')
    print(f'   Children:  {parent.get("flock_child_count", len(children))}')
    print()
    if children:
        print('   Sessions:')
        for c in children:
            print(f'     • {c.get("target", "?"):24s}  '
                  f'session {c.get("session_id", "?")}  '
                  f'[{c.get("status", "?")}]  '
                  f'round {c.get("current_round", 0)}')
    return data

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Kick off a flock (group chat) task')
    p.add_argument('--goal', help='What you want the flock to do')
    p.add_argument('--targets',
                   help='Comma-separated spaceduck IDs (e.g. duck_a,duck_b)')
    p.add_argument('--mode', default='parallel',
                   choices=['parallel', 'sequential', 'discussion'])
    p.add_argument('--max-rounds', type=int, default=3, help='1–100, default 3')
    p.add_argument('--show', metavar='FT_ID', help='Inspect a flock task by id')
    args = p.parse_args()

    cfg = load_config()

    if args.show:
        show_flock(cfg, args.show); sys.exit(0)

    if not args.goal or not args.targets:
        p.error('--goal and --targets are required (unless --show)')

    targets = [t.strip() for t in args.targets.split(',') if t.strip()]
    if not targets:
        p.error('--targets must contain at least one spaceduck_id')
    create_flock(cfg, args.goal, targets, mode=args.mode,
                 max_rounds=args.max_rounds)
