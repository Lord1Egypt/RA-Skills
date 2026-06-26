#!/bin/bash
set -e

echo "═══════════════════════════════════════════════════════════"
echo "  OpenClaw Skill Complete Test"
echo "═══════════════════════════════════════════════════════════"

export ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-YOUR_ANTHROPIC_API_KEY}"

# Test 1: Fetch
echo -e "\n[1/4] Testing fetch_models.py..."
python3 fetch_models.py
CURRENT_MODELS=$(wc -l < /tmp/free_models.txt)
echo "   Found $CURRENT_MODELS free models"

# Test 2: Test (limited sample for speed)
echo -e "\n[2/4] Testing test_models.py (sample of 5)..."
# Modify to test only first 5
head -5 /tmp/free_models.txt > /tmp/test_sample.txt
mv /tmp/test_sample.txt /tmp/free_models.txt
python3 test_models.py
VERIFIED=$(wc -l < /tmp/verified_models.txt)
echo "   Verified $VERIFIED models"

# Test 3: Apply updates
echo -e "\n[3/4] Testing apply_updates_openclaw.js..."
node apply_updates_openclaw.js

# Test 4: Validate JSON
echo -e "\n[4/4] Validating configurations..."
python3 -c "
import json
from pathlib import Path
files = [
    str(Path.home() / '.claude' / 'settings.json'),
    str(Path.home() / '.openclaw' / 'openclaw.json')
]
for f in files:
    with open(f) as fp:
        json.load(fp)
    print(f'   ✓ {f}')
print('   All JSON valid!')
"

echo -e "\n═══════════════════════════════════════════════════════════"
echo "  ✅ All tests passed!"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Files created in: ~/.openclaw/workspace/skills/updating-openrouter-free-models/"
echo "  - SKILL.md (documentation)"
echo "  - fetch_models.py (API fetcher)"
echo "  - test_models.py (batch tester)"
echo "  - apply_updates_openclaw.js (config updater)"
echo "  - restart_openclaw.sh (service restarter)"
echo ""
echo "To use this skill in OpenClaw:"
echo "  1. cd ~/.openclaw/workspace/skills/updating-openrouter-free-models"
echo "  2. ./complete_test.sh  (or run step by step)"
echo ""
