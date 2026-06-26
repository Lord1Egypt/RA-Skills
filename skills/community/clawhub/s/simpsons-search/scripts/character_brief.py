#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
FIND = SKILL_DIR / 'scripts' / 'find_character.py'

if len(sys.argv) < 2:
    print('Usage: python3 scripts/character_brief.py <name>', file=sys.stderr)
    sys.exit(2)

query = ' '.join(sys.argv[1:]).strip()
proc = subprocess.run(['python3', str(FIND), query], capture_output=True, text=True, check=True)
data = json.loads(proc.stdout)
if not data.get('matches'):
    print('No character match found.')
    sys.exit(0)
ch = data['matches'][0]
print(f"Name: {ch['name']}")
print(f"Role: {ch.get('role','')}")
print(f"Traits: {', '.join(ch.get('traits', []))}")
print(f"Voice notes: {', '.join(ch.get('voice_notes', []))}")
print(f"Themes: {', '.join(ch.get('themes', []))}")
print(f"Style: {ch.get('style','')}")
print(f"Guardrails: {ch.get('guardrails','')}")
print('\nImprov prompt:')
print(f"Write fresh lines inspired by {ch['name']}. Match the role, traits, rhythm, and themes above. Do not pretend to be the original official character in a misleading way; make it an homage-level imitation.")
