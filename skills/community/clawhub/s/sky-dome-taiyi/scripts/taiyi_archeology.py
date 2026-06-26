#!/usr/bin/env python3
"""Project archeology: summarize file types, largest files, newest files, and likely entrypoints."""
from __future__ import annotations
import argparse, collections, os
from pathlib import Path
SKIP={'.git','node_modules','__pycache__','.pytest_cache','.mypy_cache','state','backups','logs'}
parser=argparse.ArgumentParser(); parser.add_argument('path',nargs='?',default='.'); parser.add_argument('--limit',type=int,default=12); args=parser.parse_args()
root=Path(args.path).resolve(); files=[]; exts=collections.Counter()
for p in root.rglob('*'):
    if any(part in SKIP for part in p.relative_to(root).parts): continue
    if p.is_file():
        try:
            st=p.stat(); rel=str(p.relative_to(root)); files.append((rel,st.st_size,st.st_mtime)); exts[p.suffix or '<none>']+=1
        except Exception: pass
print(f'# Taiyi Archeology: {root}')
print(f'- Files: {len(files)}')
print('- Extensions: '+', '.join(f'{k}:{v}' for k,v in exts.most_common(10)))
print('\n## Likely entrypoints')
for name in ['SKILL.md','package.json','pyproject.toml','requirements.txt','Makefile','README.md','AGENTS.md','docker-compose.yml']:
    if (root/name).exists(): print(f'- {name}')
print('\n## Largest files')
for rel,size,_ in sorted(files,key=lambda x:x[1],reverse=True)[:args.limit]: print(f'- {size:>8} {rel}')
print('\n## Newest files')
for rel,size,_ in sorted(files,key=lambda x:x[2],reverse=True)[:args.limit]: print(f'- {rel}')
