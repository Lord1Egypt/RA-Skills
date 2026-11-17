# memo — Duplicate tags

For duplicate tags, use `vocabulary check` to find candidates, then `vocabulary list --json` without
a filter for the current fingerprint. `vocabulary inspect tag:<source-id> tag:<survivor-id>` takes
that `--fingerprint`; `--limit` bounds samples, not counts. Its coverage names four dependency
tables, not historical text. memo has no command that applies a preview. Similarity and preview
fingerprints never authorize alias changes or merging. Re-read and reselect after a stale-fingerprint
refusal.
