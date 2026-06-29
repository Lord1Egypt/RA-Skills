#!/usr/bin/env python3
import json, os, time, statistics
from collections import defaultdict
from pathlib import Path
EVENTS = Path(os.environ.get('SAGE_ROUTER_ROUTE_EVENTS_PATH', '~/.cache/sage-router/route-events.jsonl')).expanduser()
STATS = Path(os.environ.get('SAGE_ROUTER_LATENCY_STATS_PATH', '~/.cache/sage-router/latency-stats.json')).expanduser()
MAX_AGE_HOURS = float(os.environ.get('SAGE_ROUTER_ANALYSIS_HOURS', '24'))
cutoff = time.time() - (MAX_AGE_HOURS * 3600)
rows = []
if EVENTS.exists():
    for line in EVENTS.read_text(errors='replace').splitlines():
        if not line.strip():
            continue
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get('ts', 0) < cutoff:
            continue
        sel = ev.get('selected') or {}
        key = f"{sel.get('provider')}/{sel.get('model')}" if sel else 'NONE'
        rows.append({'intent': ev.get('intent', 'UNKNOWN'), 'model': key, 'status': ev.get('status'), 'ms': float(ev.get('totalElapsedMs') or 0), 'tokens': int(ev.get('estimatedTokens') or 0)})
summary = defaultdict(list)
for r in rows:
    summary[(r['intent'], r['model'])].append(r)
print(f'Sage Router route analysis, last {MAX_AGE_HOURS:g}h')
print(f'events={len(rows)} source={EVENTS}')
if not rows:
    print('No structured route events yet. Falling back to latency stats only.')
for intent in sorted({r['intent'] for r in rows}):
    print(f'\n[{intent}]')
    items = []
    for (i, model), vals in summary.items():
        if i != intent:
            continue
        ok = sum(1 for v in vals if v['status'] == 'ok')
        total = len(vals)
        lat = [v['ms'] for v in vals if v['ms']]
        avg = statistics.mean(lat) if lat else 0
        p50 = statistics.median(lat) if lat else 0
        items.append((-(ok/max(total,1)), avg, -ok, total, model, p50))
    for _, avg, neg_ok, total, model, p50 in sorted(items)[:10]:
        print(f'- {model}: ok={-neg_ok}/{total}, avg={avg:.0f}ms, p50={p50:.0f}ms')
if STATS.exists():
    data = json.loads(STATS.read_text())
    print('\nLatency-stat leaders by intent, minimum 3 successes:')
    for intent, providers in sorted((data.get('intents') or {}).items()):
        leaders = []
        for provider, models in providers.items():
            for model, st in models.items():
                succ = int(st.get('successes') or 0)
                fail = int(st.get('failures') or 0)
                if succ < 3:
                    continue
                rate = succ / max(1, succ + fail)
                lat = float(st.get('latency_ewma_ms') or 999999)
                leaders.append((-rate, lat, -succ, f'{provider}/{model}'))
        if leaders:
            print(f'[{intent}]')
            for neg_rate, lat, neg_succ, model in sorted(leaders)[:5]:
                print(f'- {model}: success={-neg_succ}, rate={-neg_rate:.0%}, ewma={lat:.0f}ms')
