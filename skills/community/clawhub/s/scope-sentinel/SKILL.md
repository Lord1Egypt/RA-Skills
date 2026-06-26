---
name: scope-sentinel
version: 1.0.0
description: >
  Monitors your working session and detects when you've drifted from your
  stated task into unrelated changes. The coding equivalent of a GPS
  "recalculating" — notices when you've taken a wrong turn, tells you
  where you veered, and offers to get you back on track before you've
  refactored half the codebase "while you were in there."
author: J. DeVere Cooley
category: everyday-tools
tags:
  - focus
  - scope-management
  - productivity
  - discipline
metadata:
  openclaw:
    emoji: "🎯"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - productivity
---

# Scope Sentinel

> "The most expensive line of code is the one you didn't need to write. The most expensive refactor is the one you started 'while you were in there.'"

## What It Does

You sit down to fix a bug in the checkout flow. Two hours later you've reformatted the auth module, added types to three utility files, renamed a database column, and upgraded a dependency. The bug? Still there.

Scope Sentinel watches what you're *actually doing* and compares it to what you *said* you'd do. When the delta grows too large, it intervenes — not to stop you, but to make the drift *visible* so you can choose consciously.

## The Drift Model

### Scope Definition
At the start of a task, your scope is defined by:

```
SCOPE ANCHOR:
├── Task statement: "Fix checkout failing for international addresses"
├── Target files: src/checkout/address.ts, src/checkout/validation.ts
├── Target behavior: International addresses should pass validation
├── Branch name: fix/international-address-checkout
└── Estimated files to touch: 2-4
```

### Drift Detection
As you work, every file modification is classified:

| Classification | Description | Example |
|---|---|---|
| **On-scope** | Directly addresses the stated task | Fixing the address validation regex |
| **Adjacent** | Related to the task, reasonable to include | Updating the test for address validation |
| **Tangential** | Same area of code but different concern | Adding types to the checkout module |
| **Drift** | Different area, different concern | Refactoring the auth module |
| **Rabbit hole** | Deep change triggered by a discovery during on-scope work | Upgrading a dependency because you noticed it was outdated |

### The Drift Gradient

```
ON-SCOPE ──── ADJACENT ──── TANGENTIAL ──── DRIFT ──── RABBIT HOLE
   ✓              ✓             ⚠             🔴           🕳️
 "This is       "This is      "This is      "This is     "What year
  the fix"      part of       related but    a different   is it?"
                 the fix"     not the fix"   task"
```

## How It Works

```
Phase 1: ANCHOR
├── Capture the task statement (from branch name, commit message, or explicit declaration)
├── Identify the target area of the codebase
├── Establish the scope boundary (files, modules, behaviors)
└── Set drift tolerance (tight, normal, or exploratory)

Phase 2: MONITOR
├── For every file modification, classify:
│   ├── Is this file in the target area?
│   ├── Does this change relate to the stated task?
│   ├── Is this change necessary for the task to succeed?
│   └── Would this change make sense as a separate commit/PR?
├── Track accumulated drift:
│   ├── Files touched outside scope
│   ├── Lines changed outside scope
│   └── Time spent outside scope
└── Track scope expansion events (when you discover the task is bigger than expected)

Phase 3: ALERT
├── When drift accumulates past threshold:
│   ├── Name the drift ("You've started refactoring auth — this is unrelated to checkout")
│   ├── Quantify it ("4 files, 87 lines, ~25 minutes of off-scope work")
│   ├── Offer choices:
│   │   ├── STASH: Save off-scope changes for a separate task
│   │   ├── COMMIT SEPARATELY: Make a separate commit for the off-scope work
│   │   ├── EXPAND SCOPE: Acknowledge the scope grew (with justification)
│   │   └── CONTINUE: You're aware and choosing to continue
│   └── Log the decision for later review
└── Resume monitoring with updated scope (if expanded)

Phase 4: SESSION SUMMARY
├── At end of session, report:
│   ├── Time on-scope vs. time drifted
│   ├── Files changed on-scope vs. off-scope
│   ├── Drift events and how they were resolved
│   └── Suggested follow-up tasks for off-scope discoveries
```

