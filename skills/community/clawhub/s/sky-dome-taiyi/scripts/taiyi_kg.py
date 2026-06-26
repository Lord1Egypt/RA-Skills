#!/usr/bin/env python3
"""Extract a simple markdown knowledge graph from notes."""
from __future__ import annotations
import argparse, re, sys, collections
parser=argparse.ArgumentParser(); parser.add_argument('file',nargs='?'); args=parser.parse_args()
txt=open(args.file,errors='ignore').read() if args.file else sys.stdin.read()
edges=[]
patterns=[(r'(.+?)\s*->\s*(.+)','relates_to'),(r'(.+?)\s+depends on\s+(.+)','depends_on'),(r'(.+?)\s+blocks\s+(.+)','blocks'),(r'(.+?)\s+verifies\s+(.+)','verifies')]
for line in txt.splitlines():
    line=line.strip('- *\t ')
    for pat,rel in patterns:
        m=re.match(pat,line,re.I)
        if m: edges.append((m.group(1).strip(),rel,m.group(2).strip()))
print('# Taiyi Knowledge Graph\n')
print('| Source | Relation | Target |')
print('|---|---|---|')
for a,r,b in edges: print(f'| {a} | {r} | {b} |')
