#!/usr/bin/env python3
"""Update/read Taiyi pulse state."""
from __future__ import annotations
import argparse, datetime, json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('--state',default='state/taiyi-state.json'); parser.add_argument('--mode'); parser.add_argument('--mission'); parser.add_argument('--evidence',action='append',default=[]); parser.add_argument('--step'); args=parser.parse_args()
p=Path(args.state)
data=json.loads(p.read_text()) if p.exists() else {"active":True,"identity":{"name_zh":"天穹-太一"}}
if args.mode: data['mode']=args.mode
if args.mission: data['mission']=args.mission
if args.step: data['active_step']=args.step
if args.evidence: data.setdefault('evidence',[]).extend(args.evidence)
data['last_pulse']=datetime.datetime.now().isoformat(timespec='seconds')
p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:data.get(k) for k in ['active','mode','mission','active_step','last_pulse','evidence']},ensure_ascii=False,indent=2))
