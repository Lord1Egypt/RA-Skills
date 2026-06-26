# Skill Evolution

## How to use this file

**Trigger**: After any run with a repeatable fix or a config/workflow change that improves results → propose a new entry following below **Approval** protocol.
If uneventful, skip.

## Purpose

Store all practical experience from real usage. Gotchas capture failures; Success Patterns capture what worked well. This skill evolves through both.

**Main SKILL.md**: Keep 3 most critical Gotchas and 3 most recent Success Patterns in SKILL.md. This file holds the full archive.

**Workflow:**
- Commit baseline before changes
- Helped → Success Patterns entry. Worse/Pitfalls → undo if needed then log as gotcha

- **Approval**: 
  - SKILL.md table updates and escalation of severe gotchas
  to Critical Directives require user approval.
  - Entries here (full archive as below) are just recording — no approval needed, but be smart to record

**What to record vs Gotchas** (some items could go either way):
- Parameter tuning that improved performance — **Success Pattern**
- Workflow redesign that proved reliable — **Success Pattern**
- Any eventful experience that made this skill better — **Success Pattern**
- Failures with a repeatable fix — **Gotcha**
- Trivial changes (e.g., fixing a typo) — **neither**


## Gotchas Archive
| ID | Date | Issue / Symptom | Fix |
|----|------|-----------------|-----|
| G01 | 2026-05-30 | Memory reliance — wrote Success Patterns from stale context/injected text, not current file | Read the file now before any edit — context freezes at load time |
| G02 | 2026-05-30 | Closure seeking — after description + skillSearchList fix, assumed workflow done, skipped evolution-approval step | Review the full step checklist after each sub-task |
| G03 | 2026-05-30 | Cognitive laziness — skipped reading `skill-evolution.md` reference; also wrote to template table instead of zao-skill's own Gotchas/Success Patterns | Follow every "see references/X" instruction; scan for ambiguity (two tables with same name)


## Success Patterns
> Free-form entries. Record what worked, why, and what was learned.
> Each entry starts with `### YYYY-MM-DD — summary`; context inline.

### YYYY-MM-DD — (example) Increased response accuracy
By adjusting the temperature parameter from 0.7 to 0.3 for factual
queries, accuracy improved from 82% to 94%. The change was validated
across 3 different skill types. Lower temperature may not work well
for creative tasks — keep that in mind.

...
