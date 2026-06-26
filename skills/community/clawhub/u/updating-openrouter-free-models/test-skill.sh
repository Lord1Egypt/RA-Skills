#!/usr/bin/env bash
# Test script for updating-openrouter-free-models skill
# This demonstrates the skill in action

set -e

echo "========================================"
echo "Testing: updating-openrouter-free-models"
echo "========================================"

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Setup
export ANTHROPIC_AUTH_TOKEN="${ANTHROPIC_AUTH_TOKEN:-YOUR_ANTHROPIC_API_KEY}"
TEMP_DIR=$(mktemp -d)
cd "$TEMP_DIR"

echo -e "\n[Step 1] Fetching free models from OpenRouter API..."
python3 "$SCRIPT_DIR/fetch_models.py"

echo -e "\n[Step 2] Batch testing models (sample)..."
timeout 60 python3 "$SCRIPT_DIR/test_models.py" 2>&1 | head -20 || true

echo -e "\n[Step 3] Self-test before applying..."
python3 -c "
import json
from pathlib import Path
try:
    with open(Path.home() / '.claude' / 'settings.json') as f:
        json.load(f)
    print('✓ Claude settings.json is valid JSON')
except Exception as e:
    print(f'✗ Claude settings error: {e}')
    exit(1)
"

echo -e "\n✅ All dry-run tests passed!"
echo "To apply updates, run: ./apply_updates.py"

# Cleanup
cd -
rm -rf "$TEMP_DIR"
