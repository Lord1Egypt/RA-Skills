#!/usr/bin/env python3
"""Generate a concise technical report template."""
from __future__ import annotations
import argparse, datetime, re
from pathlib import Path
def slug(s): return re.sub(r'-+','-',re.sub(r'[^\w\u4e00-\u9fff-]+','-',s.lower())).strip('-') or 'report'
parser=argparse.ArgumentParser(); parser.add_argument('title'); parser.add_argument('--dir',default='reports'); args=parser.parse_args()
out=Path(args.dir); out.mkdir(parents=True,exist_ok=True); p=out/f"{datetime.datetime.now():%Y%m%d-%H%M%S}-{slug(args.title)}.md"
p.write_text(f'''# {args.title}\n\nCreated: {datetime.datetime.now().isoformat(timespec='seconds')}\n\n## Executive Summary\n\n## Goal\n\n## Method\n\n## Evidence\n\n## Findings\n\n## Changes Made\n\n## Verification\n\n## Risks / Open Questions\n\n## Next Actions\n\n''',encoding='utf-8')
print(p)
