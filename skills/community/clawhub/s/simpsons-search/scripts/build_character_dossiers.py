#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CORPUS = SKILL_DIR / 'references' / 'simpsons-corpus.json'
DB = SKILL_DIR / 'references' / 'simpsons-characters.json'
OUT = SKILL_DIR / 'references' / 'simpsons-character-dossiers.json'

if not CORPUS.exists() or not DB.exists():
    print(json.dumps({'error': 'missing corpus or character db'}))
    sys.exit(2)

corpus = json.loads(CORPUS.read_text(encoding='utf-8')).get('episodes', [])
chars = json.loads(DB.read_text(encoding='utf-8')).get('characters', [])

STOP = {
    'the','and','for','that','with','this','from','have','your','you','are','not','but','all','was','just','they','him','her','his','she','our','out','get','got','too','can','who','what','when','where','why','how','into','over','than','then','them','their','there','here','about','like','dont','didnt','cant','wont','ive','youre','its','i','a','an','to','of','in','on','is','it','be','we','he','me','my','at','as','or'
}


def norm(s: str) -> str:
    return re.sub(r'[^a-z0-9 ]+', ' ', s.lower()).strip()


def tokens(s: str):
    return [t for t in norm(s).split() if len(t) >= 3 and t not in STOP]

char_defs = []
for ch in chars:
    keys = [norm(ch['name'])] + [norm(a) for a in ch.get('aliases', [])]
    keys = [k for k in keys if k]
    char_defs.append((ch, keys))

all_names = [c['name'] for c in chars]

out = []
for ch, keys in char_defs:
    mention_eps = Counter()
    nearby_terms = Counter()
    related = Counter()
    examples = []
    catchphrases = Counter()

    for ep in corpus:
        lines = [ln.strip() for ln in ep.get('text', '').splitlines() if ln.strip()]
        ep_hit = False
        for idx, line in enumerate(lines):
            low = norm(line)
            if not any(k in low for k in keys):
                continue
            ep_hit = True
            if len(examples) < 30 and len(line) <= 220:
                examples.append({'episode': ep['title'], 'url': ep['url'], 'line': line})

            window = ' '.join(lines[max(0, idx-1):min(len(lines), idx+2)])
            for t in tokens(window):
                nearby_terms[t] += 1

            # crude catchphrase heuristic: short quoted-ish memorable lines or repeated short lines
            simple = re.sub(r'\s+', ' ', line).strip()
            if 8 <= len(simple) <= 90:
                catchphrases[simple] += 1

            for other in all_names:
                if other == ch['name']:
                    continue
                other_norm = norm(other)
                if other_norm and other_norm in low:
                    related[other] += 1
        if ep_hit:
            mention_eps[ep['title']] += 1

    dossier = {
        'name': ch['name'],
        'top_terms': [t for t, _ in nearby_terms.most_common(20)],
        'related_characters': [{'name': n, 'count': c} for n, c in related.most_common(10)],
        'episode_presence': [{'title': t, 'count': c} for t, c in mention_eps.most_common(15)],
        'example_lines': examples[:20],
        'candidate_catchphrases': [{'line': t, 'count': c} for t, c in catchphrases.most_common(15)],
    }
    out.append(dossier)

OUT.write_text(json.dumps({'characters': out}, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'written': str(OUT), 'count': len(out)}))
