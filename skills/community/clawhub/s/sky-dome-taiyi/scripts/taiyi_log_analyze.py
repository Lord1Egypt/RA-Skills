#!/usr/bin/env python3
"""Analyze logs: count levels, extract errors, cluster repeated messages."""
from __future__ import annotations
import argparse, collections, re, sys
parser=argparse.ArgumentParser(); parser.add_argument('file',nargs='?'); parser.add_argument('--limit',type=int,default=20); args=parser.parse_args()
txt=open(args.file,errors='ignore').read() if args.file else sys.stdin.read()
lines=txt.splitlines(); levels=collections.Counter(); clusters=collections.Counter(); samples=[]
for line in lines:
    low=line.lower()
    for lvl in ['fatal','error','warn','warning','fail','exception','traceback','timeout','denied','refused']:
        if lvl in low: levels[lvl]+=1
    if any(k in low for k in ['error','exception','failed','traceback','timeout','denied','refused']):
        norm=re.sub(r'\b\d+\b','<n>',line); norm=re.sub(r'0x[0-9a-fA-F]+','<hex>',norm); norm=re.sub(r'/[^\s]+','<path>',norm)
        clusters[norm[:220]]+=1
        if len(samples)<args.limit: samples.append(line[:500])
print(f'# Taiyi Log Analysis\n\nLines: {len(lines)}\n')
print('## Level counts')
for k,v in levels.most_common(): print(f'- {k}: {v}')
print('\n## Repeated error clusters')
for msg,c in clusters.most_common(args.limit): print(f'- x{c} {msg}')
print('\n## Samples')
for s in samples: print(f'- {s}')
