---
name: taku-reflect
description: >
  User-invoked reflection. Three modes: Learn (script-backed recording, searching,
  pruning, exporting, and optional bootstrap for user-approved patterns, pitfalls,
  preferences, discoveries), Retro (weekly engineering retrospective with git commit analysis,
  metrics, team breakdowns, trends), and Write Skill (codify recurring learnings into reusable skills).
  Triggers on "what have we learned", "add learning", "show learnings", "weekly retro",
  "what did we ship", "engineering retrospective", "write a skill", "create a skill",
  "codify this pattern", "总结一下", "学到了什么", "记录一下", "回顾这周",
  "做个retro", "写个技能", "把这个模式固化". Also invoke when the user expresses
  satisfaction or frustration after completing work — these are natural reflection moments.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Reflect — Learn + Retro + Write Skill

Three modes: capture learnings (default), weekly retrospective, or codify recurring patterns into skills.

Rule labels: `[IRON LAW]` means a non-negotiable correctness constraint. `[GUIDANCE]` means a strong default that may adapt when context justifies it.

## Mode Selection

- **Learn** (default): "what have we learned", "add learning", "show learnings", "prune learnings"
- **Retro**: "weekly retro", "what did we ship", "retrospective", or `--retro` flag
- **Write Skill**: "write a skill", "create a skill", "codify this pattern", "edit this skill"

---

## Learn Mode

Capture only what the user explicitly wants to preserve so future sessions can reuse it.

### Invocation Rule

[IRON LAW] `/taku-reflect` is manual. Do not create or update long-term learnings unless the user explicitly invokes reflect.

### Storage

Learnings live in `.taku/learnings/{project-slug}.jsonl`. Each line:

```json
{"id":"L2026-04-21-001","timestamp":"2026-04-21T12:00:00Z","type":"preference/high","context":"Multi-file repository change","learning":"User prefers plan-first before non-trivial edits","action":"Start with code reading and short execution plan","apply_when":{"task_types":["feature","refactor","bugfix"],"keywords":["multi-file","plan","design"]},"status":"active"}
```

### Types

Each type includes a confidence suffix: `/high`, `/medium`, or `/low`.

- **pattern** — A reusable approach that worked well
- **pitfall** — A mistake to avoid
- **preference** — A user-stated preference or convention
- **discovery** — A non-obvious insight about the codebase

Confidence meanings: **high** — verified by testing or user confirmation. **medium** — observed pattern, likely correct. **low** — hypothesis, needs validation.

### Required Fields

**Auto-generated** (no user confirmation needed):
- `id` — Stable identifier, auto-generated as `L{date}-{seq}`
- `timestamp` — ISO8601 UTC, auto-generated
- `status` — Defaults to `active`; only changes during PRUNE

**User confirms:**
- `type` — `pattern|pitfall|preference|discovery` with `/confidence` suffix (e.g., `pattern/high`, `pitfall/medium`)
- `context` — What work this came from
- `learning` — The reusable takeaway
- `action` — What future sessions should do
- `apply_when` — Task types and keywords for later recall (`task_types` + `keywords`)

### Script-Backed Operations

Use `scripts/learnings.py` for all learnings file operations. Do not hand-edit `.taku/learnings/*.jsonl` unless the script is unavailable and the user explicitly approves a fallback.

**ADD:** Gather `type` (with confidence suffix), `context`, `learning`, `action`, and minimal `apply_when` values. Append only after the user confirms the learning should be kept.

```bash
python3 <path-to-this-skill>/scripts/learnings.py add --project-root . --type preference/high --context "..." --learning "..." --action "..." --task-types feature,refactor --keywords plan,design
```

**SEARCH:** Query existing learnings through the script and present matches grouped by type when useful.

```bash
python3 <path-to-this-skill>/scripts/learnings.py search --project-root . --query "plan" --task-type feature --keywords plan,design
```

**PRUNE:** Use the script to list stale or low-confidence candidates. Present each flagged entry: Remove / Keep / Update. Do not delete automatically.

```bash
python3 <path-to-this-skill>/scripts/learnings.py prune --project-root . --days 30
```

**EXPORT:** Convert to markdown through the script. Offer to append exported content to `AGENTS.md` or `CLAUDE.md` only when the user confirms an upgrade.

