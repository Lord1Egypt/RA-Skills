#!/usr/bin/env python3
import json
import sys
from pathlib import Path

if len(sys.argv) != 3:
    print('Usage: create-launch-plan.py <input.json> <output.md>')
    sys.exit(1)

inp = Path(sys.argv[1])
out = Path(sys.argv[2])

data = json.loads(inp.read_text(encoding='utf-8'))

required = ['product_name', 'channel', 'price_tiers', 'target_segment', 'goal_30_days']
missing = [k for k in required if k not in data]
if missing:
    print('Missing keys:', ', '.join(missing))
    sys.exit(1)

md = f"""# 30-Day Launch Plan: {data['product_name']}

## Channel
{data['channel']}

## Target segment
{data['target_segment']}

## Pricing tiers
{data['price_tiers']}

## Goal (30 days)
{data['goal_30_days']}

## Execution sequence
1. Validate endpoint reliability and auth in production.
2. Publish listing with 2 working examples.
3. Launch outreach wave #1 (30 prospects).
4. Track activations and follow up on heavy trial users.
5. Convert first paid users and collect feedback.
"""

out.write_text(md, encoding='utf-8')
print(f'Wrote {out}')
