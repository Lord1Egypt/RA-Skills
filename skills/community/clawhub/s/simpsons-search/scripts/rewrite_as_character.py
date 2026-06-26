#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
BRIEF = SKILL_DIR / 'scripts' / 'character_brief.py'
FIND = SKILL_DIR / 'scripts' / 'find_character.py'

if len(sys.argv) < 3:
    print('Usage: python3 scripts/rewrite_as_character.py <character> <text...>', file=sys.stderr)
    sys.exit(2)

character = sys.argv[1]
text = ' '.join(sys.argv[2:]).strip()
proc = subprocess.run(['python3', str(FIND), character], capture_output=True, text=True, check=True)
data = json.loads(proc.stdout)
if not data.get('matches'):
    print(json.dumps({'error': 'no character match'}))
    sys.exit(3)
ch = data['matches'][0]
prompt = {
    'character': ch['name'],
    'source_text': text,
    'instructions': [
        'Rewrite the source text as fresh dialogue inspired by this character.',
        'Match the role, traits, rhythm, and themes.',
        'Do not quote canon lines unless explicitly asked.',
        'Do not claim to be the official original character.',
    ],
    'brief': ch,
}
print(json.dumps(prompt, indent=2, ensure_ascii=False))
