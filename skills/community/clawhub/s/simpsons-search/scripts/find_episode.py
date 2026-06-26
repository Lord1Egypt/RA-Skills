#!/usr/bin/env python3
import difflib
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
INDEX = SKILL_DIR / 'references' / 'simpsons-episodes.json'

if len(sys.argv) < 2:
    print('Usage: python3 scripts/find_episode.py <query>', file=sys.stderr)
    sys.exit(2)

query = ' '.join(sys.argv[1:]).strip().lower()
if not INDEX.exists():
    print(json.dumps({'error': 'missing_index', 'hint': 'Run scripts/build_index.py first'}))
    sys.exit(3)

data = json.loads(INDEX.read_text(encoding='utf-8'))
episodes = data.get('episodes', [])

def score(title: str) -> float:
    t = title.lower()
    if query == t:
        return 1.0
    if query in t:
        return 0.95
    return difflib.SequenceMatcher(None, query, t).ratio()

matches = sorted(
    ({'title': ep['title'], 'url': ep['url'], 'score': round(score(ep['title']), 4)} for ep in episodes),
    key=lambda x: x['score'],
    reverse=True,
)[:10]

print(json.dumps({'query': query, 'matches': matches}, indent=2))
