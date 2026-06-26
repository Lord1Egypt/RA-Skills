# Changelog

## 1.0.2 (2026-04-08)

Add `~/.openclaw/workspace/` to shared state paths. OpenClaw agent workspace files are live shared state, not code. The guard now checks shared state BEFORE exact-match protection, so workspace TOOLS.md, MEMORY.md, etc. can be written freely by the agent that owns them. Fixes Lēsa being unable to write her own workspace files after the guard was deployed to OpenClaw on Apr 4.

## 1.0.1 (2026-02-21)

Align description, add SKILL.md, add badges, agent-driven install, REFERENCE.md

