# Summary — Cross-Team Activity Summary

Generate a summary of the last 24 hours of SageOx distilled activity
across all configured teams.

## Prerequisites

This capability requires `claude -p` for synthesis. Verify Claude
credentials work before proceeding:

```bash
claude -p "say hi" --model claude-sonnet-4-6
```

If it fails with an auth error, tell the user to either run
`claude login` (Pro/Max OAuth) or export `ANTHROPIC_API_KEY`.

## Pipeline

### Step 1: Load manifest and summary state

1. Read `~/.openclaw/memory/sageox-distill-repos.json` — extract unique
   `team_id` values.
2. Read `~/.openclaw/memory/sageox-summary-state.json` if it exists.
   Missing file → empty state (first run). Malformed → proceed as empty
   and emit one warning to **stderr** (not stdout):
   ```text
   warning: sageox-summary-state.json was unreadable, starting from empty state
   ```

### Step 2: Select new entries per team

For each unique `team_id`, run the bundled selection script:

```bash
STATE_FILE=~/.openclaw/memory/sageox-summary-state.json
NEW_IDS="$(bash scripts/select-new-entries.sh "$TEAM_ID" 24h "$STATE_FILE")"
```

- Empty `NEW_IDS` for a team → skip it, log to stderr.
- **All** teams empty → stop. Print one line to stdout:
  `No new distilled content since last summary.` Do not invoke Claude.

### Step 3: Fetch content and build prompt

For each team with new entries:

```bash
TEAM_BLOCK="$(ox distill history show \
  --team "$TEAM_ID" \
  --format content \
  $NEW_IDS)"
```

Read the template from `assets/SUMMARIZE.md`. Substitute:

- `{{ENTRIES}}` — one section per team:
  ```text
  ### Team "<team_id>"

  <TEAM_BLOCK>
  ```

- `{{MULTI_TEAM_RULES}}` — if two or more teams have content:
  ```text
  - Organize the summary by team, using each team ID as a section header
  - Attribute insights to the correct team
  ```
  Otherwise, empty string.

Do not re-wrap or mutate the markdown inside `TEAM_BLOCK`.

### Step 4: Run Claude

```bash
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout)"
"$TIMEOUT_BIN" 600 claude -p --model claude-sonnet-4-6 <<< "$PROMPT"
```

No `--add-dir`, no `--allowedTools` — content is inline. If it fails
(non-zero, timeout 124, network error), surface the error and **do not**
proceed to step 5.

### Step 5: Update summary state

Only if Claude succeeded. For each team with new entries:

```bash
printf '%s\n' "$NEW_IDS" \
  | bash scripts/update-state.sh "$STATE_FILE" "$TEAM_ID"
```

Teams skipped in step 2 are not touched here.

### Step 6: Return the summary

Return Claude's stdout directly. It is formatted for Slack mrkdwn.
Prefix with a one-line header showing how many teams were summarized
and any that were skipped.
