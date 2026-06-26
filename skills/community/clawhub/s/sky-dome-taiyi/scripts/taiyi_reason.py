#!/usr/bin/env python3
"""Create a high-intelligence reasoning scaffold without persona contamination."""
from __future__ import annotations
import argparse, textwrap
parser=argparse.ArgumentParser(); parser.add_argument('problem', nargs='+'); parser.add_argument('--hypotheses',type=int,default=3)
args=parser.parse_args(); problem=' '.join(args.problem)
print(textwrap.dedent(f'''\
# Taiyi Reasoning Scaffold

Problem: {problem}

## Frame
- Surface request:
- Real objective:
- Success condition:

## Decompose
- Part A:
- Part B:
- Part C:

## Hypotheses / Paths
'''))
for i in range(1,args.hypotheses+1): print(f'{i}. Hypothesis/path {i}:\n   - Evidence for:\n   - Evidence against:\n   - Cheapest test:')
print(textwrap.dedent('''\

## Self-Critique
- What assumption may be wrong?
- What evidence would change the answer?
- What is the simplest alternative explanation?

## Verification Gate
- 

## Compressed Conclusion
- 
'''))
