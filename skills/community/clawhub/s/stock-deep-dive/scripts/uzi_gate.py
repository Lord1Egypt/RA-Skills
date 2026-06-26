#!/usr/bin/env python3
# UZI Gate: 5 critical checks
import sys, json
data = json.load(sys.stdin)
pass_gate = len(data.get('issues', [])) == 0
print(json.dumps({'gate_pass': pass_gate}))
