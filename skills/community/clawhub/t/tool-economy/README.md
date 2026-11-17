# Tool Economy

> Every tool call is an expense. Spend wisely.

A [Hermes Agent](https://hermes-agent.nousresearch.com/docs) / OpenClaw skill that
teaches AI agents to **minimize tool-call overhead** — tokens and latency —
without sacrificing correctness.

## Why

Every tool invocation costs:

- **Tokens** — the call's arguments and its full result travel through context.
- **Latency** — each call is at least one network/compute round-trip.
- **Reasoning overhead** — serial calls force extra planning turns between them.

Wasteful patterns (re-reading files, serializing independent calls, chaining weak
commands) compound quickly. `Tool Economy` gives the agent a discipline and a
measurable score so it can self-correct.

## What's Included

- **`SKILL.md`** — the core skill: principles, checklist, quick-reference table.
- **`references/`**
  - `batching.md` — how and when to parallelize independent tool calls.
  - `budgeting.md` — estimating, tracking, and reconciling a tool budget.
  - `antipatterns.md` — catalog of 10 wasteful patterns and their fixes.
- **`scripts/analyze_session.py`** — analyze a session log and report:
  - total / redundant calls
  - serializable-but-parallel (missed batching) calls
  - estimated overhead (extra round-trips × latency)
  - a **tool economy score** (0–100)
- **`scripts/sample_session.json`** — example input for the analyzer.

## Quick Start

```bash
# Analyze a session log
python3 scripts/analyze_session.py scripts/sample_session.json
```

Example output:

```
Tool Economy Report
===================
Total tool calls              : 12
Redundant calls               : 2
Missed parallel opportunities : 3
Estimated extra round-trips   : 5
Estimated overhead            : 1500 ms
Tool economy score            : 58/100  [Fair]

Top waste sources:
  1. redundant_read        x2   (~600 ms)
  2. missed_batching       x3   (~900 ms)
```

## Session Log Format

The analyzer accepts a JSON array of tool-call records:

```json
[
  {
    "turn": 1,
    "tool": "read_file",
    "args": {"path": "src/main.py"},
    "calls_in_turn": 1
  },
  ...
]
```

Only `tool` and `args` are required; `turn` and `calls_in_turn` are used for
missed-batching detection (see `scripts/analyze_session.py --help`).

## Installation (Hermes Agent)

Copy or symlink this directory into your skills folder:

```bash
cp -r tool-economy ~/.hermes/skills/
```

Hermes auto-discovers skills with a valid `SKILL.md`. See the
[skills docs](https://hermes-agent.nousresearch.com/docs) for details.

## Principles (TL;DR)

1. **Batch** independent calls into one turn.
2. **Don't re-read** what's already in context.
3. **Cache** expensive results for the session.
4. **Prefer one strong command** over a chain of weak ones.
5. **Track a tool budget** and replan when over.

## License

MIT © Denis Voronin
