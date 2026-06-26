#!/usr/bin/env python3
"""Search Taiyi reference recipes/playbooks by keyword."""
from __future__ import annotations
import argparse, re
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('query'); parser.add_argument('--dir',default=str(Path(__file__).resolve().parents[1]/'references')); parser.add_argument('--limit',type=int,default=12); args=parser.parse_args()
q=args.query.lower(); hits=[]
for p in Path(args.dir).glob('*.md'):
    text=p.read_text(errors='ignore')
    blocks=re.split(r'(?=^## )', text, flags=re.M)
    for b in blocks:
        if q in b.lower():
            title=b.splitlines()[0].strip('# ').strip() if b.splitlines() else p.name
            snippet=' '.join(b.splitlines()[1:8])[:500]
            hits.append((p.name,title,snippet))
for file,title,snip in hits[:args.limit]:
    print(f'## {title}\nFile: {file}\n{snip}\n')
if not hits: print('no matches')
