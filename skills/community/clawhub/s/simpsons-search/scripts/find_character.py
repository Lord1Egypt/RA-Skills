#!/usr/bin/env python3
import difflib
import json
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DB = SKILL_DIR / 'references' / 'simpsons-characters.json'

if len(sys.argv) < 2:
    print('Usage: python3 scripts/find_character.py <name>', file=sys.stderr)
    sys.exit(2)

query = ' '.join(sys.argv[1:]).strip().lower()
data = json.loads(DB.read_text(encoding='utf-8'))
characters = data.get('characters', [])

def score(ch):
    names = [ch.get('name', '')] + ch.get('aliases', [])
    best = 0.0
    for name in names:
        n = name.lower()
        if query == n:
            return 1.0
        if query in n or n in query:
            best = max(best, 0.95)
        best = max(best, difflib.SequenceMatcher(None, query, n).ratio())
    return best

matches = sorted(characters, key=score, reverse=True)[:5]
out = []
for ch in matches:
    out.append({
        'name': ch['name'],
        'aliases': ch.get('aliases', []),
        'role': ch.get('role'),
        'traits': ch.get('traits', []),
        'voice_notes': ch.get('voice_notes', []),
        'themes': ch.get('themes', []),
        'style': ch.get('style'),
        'guardrails': ch.get('guardrails'),
        'score': round(score(ch), 4),
    })

print(json.dumps({'query': query, 'matches': out}, indent=2, ensure_ascii=False))
