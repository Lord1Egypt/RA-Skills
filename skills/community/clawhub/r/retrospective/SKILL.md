---
name: retrospective
description: Run a structured weekly agent retrospective. Analyses wins, failures, skill gaps, cron health, and config issues from the last 7 days. Produces honest, specific output — not generic platitudes. Auto-schedules a Friday cron job. Trigger on "retrospective", "retro", "reflect", "review my work", "what went well", "what should I improve".
---

# Agent Retrospective

Run a structured self-review covering the last 7 days from the run date. Produce honest, specific analysis — not generic platitudes.

## Process

### 1. Gather Context

- Read `memory/` files for the review period (daily logs)
- Read `MEMORY.md` for long-term context (pending tasks, blocked items, decisions)
- Check cron job history: `cron(action="list")` — note failures and consecutive errors
- Check session status for usage patterns

### 2. Analyse: What Went Well

List concrete wins with evidence:
- Tasks completed successfully
- Automations that ran reliably
- Problems solved creatively
- Time/effort saved for the user

Keep it brief. 3-7 bullet points max.

### 3. Analyse: What Didn't Go Well

Be brutally honest. For each struggle:
- **What**: The specific task or goal
- **Why it failed**: Root cause (not symptoms)
- **Time wasted**: Rough estimate of turns/attempts spent
- **Pattern**: Is this a recurring struggle or one-off?

Categories to check:
- Bot detection / scraping failures
- Browser automation reliability
- API quota / auth issues
- Tasks attempted manually that a skill could handle
- Blocked items that stayed blocked too long
- Over-engineering (built when a simpler approach existed)
- Responsiveness issues (slow replies, timeouts, retries)
- Communication issues (user had to repeat themselves)

### 4. Skill Gap Analysis

Search for skills that address identified struggles. For each promising skill:
- Note name, version, relevance score
- Assess whether it genuinely solves the problem vs. being a low-quality wrapper
- Recommend install only if it clearly saves future effort

Also check: are any installed skills underused or misconfigured?

### 5. Config & Infrastructure Review

Check for improvements to:
- **Cron jobs**: Any consistently failing? Should any be added/removed?
- **Auth/credentials**: Any expired, rotated, or missing?
- **Memory/context**: Is MEMORY.md getting stale? Are daily logs being written?
- **Tool config**: Any env vars, API keys, or integrations that need attention?
- **Workspace hygiene**: Temp files, stale scripts, orphaned projects?

### 6. Recommendations

Produce a prioritised action list:
1. **Quick wins** (< 5 min each) — config fixes, skill installs, cleanup
2. **Medium effort** (< 1 hour) — new automations, script fixes, unblocking items
3. **Larger projects** — new integrations, architectural changes

Each recommendation must be specific and actionable (not "improve scraping" but "install X to bypass Cloudflare on Y").

## Output Format

Write the retro to `memory/retro-YYYY-MM-DD.md`:

```markdown
# Retrospective — [date range]

## Wins
- [concrete win with evidence]

## Struggles
| Task | Root Cause | Time Spent | Recurring? |
|------|-----------|------------|------------|
| ... | ... | ... | yes/no |

## Skill Gaps
| Problem | Skill | Action |
|---------|-------|--------|
| ... | skill-name v1.0 | install / skip / evaluate |

## Config Issues
- [specific issue + fix]

## Action Items
### Quick Wins
1. [action]

### Medium Effort
1. [action]

### Larger Projects
1. [action]
```

## Scheduling

Set up a weekly cron job on first use (check `cron(action="list")` first — only create once):

```
cron(action="add", job={
  "name": "Weekly Retrospective",
  "schedule": {"kind": "cron", "expr": "0 16 * * 5", "tz": "local"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run a full retrospective for the last 7 days following the retrospective skill. Read memory files, check cron status, search for skills addressing struggles, write retro to memory/retro-YYYY-MM-DD.md, update MEMORY.md with key findings, deliver a concise summary."
  },
  "delivery": {"mode": "announce"}
})
```

## Guidelines

- **No fluff.** Every line should contain information.
- **Be self-critical.** The point is improvement, not a highlight reel.
- **Cite evidence.** Reference specific memory files, dates, error messages.
- **Don't recommend skills blindly.** Only recommend if genuinely useful.
- **Cap action items at 10.** Prioritise ruthlessly.
- **Update MEMORY.md** with key findings after the retro.
