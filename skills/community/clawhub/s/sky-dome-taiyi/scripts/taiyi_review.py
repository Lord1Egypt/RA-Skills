#!/usr/bin/env python3
"""Create a Taiyi review/postmortem document."""
from __future__ import annotations
import argparse, datetime, re
from pathlib import Path

def slug(s): return re.sub(r'-+','-',re.sub(r'[^\w\u4e00-\u9fff-]+','-',s.lower())).strip('-') or 'review'
parser=argparse.ArgumentParser(); parser.add_argument('topic'); parser.add_argument('--dir',default='reviews'); args=parser.parse_args()
out=Path(args.dir); out.mkdir(parents=True,exist_ok=True)
path=out/f"{datetime.datetime.now():%Y-%m-%d-%H%M%S}-{slug(args.topic)}.md"
path.write_text(f'''# Taiyi Review: {args.topic}

Created: {datetime.datetime.now().isoformat(timespec='seconds')}

## Original goal

## What happened

## Evidence

## What worked

## What failed / friction

## Root cause or pattern

## Durable lesson

## Should memory be updated?

- [ ] No, transient only
- [ ] Yes, safe durable preference/lesson
- [ ] Yes, update skill/script/checklist

## Next improvement

''',encoding='utf-8')
print(path)
