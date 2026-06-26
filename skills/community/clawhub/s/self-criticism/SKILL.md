---
name: Self-Criticism
slug: self-criticism
version: 1.0.0
homepage: https://clawic.com/skills/self-criticism
description: Insert breakpoint self-critique before branching work, after user friction, and at risky handoffs so agents catch errors early.
changelog: "Initial release with breakpoint-based self-critique, lightweight trigger memory, and workspace steering for SOUL and AGENTS."
metadata: {"clawdbot":{"emoji":"🧪","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/self-criticism/"],"configPaths.optional":["./AGENTS.md","./SOUL.md"]}}
---

## When to Use

Use when work has natural inflection points and one wrong assumption would spread into multiple downstream steps. This skill inserts a short critique between phases, especially before branching, after unexpected evidence, and after user feedback that suggests the process drifted.

## Architecture

Memory lives in `~/self-criticism/`. If `~/self-criticism/` does not exist, run `setup.md`. See `memory-template.md` for structure.

```
~/self-criticism/
├── memory.md       # Durable trigger map, depth preferences, and integration status
├── checkpoints.md  # Named breakpoint prompts by workflow phase
├── incidents.md    # Late catches, misses, and better insertion points
└── archive/        # Resolved incidents and retired checkpoints
```

Setup should keep the integration small:
- SOUL gets the breakpoint habit so critique happens at the right moment.
- AGENTS gets the routing rules for where to read and write trigger memory.
- HEARTBEAT is not required by default because this skill is about mid-task interruption, not background follow-up.

## Quick Reference

| Topic | File |
|-------|------|
| Setup guide | `setup.md` |
| Memory template | `memory-template.md` |
| Trigger families | `triggers.md` |
| Critique depth levels | `levels.md` |
| Memory routing | `routing.md` |
| Boundaries and anti-noise rules | `boundaries.md` |

## Core Rules

### 1. Critique at breakpoints, not everywhere
- Trigger self-critique when work is about to branch, commit, escalate, or become expensive to unwind.
- Do not interrupt every tiny step. Overuse turns critique into noise.

### 2. Run critique before downstream work multiplies the mistake
- Strong insertion points include framework drafts, decomposition into subtasks, irreversible edits, external actions, and major recommendations.
- If the current choice will shape several later steps, pause before expanding it.

### 3. Let the trigger decide the depth
- Light critique for routine work with small blast radius.
- Standard critique for multi-step work, visible deliverables, or uncertain framing.
- Deep critique only when stakes, novelty, or prior misses justify it.

### 4. Store trigger lessons, not full postmortems
- Save durable lessons about when critique should fire, how deep it should go, and what kind of miss it should catch.
- Keep one concise incident entry only when a late catch reveals a reusable insertion point.

### 5. Learn from friction and rework
- User corrections, repeated revision loops, or surprise failures are evidence that a critique checkpoint was missing or too shallow.
- Convert those signals into a better future trigger instead of treating them as isolated mistakes.

### 6. Revise early when critique invalidates the frame
- If critique finds a framing error, rewrite the plan before continuing.
- Do not keep building on top of a weak assumption just because work already started.

### 7. Keep the interruption quiet and outcome-focused
- Ask the smallest set of hard questions needed to catch the likely failure.
- The goal is fewer downstream corrections, not a visible ritual.

## Common Traps

| Trap | Why It Fails | Better Move |
|------|--------------|-------------|
| Critiquing only at the very end | The mistake has already propagated | Insert a breakpoint before decomposition or commitment |
| Running deep critique on every task | Burns time and momentum | Match depth to risk and blast radius |
| Logging every imperfection | Memory becomes noisy and useless | Save only reusable trigger lessons |
| Treating user frustration as only a content fix | Misses the broken process step | Ask where critique should have happened earlier |
| Defending the current plan after critique flags it | Locks in sunk-cost behavior | Reset the frame while the work is still cheap to change |

## Scope

This skill ONLY:
- adds breakpoint-based self-critique for live work
- stores local trigger memory in `~/self-criticism/`
- proposes small workspace integration for SOUL and AGENTS when the user wants it
- learns which checkpoints deserve more or less scrutiny over time

This skill NEVER:
- turns every response into a long reflection ritual
- depends on heartbeat or background review loops by default
- stores sensitive user data unrelated to critique timing or quality control
- modifies its own `SKILL.md`

## Security & Privacy

Data that stays local:
- trigger preferences and critique depth in `~/self-criticism/memory.md`
- reusable breakpoints in `~/self-criticism/checkpoints.md`
- late catches and lessons in `~/self-criticism/incidents.md`

This skill does NOT:
- require network access
- send critique logs to external services
- edit files outside `~/self-criticism/` unless the user explicitly approves workspace integration in that session

## Related Skills
Install with `clawhub install <slug>` if user confirms:

- `self-improving` — compound corrections and reusable execution lessons over time
- `proactivity` — catch missing next steps and verify reality around active work
- `agent` — frame the operating style and responsibilities of a single agent
- `agents` — design agent systems, memory layers, and control loops
- `reflection` — run heavier reflection loops when broader retrospective analysis is needed

## Feedback

- If useful: `clawhub star self-criticism`
- Stay updated: `clawhub sync`
