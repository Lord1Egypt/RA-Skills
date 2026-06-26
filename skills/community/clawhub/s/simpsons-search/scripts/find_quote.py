#!/usr/bin/env python3
import json
import math
import re
import sys
import urllib.request
from collections import Counter, defaultdict
from html import unescape
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
INDEX = SKILL_DIR / 'references' / 'simpsons-episodes.json'
CORPUS = SKILL_DIR / 'references' / 'simpsons-corpus.json'
SEARCH_INDEX = SKILL_DIR / 'references' / 'simpsons-search-index.json'
CACHE_DIR = SKILL_DIR / 'references' / 'cache'
CACHE_DIR.mkdir(parents=True, exist_ok=True)

if len(sys.argv) < 2:
    print('Usage: python3 scripts/find_quote.py <query> [limit]', file=sys.stderr)
    sys.exit(2)

query = ' '.join(sys.argv[1:-1]).strip() if len(sys.argv) > 2 and sys.argv[-1].isdigit() else ' '.join(sys.argv[1:]).strip()
limit = int(sys.argv[-1]) if len(sys.argv) > 2 and sys.argv[-1].isdigit() else 5

STOP = {
    'the','and','for','that','with','this','from','have','your','you','are','not','but','all','was','just','they','him','her','his','she','our','out','get','got','too','can','who','what','when','where','why','how','into','over','than','then','them','their','there','here','about','like','dont','didnt','cant','wont','ive','youre','its'
}

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9']+", ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

query_norm = normalize(query)
terms = [t for t in query_norm.split() if len(t) >= 2 and t not in STOP]
if not terms and query_norm:
    terms = query_norm.split()

if not INDEX.exists():
    print(json.dumps({'error': 'missing_index', 'hint': 'Run scripts/build_index.py first'}))
    sys.exit(3)

def slug(url: str) -> str:
    return re.sub(r'[^a-zA-Z0-9._-]+', '_', url)[:180] + '.json'

def load_episode_cache(ep):
    cache = CACHE_DIR / slug(ep['url'])
    if cache.exists():
        return json.loads(cache.read_text(encoding='utf-8'))
    html = urllib.request.urlopen(ep['url']).read().decode('utf-8', errors='replace')
    m = re.search(r'<div[^>]+class="scrolling-script-container"[^>]*>(.*?)</div>', html, re.I | re.S)
    content = m.group(1) if m else html
    text = re.sub(r'(?i)<br\s*/?>', '\n', content)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text)
    text = text.replace('\r', '')
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    parsed = {'title': ep['title'], 'url': ep['url'], 'text': text.strip()}
    cache.write_text(json.dumps(parsed), encoding='utf-8')
    return parsed

def make_excerpt(text: str, qnorm: str, terms_):
    original = re.sub(r'\s+', ' ', text).strip()
    original_norm = normalize(original)
    pos = 0
    if qnorm and qnorm in original_norm:
        words = original_norm.split()
        qwords = qnorm.split()
        for i in range(0, max(0, len(words) - len(qwords) + 1)):
            if words[i:i+len(qwords)] == qwords:
                orig_words = original.split()
                i = min(i, len(orig_words)-1)
                pos = max(0, sum(len(w)+1 for w in orig_words[:i]))
                break
    else:
        orig_l = original.lower()
        best = None
        for t in terms_:
            p = orig_l.find(t)
            if p != -1 and (best is None or p < best):
                best = p
        pos = best if best is not None else 0
    start = max(0, pos - 180)
    end = min(len(original), pos + 260)
    excerpt = original[start:end].strip()
    if start > 0:
        excerpt = '…' + excerpt
    if end < len(original):
        excerpt += '…'
    return excerpt

# Fast path: use inverted index + corpus
if SEARCH_INDEX.exists() and CORPUS.exists():
    sidx = json.loads(SEARCH_INDEX.read_text(encoding='utf-8'))
    corpus = json.loads(CORPUS.read_text(encoding='utf-8')).get('episodes', [])
    meta = sidx.get('meta', [])
    term_map = sidx.get('terms', {})
    N = max(1, len(meta))

    candidate_scores = defaultdict(float)
    coverages = Counter()
    for term in terms:
        postings = term_map.get(term, {})
        df = len(postings)
        idf = math.log((N + 1) / (df + 1)) + 1.0
        for doc_id, count in postings.items():
            d = int(doc_id)
            candidate_scores[d] += idf * min(count, 8)
            coverages[d] += 1

    for i, m in enumerate(meta):
        if query_norm and query_norm in m.get('title_norm', ''):
            candidate_scores[i] += 20.0

    shortlisted = sorted(candidate_scores.items(), key=lambda x: (x[1], coverages[x[0]]), reverse=True)[:120]
    results = []
    for doc_id, base in shortlisted:
        ep = corpus[doc_id]
        text_norm = ep.get('norm') or normalize(ep.get('text', ''))
        score = base + coverages[doc_id] * 6.0
        if query_norm and query_norm in text_norm:
            score += 80.0
        if query_norm and query_norm in meta[doc_id].get('title_norm', ''):
            score += 20.0
        excerpt = make_excerpt(ep['text'], query_norm, terms)
        results.append({
            'title': ep['title'],
            'url': ep['url'],
            'score': round(score, 3),
            'excerpt': excerpt,
        })
    results.sort(key=lambda x: x['score'], reverse=True)
    print(json.dumps({'query': query, 'results': results[:limit]}, indent=2, ensure_ascii=False))
    sys.exit(0)

# Fallback path: no search index yet
if not CORPUS.exists():
    data = json.loads(INDEX.read_text(encoding='utf-8'))
    episodes = data.get('episodes', [])
    def title_score(ep):
        t = ep['title'].lower()
        s = 0.0
        if query_norm in normalize(t):
            s += 20
        for term in terms:
            if term in normalize(t):
                s += 4
        return s
    shortlist = sorted(episodes, key=title_score, reverse=True)[:120]
    corpus_eps = []
    for ep in shortlist:
        try:
            parsed = load_episode_cache(ep)
        except Exception:
            continue
        corpus_eps.append({
            'title': parsed['title'],
            'url': parsed['url'],
            'text': parsed['text'],
            'norm': normalize(parsed['text']),
        })
else:
    corpus_eps = json.loads(CORPUS.read_text(encoding='utf-8')).get('episodes', [])

results = []
for ep in corpus_eps:
    text_norm = ep.get('norm', '')
    score = 0.0
    title_norm = normalize(ep['title'])
    if query_norm and query_norm in text_norm:
        score += 80.0
    if query_norm and query_norm in title_norm:
        score += 20.0
    coverage = 0
    for term in terms:
        c = text_norm.count(term)
        if c:
            coverage += 1
            score += min(c, 8)
    score += coverage * 6.0
    if coverage == 0 and query_norm not in text_norm and query_norm not in title_norm:
        continue
    results.append({
        'title': ep['title'],
        'url': ep['url'],
        'score': round(score, 3),
        'excerpt': make_excerpt(ep['text'], query_norm, terms),
    })
results.sort(key=lambda x: x['score'], reverse=True)
print(json.dumps({'query': query, 'results': results[:limit]}, indent=2, ensure_ascii=False))
