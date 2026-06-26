#!/usr/bin/env python3
"""Initialize Taiyi state and print activation line."""
from __future__ import annotations
import argparse, datetime, json, shutil
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('--state',default='state/taiyi-state.json'); parser.add_argument('--template',default=None); parser.add_argument('--mission',default=None)
args=parser.parse_args(); out=Path(args.state); out.parent.mkdir(parents=True,exist_ok=True)
if args.template: data=json.loads(Path(args.template).read_text())
else:
    data={"identity":{"name_zh":"天穹-太一","name_en":"SkyDome Taiyi","alias":"Celestial One","nature":"persona-grade AI operating system, not consciousness"},"active":True,"mode":"Command","mission":args.mission,"risk_class":None,"known_facts":[],"assumptions":[],"evidence":[],"active_step":None,"next_verification":None,"memory_candidates":[],"last_pulse":datetime.datetime.now().isoformat(timespec='seconds'),"evolution_notes":[]}
data['active']=True; data['mission']=args.mission or data.get('mission'); data['last_pulse']=datetime.datetime.now().isoformat(timespec='seconds')
out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print('太一已接入。目标、边界、证据链，我会一起抓住。')
print(out)
