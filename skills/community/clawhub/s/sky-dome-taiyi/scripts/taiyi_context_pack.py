#!/usr/bin/env python3
"""Pack messy notes/stdin into a compact context capsule."""
from __future__ import annotations
import argparse, sys, re
parser=argparse.ArgumentParser(); parser.add_argument('--max-lines',type=int,default=40); parser.add_argument('file',nargs='?')
args=parser.parse_args(); txt=open(args.file,encoding='utf-8',errors='ignore').read() if args.file else sys.stdin.read()
lines=[re.sub(r'\s+',' ',x).strip() for x in txt.splitlines()]
lines=[x for x in lines if x]
# crude but useful: keep headings, bullets, errors, TODOs, file paths, commands
picked=[]
for x in lines:
    low=x.lower()
    if x.startswith(('#','-','*')) or any(k in low for k in ['error','failed','todo','fixme','next','decision','changed','blocked']) or '/' in x or '`' in x:
        picked.append(x)
    if len(picked)>=args.max_lines: break
if not picked: picked=lines[:args.max_lines]
print('# Context Capsule / 上下文胶囊\n')
for x in picked: print(f'- {x}')
