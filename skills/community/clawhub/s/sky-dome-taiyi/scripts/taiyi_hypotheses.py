#!/usr/bin/env python3
"""Generate a compact hypothesis ledger template."""
from __future__ import annotations
import argparse
parser=argparse.ArgumentParser(); parser.add_argument('topic',nargs='+'); parser.add_argument('-n',type=int,default=3); args=parser.parse_args()
print(f'# Hypothesis Ledger: {" ".join(args.topic)}\n')
print('| # | Hypothesis | Evidence For | Evidence Against | Cheapest Test | Status |')
print('|---|---|---|---|---|---|')
for i in range(1,args.n+1): print(f'| {i} |  |  |  |  | open |')
