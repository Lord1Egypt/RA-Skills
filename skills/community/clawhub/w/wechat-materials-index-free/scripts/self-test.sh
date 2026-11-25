#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
node scripts/validate-fixtures.mjs
for file in SKILL.md manifest.yaml agents/openai.yaml README.md README.en.md LICENSE icon-512.png assets/promo.png; do
  test -s "$file"
done
file icon-512.png | grep -Eq 'PNG image data, 512 x 512'
file assets/promo.png | grep -Eq 'PNG image data, 1600 x 900'
echo "self-test passed: metadata, offline fixtures, icon and promo are valid"
