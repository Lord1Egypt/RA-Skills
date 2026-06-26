#!/usr/bin/env python3
"""Evaluate prompt/task instruction quality heuristically."""
from __future__ import annotations
import argparse, sys, json, re
parser=argparse.ArgumentParser(); parser.add_argument('file',nargs='?'); args=parser.parse_args()
txt=open(args.file,encoding='utf-8',errors='ignore').read() if args.file else sys.stdin.read()
checks={
 'goal': bool(re.search(r'goal|目标|目的|任务',txt,re.I)),
 'context': bool(re.search(r'context|背景|现状|输入',txt,re.I)),
 'constraints': bool(re.search(r'constraint|限制|要求|不要|必须',txt,re.I)),
 'output_format': bool(re.search(r'format|格式|输出|json|markdown|表格',txt,re.I)),
 'success_gate': bool(re.search(r'success|verify|验证|通过|标准|验收',txt,re.I)),
 'examples': bool(re.search(r'example|示例|例如',txt,re.I)),
}
score=sum(checks.values())*100//len(checks)
print(json.dumps({'score':score,'checks':checks,'missing':[k for k,v in checks.items() if not v]},ensure_ascii=False,indent=2))
