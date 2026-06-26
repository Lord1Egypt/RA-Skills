#!/usr/bin/env python3
"""Score a task and recommend a SkyDome Taiyi mode."""
from __future__ import annotations
import argparse
parser=argparse.ArgumentParser()
for name in ['urgency','impact','risk','uncertainty','reversibility']:
    parser.add_argument(f'--{name}', type=int, default=3, help='1-5')
args=parser.parse_args()
score=args.urgency+args.impact+args.risk+args.uncertainty+(6-args.reversibility)
if args.risk>=4 or args.reversibility<=2:
    mode='Sentinel / 哨兵'
elif score>=19:
    mode='Command / 指挥'
elif args.uncertainty>=4:
    mode='Oracle / 太卜'
elif args.impact>=4:
    mode='Command / 指挥'
else:
    mode='Flash / 闪电'
print(f'''Taiyi Score: {score}/25
Recommended Mode: {mode}
Inputs: urgency={args.urgency}, impact={args.impact}, risk={args.risk}, uncertainty={args.uncertainty}, reversibility={args.reversibility}
''')
