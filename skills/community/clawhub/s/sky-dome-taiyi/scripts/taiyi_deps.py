#!/usr/bin/env python3
"""Detect dependency manifests and print useful install/test hints without installing."""
from __future__ import annotations
import argparse, json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('path',nargs='?',default='.'); args=parser.parse_args(); root=Path(args.path)
print(f'# Taiyi Dependency Map: {root.resolve()}')
if (root/'package.json').exists():
    pkg=json.loads((root/'package.json').read_text())
    print('- Node package.json found')
    print('  scripts: '+', '.join(pkg.get('scripts',{}).keys()))
    print('  deps: '+str(len(pkg.get('dependencies',{})))+', devDeps: '+str(len(pkg.get('devDependencies',{}))))
    if (root/'pnpm-lock.yaml').exists(): print('  preferred install: pnpm install')
    elif (root/'package-lock.json').exists(): print('  preferred install: npm ci')
if (root/'pyproject.toml').exists(): print('- Python pyproject.toml found')
if (root/'requirements.txt').exists(): print('- Python requirements.txt found')
if (root/'Cargo.toml').exists(): print('- Rust Cargo.toml found')
if (root/'go.mod').exists(): print('- Go go.mod found')
if (root/'Makefile').exists(): print('- Makefile found: try `make help` or inspect targets')
