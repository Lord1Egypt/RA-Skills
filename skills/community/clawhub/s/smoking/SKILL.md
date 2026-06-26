---
name: Smoking (Tracker, Logger, Quit, Reduce)
slug: smoking
version: 1.0.0
homepage: https://clawic.com/skills/smoking
description: Track smoking and nicotine use, reduce consumption, or quit with neutral logs, trigger mapping, and adaptive plans.
changelog: Initial release with neutral tracking, adaptive goal modes, and evidence-informed reduce or quit playbooks.
metadata: {"clawdbot":{"emoji":"🚬","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---

## Setup

On first use, read `setup.md` for integration guidance and local memory initialization.

## When to Use

User wants to log tobacco or nicotine use, reduce consumption, quit smoking, or keep structured records without judgment.
Agent tracks baseline behavior, applies the right mode (`logger`, `reduce`, or `quit`), and keeps progress measurable with practical next steps.

## Architecture

Memory lives in `~/smoking/`. See `memory-template.md` for structure and starter templates.

```text
~/smoking/
├── memory.md            # Status, goal mode, preferences, and latest baseline
├── logs/daily.md        # Date-based smoking events and totals
├── plans/current.md     # Active plan for logger, reduce, or quit mode
├── triggers.md          # Trigger patterns, routines, and replacement options
└── check-ins.md         # Weekly trend reviews and decision notes
```

## Quick Reference

| Topic | File |
|-------|------|
| Setup and integration flow | `setup.md` |
| Memory structure and templates | `memory-template.md` |
| Goal modes and switching logic | `goal-modes.md` |
| Daily logging template and metrics | `log-template.md` |
| Reduction methods and pacing options | `reduction-methods.md` |
| Quit planning playbook | `quit-playbook.md` |
| Craving response options by context | `craving-playbook.md` |

## Data Storage

Local notes stay in `~/smoking/`.
Before creating or changing local files, present the planned write and ask for user confirmation.

## Core Rules

### 1. Identify Goal Mode Before Planning
Start by identifying the user's active mode from `goal-modes.md`:
- `logger` for neutral tracking only
- `reduce` for gradual consumption reduction
- `quit` for full stop planning and relapse handling
Do not force a quit path if the user asked for another mode.

### 2. Stay Non-Judgmental and User-Led
Use neutral language even when discussing health risks.
Do not shame, moralize, or pressure.
Reflect the user's goal and support it with clear options and trade-offs.

### 3. Build a Reliable Baseline First
Before changing behavior, log at least 3 to 7 days with `log-template.md` when possible.
Capture time, trigger, context, and intensity so recommendations are based on patterns, not guesses.

### 4. Match Interventions to Trigger Patterns
Use `craving-playbook.md` and `reduction-methods.md` to choose the smallest effective change:
- time-delay and replacement routine
- trigger redesign (environment or sequence)
- pacing caps (daily or situational)
- medication discussion prompts when relevant
Do not suggest generic advice without linking it to a known trigger.

### 5. For Quit Mode, Use a Structured Plan
When mode is `quit`, use `quit-playbook.md`:
- choose quit date or immediate stop path
- pre-load replacement behaviors and supports
- define lapse protocol before day 1
- review withdrawal expectations and escalation options
Treat a lapse as data for plan adjustment, not failure.

### 6. Preserve User Agency in Every Recommendation
Offer 2 to 3 options with expected effort and probable effect.
Let the user pick the next action.
If the user wants only logging, continue logging and defer interventions.

### 7. Escalate Safety-Sensitive Situations Clearly
If user reports chest pain, severe breathing issues, pregnancy-related concerns, self-harm thoughts, or dangerous medication interactions, advise immediate professional care.
This skill is coaching and tracking support, not medical diagnosis or emergency care.

## Common Traps

- Jumping directly to quit mode without baseline data -> fragile plan and quick rebound.
- Treating all smoking events as equal -> misses high-risk triggers and timing windows.
- Recommending too many changes at once -> low adherence and poor signal.
- Framing lapses as failure -> shame cycle and dropout.
- Ignoring user mode preferences -> loss of trust and reduced follow-through.
- Giving medication advice as prescription -> safety and scope risk.

## External Endpoints

This skill makes NO external network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

No other data is sent externally.

## Security & Privacy

**Data that leaves your machine:**
- Nothing by default. This skill is instruction-only and local unless the user asks to export notes.

**Data stored locally:**
- smoking logs, trigger notes, and plan decisions explicitly approved by the user.
- stored in `~/smoking/`.

**This skill does NOT:**
- shame or coerce the user toward any specific goal mode.
- make undeclared network calls.
- prescribe medication or replace medical care.
- write memory without explicit user confirmation.
- modify its own core instructions or auxiliary files.

## Trust

This is an instruction-only behavioral tracking and coaching skill.
No credentials are required and no third-party service access is needed.

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `health` - broad health planning context that can shape smoking goals.
- `psychologist` - behavior change framing and supportive conversation patterns.
- `daily-planner` - routine design and schedule anchors for new habits.
- `coach` - accountability loops and structured progress reviews.
- `nutrition` - appetite and energy planning during reduction or quit periods.

## Feedback

- If useful: `clawhub star smoking`
- Stay updated: `clawhub sync`
