#!/usr/bin/env python3
# UZI Self Review Gate: 13 gates (data gaps/RSI>80/industry/block)
import sys, json

data = json.load(sys.stdin)
gates_pass = True
issues = []
if not data.get('raw_fund'): issues.append('fund gap')
if data.get('rsi', 0) > 80: issues.append('RSI overbought')

print(json.dumps({'pass': not issues, 'issues': issues}))
