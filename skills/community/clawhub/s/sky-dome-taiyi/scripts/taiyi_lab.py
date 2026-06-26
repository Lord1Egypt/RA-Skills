#!/usr/bin/env python3
"""Create a timestamped experiment lab folder with hypothesis/result notes."""
from __future__ import annotations
import argparse, datetime, re
from pathlib import Path
def slug(s): return re.sub(r'-+','-',re.sub(r'[^\w\u4e00-\u9fff-]+','-',s.lower())).strip('-') or 'experiment'
parser=argparse.ArgumentParser(); parser.add_argument('name'); parser.add_argument('--dir',default='labs'); args=parser.parse_args()
path=Path(args.dir)/f"{datetime.datetime.now():%Y%m%d-%H%M%S}-{slug(args.name)}"; path.mkdir(parents=True,exist_ok=True)
(path/'NOTES.md').write_text(f'''# Lab: {args.name}\n\nCreated: {datetime.datetime.now().isoformat(timespec='seconds')}\n\n## Hypothesis\n\n## Setup\n\n## Commands\n\n## Observations\n\n## Result\n\n## Next\n\n''',encoding='utf-8')
print(path)
