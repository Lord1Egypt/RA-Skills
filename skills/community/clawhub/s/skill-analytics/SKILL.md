---
name: skill-analytics
description: "Monitor ClawHub skill performance with file-based state tracking. Fetches public stats via web_fetch, tracks recommendations and their outcomes, avoids repetitive suggestions. Day-of-week rotation for varied analysis focus. Use when: (1) cron fires daily analytics, (2) user asks about skill performance, (3) adoption strategy or growth advice, (4) 'how is my skill doing', 'skill stats'. Homepage: https://clawhub.ai/skills/skill-analytics"
---

# Skill Analytics v2.0

**Install:** `clawhub install skill-analytics`

ClawHub skill portfolio monitoring with state tracking. Remembers what it recommended.

## Language

Detect from user's message language. Default: English.

## State Files

All state stored in `memory/skill-analytics/`:

| File | Purpose |
|------|---------|
| `state.json` | Rotation day, last run, recommendation IDs |
| `recommendations.md` | Active recommendations with status |
| `ideas-tried.md` | Topics already covered (avoid repeats) |

Create directory and files on first run if they don't exist.

## Day-of-Week Rotation

Use day-of-week (Monday=1, Sunday=7) from `state.json` (not current calendar day — track continuously):

| Day | Focus |
|-----|-------|
| 1 | Adoption Funnel |
| 2 | Competitive Analysis |
| 3 | Content & Copy |
| 4 | Feature Gap |
| 5 | Monetization |
| 6 | Cross-Promotion |
| 7 | Wildcard |

After each run: increment day in `state.json`, wrap at 7.

## Anti-Repetition Protocol

Before generating recommendations:

1. Read `memory/skill-analytics/recommendations.md`
2. Read `memory/skill-analytics/ideas-tried.md`
3. **Skip** any recommendation already listed as "Pending" or already tried
4. Only generate NEW recommendations
5. If no new insights exist: say "No new recommendations this run. Previous {N} are still pending."

### Recommendation Format

```markdown
| # | Recommendation | Date | Status | Result |
|---|---------------|------|--------|--------|
| 1 | **Short title** — one-line action | YYYY-MM-DD | Pending | - |
```

After user marks as done: change Status to "✅ Completed" with Result.

## Data Collection

Use built-in tools only (web_fetch, web_search):

```
web_fetch https://clawhub.ai/tommot2/{slug}
web_search "clawhub {skill category}"
```

Extract: downloads, installs, stars, version count.

**No CLI tools, no npm packages, no credentials.**

## Output Format

```
## 📊 Skill Analytics — {date}

### Dashboard
| Skill | DL | ⭐ | Versions |
|-------|---:|:--:|:--------:|
| ... | ... | ... | ... |

### Focus: {day focus}
{2-3 paragraphs of actual analysis. Concrete numbers.}

### New Recommendations
1. **{title}** — {one-line action}
   - Effekt: {estimated}
   - Innsats: {Lav/Middels/Høy}

### Previous Status
- Pending: {N} recommendations
- Completed: {N} recommendations
- Skipped (repeats): {N}

### Next Run
Focus: Day {N+1} — {focus}
```

## Phase Indicator

Based on total installs across portfolio:

| Phase | Installs | Focus |
|-------|:--------:|-------|
| 🌱 Seed | 0-10 | Visibility |
| 🌿 Grow | 10-100 | Conversion |
| 🌳 Scale | 100-1000 | Monetization |
| 🏢 Sustain | 1000+ | Retention |

## Quick Commands

| User says | Action |
|-----------|--------|
| "skill stats" | Quick dashboard |
| "skill analytics" | Full analysis |
| "fulført #3" | Mark recommendation #3 as completed |
| "alle anbefalinger" | Show all with status |

## Guidelines for Agent

1. **Always read state before running** — check recommendations and ideas-tried
2. **Write state after running** — update state.json, add new recommendations
3. **Never repeat** — check ideas-tried.md before suggesting
4. **Use built-in tools only** — web_fetch and web_search
5. **No personal data in searches** — only public ClawHub data
6. **Keep output concise** — max 40 lines per report
7. **Language follows user**

## What This Skill Does NOT Do

- Does NOT read MEMORY.md, SOUL.md, or other workspace files
- Does NOT access credentials or private data
- Does NOT use external CLI tools or npm packages
- Does NOT modify any files outside `memory/skill-analytics/`

## More by TommoT2

- **context-brief** — Persistent context survival across sessions
- **setup-doctor** — Diagnose and fix OpenClaw setup issues
- **tommo-skill-guard** — Security scanner for installed skills

Install the full suite:
```bash
clawhub install skill-analytics context-brief setup-doctor tommo-skill-guard
```
