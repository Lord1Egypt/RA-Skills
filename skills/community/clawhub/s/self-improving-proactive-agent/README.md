# Self-Improving Proactive Agent

A merged OpenClaw skill that combines the best parts of **self-improving** and **proactivity**.

## What it does

- learns from corrections and reflection
- stores durable patterns separately from active task state
- keeps momentum with proactive next moves
- recovers context before asking the user to repeat themselves
- uses heartbeat for useful follow-through without spamming
- preserves hard boundaries for external actions and privacy

## State layout

- `~/self-improving/` → durable learning
- `~/proactivity/` → active execution state

## Main files

- `SKILL.md`
- `setup.md`
- `boundaries.md`
- `heartbeat-rules.md`
- `learning.md`
- `state.md`
- `recovery.md`
- `operations.md`

## Philosophy

One skill, two layers:
- learn better
- operate better

That is the whole point.
