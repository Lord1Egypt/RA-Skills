---
name: speed-run
version: 1.0.0
description: >
  Gamifies coding tasks with speedrun mechanics — timer splits, personal
  bests, categories, and tricks. How fast can you fix a bug? Ship a feature?
  Write a test suite? Set your PB, grind for optimization, and compete
  against yourself. It's Games Done Quick, but for software engineering.
author: J. DeVere Cooley
category: fun-tools
tags:
  - gamification
  - speedrun
  - timer
  - competition
metadata:
  openclaw:
    emoji: "⏱️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - fun
      - productivity
---

# Speed Run

> "Any task is a speedrun if you time it."

## What It Does

Start a timer. Do the thing. Stop the timer. See your splits. Beat your personal best. Celebrate with speedrun commentary.

Speed Run turns every coding task into a **timed challenge** with splits, categories, tricks, and personal records — using real speedrunning terminology and mechanics. It tracks your times, identifies your fastest and slowest phases, and helps you optimize your workflow the same way speedrunners optimize routes.

## Speedrun Categories

### Any% (Just Ship It)
Complete the task as fast as possible. No constraints on code quality, test coverage, or documentation. Skip everything that's not strictly necessary.

**Valid for:** Prototypes, hackathons, "just make it work" emergencies.

```
CATEGORY: Any% Bug Fix
RULES:
├── Timer starts when you read the bug report
├── Timer stops when the fix is committed
├── No quality gates (tests optional, review optional)
├── Skips allowed (copy-paste from StackOverflow = valid strat)
└── Glitches allowed (force push = frame-perfect skip)
```

### 100% (Full Completion)
Complete the task with ALL quality gates: tests written, docs updated, code reviewed, CI green, deployed to production.

**Valid for:** Real work that matters. The "true ending" speedrun.

```
CATEGORY: 100% Feature Ship
RULES:
├── Timer starts when you read the ticket
├── Timer stops when it's deployed to production
├── All tests must pass (including new tests for the feature)
├── Documentation must be updated
├── Code review must be completed
├── CI must be green
└── No skips, no glitches. Full completion.
```

### Glitchless (No Shortcuts)
Complete the task without any "tricks" — no copy-paste from AI, no StackOverflow, no pulling from previous projects. Pure from-scratch implementation.

**Valid for:** Learning, skill development, proving mastery.

### Low% (Minimal Changes)
Fix the bug or ship the feature with the absolute minimum number of lines changed. The golf version of coding.

**Valid for:** Bug fixes, optimizations, code golf enthusiasts.

### New Game+ (Second Run)
Redo a task you've done before, but harder — stricter type constraints, higher coverage requirements, better performance benchmarks.

## The Speedrun Timer

