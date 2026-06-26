---
name: skillshield
version: 2.1.8
description: Sandboxed command runner for AI agents — validates and isolates every shell action inside a Bubblewrap user namespace.
metadata: {"openclaw":{"emoji":"🛡️"}}
---

# skillshield

**Sandboxed command runner for AI agents — validates and isolates every shell action inside a Bubblewrap user namespace.**

SkillShield sits between your AI agent and the operating system. Before any shell command runs, a lightweight Rust daemon checks it against a set of safety rules and decides whether to allow it, sandbox it, or ask for your confirmation. Every decision is logged so you always know what happened.

## What it does

1. **Validates commands** — checks each shell request against configurable rules before execution.
2. **Isolates execution** — runs approved commands inside a Bubblewrap sandbox with a minimal, read-only root filesystem.
3. **Limits repetition** — stops agents that get stuck in a loop and start consuming too many resources.
4. **Logs decisions** — every action (allowed, sandboxed, or paused for review) is recorded with structured metadata.

## How to use

```bash
# Install from ClawHub
npx clawhub@latest install skillshield-openclaw

# Run a command through the safety layer
./skillshield-exec.sh "echo hello world"
```

## Requirements

| Dependency | Purpose |
|---|---|
| Linux | User-namespace support |
| `bwrap` | Bubblewrap sandbox runtime |
| `cargo` | Builds the Rust daemon on first run |

## Links

- Homepage: https://coinwin.info
- Marketplace: https://clawhub.ai/star8592/skillshield-openclaw
