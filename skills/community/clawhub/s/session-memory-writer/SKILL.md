---
name: session-memory-writer
version: 1.0.0
description: Write structured task outcome blocks to memory/YYYY-MM-DD.md at session
  end. Enforces format consistency for Langfuse backfill, Quill journal generation,
  and QMD search. Use after every subagent completion.
metadata:
  openclaw:
    emoji: 🧠
---

# SKILL: session-memory-writer

**Use when:** Writing `memory/YYYY-MM-DD.md` at the end of a session, or logging any subagent task outcome.

**Why this exists:** Memory files are the single source of truth for Langfuse backfill, Quill journal generation, Liv's CCP updates, and QMD search. Format drift = invisible tasks = broken observability. The regex parsers don't forgive variation.

---

## 1. Task Outcome Block (mandatory for every subagent completion)

Every agent task gets **exactly** this structure. No exceptions.

```markdown
### [AgentName] Task — YYYY-MM-DD HH:MM
- **Task:** one-line description of what was asked
- **Outcome:** ✅ complete / ⚠️ partial / ❌ failed
- **Metric:** pass/fail, score, or N/A
- **Kept:** yes / no / pending-review
- **Time:** ~X minutes
- **Notes:** what worked, what didn't, key decisions, surprises
```

**Real examples from 2026-03-24:**
```markdown
### Kit Task — 2026-03-24 06:45
- **Task:** Rebuild /setup page — full agent configuration wizard (5 tabs)
- **Outcome:** ✅ complete
- **Metric:** pass — clean build, 200 on live URL
- **Kept:** yes
- **Time:** ~15 min
- **Notes:** Built all 5 tabs with localStorage persistence. No features cut. Clean TypeScript build first pass.
```

### Why the format is non-negotiable

`langfuse-backfill-historical.py` uses this regex pattern to find task blocks:

```
### [Name] Task — YYYY-MM-DD
```

The **em-dash** (`—`) and **space on both sides** are required. These all break the parser:

| ❌ Wrong | Why it fails |
|---|---|
| `### Kit Task 2026-03-24` | Missing `—` separator — regex miss |
| `### Kit Task: 2026-03-24` | Colon instead of em-dash — regex miss |
| `### Kit Task —\n2026-03-24` | Date on separate line — regex miss |
| `- **Outcome:** done` | Not `✅ complete` — field extraction returns empty |
| `- **Outcome:** complete ✅` | Emoji at end, not start — field extraction may miss |

---

## 2. Daily File Structure

**Naming:** `memory/YYYY-MM-DD.md`

One file per day. **Append throughout the day — never overwrite.**

Dream cycle archives files >7 days old to `memory/archive/`.

**Typical file structure (top to bottom):**

```markdown
# Daily Log — YYYY-MM-DD (Day)
_AEST timezone. Written end-of-day._

---

## Summary
[Optional 2-3 sentence overview — only for full sessions]

---

## Cross-Repo Activity — YYYY-MM-DD [Dream Cycle]
[Automatically captured — don't write this manually]

---

### [Agent] Task — YYYY-MM-DD HH:MM
[Task block — see Section 1]

### [Agent] Task — YYYY-MM-DD HH:MM
[Next task block]

---

### Loki Session — YYYY-MM-DD HH:MM–HH:MM (MAIN SESSION)
[Session summary block — see Section 3]
```

---

## 3. Loki Session Summary Block

For the main session (Loki's own summary at end of day):

```markdown
### Loki Session — YYYY-MM-DD HH:MM–HH:MM (MAIN SESSION)
- **Projects touched:** [list]
- **Outcome:** ✅/⚠️/❌ + brief summary

#### Deliverables this session
1. [numbered list — one line per deliverable]

#### Key decisions
- [append-only, dated — architecture choices, trade-offs made]

#### Blockers / Next
- [what's pending, who owns it, expected resolution]
```

---

## 4. OUTBOX Entry Format

Write OUTBOX entries in `OUTBOX.md` (agents append here; Quill reads it to write journals).

```markdown
## YYYY-MM-DD — [Short description of work]

**Tasks completed:**
1. [Brief description of each major deliverable]

**Key technical decisions:**
- [Non-obvious choices made]

**Repos touched:** [repo names + commit hashes if known]
```

**Write an OUTBOX entry when:**
- Agent completed >1 significant task in a session
- Work touched a shared codebase
- A lesson was learned that other agents should know
- A Notion journal entry would be worth writing

**Skip OUTBOX when:**
- Single minor task (e.g. fixed a typo, updated a README)
- No code shipped, no decisions made
- Routine heartbeat check with nothing found

---

## 5. What to Capture vs Skip

### Always capture
- Every subagent task completion (task block, even short ones)
- Key decisions that affected architecture or priorities
- Non-obvious fixes — these become skill content
- Blockers with owner and expected resolution
- Tool commands that worked after debugging

### Skip
- Internal tool calls that changed nothing
- Routine tasks with no learning ("updated the README")
- Heartbeat checks unless something was found
- Chat filler and clarification exchanges
- Dead ends that led nowhere useful

---

## 6. Downstream Dependencies (why format matters)

| Consumer | What it depends on | What breaks if format drifts |
|---|---|---|
| `langfuse-backfill-historical.py` | `### [Name] Task — YYYY-MM-DD` header pattern | Task not extracted → gap in Langfuse observability |
| Quill journal pipeline | OUTBOX `## YYYY-MM-DD — ` headers | Quill misses entries or writes empty journals |
| Liv CCP session update | Task outcome blocks to build Notion daily log body | Notion log is empty or incomplete |
| QMD memory search | Consistent structure across files | Retrieval quality degrades; semantic search misses context |

---

## 7. Common Mistakes

| Mistake | Fix |
|---|---|
| `### Kit Task:` (colon) | Use `### Kit Task —` (em-dash, spaces) |
| Date on separate line from header | Keep date on same line: `### Kit Task — 2026-03-24 14:00` |
| `Outcome: done` | Use exactly `✅ complete` / `⚠️ partial` / `❌ failed` |
| Skipping the Notes field | **Most important field** — this is what gets turned into skills and journals |
| One giant session block | One block **per task**, not per session |
| Writing prose narrative instead of task blocks | Prose is unreadable to parsers. 2026-03-23.md is the cautionary example. |
| Forgetting the time | Approximate is fine (`~10 min`) — needed for Langfuse duration metadata |

---

## 8. Quick Reference — Copy-Paste Templates

**Task block:**
```markdown
### [AgentName] Task — YYYY-MM-DD HH:MM
- **Task:** 
- **Outcome:** ✅ complete
- **Metric:** pass
- **Kept:** yes
- **Time:** ~X min
- **Notes:** 
```

**Session summary:**
```markdown
### Loki Session — YYYY-MM-DD HH:MM–HH:MM (MAIN SESSION)
- **Projects touched:** 
- **Outcome:** ✅ 

#### Deliverables this session
1. 

#### Key decisions
- 

#### Blockers / Next
- 
```

**OUTBOX entry:**
```markdown
## YYYY-MM-DD — [Short description]

**Tasks completed:**
1. 

**Key technical decisions:**
- 

**Repos touched:** 
```
