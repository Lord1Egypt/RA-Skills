---
name: shark-clean
description: "Clean up shark state files (.shark-done, SHARK_LOG.md, pending.json, timings.jsonl)"
---

# Shark Clean

Remove shark state files from the skill base directory:
- `.shark-done`
- `SHARK_LOG.md`
- `shark-exec/state/pending.json`
- `state/timings.jsonl` (only if user confirms — timing history is valuable)

Report what was cleaned.
