#!/usr/bin/env python3
"""Taiyi dream consolidation: summarize tasks/reviews/memory into a safe dream report."""
from __future__ import annotations
import argparse, datetime, json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('--state',default='state'); parser.add_argument('--out',default='dreams'); args=parser.parse_args()
state=Path(args.state); out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
items=[]
for name in ['taiyi-tasks.json','taiyi-memory.jsonl']:
    p=state/name
    if p.exists(): items.append((name,p.read_text(errors='ignore')[-4000:]))
review_dir=Path('reviews')
if review_dir.exists():
    for p in sorted(review_dir.glob('*.md'))[-5:]: items.append((str(p),p.read_text(errors='ignore')[-2000:]))
path=out/f"{datetime.datetime.now():%Y-%m-%d-%H%M%S}-taiyi-dream.md"
body=['# Taiyi Dream / 太一梦境整理', '', f'Created: {datetime.datetime.now().isoformat(timespec="seconds")}', '', '## Purpose', 'Consolidate recent traces into safe, reusable lessons. This is file-based reflection, not consciousness.', '', '## Inputs']
for name,txt in items:
    body += [f'### {name}', '```text', txt[:2000], '```']
body += ['', '## Dream Questions', '- What pattern repeated?', '- What should be strengthened?', '- What should be inhibited?', '- What belongs in durable memory?', '- What should become a script/checklist/skill?', '', '## Consolidated Lessons', '- TODO', '', '## Next Evolution', '- TODO']
path.write_text('\n'.join(body),encoding='utf-8')
print(path)
