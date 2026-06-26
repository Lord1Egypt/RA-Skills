#!/usr/bin/env python3
"""Copy a skill/package into a clean staging directory with denylist filtering."""
from __future__ import annotations
import argparse, shutil
from pathlib import Path
DENY_DIRS={'.git','node_modules','__pycache__','.pytest_cache','.mypy_cache','state','backups','backup','reports','logs','tmp','temp','context-checkpoints'}
DENY_SUFFIX={'.pyc','.pyo','.log','.pid','.tmp','.bak','.tar','.gz','.zip'}
DENY_NAMES={'.env','.env.local','secrets.json','credentials.json'}
parser=argparse.ArgumentParser()
parser.add_argument('src')
parser.add_argument('dst')
parser.add_argument('--force', action='store_true')
args=parser.parse_args()
src=Path(args.src).resolve(); dst=Path(args.dst).resolve()
if not src.is_dir(): raise SystemExit(f'source not dir: {src}')
if dst.exists():
    if not args.force: raise SystemExit(f'destination exists: {dst} (use --force)')
    shutil.rmtree(dst)
dst.mkdir(parents=True)
for p in src.rglob('*'):
    rel=p.relative_to(src)
    if any(part in DENY_DIRS for part in rel.parts): continue
    if p.name in DENY_NAMES: continue
    if p.is_file() and ''.join(p.suffixes[-2:]) == '.tar.gz': continue
    if p.is_file() and p.suffix in DENY_SUFFIX: continue
    target=dst/rel
    if p.is_dir():
        target.mkdir(exist_ok=True)
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p,target)
print(dst)
for f in sorted(x.relative_to(dst) for x in dst.rglob('*') if x.is_file()):
    print(f)
