# Session Context Bridge 🔗

> Never start from zero. Carry context across sessions automatically.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/type-agent--skill-blue)](SKILL.md)

**Why this exists:** claude-mem proved that cross-session context persistence is a 65K-star need. But it requires installation, a worker service, and a database. This skill achieves 80% of the value with 0 dependencies — just markdown files.

## The Problem

Every new session starts blind. You lose:
- Active task state and progress
- Key decisions and their reasoning
- File relationships and project map
- Environment configuration
- Blockers and dependencies

## The Solution

Simple, structured markdown files in a `.context/` directory:

```
.context/
├── current.md        ← What you're working on NOW
├── archive/           ← Previous sessions
└── decisions.md       ← Architectural decisions with reasoning
```

## Quick Start

```
# Install as an agent skill
# Claude Code: Copy SKILL.md to .claude/skills/session-context-bridge/
# OpenClaw: Copy to ~/.openclaw/workspace/skills/session-context-bridge/

# At end of session: "save my context"
# At start of session: "restore my context"
# Always: "update context" after important decisions
```

## Why Not Just Use Memory Tools?

| | Memory tools | Context Bridge |
|--|-------------|----------------|
| Setup | Install + configure | Just markdown files |
| Dependencies | SDK, database, worker | None |
| Portability | Tied to specific tool | Works everywhere |
| Granularity | Automatic (may miss) | Structured (you control) |
| Search | Vector search | Markdown + grep |
| Best for | Large knowledge bases | Active task continuity |

## Use Together

They complement each other:
- **Context Bridge:** Active task state, decisions, environment
- **Memory tools:** Long-term knowledge, patterns, learned lessons

## Works With

- OpenClaw (native workspace integration)
- Claude Code
- Cursor
- Any agent that can read/write files

## License

MIT
