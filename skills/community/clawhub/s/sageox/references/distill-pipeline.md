# Distill Pipeline — Multi-Repo Automated Distillation

Sync team contexts, index GitHub activity, and run the distillation
pipeline across all repos in the manifest.

Pairs with the **Summary** capability — this pipeline writes the daily
source files that summary synthesizes.

## Repo manifest

The list of repos is stored in
`~/.openclaw/memory/sageox-distill-repos.json` (shared with the
manifest gate in the main SKILL.md). The user can say "add repo",
"remove repo", or "show repos" to manage it.

## Pipeline phases

Run all phases in order. Each phase is non-fatal for individual repos —
log errors and continue.

### Phase 1: Sync and Index

Group repos by `team_id` from the manifest.

For each team:

1. **Sync team context** — run from the first repo in the team group:
   ```bash
   ox sync --all-teams
   ```

2. **Index GitHub activity** — run for EACH repo in the team group:
   ```bash
   ox index github
   ```

Both commands run from the repo's directory (`cd` to the path from
the manifest). Neither needs Claude credentials.

### Phase 2: Wait for daemon sync

After all sync and index commands, the SageOx daemon processes them
asynchronously. Before distilling, verify completion.

For each repo:
1. Run `ox daemon status` in the repo directory.
2. If still processing: wait 10 seconds, check again.
3. Repeat up to 30 times (5 minutes max).
4. If still not finished after 30 attempts: report which repos are
   pending, ask the user whether to proceed or abort.
5. If daemon reports an error: surface the full message, ask whether
   to proceed or abort.

### Phase 3: Distill

For each unique team (grouped by `team_id`), run distill from the first
repo in that team's group:

```bash
ox distill --sync --layer daily --concurrency 3 --model sonnet --quiet
```

`--quiet` suppresses non-error output. If `ox distill` exits 0, report
`<team_id>: ok`. If non-zero, report `<team_id>: failed — <reason>`
and continue with the next team.

## Output

After all teams have run, print one line per team (`<team_id>: ok` or
`<team_id>: failed — <reason>`). If every team passed, `all ok` is
sufficient.