```bash
python3 <path-to-this-skill>/scripts/learnings.py export --project-root .
```

**Why JSONL over markdown:** JSONL entries can be searched with grep, parsed programmatically, and deduplicated. Markdown learnings files become unstructured text that's hard to query or prune.

### Auto-Recall

Other Taku phases may search existing learnings automatically, but only as context:

- Search with `scripts/learnings.py search` after task classification and before PLAN, BUILD, REVIEW, and VERIFY
- Filter by task type and simple keyword overlap
- Prefer `high` confidence, then `medium`
- Show at most 3-5 relevant learnings

This recall must never create, edit, or prune learnings. Long-term memory changes happen only inside `/taku-reflect`.

### Project Bootstrap

On the first successful reflect run for a project, check whether the project-level instruction files advertise the optional Taku learnings protocol.

**When to check:**

- `.taku/` already exists or this reflect run is about to create `.taku/learnings/{project-slug}.jsonl`
- Run `python3 <path-to-this-skill>/scripts/learnings.py bootstrap-check --project-root .`
- Treat the result as a suggestion only

**Target selection:**

- If only `AGENTS.md` exists, suggest installing the protocol there
- If only `CLAUDE.md` exists, suggest installing the protocol there
- If both files exist, suggest installing the same protocol block into both files so non-Taku sessions do not depend on which project instruction file gets loaded
- If one file already has the block and the other does not, suggest installing only the missing file
- If neither file exists, do not create one automatically; note that no project-level bootstrap target exists yet

**Protocol block:** The script owns this exact block.

```md
<!-- TAKU_LEARNINGS_PROTOCOL:START -->
## Taku Learnings

If `.taku/learnings/{project-slug}.jsonl` exists, consult it before non-trivial planning, implementation, review, or debugging. Treat matching entries as context, not hard rules.

Do not create, edit, or prune learnings unless the user explicitly invokes `/taku-reflect`. Only stable repeated preferences should be promoted into project-level instructions.
<!-- TAKU_LEARNINGS_PROTOCOL:END -->
```

**Rules:**

- This is a bootstrap protocol, not a promotion of specific learnings
- The JSONL file is the canonical source; `AGENTS.md` and `CLAUDE.md` are optional discovery layers
- Detect existing installation by the `TAKU_LEARNINGS_PROTOCOL` markers
- Never install automatically. Show a `Project Bootstrap Suggestion`; if the user explicitly says to install it, run:

```bash
python3 <path-to-this-skill>/scripts/learnings.py bootstrap-install --project-root . --targets AGENTS.md,CLAUDE.md
```

### Output Format

When running learn mode, organize results as:

- **Recorded** — learnings added or updated in this reflect run
- **Relevant Existing Learnings** — prior entries relevant to the current work
- **Promotion Suggestions** — suggestions only; do not upgrade anything automatically
- **Project Bootstrap Suggestion** — suggest installing the Taku learnings protocol in `AGENTS.md` and/or `CLAUDE.md` when the project has not been bootstrapped yet

---

## Retro Mode

Analyze what the team shipped, how the work happened, and where to improve. Evidence-based, specific, candid.

Use `references/retro-report.md` as the local report scaffold; fill it with evidence from the steps below and remove placeholders.

### Arguments

- `/taku-reflect` — learn mode (default)
- `/taku-reflect --retro` — last 7 days
- `/taku-reflect --retro 14d` — last 14 days
- `/taku-reflect --retro 30d` — last 30 days

### Step 1: Gather Raw Data

```bash
git config user.name && git config user.email
git log origin/<base> --since="<window>" --format="%H|%aN|%ae|%ai|%s" --shortstat
git log origin/<base> --since="<window>" --format="COMMIT:%H|%aN" --numstat
git log origin/<base> --since="<window>" --format="" --name-only | grep -v '^$' | sort | uniq -c | sort -rn
git shortlog origin/<base> --since="<window>" -sn --no-merges
```

### Step 2: Compute Metrics

Summary: commits, contributors, PRs, insertions, deletions, net LOC, test LOC ratio, active days, sessions, avg LOC/session-hr. Per-author leaderboard sorted by commits.

### Step 3: Time & Session Patterns

Hourly histogram. Detect sessions (45-min gap). Classify: Deep (50+ min), Medium (20-50), Micro (<20).

