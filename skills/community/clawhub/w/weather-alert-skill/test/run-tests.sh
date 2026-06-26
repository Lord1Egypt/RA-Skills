#!/usr/bin/env bash
set -euo pipefail

grep -q '"version": "0.2.1"' package.json
grep -q '^version: 0.2.1$' skill.yaml
grep -q 'normalizeSeverity' src/index.js
bash scripts/lint.sh >/dev/null
bash scripts/publish.sh --dry-run >/dev/null
echo "tests passed"
