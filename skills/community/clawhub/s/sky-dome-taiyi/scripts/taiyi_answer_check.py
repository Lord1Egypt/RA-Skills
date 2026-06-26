#!/usr/bin/env python3
"""Check an answer draft for common 'skill made me dumb' smells."""
from __future__ import annotations
import argparse, re, sys, json
parser=argparse.ArgumentParser(); parser.add_argument('file',nargs='?'); args=parser.parse_args()
txt=open(args.file,encoding='utf-8',errors='ignore').read() if args.file else sys.stdin.read()
smells=[]
if len(txt)>2000: smells.append('too long for default response')
if len(re.findall(r'太一|SkyDome|Celestial|模式|系统',txt))>8: smells.append('persona/lore overused')
if re.search(r'我会|将会|接下来我会',txt) and not re.search(r'已|done|完成|验证|evidence|证据',txt,re.I): smells.append('promise without evidence')
if re.search(r'成功|完成|搞定',txt) and not re.search(r'验证|证据|读回|test|status|diff|doctor|quality',txt,re.I): smells.append('success claim lacks evidence marker')
if txt.count('\n')>30: smells.append('too many lines')
print(json.dumps({'smells':smells,'recommendation':'ship' if not smells else 'tighten: result + evidence + next'},ensure_ascii=False,indent=2))
