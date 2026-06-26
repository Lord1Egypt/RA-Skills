#!/usr/bin/env python3
import json
import re
import time
import urllib.request
from html import unescape
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
INDEX = SKILL_DIR / 'references' / 'simpsons-episodes.json'
CACHE_DIR = SKILL_DIR / 'references' / 'cache'
CORPUS = SKILL_DIR / 'references' / 'simpsons-corpus.json'
CACHE_DIR.mkdir(parents=True, exist_ok=True)

if not INDEX.exists():
    raise SystemExit('missing index; run build_index.py first')

data = json.loads(INDEX.read_text(encoding='utf-8'))
episodes = data.get('episodes', [])

script_pat = re.compile(r'<div[^>]+class="scrolling-script-container"[^>]*>(.*?)</div>', re.I | re.S)
linebreak_pat = re.compile(r'(?i)<br\s*/?>')
tag_pat = re.compile(r'<[^>]+>')
space_pat = re.compile(r'[ \t]+')
paragraph_pat = re.compile(r'\n\s*\n+')

def slug(url: str) -> str:
    return re.sub(r'[^a-zA-Z0-9._-]+', '_', url)[:180] + '.json'

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9']+", ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

existing = {}
if CORPUS.exists():
    try:
        old = json.loads(CORPUS.read_text(encoding='utf-8'))
        existing = {ep['url']: ep for ep in old.get('episodes', [])}
    except Exception:
        existing = {}

corpus = []
for i, ep in enumerate(episodes, 1):
    cache = CACHE_DIR / slug(ep['url'])
    if ep['url'] in existing:
        corpus.append(existing[ep['url']])
        continue
    if cache.exists():
        parsed = json.loads(cache.read_text(encoding='utf-8'))
    else:
        html = urllib.request.urlopen(ep['url']).read().decode('utf-8', errors='replace')
        m = script_pat.search(html)
        content = m.group(1) if m else html
        text = linebreak_pat.sub('\n', content)
        text = tag_pat.sub(' ', text)
        text = unescape(text)
        text = text.replace('\r', '')
        text = paragraph_pat.sub('\n\n', text)
        text = space_pat.sub(' ', text)
        parsed = {'title': ep['title'], 'url': ep['url'], 'text': text.strip()}
        cache.write_text(json.dumps(parsed), encoding='utf-8')
        time.sleep(0.15)
    corpus.append({
        'title': parsed['title'],
        'url': parsed['url'],
        'text': parsed['text'],
        'norm': normalize(parsed['text']),
    })
    if i % 25 == 0:
        CORPUS.write_text(json.dumps({'count': len(corpus), 'episodes': corpus}, ensure_ascii=False), encoding='utf-8')
    if i % 50 == 0:
        print(json.dumps({'progress': i, 'total': len(episodes), 'built': len(corpus)}), flush=True)

CORPUS.write_text(json.dumps({'count': len(corpus), 'episodes': corpus}, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'written': str(CORPUS), 'count': len(corpus)}))
