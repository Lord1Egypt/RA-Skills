# Plan: Daily Dev Summary

**Date:** 2026-03-11
**Author:** cc-mini
**Repo:** wip-ai-devops-toolbox-private

## Goal

Every day, automatically scan all repos for dev updates written that day. Aggregate them into one daily summary. Save it to `wip-inc/operations/`. Parker wakes up, reads one file, knows everything that happened across the entire org.

---

## How It Works

```
wip-daily-summary                          # scan today, write summary
wip-daily-summary --date 2026-03-10       # scan a specific date
wip-daily-summary --dry-run                # preview without writing
```

### The Flow

1. **Find all repos.** Use `repos-manifest.json` (wip-repos) as the source of truth for where repos live. Falls back to scanning `ldm-os/` if no manifest.
2. **Scan each repo's `ai/dev-updates/`.** Look for files matching today's date: `YYYY-MM-DD--*`.
3. **Read each dev update.** Extract the title (first heading), author (from filename: `--cc-mini--`, `--lesa-mini--`), and content.
4. **Generate the daily summary.** One markdown file, grouped by repo, with links to the original dev update files.
5. **Write to `wip-inc/operations/daily/YYYY-MM-DD.md`.** Create the `daily/` subfolder if needed.

### Output Format

```markdown
# Daily Summary: 2026-03-11

## wip-ai-devops-toolbox

### Fix hook duplicates (cc-mini, 08:55)
- [summary extracted from dev update]

### Fix EEXIST CLI install (cc-mini, 09:15)
- [summary]

### Repo init tool (cc-mini, 10:15)
- [summary]

## memory-crystal

### [title] (agent, HH:MM)
- [summary]

---

[n] dev updates across [m] repos.
```

### What Makes a Good Summary

- The summary is NOT the full dev update. It's 2-3 bullet points per update.
- Group by repo so you can see which repos had activity.
- Include the agent name and time from the filename.
- Link to the original file for full context.
- Footer with counts.

---

## Phase 1: Core Scanner + Writer

**What to build:**
- `tools/wip-daily-summary/summary.mjs` ... the scanner
- `tools/wip-daily-summary/package.json` ... CLI entry (`wip-daily-summary`)
- `tools/wip-daily-summary/SKILL.md` ... skill documentation
- Reads `repos-manifest.json` to find all repos
- Scans `ai/dev-updates/` in each repo for today's files
- Writes summary to `wip-inc/operations/daily/YYYY-MM-DD.md`

**Status:** TODO

---

## Phase 2: Scheduled Automation

**What to build:**
- LaunchAgent or cron job that runs `wip-daily-summary` once per day (end of day, e.g. 23:00 PST)
- Could be added to LDM Dev Tools.app as another scheduled script
- Could also be triggered by `wip-release` (after a release, regenerate today's summary)

**Status:** TODO

---

## Phase 3: Notification

**What to build:**
- After writing the summary, notify Parker (iMessage via Lesa, or direct)
- Option to send via chatCompletions to Lesa so she can deliver it conversationally
- "Here's what happened today across 4 repos..."

**Status:** TODO

---

## Integration Points

- **wip-repos** ... provides the repo manifest (where to find repos)
- **wip-release** ... could trigger a summary refresh after each release
- **LDM Dev Tools.app** ... could schedule the daily run
- **Lesa** ... could deliver the summary via iMessage
- **dev-updates/** ... the source data (already being written by all agents)

---

## Output Location

```
wip-inc/
  operations/
    daily/
      2026-03-11.md
      2026-03-10.md
      ...
```

The `wip-inc/operations/` folder already exists. Create `daily/` subfolder on first run.

---

## Done Criteria

- [ ] `wip-daily-summary` scans all repos and generates a summary
- [ ] Summary grouped by repo, includes agent name and time
- [ ] Written to `wip-inc/operations/daily/YYYY-MM-DD.md`
- [ ] `--dry-run` previews without writing
- [ ] `--date` flag for specific dates
- [ ] Added to toolbox, appears in interface coverage table
- [ ] Scheduled to run daily
