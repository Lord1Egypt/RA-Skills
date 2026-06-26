#!/usr/bin/env python3
import subprocess
import json
import sys
from pathlib import Path

ticker = sys.argv[1] if len(sys.argv) > 1 else 'SOFI'

raw = {}

# analyze_stock --json
try:
    result = subprocess.run(['uv', 'run', '/data/workspace/skills/stock-analysis/scripts/analyze_stock.py', ticker, '--output', 'json'], capture_output=True, text=True, timeout=30)
    raw['analyze_stock'] = json.loads(result.stdout) if result.returncode == 0 else {'error': result.stderr}
except Exception as e:
    raw['analyze_stock'] = {'error': str(e)}

# fundamentals
try:
    result = subprocess.run(['uv', 'run', '/data/workspace/skills/stock-fundamentals/src/main.py', ticker], capture_output=True, text=True, timeout=30)
    raw['fundamentals'] = result.stdout.strip()
except Exception as e:
    raw['fundamentals'] = {'error': str(e)}

# dividend
try:
    result = subprocess.run(['uv', 'run', '/data/workspace/skills/stock-analysis/scripts/dividends.py', ticker], capture_output=True, text=True, timeout=30)
    raw['dividend'] = result.stdout.strip() if 'does not pay' not in result.stdout else None
except Exception as e:
    raw['dividend'] = None

# momentum (reuse analyze --fast for RSI/vol/mom extract)
try:
    result = subprocess.run(['uv', 'run', '/data/workspace/skills/stock-analysis/scripts/analyze_stock.py', ticker, '--fast', '--output', 'json'], capture_output=True, text=True, timeout=30)
    mom = json.loads(result.stdout)['components']['momentum'] if result.returncode == 0 else {}
    raw['momentum'] = mom
except Exception as e:
    raw['momentum'] = {'error': str(e)}

print(json.dumps(raw, indent=2))
