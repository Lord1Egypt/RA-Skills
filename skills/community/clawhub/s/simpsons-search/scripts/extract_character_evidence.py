#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CORPUS = SKILL_DIR / 'references' / 'simpsons-corpus.json'
DB = SKILL_DIR / 'references' / 'simpsons-characters.json'
OUT = SKILL_DIR / 'references' / 'simpsons-character-evidence.json'

if not CORPUS.exists() or not DB.exists():
    print(json.dumps({'error': 'missing corpus or character db'}))
    sys.exit(2)

corpus = json.loads(CORPUS.read_text(encoding='utf-8')).get('episodes', [])
chars = json.loads(DB.read_text(encoding='utf-8')).get('characters', [])

def normalize_name(name: str) -> str:
    return re.sub(r'[^a-z0-9]+', ' ', name.lower()).strip()

# Very simple speaker cues and mentions. Not perfect, but useful.
def collect_for_character(ch):
    keys = [normalize_name(ch['name'])] + [normalize_name(a) for a in ch.get('aliases', [])]
    keys = [k for k in keys if k]
    mention_counter = Counter()
    quotes = []
    for ep in corpus:
        text = ep.get('text', '')
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        for line in lines:
            low = normalize_name(line)
            hit = any(k in low for k in keys)
            if not hit:
                continue
            mention_counter[ep['title']] += 1
            if len(line) <= 220 and len(quotes) < 60:
                quotes.append({'episode': ep['title'], 'url': ep['url'], 'line': line})
    top_eps = [{'title': t, 'mentions': c} for t, c in mention_counter.most_common(12)]
    return {
        'name': ch['name'],
        'episodes': top_eps,
        'examples': quotes[:25],
    }

out = {'characters': [collect_for_character(ch) for ch in chars]}
OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'written': str(OUT), 'count': len(out['characters'])}))
