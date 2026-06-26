#!/usr/bin/env python3
"""Critique a plan/answer for reasoning weaknesses."""
from __future__ import annotations
import argparse, sys, json, re
parser=argparse.ArgumentParser(); parser.add_argument('file',nargs='?'); args=parser.parse_args()
txt=open(args.file,encoding='utf-8',errors='ignore').read() if args.file else sys.stdin.read()
issues=[]
if not re.search(r'evidence|证据|验证|test|status|diff|source|读回',txt,re.I): issues.append('no evidence/verification marker')
if re.search(r'一定|必然|肯定|obviously|definitely',txt,re.I) and not re.search(r'因为|evidence|证据',txt,re.I): issues.append('strong certainty without support')
if len(re.findall(r'可能|maybe|perhaps|guess|猜',txt,re.I))>5: issues.append('too much uncertainty without tests')
if re.search(r'\bMax\b|\bMAX\b',txt): issues.append('external persona contamination detected')
if len(txt)>3000: issues.append('too long; compress active variables')
print(json.dumps({'issues':issues,'recommendation':'revise' if issues else 'pass'},ensure_ascii=False,indent=2))
