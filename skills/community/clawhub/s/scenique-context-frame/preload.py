#!/usr/bin/env python3
# Skill entry: minimal bridge to the context_sim demo
import sys
from pathlib import Path
p = Path(__file__).resolve().parents[1] / 'context_sim.py'
if __name__=='__main__':
    mode = sys.argv[1] if len(sys.argv)>1 else 'demo'
    if p.exists():
        import runpy
        runpy.run_path(str(p), run_name='__main__')
    else:
        print('context_sim.py not found')
