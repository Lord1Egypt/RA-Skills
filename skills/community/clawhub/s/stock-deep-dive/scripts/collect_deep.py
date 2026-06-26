#!/usr/bin/env python3
# Deep Dive Collector: Parallel 8-dim + UZI
import subprocess, json, sys
ticker = sys.argv[1]
raw_analyze = subprocess.check_output(['/data/workspace/skills/stock-analysis/scripts/analyze_stock.py', ticker]).decode()
raw_div = json.dumps({'ticker': ticker, 'dividend': 'no_dividend'})
raw_fund = subprocess.check_output(['/data/workspace/skills/stock-fundamentals/src/main.py', ticker]).decode()
# Parse RSI/vol from analyze text
import re
rsi_match = re.search(r'RSI.*?(\d+\.\d+)', raw_analyze)
vol_match = re.search(r'volume_ratio.*?(\d+\.\d+)', raw_analyze)
rsi = rsi_match.group(1) if rsi_match else 'unknown'
vol = vol_match.group(1) if vol_match else 'unknown'
enrich = {'analyze': raw_analyze, 'div': raw_div, 'fund': raw_fund, 'rsi': rsi, 'vol': vol}
panel = {'avg': 5.0, 'votes': ['+10 ROE Buffett', '+0 growth Lynch']}  # Self-contained mock until parse full
dcf = subprocess.check_output(['python3', 'fin_models.py', ticker]).decode()
enrich = {'analyze': raw_analyze, 'div': raw_div, 'fund': raw_fund, 'panel': panel, 'dcf': dcf}
raw = json.dumps(enrich)
print(json.dumps(enrich))
gate = json.loads(subprocess.check_output(['python3', 'uzi_gate.py'], input=json.dumps(enrich)))
print(json.dumps({'enrich': enrich, 'gate': gate}))
