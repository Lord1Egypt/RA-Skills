#!/usr/bin/env python3
import json
import random
import re
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
CORPUS = SKILL_DIR / 'references' / 'simpsons-corpus.json'
FIND_QUOTE = SKILL_DIR / 'scripts' / 'find_quote.py'

SAMPLE_COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 50
random.seed(1337)

if not CORPUS.exists():
    print(json.dumps({'error': 'missing corpus'}))
    sys.exit(2)

corpus = json.loads(CORPUS.read_text(encoding='utf-8')).get('episodes', [])

def clean_lines(text):
    lines = []
    for ln in text.splitlines():
        ln = re.sub(r'\s+', ' ', ln).strip()
        if len(ln) < 35 or len(ln) > 140:
            continue
        if ln.count(' ') < 5:
            continue
        if ln.startswith('[') and ln.endswith(']'):
            continue
        if re.fullmatch(r'[-. !?()\[\]"\']+', ln):
            continue
        lines.append(ln)
    return lines

candidates = []
for ep in corpus:
    for ln in clean_lines(ep.get('text', '')):
        candidates.append({'title': ep['title'], 'url': ep['url'], 'quote': ln})

if len(candidates) < SAMPLE_COUNT:
    print(json.dumps({'error': 'not enough candidate quotes', 'count': len(candidates)}))
    sys.exit(3)

samples = random.sample(candidates, SAMPLE_COUNT)
results = []
correct_top1 = 0
correct_top3 = 0
for item in samples:
    proc = subprocess.run(
        ['python3', str(FIND_QUOTE), item['quote'], '3'],
        capture_output=True,
        text=True,
        check=True,
    )
    data = json.loads(proc.stdout)
    hits = data.get('results', [])
    top_titles = [h.get('title') for h in hits]
    top1_ok = bool(hits) and hits[0].get('title') == item['title']
    top3_ok = item['title'] in top_titles[:3]
    correct_top1 += 1 if top1_ok else 0
    correct_top3 += 1 if top3_ok else 0
    results.append({
        'quote': item['quote'],
        'expected_title': item['title'],
        'top_titles': top_titles,
        'top1_ok': top1_ok,
        'top3_ok': top3_ok,
    })

summary = {
    'sample_count': SAMPLE_COUNT,
    'top1_accuracy': round(correct_top1 / SAMPLE_COUNT, 4),
    'top3_accuracy': round(correct_top3 / SAMPLE_COUNT, 4),
    'top1_correct': correct_top1,
    'top3_correct': correct_top3,
    'results': results,
}
print(json.dumps(summary, indent=2, ensure_ascii=False))
