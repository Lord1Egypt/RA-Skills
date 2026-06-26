#!/usr/bin/env python3
"""Collect a compact local environment fingerprint for debugging/reproducibility."""
from __future__ import annotations
import json, os, platform, shutil, subprocess, sys

def run(cmd):
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=5)
        return r.stdout.strip() or r.stderr.strip()
    except Exception as e: return f'ERR:{e}'

tools=['python3','node','npm','pnpm','git','openclaw','clawhub','rg','fd','jq']
print(json.dumps({
  'platform': platform.platform(),
  'python': sys.version.split()[0],
  'cwd': os.getcwd(),
  'tools': {t: (run([t,'--version']).splitlines()[0] if shutil.which(t) else None) for t in tools},
  'git': run(['git','rev-parse','--show-toplevel']) if shutil.which('git') else None,
},ensure_ascii=False,indent=2))
