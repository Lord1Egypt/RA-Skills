#!/usr/bin/env python3
"""Generate a compact SkyDome Taiyi mission brief."""
from __future__ import annotations
import argparse, datetime

parser = argparse.ArgumentParser()
parser.add_argument('goal', nargs='+')
parser.add_argument('--deadline', default='unspecified')
parser.add_argument('--risk', default='auto')
args = parser.parse_args()
goal=' '.join(args.goal)
now=datetime.datetime.now().isoformat(timespec='seconds')
print(f'''# Taiyi Mission Brief

Created: {now}

## Goal
{goal}

## Deadline
{args.deadline}

## Risk Class
{args.risk}

## Success Gate
- Define the concrete evidence that proves completion.

## Constraints
- Time:
- Permissions:
- Files/systems:

## First Moves
1. Inspect actual current state.
2. Identify blockers and risk class.
3. Execute the smallest reversible step.
4. Verify with a concrete gate.
''')