## Alert Format

```
╔══════════════════════════════════════════════════════════════╗
║              SCOPE SENTINEL: DRIFT DETECTED                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  YOUR TASK: Fix checkout for international addresses         ║
║                                                              ║
║  DRIFT:                                                      ║
║  You've been modifying src/auth/middleware.ts for 18 minutes.║
║  This file is not related to checkout or address validation. ║
║                                                              ║
║  HOW YOU GOT HERE:                                           ║
║  checkout/address.ts → noticed untyped import                ║
║  → opened utils/types.ts to add types                        ║
║  → noticed auth/middleware.ts also uses these types           ║
║  → started "fixing" auth types too                           ║
║                                                              ║
║  ACCUMULATED OFF-SCOPE:                                      ║
║  ├── 3 files outside checkout/                               ║
║  ├── 47 lines of changes unrelated to the bug                ║
║  └── ~18 minutes of drift                                    ║
║                                                              ║
║  OPTIONS:                                                    ║
║  [1] STASH off-scope changes, return to checkout bug         ║
║  [2] COMMIT SEPARATELY ("add types to auth middleware")      ║
║  [3] EXPAND SCOPE (justify: "types are prerequisite")        ║
║  [4] CONTINUE (I know, I'll wrap up soon)                    ║
╚══════════════════════════════════════════════════════════════╝
```

## Session Summary

```
╔══════════════════════════════════════════════════════════════╗
║                SCOPE SENTINEL: SESSION REPORT                ║
║            Task: Fix international address checkout          ║
║            Duration: 2h 14m                                  ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  FOCUS SCORE: 68/100                                         ║
║                                                              ║
║  TIME BREAKDOWN:                                             ║
║  ├── On-scope:   1h 22m (62%)  ████████████░░░░░░░░         ║
║  ├── Adjacent:      18m (13%)  ██░░░░░░░░░░░░░░░░░░         ║
║  ├── Tangential:    16m (12%)  ██░░░░░░░░░░░░░░░░░░         ║
║  └── Drift:         18m (13%)  ██░░░░░░░░░░░░░░░░░░         ║
║                                                              ║
║  DRIFT EVENTS: 2                                             ║
║  ├── Auth middleware typing (stashed → separate task)        ║
║  └── Utility function rename (committed separately)          ║
║                                                              ║
║  FOLLOW-UP TASKS GENERATED:                                  ║
║  ├── "Add TypeScript types to auth middleware"                ║
║  └── "Rename formatAddress → formatPostalAddress globally"   ║
║                                                              ║
║  TASK STATUS: Bug fixed. PR ready.                           ║
╚══════════════════════════════════════════════════════════════╝
```

## Drift Tolerance Modes

| Mode | Threshold | Best For |
|---|---|---|
| **Tight** | Alert after 1 off-scope file or 5 minutes of drift | Bug fixes, hotfixes, time-sensitive tasks |
| **Normal** | Alert after 3 off-scope files or 15 minutes of drift | Feature work, standard development |
| **Exploratory** | Alert after 6 off-scope files or 30 minutes of drift | Refactoring, investigation, learning a new codebase |
| **Off** | No alerts | Freeform hacking, prototyping, creative exploration |

## When to Invoke

- **At the start of every focused task.** Set your scope anchor.
- When working on bug fixes (scope drift is most costly here)
- When working against a deadline (every drifted minute hurts)
- When you notice yourself saying "while I'm in here..." (the classic drift phrase)
- During code review prep (to ensure your PR is focused)

## Why It Matters

Scope drift isn't laziness — it's a natural consequence of how developers think. You see a problem, you want to fix it. The impulse is productive. But unchecked, it turns a 30-minute bug fix into a 4-hour PR that touches 15 files and is impossible to review.

Scope Sentinel doesn't stop you from doing extra work. It makes sure the extra work is **deliberate**, not accidental.

Zero external dependencies. Zero API calls. Pure file-change monitoring.
