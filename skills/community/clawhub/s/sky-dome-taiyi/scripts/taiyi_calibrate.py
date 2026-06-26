#!/usr/bin/env python3
"""Anti-dumb calibration: produce a compact task focus card."""
from __future__ import annotations
import argparse, textwrap
parser=argparse.ArgumentParser(); parser.add_argument('goal', nargs='+'); parser.add_argument('--evidence',default=''); parser.add_argument('--constraint',action='append',default=[]); parser.add_argument('--gate',default='smallest meaningful verification')
args=parser.parse_args(); goal=' '.join(args.goal)
print(textwrap.dedent(f'''\
# Taiyi Calibration / 太一校准

Goal: {goal}
Evidence: {args.evidence or 'not inspected yet'}
Constraints: {', '.join(args.constraint) if args.constraint else 'none stated'}
Active step: inspect or act on the smallest reversible step
Verification gate: {args.gate}

Anti-dumb rule: no lore, no long framework, no success claim without evidence.
'''))
