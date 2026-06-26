# Questionnaire Codebook Maker

A ClawHub/OpenClaw text skill for converting questionnaire items into clean codebooks and scoring notes.

## Test

```bash
python3 scripts/make_codebook.py examples/demo_items.csv --out-dir output
```

Expected behavior: the script writes `output/codebook.md` and `output/variable_map.tsv`.
