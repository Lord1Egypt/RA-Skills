#!/usr/bin/env python3
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CORPUS = SKILL_DIR / 'references' / 'simpsons-corpus.json'
OUT = SKILL_DIR / 'references' / 'simpsons-search-index.json'

STOP = {
    'the','and','for','that','with','this','from','have','your','you','are','not','but','all','was','just','they','him','her','his','she','our','out','get','got','too','can','who','what','when','where','why','how','into','over','than','then','them','their','there','here','about','like','dont','didnt','cant','wont','ive','youre','its','i','a','an','to','of','in','on','is','it','be','we','he','me','my','at','as','or'
}

def norm(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9']+", ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

if not CORPUS.exists():
    print(json.dumps({'error': 'missing corpus; run build_corpus.py first'}))
    sys.exit(2)

data = json.loads(CORPUS.read_text(encoding='utf-8'))
episodes = data.get('episodes', [])

term_to_docs = defaultdict(dict)
meta = []
for idx, ep in enumerate(episodes):
    text = ep.get('norm') or norm(ep.get('text', ''))
    title = ep.get('title', '')
    title_norm = norm(title)
    tf = Counter(t for t in text.split() if len(t) >= 2 and t not in STOP)
    for term, count in tf.items():
        term_to_docs[term][str(idx)] = count
    meta.append({'title': title, 'url': ep.get('url'), 'title_norm': title_norm})

serializable = {
    'count': len(meta),
    'meta': meta,
    'terms': term_to_docs,
}
OUT.write_text(json.dumps(serializable, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'written': str(OUT), 'episodes': len(meta), 'terms': len(term_to_docs)}))
