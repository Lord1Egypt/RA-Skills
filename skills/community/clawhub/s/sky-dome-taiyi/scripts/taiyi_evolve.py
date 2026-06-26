#!/usr/bin/env python3
"""Suggest safe self-evolution improvements from a skill directory."""
from __future__ import annotations
import argparse, json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('path',nargs='?',default='.'); args=parser.parse_args()
root=Path(args.path); skill=root/'SKILL.md'; text=skill.read_text(errors='ignore') if skill.exists() else ''
suggestions=[]
if 'Quick Start' not in text and '快速' not in text: suggestions.append('add a Quick Start section')
if 'Verification' not in text and '验证' not in text: suggestions.append('add explicit verification gates')
if 'Memory' not in text and '记忆' not in text: suggestions.append('add memory law and storage boundaries')
if not (root/'scripts').exists(): suggestions.append('add scripts for repeated deterministic tasks')
if not (root/'references').exists(): suggestions.append('move detailed patterns into references')
if len(text.splitlines())>500: suggestions.append('reduce SKILL.md length or split optional depth into references')
if not suggestions: suggestions.append('no obvious structural evolution; improve based on real user friction')
print(json.dumps({'path':str(root.resolve()),'suggestions':suggestions},ensure_ascii=False,indent=2))