### Step 4: Work Patterns

Commit type breakdown by conventional prefix. Flag fix ratio > 50%. Hotspot analysis: top 10 files. Flag files changed 5+ times.

### Step 5: Team Member Analysis

For each contributor: commits, LOC, test ratio, areas, biggest ship.
**Praise** (anchored in commits): 1-2 things. **Growth area** (framed as investment): 1 thing.

### Step 6: Week-over-Week Trends

Load prior retro from `.taku/retros/`. Compare key metrics.

### Step 7: Narrative

Output: Summary table + trends, Time & sessions, Your week + team, Top 3 Wins + 3 Improvements + 3 Habits.

### Step 8: Save

Save to `.taku/retros/{date}.md`. Append trends to `.taku/retros/trends.jsonl`.

---

## Write Skill Mode

Codify recurring patterns into reusable skills, but only after the user confirms they want to write one.

Full process in `references/writing-skills.md`. Load it and follow the instructions. That reference is substantial (~200 lines) with its own anti-rationalization table and known pitfalls — it functions as a self-contained skill within the reflect directory, not a lightweight helper.

Quick summary:
- Choose skill type: TECHNIQUE (concrete method), PATTERN (mental model), REFERENCE (lookup table)
- Follow RED-GREEN-REFACTOR: baseline test → write minimal skill → close loopholes
- Keep under 500 lines; split to `references/` if needed
- Description field: triggering conditions only, never summarize workflow

### Promotion Paths

Keep upgrades narrow. Only suggest these two:

1. **Project-level constraint candidate**
   - Condition: `type=preference/high`, repeated or confirmed 2+ times
   - Suggestion: propose upgrading the preference into `AGENTS.md` if present, otherwise `CLAUDE.md`
   - Rule: never write the file automatically; ask the user first

2. **Write Skill candidate**
   - Condition: the same pattern, pitfall, or decision method recurs across 2-3 sprints
   - Suggestion: `This pattern keeps recurring. Suggest codifying it as a skill.`
   - Rule: ask the user whether to proceed before loading `references/writing-skills.md`

Bootstrap is separate from promotion. Installing the Taku learnings protocol in `AGENTS.md` or `CLAUDE.md` only makes the knowledge base discoverable; it must not be used to smuggle concrete learnings past the promotion rules above.

---

## Anti-Rationalization

| Excuse | Why it's wrong |
|--------|---------------|
| "I'll remember this" | You won't. Next session starts fresh. Write it down. |
| "This is too obvious to log" | Obvious now. Not obvious in 3 weeks after 50 other sessions. |
| "We didn't do much this week" | Even small weeks have patterns worth examining. |
| "Retros waste time" | 5 minutes of reflection saves hours of repeated mistakes. |

## Known Pitfalls

**Learnings file becomes a dumping ground.** Over 30 sessions, 200+ entries. Most trivial. Signal buried in noise.

*Prevention:* Use PRUNE regularly. Every 30 days, remove trivial observations, update stale patterns, delete low-confidence entries. 30 high-quality insights > 200 entries of noise.

**Retro becomes a vanity metric exercise.** "142 commits, 8,400 lines." But 6,000 were generated code and 40 were auto-bumps.

*Prevention:* Step 4 computes commit type breakdown and flags fix ratio. Note when metrics are inflated. Value is in analysis, not numbers.

**Saving learnings but never searching them.** 50 learnings recorded, none referenced. Team repeated the same mistake 3 times.

*Prevention:* Auto-search relevant learnings in later phases as context. Query the knowledge base, don't just write to it.

**Auto-upgrading without consent.** A repeated preference was detected and silently written into a project rule file. The user disagreed with the wording and had to undo it.

*Prevention:* Promotion Suggestions are suggestions only. Upgrades to `AGENTS.md`, `CLAUDE.md`, or a new skill always require explicit user confirmation first.

**Bootstrap drift between `AGENTS.md` and `CLAUDE.md`.** One file mentioned `.taku/learnings` and the other did not. Different agents got different behavior depending on which instruction file they loaded.

*Prevention:* When both files exist, suggest injecting the exact same `TAKU_LEARNINGS_PROTOCOL` block into both. If only one file is missing the block later, patch only the missing file instead of rewriting both.
