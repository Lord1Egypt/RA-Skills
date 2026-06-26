#!/usr/bin/env python3
"""Score a skill or project for practical usefulness."""
from __future__ import annotations
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('path', nargs='?', default='.'); args=ap.parse_args()
    root=Path(args.path).resolve(); skill=root/'SKILL.md'
    score=0; notes=[]
    files=[p for p in root.rglob('*') if p.is_file()]
    if skill.exists(): score+=20; notes.append('has SKILL.md')
    text=skill.read_text(errors='ignore') if skill.exists() else ''
    checks=[('clear description','description:' in text,15),('quick start','Quick' in text or '快速' in text,10),('verification gates','Verification' in text or '验证' in text,15),('safety rules','Safety' in text or '风险' in text or '安全' in text,10),('references', any('references/' in str(p.relative_to(root)) for p in files),10),('scripts', any('scripts/' in str(p.relative_to(root)) for p in files),15),('clean size', len(text.splitlines())<=650 if text else False,5)]
    for name,ok,pts in checks:
        if ok: score+=pts; notes.append(f'+ {name}')
        else: notes.append(f'- missing/weak: {name}')
    print(json.dumps({'path':str(root),'score':min(score,100),'notes':notes},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