```
╔══════════════════════════════════════════════════════════════╗
║                  ⏱️ SPEED RUN ACTIVE ⏱️                      ║
║  Category: 100% Bug Fix                                      ║
║  Task: "Fix checkout failing for international addresses"    ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CURRENT: 00:23:47                                           ║
║  PB:      00:31:12  (SET Feb 18 — similar bug)              ║
║  PACE:    ▲ 7:25 AHEAD OF PB                                ║
║                                                              ║
║  SPLITS:                                                     ║
║  ├── ✅ Reproduce bug ......... 00:03:12  (PB: 00:04:30) ▲  ║
║  ├── ✅ Identify root cause ... 00:08:45  (PB: 00:12:15) ▲  ║
║  ├── ✅ Write fix ............. 00:05:23  (PB: 00:06:44) ▲  ║
║  ├── 🔄 Write tests .......... 00:06:27  (PB: 00:04:30) ▼  ║
║  ├── ⬜ Code review ........... —         (PB: 00:02:18)    ║
║  └── ⬜ CI + Deploy ........... —         (PB: 00:00:55)    ║
║                                                              ║
║  GOLD SPLITS: 3/6    PERSONAL BEST PACE: YES                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Split Definitions

| Split | Starts When | Ends When |
|---|---|---|
| **Reproduce** | You read the bug report | You can consistently trigger the bug |
| **Root Cause** | Bug reproduced | You've identified the specific code causing the issue |
| **Write Fix** | Root cause identified | Fix implemented (code changed) |
| **Write Tests** | Fix implemented | Tests written and passing |
| **Code Review** | PR opened | PR approved |
| **CI + Deploy** | PR approved | Merged and deployed |

For feature work:
| Split | Starts When | Ends When |
|---|---|---|
| **Design** | Ticket read | Approach decided |
| **Scaffold** | Approach decided | File structure and interfaces created |
| **Implement** | Scaffold done | Core logic complete |
| **Test** | Implementation done | Tests written and passing |
| **Polish** | Tests passing | Edge cases handled, docs updated |
| **Ship** | Polished | Reviewed, merged, deployed |

## Personal Best Tracking

```
╔══════════════════════════════════════════════════════════════╗
║                 ⏱️ PERSONAL BESTS                            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  CATEGORY                    PB          DATE       RUNS     ║
║  ─────────────────────────── ─────────── ────────── ─────    ║
║  Any% Bug Fix                00:08:23    Feb 22     12       ║
║  100% Bug Fix                00:31:12    Feb 18     8        ║
║  Any% Feature (small)        00:42:17    Jan 30     5        ║
║  100% Feature (small)        02:14:33    Feb 10     3        ║
║  100% Feature (medium)       06:47:12    Feb 25     2        ║
║  Low% Bug Fix (lines)        1 line      Mar 01     4        ║
║  Test Suite (new module)     00:18:44    Feb 20     3        ║
║  Code Review                 00:12:30    Feb 28     15       ║
║                                                              ║
║  LIFETIME STATS:                                             ║
║  ├── Total runs: 52                                          ║
║  ├── Total time: 47h 23m                                     ║
║  ├── PBs this month: 4                                       ║
║  ├── Gold splits: 34%                                        ║
║  └── Average improvement per run: 8%                         ║
║                                                              ║
║  🏅 MOST IMPROVED: Bug Reproduction (-40% since first run)   ║
║  🐌 NEEDS WORK: Code Review split (slowest relative to PB)  ║
╚══════════════════════════════════════════════════════════════╝
```

## Speedrun Finish Screen

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║  ⏱️ RUN COMPLETE!                                            ║
║                                                              ║
║  Category:  100% Bug Fix                                     ║
║  Task:      Fix international address checkout               ║
║  Time:      00:28:34                                         ║
║  Previous PB: 00:31:12                                       ║
║                                                              ║
║  🎉 NEW PERSONAL BEST! 🎉                                    ║
║  Improvement: -2:38 (-8.5%)                                  ║
║                                                              ║
║  SPLIT ANALYSIS:                                             ║
║  ├── Reproduce ......... 00:03:12  GOLD ⭐ (best ever)      ║
║  ├── Root Cause ........ 00:08:45  GOLD ⭐ (best ever)      ║
║  ├── Write Fix ......... 00:05:23  GOLD ⭐ (best ever)      ║
║  ├── Write Tests ....... 00:06:27  +1:57 from PB           ║
║  ├── Code Review ....... 00:03:42  GOLD ⭐ (best ever)      ║
║  └── CI + Deploy ....... 00:01:05  +0:10 from PB           ║
║                                                              ║
║  COMMENTARY:                                                 ║
║  "Incredible root cause identification — shaved 3 minutes    ║
║  off the PB there. The test writing was slower this run,     ║
║  possibly because the fix touched more edge cases. But       ║
║  that's fine — 100% category means tests are mandatory.      ║
║  The review split was phenomenal — reviewer was online and    ║
║  approved in under 4 minutes. RNG was good today."          ║
║                                                              ║
║  TRICKS USED:                                                ║
║  ├── "Quick Repro" — Used existing test fixture to reproduce ║
║  ├── "Blame Skip" — Used git blame to jump to root cause     ║
║  └── "Pre-staged" — Had test template ready before fixing    ║
║                                                              ║
║  NEXT RUN OPTIMIZATION:                                      ║
║  Write test FIRST (TDD strat). Testing took longer because   ║
║  you wrote the fix before understanding all edge cases.      ║
║  TDD forces edge case discovery earlier = faster total time. ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Speedrun Tricks & Strategies

| Trick | Description | Time Saved |
|---|---|---|
| **Blame Skip** | Use `git blame` to jump straight to last meaningful change | ~3 min |
| **Fixture Repro** | Use existing test fixtures to reproduce bugs instead of manual testing | ~5 min |
| **Template Strats** | Keep file/test templates ready for common patterns | ~2 min |
| **TDD Route** | Write test first — forces faster root cause ID | ~4 min |
| **Parallel Review** | Open draft PR during test writing so reviewer can start early | ~5 min |
| **Commit Stacking** | Make small, reviewable commits that can be approved incrementally | ~3 min |
| **Binary Search** | `git bisect` to find the breaking commit in O(log n) | Variable |

## When to Invoke

- **Anytime you start a task** — just add a timer. Instant gamification.
- When you want to improve your workflow (splits show where time goes)
- Friday afternoon bug fixes (speedrun mode makes them fun)
- Hackathons (natural fit for Any% category)
- Personal development (track improvement over time)
- When procrastinating (the timer creates urgency)

## Why It Matters

Speedrunning isn't about going fast. It's about **understanding your process** — knowing where time goes, identifying bottlenecks, and systematically optimizing. The splits don't just tell you how fast you were. They tell you which skills to practice.

Also, it's incredibly satisfying to beat your PB on a bug fix. That dopamine hit is real.

Zero external dependencies. Zero API calls. Pure timer-driven self-improvement.
