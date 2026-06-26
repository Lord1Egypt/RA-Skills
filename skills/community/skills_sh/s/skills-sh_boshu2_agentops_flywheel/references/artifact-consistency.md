# Artifact Consistency Validation

Cross-reference validation: scan knowledge artifacts for broken internal references.

```bash
# Preferred: run the helper script (handles fenced code blocks, placeholders, allowlist).
skills/flywheel/scripts/artifact-consistency.sh

# Optional: include each broken reference for cleanup work.
skills/flywheel/scripts/artifact-consistency.sh --verbose

# Optional: disable allowlist to inspect all historical breakage.
skills/flywheel/scripts/artifact-consistency.sh --no-allowlist

# Optional: use a custom allowlist.
skills/flywheel/scripts/artifact-consistency.sh --allowlist path/to/allowlist.txt
```

The helper script:
- Scans `.agents/**/*.md` excluding `.agents/ao/*`
- Ignores fenced code blocks
- Extracts references to `.agents/...(.md|.json|.jsonl)`
- Skips template placeholders (`YYYY`, `<...>`, `{...}`, wildcards, `...`)
- Applies allowlist patterns from `references/artifact-consistency-allowlist.txt`
- Reports `TOTAL_REFS`, `BROKEN_REFS`, `CONSISTENCY`, `STATUS`
- With `--verbose`, emits `BROKEN_REF=<source> -> <target>` lines

## Allowlist Format

`<source-glob> -> <target-glob>`

Examples:
- `* -> .agents/ao/*` (ignore transient runtime telemetry references)
- `.agents/research/* -> .agents/rpi/phase-*-summary.md` (scope to one source family)

Guidelines:
- Prefer narrow patterns first.
- Keep entries for historical or non-literal references only.
- Remove entries when underlying references are fixed or retired.

## Health Indicator

| Consistency | Status |
|-------------|--------|
| >90% | Healthy |
| 70-90% | Warning |
| <70% | Critical |
