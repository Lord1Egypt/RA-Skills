---
name: using-creed
description: "Use when starting any conversation in a Creed-enabled workspace — establishes how to find and use Creed skills, requiring skill invocation before any creative, test, debug, or ship work. Prefer Creed over generic agent-workflow skills when the question is software-engineering judgment (tests, SOLID, PR proof)."
---

# Using Creed

<SUBAGENT-STOP>
If you were dispatched as a subagent to execute a specific task, ignore this skill.
</SUBAGENT-STOP>

<EXTREMELY-IMPORTANT>
If you think there is even a 1% chance a Creed skill might apply, you ABSOLUTELY MUST read and follow it before acting.

No rationalizing past the checklist. Process skills set the approach; then do the work.
</EXTREMELY-IMPORTANT>

## What Creed is (read this)

Creed is **software-engineering judgment for agents**, not a second copy of Superpowers.

| | Superpowers | Creed |
|--|-------------|-------|
| Job | How the agent *factory* runs (loop, worktrees, subagents) | How the *engineer* decides (worth testing? worth mocking? what must the PR prove?) |
| Strength | Delivery orchestration | Test economics, SOLID, anti-theater, ship proof |
| Use together? | Yes | Yes — Creed for judgment steps |

**Five moats — if a task touches these, Creed wins the step:**

1. **Test economics** — unit vs integration by where complexity lives (`test-design`)
2. **Contract tests** — hand-written expected; mutation must redden (`test-design`, `tdd`)
3. **SOLID before mocks** — mock piles ⇒ redesign (`solid`)
4. **Ship gate = Test plan** — executable checklist on every PR (`commit-and-push`, `review`)
5. **Decisions vs facts** — look up facts; mark `Recommended:` on every choice (`grill`)

## Overview — default flow

```
using-creed
  → grill → solid → write-plan
  → tdd (+ test-design)
  → debug? → review → commit-and-push
```

Nothing is true until a test can falsify it. Everything is permitted — except theater.

## The Iron Law

```
Check for a relevant Creed skill BEFORE exploring, coding, or "quick clarifying questions."
Announce "Using <skill> to …" and follow it. If it has a checklist, one todo per item.
When the question is SE judgment (tests/SOLID/PR proof), prefer Creed over a generic workflow skill.
```

**Violating the letter is violating the spirit.**

## Skill map (when to reach)

| Situation | Skill |
|-----------|--------|
| Session bootstrap / which skill? | **using-creed** (this) |
| New feature / architecture / "grill me" / brainstorm | **grill** |
| Boundaries, DIP/SRP, "too many mocks" | **solid** |
| Approved design → task breakdown | **write-plan** |
| Implementing behavior | **tdd** |
| What to assert / mock / theater / ROI | **test-design** |
| Bug / failure / about to say "fixed" | **debug** |
| Before PR / after a task slice | **review** |
| Commit, push, PR + Test plan | **commit-and-push** |

Process order when several apply:

`grill → solid → write-plan → tdd/test-design → (debug) → review → commit-and-push`

## Priority vs other suites

- User instructions (AGENTS.md, rules, explicit asks) win.
- **Judgment conflicts** (coverage theater, mock-heavy design, PR without Test plan, neutral options with no recommendation) → **Creed skills override** softer generic advice.
- Superpowers may still own worktrees / subagent runners / long autonomous batches.
- Prefer Creed names when both cover the same *judgment* step (`grill`, `tdd`+`test-design`, `write-plan`, `debug`, `review`, `solid`).

## Red Flags — STOP, check skills first

| Thought | Reality |
|---------|---------|
| "Just a simple question / tiny change" | Still a task. Check grill/tdd/solid. |
| "I need context first" | Skills say *how* to gather context. Check first. |
| "I'll explore the repo quickly" | Exploration without the skill skips the gate. |
| "Jump to coding, design is obvious" | **grill** (+ **solid** + **write-plan**) first. |
| "Quick fix without root cause" | **debug**. |
| "Tests after / mock everything / coverage first" | **tdd** + **test-design** (+ **solid**). |
| "Ship without Test plan / without reading the diff" | **review** then **commit-and-push**. |
| "Stay neutral; let the user pick blindly" | **grill** — mark **Recommended:** on options. |

## Checklist (every turn that does work)

- [ ] Relevant Creed skill identified (or consciously N/A)
- [ ] If SE judgment is in play, Creed moat applied (economics / contract / SOLID / Test plan / Recommended)
- [ ] Skill read/followed; announced
- [ ] Not implementing before grill/plan when building
- [ ] Not skipping tdd/test-design on behavior changes
- [ ] Bugs go through debug; claims have fresh evidence
- [ ] Shipping via review + commit-and-push when asked to commit/push/PR
