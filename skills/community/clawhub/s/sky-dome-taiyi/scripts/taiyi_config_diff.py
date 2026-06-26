#!/usr/bin/env python3
"""Diff two JSON/YAML-ish text config files with normalized JSON support."""
from __future__ import annotations
import argparse, difflib, json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('old'); parser.add_argument('new'); args=parser.parse_args()
def norm(p):
    txt=Path(p).read_text(errors='ignore')
    try: return json.dumps(json.loads(txt),ensure_ascii=False,indent=2,sort_keys=True).splitlines()
    except Exception: return txt.splitlines()
a=norm(args.old); b=norm(args.new)
print('\n'.join(difflib.unified_diff(a,b,fromfile=args.old,tofile=args.new,lineterm='')))
