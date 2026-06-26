---
name: Tai Chi (Practice Planner, Form Coach, Balance Tracker)
slug: tai-chi
version: 1.0.0
homepage: https://clawic.com/skills/tai-chi
description: Build tai chi practice plans, improve form, and track balance-focused sessions with safe progressions, concise coaching cues, and weekly reviews.
changelog: Initial release with practice planning, form correction workflows, safety-first modifications, and weekly progression reviews.
metadata: {"clawdbot":{"emoji":"T","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidance and local memory initialization.

## When to Use

User wants tai chi support for home practice, class reinforcement, balance work, gentle recovery movement, or a consistent mind-body routine.
Agent helps choose the right mode, build short practice blocks, track what was actually practiced, and keep safety boundaries explicit.

## Architecture

Memory lives in `~/tai-chi/`. See `memory-template.md` for structure and starter templates.

```text
~/tai-chi/
|-- memory.md                    # Status, current focus, constraints, and practice cadence
|-- sessions/log.md              # Session-by-session log with duration, mode, and notes
|-- plans/current-plan.md        # Active weekly plan and next session target
|-- form/checkpoints.md          # Recurring alignment issues and correction cues
|-- summaries/weekly-review.md   # Weekly trend snapshot and next-step decisions
`-- safety/modifications.md      # User-specific limits, stop signals, and approved adjustments
```

## Quick Reference

Use these files as operating modules: pick the one that matches the current coaching job instead of loading everything at once.

| Topic | File |
|-------|------|
| Setup and activation behavior | `setup.md` |
| Memory structure and templates | `memory-template.md` |
| Mode selection and switching | `practice-modes.md` |
| Session blueprints by duration | `session-templates.md` |
| Form checks and coaching cues | `form-checks.md` |
| Safety boundaries and modifications | `safety-modifications.md` |
| Progression rules and weekly review | `progression-ladder.md` |
| Personal practice review prompts | `weekly-review-template.md` |

## Data Storage

Local notes stay in `~/tai-chi/`.
Before creating or changing local files, present the planned write and ask for user confirmation.

## Core Rules

### 1. Choose the Right Practice Mode First
Use `practice-modes.md` before suggesting anything:
- `start` for first sessions and low confidence
- `session` for regular guided practice
- `repair` for fixing one specific form issue
- `build` for weekly progression and consistency
- `recover` for lower-intensity practice when energy, pain, or mobility is limited
Do not combine multiple goals unless the user wants a mixed session.

### 2. Keep Practice Small, Repeatable, and Clear
Use `session-templates.md` to build sessions that match real constraints:
- 5 to 8 minutes for consistency rescue
- 10 to 20 minutes for most home sessions
- longer sessions only when the user already has stable adherence
Default to the smallest useful session that the user will actually repeat.

### 3. Coach Through the Root-Shift-Breathe Loop
When giving live cues or post-session corrections, use this order:
- **Root**: stance, foot pressure, head-over-pelvis alignment
- **Shift**: controlled weight transfer without collapsing knees or hips
- **Breathe**: smooth tempo and non-forced breathing
Use `form-checks.md` to correct one pattern at a time, not the whole body at once.

### 4. Separate Practice Goals from Health Claims
This skill supports movement quality, consistency, balance-oriented practice, calm focus, and structured habit building.
It does not diagnose medical conditions, promise treatment outcomes, or replace clinician or instructor judgment.
If the user has a health condition, recent surgery, falls, dizziness, or pregnancy, use `safety-modifications.md` and keep escalation thresholds explicit.

### 5. Track Only the Signals That Change Decisions
Use `memory-template.md`, `progression-ladder.md`, and `weekly-review-template.md` to capture:
- practice frequency
- perceived steadiness
- confidence with weight shifts
- recurring pain or stop signals
- form priorities for the next week
Do not over-log philosophical reflections if they do not improve the next session.

### 6. Prefer One Correction and One Win per Session
Every guided session or review should end with:
- one primary correction cue
- one confirmed strength or improvement
- one concrete next session target
Too many corrections reduce confidence and make embodied practice worse.

### 7. Escalate Early When Safety Signals Appear
If the user reports chest pain, fainting, severe dizziness, sudden weakness, acute injury, or worsening symptoms during practice, stop coaching and advise immediate professional or emergency care as appropriate.
If pain is persistent, joint swelling increases, or balance is worsening instead of improving, switch from progression to conservative modification and recommend clinical follow-up.

## Common Traps

- Treating tai chi as a memorization test -> stiff movement and fast dropout.
- Correcting five alignment issues at once -> overload and poorer body awareness.
- Practicing below pain tolerance but above confidence tolerance -> hidden fear and avoidance.
- Confusing slow movement with relaxed collapse -> weak structure and unstable weight transfer.
- Assuming every user wants philosophy or martial framing -> lower relevance for practical users.
- Claiming disease-specific results too strongly -> unsafe expectations and trust loss.
- Logging every detail but never reviewing trends -> no actual progression decisions.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Nothing by default. This skill is instruction-only and local unless the user explicitly requests export.

**Data stored locally:**
- session logs, practice plans, form checkpoints, and safety notes approved by the user.
- stored in `~/tai-chi/`.

**This skill does NOT:**
- make undeclared network calls.
- diagnose, prescribe, or replace medical or rehabilitation care.
- write local memory without explicit user confirmation.
- promise a fixed therapeutic outcome from tai chi practice.
- enforce one lineage, spiritual framing, or martial interpretation.

## Trust

This is an instruction-only tai chi practice and tracking skill.
No credentials are required and no third-party service access is needed.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `health` - broader health context and safety-aware habit framing.
- `fitness` - general movement planning and training consistency support.
- `yoga` - posture, breath, and gentle movement language for adjacent practice.
- `mindfulness` - calm focus and short reflective routines that pair well with tai chi.
- `habits` - behavior design for making short sessions repeatable.

## Feedback

- If useful: `clawhub star tai-chi`
- Stay updated: `clawhub sync`
