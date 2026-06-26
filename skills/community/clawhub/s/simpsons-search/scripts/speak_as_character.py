#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
FIND = SKILL_DIR / 'scripts' / 'find_character.py'
DOSSIERS = SKILL_DIR / 'references' / 'simpsons-character-dossiers.json'

if len(sys.argv) < 3:
    print('Usage: python3 scripts/speak_as_character.py <character> <topic/text>', file=sys.stderr)
    sys.exit(2)

character = sys.argv[1]
text = ' '.join(sys.argv[2:]).strip()
proc = subprocess.run(['python3', str(FIND), character], capture_output=True, text=True, check=True)
data = json.loads(proc.stdout)
if not data.get('matches'):
    print(json.dumps({'error': 'no character match'}))
    sys.exit(3)
brief = data['matches'][0]

dossier = None
if DOSSIERS.exists():
    all_dossiers = json.loads(DOSSIERS.read_text(encoding='utf-8')).get('characters', [])
    for d in all_dossiers:
        if d.get('name') == brief['name']:
            dossier = d
            break

out = {
    'character': brief['name'],
    'task': text,
    'style_guide': {
        'role': brief.get('role'),
        'traits': brief.get('traits', []),
        'voice_notes': brief.get('voice_notes', []),
        'themes': brief.get('themes', []),
        'style': brief.get('style'),
        'guardrails': brief.get('guardrails'),
        'top_terms': dossier.get('top_terms', [])[:12] if dossier else [],
        'related_characters': dossier.get('related_characters', [])[:6] if dossier else [],
        'candidate_catchphrases': dossier.get('candidate_catchphrases', [])[:6] if dossier else [],
    },
    'instructions': [
        'Write fresh original dialogue inspired by the character.',
        'Match the rhythm and worldview more than surface catchphrases.',
        'Use catchphrase-like language sparingly.',
        'Do not claim to be the official original character.',
    ]
}
print(json.dumps(out, indent=2, ensure_ascii=False))
