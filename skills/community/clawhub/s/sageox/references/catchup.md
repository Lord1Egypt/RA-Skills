# Catchup — What Happened While You Were Away

Orchestrates multiple ox commands to generate a structured briefing of
team and repo activity since the user was last active.

## Workflow

### Step 1: Determine time window

Ask: "How long were you away?" Parse into a duration:
- "since yesterday" → `24h`
- "a few days" → `3d`
- "a week" → `7d`
- Default if unclear: `24h`

### Step 2: Gather data

Run these commands from the selected repo directory. Each is non-fatal —
if one fails, log the error and continue with the rest.

**Distilled history:**

```bash
ox distill history list --since <duration> --layer daily --format json
```

If entries exist, fetch their content:

```bash
ox distill history show --team <team_id> --format content <entry-ids>
```

**Recent sessions:**

```bash
ox session list --since <duration>
```

**Code insights:**

```bash
ox code insights --days <N> --json
```

Where `<N>` matches the duration (24h → 1, 3d → 3, 7d → 7).

### Step 3: Synthesize

Build a prompt by substituting gathered data into `assets/CATCHUP.md`:
- `{{DISTILLED}}` — distilled daily entries (content from step 2)
- `{{SESSIONS}}` — session list output
- `{{INSIGHTS}}` — code insights JSON
- `{{DURATION}}` — how long they were away

Run synthesis:

```bash
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout)"
"$TIMEOUT_BIN" 600 claude -p --model claude-sonnet-4-6 <<< "$PROMPT"
```

`claude -p` uses whatever credentials `claude` already has — either
OAuth from `claude login` or `ANTHROPIC_API_KEY` from the shell.

If synthesis fails (non-zero exit, timeout exit 124), surface the error
to the user and offer to show the raw data instead.

### Step 4: Present

Return Claude's output directly. The output should follow this structure:

- **What shipped** — completed work, merged PRs
- **What's in progress** — active work, open PRs
- **What you should know** — decisions, blockers, surprises
- **Potential conflicts** — overlap with the user's likely work areas

## Handling missing data

- **No distilled history:** skip that section, note "No distilled
  entries for this period. Run the distill capability to generate them."
- **No sessions:** skip that section, note "No recorded sessions."
- **No code insights:** skip that section.
- **All empty:** tell the user "No recorded activity found for the last
  <duration>. This could mean no sessions were recorded, or distillation
  hasn't been run. Try the distill capability first."

## Multi-repo catchup

If the manifest has multiple repos and the user wants to catch up across
all of them, iterate through each repo:
1. `cd` to each repo path
2. Gather data from each
3. Include all data in the synthesis prompt, grouped by repo

This produces a cross-repo briefing. Label each section by repo name.
