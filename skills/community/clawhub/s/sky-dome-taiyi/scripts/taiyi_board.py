#!/usr/bin/env python3
"""Render a markdown board for Taiyi workflow runs."""
from __future__ import annotations
import argparse, json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('--dir',default='state/workflows'); args=parser.parse_args()
root=Path(args.dir)
print('# Taiyi Workflow Board\n')
if not root.exists(): print('No workflow runs.'); raise SystemExit
for p in sorted(root.glob('*.json')):
    r=json.loads(p.read_text())
    total=len(r['steps']); done=sum(1 for s in r['steps'] if s.get('status')=='done')
    active=next((s['title'] for s in r['steps'] if s.get('status')=='active'),'complete')
    print(f"## {r['title']}")
    print(f"- File: `{p.name}`")
    print(f"- Template: {r.get('template')}")
    print(f"- Progress: {done}/{total}")
    print(f"- Active: {active}\n")
