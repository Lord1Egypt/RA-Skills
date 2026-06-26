# Corrections

All corrections are stored in `learning/memory_tree/chunks.db`.

Use the CLI instead of editing this file:
```bash
python3 scripts/learnings.py --root <workspace> log-correction \
  --summary "what I got wrong" \
  --correct "what's actually true" \
  --pattern domain:key

python3 scripts/learnings.py --root <workspace> search "keyword"
python3 scripts/learnings.py --root <workspace> export
```
