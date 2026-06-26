# LDM OS: Learning Dreaming Machines

## All your AIs. One system.

You use Claude Code, GPT, OpenClaw, others. They don't share memory. They don't know each other. They don't know how to work together.

LDM OS is the shared infrastructure layer. Install it once and every AI you use gets:

- **Identity** ... each AI gets its own behavior, personality, and skills
- **Memory** ... shared memory across all your AIs, secure, sovereign, yours to take anywhere
- **Ownership** ... every interaction, every memory, across every AI you use is yours, portable, encrypted, never locked in
- **Collaboration** ... your AIs communicate, share tools, and work together
- **Compatibility** ... any skill, plugin, or tool works with all your AIs. Install once, use everywhere.
- **Payments** ... your AI hits a paywall, you approve it with Face ID, Apple Pay for your AI

## What does it install?

- `~/.ldm/extensions/` ... where tools and plugins live
- `~/.ldm/agents/` ... each AI gets its own identity, personality, and memory here
- `~/.ldm/memory/` ... shared memory across all your AIs (including the Memory Crystal)
- `~/.ldm/state/` ... configuration and sync state
- `~/.ldm/shared/rules/` ... dev conventions deployed to every AI harness

## What changes for this AI?

- Boot sequence reads from `~/.ldm/agents/` (identity, memory, daily logs)
- Rules deployed to `~/.claude/rules/` (git conventions, security, release pipeline)
- Extensions like Memory Crystal, wip-release are managed centrally
- Stop hooks write to crystal and daily logs after every turn

## What changes across all my AIs?

- Shared memory (crystal.db) accessible to every AI
- Shared rules (same conventions everywhere)
- Shared extensions (install once, every AI sees it)
- Agent identity (each AI is its own entity with its own prefix)
