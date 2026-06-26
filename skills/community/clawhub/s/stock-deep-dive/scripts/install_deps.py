#!/usr/bin/env python3
# Standalone deps setup for stock-deep-dive (uv venv + pip)
import subprocess
import sys
from pathlib import Path

def main():
    skill_dir = Path(__file__).parent
    venv_dir = skill_dir / '.venv'
    
    # uv venv
    subprocess.run([sys.executable, '-m', 'uv', 'venv', str(venv_dir)], check=True)
    
    # Activate & pip
    pip = venv_dir / 'bin' / 'pip'
    subprocess.run([pip, 'install', 'yfinance', 'pandas', 'numpy', 'requests', 'jsonschema'], check=True)
    
    print('✅ Deps ready: uv run scripts/collect.py [TICKER]')
    
if __name__ == '__main__':
    main()
