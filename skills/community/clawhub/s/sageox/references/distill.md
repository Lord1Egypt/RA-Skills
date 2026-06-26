# Distill — Interactive Single-Repo Distillation

Distill team observations into structured memory summaries for the
current repo using `ox distill`.

## How distillation works

ox distill reads observations, session facts, discussion facts, and
GitHub facts, then uses an LLM to synthesize them into memory layers:

- **Daily** — `memory/daily/YYYY-MM-DD-{uuid}.md` — raw activity summaries
- **Weekly** — `memory/weekly/YYYY-Www-{uuid}.md` — synthesis of daily
- **Monthly** — `memory/monthly/YYYY-MM-{uuid}.md` — synthesis of weekly

## Running a distill

### Basic usage

```bash
ox distill
```

Runs daily distillation for the last 7 days. Automatically runs weekly
and monthly roll-ups if layer boundaries have been crossed.

### With options

```bash
ox distill --layer <layer> --model <model> [--sync] [--concurrency N] [--quiet]
```

**Layer selection:**
- `daily` — recent activity (most common)
- `weekly` — roll up daily summaries into weekly
- `monthly` — roll up weekly summaries into monthly

**Model selection:**
- `sonnet` (default) — good balance of speed and quality
- `opus` — deeper analysis, slower
- `haiku` — fast, lightweight

**Other flags:**
- `--sync` — sync ledger and team context before distilling
- `--concurrency N` — parallel LLM calls (1-8, default 1)
- `--dry-run` — show what would be distilled without LLM calls
- `--all` — process full history (default: last 7 days)
- `--no-push` — skip pushing results to remote
- `--verbose` — log full prompts to stderr

### Guided workflow

When the user asks to distill, guide them:

1. "Which layer? daily (default), weekly, or monthly?"
2. "Which model? sonnet (default), opus, or haiku?"
3. "Sync first? (pulls latest team context before distilling)"
4. Run the distill with chosen options.
5. Report results: success or failure per team.

## Viewing distilled history

### List entries

```bash
ox distill history list --since 7d [--layer daily] [--format json|text]
ox distill history list --all-teams --since 30d
```

### Show specific entry

```bash
ox distill history show <id> --format content
```

### Show recent history as narrative

```bash
ox distill history since 7d --format content
```

## Examples

```bash
# Interactive daily distill with sync
ox distill --layer daily --model sonnet --sync

# Dry run to preview
ox distill --dry-run

# View last week's distilled entries
ox distill history list --since 7d --layer daily --format text

# Read a specific entry
ox distill history show 2026-04-20-abc123 --format content
```
