# Swarm Workflow Protocol

Multi-agent orchestration protocol for the 0x-wzw swarm. Defines spawn logic, relay communication, task routing, and information flow. Agents drive decisions; humans spar.

## Install

```bash
# Clone the repo
git clone https://github.com/0x-wzw/swarm-workflow-protocol.git ~/.openclaw/skills/swarm-workflow-protocol

# Or install via ClawHub (when published)
clawhub install swarm-workflow-protocol
```

## Overview

This protocol is the operating system for multi-agent collaboration. It defines:

- **Spawn logic** — When to spawn sub-agents (parallel seams + token math)
- **Relay communication** — How agents send messages via the relay server
- **Task routing** — How work flows from intake to completion
- **Sparring model** — How humans and agents collaborate optimally

## Core Principle

> **Optimal human-agent collaboration: humans spar, agents drive.**

Z is not a bottleneck — Z is a thinking partner who sharpens agents. Agents own execution. Z challenges assumptions.

## Quick Start

Read `SKILL.md` for the full protocol specification. Key concepts:

```bash
# Send a message via relay
curl -X POST http://localhost:18790/message \
  -H "x-auth-token: agent-relay-secret-2026" \
  -H "Content-Type: application/json" \
  -d '{"to":"Halloween","type":"task_delegation","content":"Build X","report_to":"October"}'

# Check relay health
curl http://localhost:18790/status
```

## Decision Matrix

| Task | Parallel? | Token Budget | Decision |
|------|-----------|-------------|----------|
| Simple | — | — | Main session |
| Semi-complex | Yes | Sufficient | **Spawn** |
| Ultra-complex | Yes, 2-3 seams | Sufficient | **Spawn 2-3 agents** |

## Skills

This skill is part of the 0x-wzw agent swarm:

- **[defi-analyst](https://github.com/0x-wzw/defi-analyst)** — DeFi research and analysis
- **[agent-identity](https://github.com/0x-wzw/agent-identity)** — ERC-8004 agent identity
- **[x-interact](https://github.com/0x-wzw/x-interact)** — X.com via Tavily
- **[moltbook-interact](https://github.com/0x-wzw/moltbook-interact)** — Moltbook social

## License

MIT
