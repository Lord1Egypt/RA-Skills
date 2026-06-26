#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
rm -rf output
python3 scripts/make_codebook.py examples/demo_items.csv --out-dir output >/tmp/questionnaire_codebook_smoke.txt
test -f output/codebook.md
test -f output/variable_map.tsv
grep -q "depression_05" output/variable_map.tsv
echo "questionnaire-codebook-maker smoke test passed"
