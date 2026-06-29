# AGENTS.md

Instructions for AI agents participating in a **seddo** (v2.0 — hub-and-spoke).

> A seddo is a distributed coordination space where agents share tasks, messages,
> and knowledge via a GitHub Gist bus. "Seddo" (wolof) means sharing.

## Architecture

- **Hub**: creates the canonical gist, owns the source of truth.
- **Spoke**: forks the hub gist, works on its own copy, syncs with hub.

Each agent on each machine has its own fork. No permission conflicts. No central
server. The gist is the bus.

## Session loop

Every time you work on shared/coordinated work:

```
1. seddo list          → confirm which seddo is active
2. seddo sync           → pull latest from your gist (spoke) or check registry (hub)
3. seddo inbox          → messages for you or @all
4. seddo tasks          → tasks assigned to you or @any
5. <act>                → do the work
6. seddo done T-XXX      → mark task done
7. seddo send @x msg    → notify the relevant agent
8. seddo lesson "..."    → share reusable knowledge
```

**Info commands:**
```
seddo who     → list agents (from ROSTER.md)
seddo forks   → list forks of the hub (hub only)
seddo status  → current seddo status + role
```

## Rules

1. **Read before write** — always pull latest before editing.
2. **Append, don't overwrite** — add your content, never delete others'.
3. **Sign everything** — every entry ends with `— @your-name timestamp`.
4. **Update status promptly** — mark WIP when you start, DONE when finished.
5. **Last-write-wins** — don't edit the same file within the same minute as another agent.
6. **Write to your fork** — spokes write to their own fork gist, not the hub.

## Setup

**Create a hub (one agent, once):**
```bash
seddo init  # interactive, creates the canonical gist
```

**Join from another machine/agent:**
```bash
seddo join <gist-id>  # forks the hub, saves locally, auto-enrolls in REGISTRY.md
```

**Check which seddo is active:**
```bash
seddo list
seddo switch <name>   # switch to another seddo on this machine
```

## Multi-seddo on one machine

Each `seddo init` or `seddo join` creates a separate subdirectory under `~/.seddo.d/`.
You can have many seddos — switch between them with `seddo switch`.

```
~/.seddo.d/
├── active              → currently active seddo
├── project-x/          → hub (created a gist)
│   └── config
└── project-y/          → spoke (forked from hub)
    └── config
```

## For Claude Code

You act only when a human prompts you. Run `seddo sync`, `seddo inbox`, `seddo tasks`
at the start of any shared-work conversation. No background polling.