# Lobster Integration

`run-pr-review.sh` auto-detects Lobster and uses the structured
`pr-review-workflow.lobster` pipeline when it is available. When Lobster is
absent or `--no-lobster` is passed, the same data-gathering scripts run
directly in a pipe-through fallback. The agent's analysis layer is identical
in both cases.

---

## Workflow overview

```
run-pr-review.sh <pr>
  │
  ├─ Lobster present?  ─yes─► pr-review-workflow.lobster
  │                              step 1: fetch-pr.sh       → PR metadata + diff
  │                              step 2: fetch-ci.sh        → CI check runs
  │                              step 3: fetch-reviews.sh   → review comments
  │                              step 4: merge-pr-context.py → pr-context-v0
  │
  └─ no ──────────────────────► direct pipe-through
                                 fetch-pr.sh | fetch-ci.sh | fetch-reviews.sh
                                   └─► merge-pr-context.py → pr-context-v0
```

The `pr-context-v0` envelope lands on stdout. The agent then performs the
layered review analysis on that context.

---

## Quick start

```bash
# Auto-detect Lobster (preferred)
scripts/run-pr-review.sh https://github.com/owner/repo/pull/123

# Bare number — needs --repo
scripts/run-pr-review.sh 42 --repo owner/repo

# Force direct path (no Lobster)
scripts/run-pr-review.sh https://github.com/owner/repo/pull/123 --no-lobster
```

---

## Lobster path (explicit)

```bash
lobster run --file scripts/pr-review-workflow.lobster \
  --args-json '{"pr":"https://github.com/owner/repo/pull/123"}'

# Dry-run (no GitHub API calls — validates workflow plan only)
lobster run --dry-run --file scripts/pr-review-workflow.lobster \
  --args-json '{"pr":"https://github.com/owner/repo/pull/123"}'

# Tool-mode (JSON envelope on stdout — for agent integration)
lobster run --mode tool --file scripts/pr-review-workflow.lobster \
  --args-json '{"pr":"https://github.com/owner/repo/pull/123"}'
```

---

## Workflow args

| Arg    | Type   | Default | Description |
|--------|--------|---------|-------------|
| `pr`   | string | —       | PR URL or bare number (required) |
| `repo` | string | `""`    | `owner/repo` — needed when `pr` is a bare number |

---

## Workflow steps

| Step | Script | Exit 1 meaning | Wrapped? |
|------|--------|----------------|----------|
| `fetch_pr` | `fetch-pr.sh` | — (always fatal) | No |
| `fetch_ci` | `fetch-ci.sh` | checks failing/pending | Yes — `lobster-safe-run.sh` |
| `fetch_reviews` | `fetch-reviews.sh` | no reviews yet | Yes — `lobster-safe-run.sh` |
| `merge` | `merge-pr-context.py` | optional blobs absent | Yes — `lobster-safe-run.sh` |

`lobster-safe-run.sh` absorbs exit 1 (expected soft signal) and propagates
exit ≥2 (real errors) so Lobster aborts the workflow on genuine failures.

---

## Exit codes

| Code | Meaning |
|------|---------|
| `0` | `pr-context-v0` envelope complete |
| `1` | Partial context — pr data present, optional blobs absent |
| `2` | Error — workflow or script failed |
| `3` | Lobster required (`--lobster-mode`) but not installed |

---

## Direct fallback scripts

```bash
# PR metadata + diff
scripts/fetch-pr.sh https://github.com/owner/repo/pull/123

# CI status
scripts/fetch-ci.sh https://github.com/owner/repo/pull/123

# Review comments
scripts/fetch-reviews.sh https://github.com/owner/repo/pull/123

# Full merged context (pipe-through)
{
  scripts/fetch-pr.sh https://github.com/owner/repo/pull/123
  scripts/fetch-ci.sh https://github.com/owner/repo/pull/123
  scripts/fetch-reviews.sh https://github.com/owner/repo/pull/123
} | scripts/merge-pr-context.py
```

---

## Shell requirements

The workflow file (`pr-review-workflow.lobster`) uses bash parameter expansion
syntax — specifically `${VAR:+word}` (expand `word` only when `VAR` is set and
non-empty) — in step `command` strings.  Lobster must execute those commands
through a **bash** shell (not `sh` or `dash`); the expansion is a bash-ism
that is not universally portable across POSIX shells.  Lobster's default
executor uses `bash` on Linux/macOS, so this works without extra configuration
in standard environments.

---

## Installing Lobster

Lobster source lives at `github.com/openclaw/lobster`; the npm package is currently published as `@clawdbot/lobster`.

```bash
npm install -g @clawdbot/lobster
# or, without a global install:
npx @clawdbot/lobster version
```

Lobster is optional. All scripts work without it — the agent gets the same
`pr-context-v0` envelope from the direct pipe-through path.
