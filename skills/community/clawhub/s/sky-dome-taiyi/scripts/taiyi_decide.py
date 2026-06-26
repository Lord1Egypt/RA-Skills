#!/usr/bin/env python3
"""Weighted decision matrix."""
from __future__ import annotations
import argparse, csv, json, sys
parser=argparse.ArgumentParser(); parser.add_argument('csvfile',nargs='?',help='CSV: option,criterion,score,weight'); args=parser.parse_args()
rows=list(csv.DictReader(open(args.csvfile) if args.csvfile else sys.stdin))
scores={}; details={}
for r in rows:
    opt=r['option']; score=float(r.get('score',0)); weight=float(r.get('weight',1)); val=score*weight
    scores[opt]=scores.get(opt,0)+val; details.setdefault(opt,[]).append({**r,'weighted':val})
print(json.dumps({'ranking':sorted(scores.items(),key=lambda x:x[1],reverse=True),'details':details},ensure_ascii=False,indent=2))
