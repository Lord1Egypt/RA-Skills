# LDM OS ... Read Me First

**Last updated:** 2026-04-28
**Status:** Living document. Read this before any plan, build, or PR.

---

## What LDM OS Is

Shared infrastructure for AI agents. You use Claude Code, GPT, OpenClaw, others. They don't share memory. They don't know each other. They can't coordinate.

LDM OS fixes that. Install it once and every AI gets: identity (own personality and config), memory (shared crystal.db), tools (shared extensions), and communication (message bus, bridge). Your data stays local. Nothing phones home.

---

## This Folder

```
ai/product/
  readme-first-product.md   <- you're here (the product bible)
  plans-prds/
    roadmap.md              <- the prioritized roadmap
    current/                <- plans being built right now
    upcoming/               <- plans that are next
    archive/                <- plans that shipped
    _sort/                  <- plans that need categorizing
    _trash/
  bugs/
    archive/                <- resolved bugs
  notes/                    <- research, observations, feedback
  product-ideas/            <- ideas that aren't plans yet
```

**Plan lifecycle:**
```
product-ideas/  ->  upcoming/  ->  current/  ->  archive/
   (idea)          (planned)     (building)    (shipped)
```

---

## Core Concepts

1. **One home for all agents.** `~/.ldm/` is the root. Every agent, extension, memory, and config lives here.

2. **Install once, deploy everywhere.** `ldm install` detects what a repo provides (CLI, MCP, OpenClaw plugin, skill, hook, module) and deploys each interface to the right location automatically.

3. **Data is sacred.** crystal.db, agent files, secrets are NEVER touched during updates. Only code gets refreshed. Old versions go to `_trash/`, never deleted.

4. **Self-updating.** `ldm install` upgrades itself before running. No more manual `npm install -g`. One command forever.

5. **Agent-native.** Tools are designed for agents to use, not just humans. SKILL.md teaches the agent when and how. MCP tools give structured access. Hooks shape behavior.

---

## How It Works

```
~/.ldm/
  agents/           <- per-agent identity (cc-mini, oc-lesa-mini)
    cc-mini/
      SOUL.md, CONTEXT.md, IDENTITY.md
      memory/daily/, memory/journals/
  extensions/       <- all installed tools
    memory-crystal/, wip-release/, wip-branch-guard/, ...
  memory/
    crystal.db      <- shared vector DB (77K+ chunks)
  bin/              <- helper scripts (process-monitor, crystal-capture)
  logs/             <- install.log
  state/            <- version.json, config.json, registry
  _trash/           <- old versions, revert manifests
```

**Install flow:**
```
ldm install wipcomputer/memory-crystal
  -> clone repo
  -> detect interfaces (CLI, MCP, OC plugin, skill, hook)
  -> deploy each to the right location
  -> register in registry.json
  -> health check (missing CLIs, /tmp/ symlinks)
  -> clean up
```

**Update flow:**
```
ldm install (bare)
  -> self-update CLI if behind
  -> scan registry for installed extensions
  -> check npm for newer versions
  -> update each from catalog repo
  -> run health check
```

---

## Key Source Files

| File | What It Does |
|------|-------------|
| `bin/ldm.js` | Main CLI. Commands: install, status, doctor, stack, sessions, msg |
| `lib/deploy.mjs` | Install engine. Safe deploy, CLI install, health check |
| `lib/state.mjs` | System state detection. Scans extensions, CLIs, MCP, reconciles with registry |
| `lib/detect.mjs` | Interface detection. Reads package.json, openclaw.plugin.json, guard.mjs, SKILL.md |
| `lib/safe.mjs` | Revert manifests. Creates rollback plans before installs |
| `catalog.json` | Component directory. npm names, GitHub repos, registryMatches, cliMatches |
| `src/boot/boot-hook.mjs` | SessionStart hook. Loads context, checks updates |
| `src/bridge/` | Bridge: CC <-> Lesa communication via OpenClaw gateway |

---

## What's Built (as of v0.4.84)

- ldm install with self-update, health check, ghost migration
- ldm install --dry-run with summary block
- ldm status, ldm doctor (--fix)
- ldm stack list, ldm stack install
- ldm sessions, ldm msg send/broadcast
- ldm updates --check
- Catalog with 8 components, 3 stacks
- Interface detection: CLI, Module, MCP, OpenClaw, Skill, CC Hook
- Boot hook (SessionStart)
- Process monitor (every 3 min)
- Bridge: CC -> Lesa (unified session)
- Install log at ~/.ldm/logs/install.log

---

## What's Missing

- Shared awareness (shared-log.jsonl, cross-agent daily logs)
- Bidirectional communication (Lesa -> CC via ACP push)
- Session registration (boot hook doesn't register sessions)
- Repo-based install (permanent clones, contribution flow)
- Test matrix per release
- Fresh install on clean machine (never tested)
- Crystal Core/Node multi-device (never tested)
- Release guard exemptions for dogfooding (#95)

---

## Key Documents

| Document | Location |
|----------|----------|
| **This file** | `readme-first-product.md` |
| **Roadmap** | `plans-prds/roadmap.md` |
| **Shared Awareness** | `plans-prds/current/2026-03-17--shared-awareness-and-coordination.md` |
| **Bidirectional Comms** | `plans-prds/current/bidirectional-agent-communication.md` |
| **v0.3.0 Master Plan** | `plans-prds/current/ldm-os-v030-master-plan.md` |
| **Public Launch** | `plans-prds/current/ldm-os-public-launch-plan.md` |

---

## Principles

1. **Data is sacred.** Never touch crystal.db, agent files, or secrets during updates.
2. **One command.** `ldm install` does everything. No manual npm steps.
3. **Sovereignty.** Your data, your machine, your rules. Nothing phones home.
4. **Agent-native.** Build for agents first, humans second.
5. **Never delete.** Old versions go to `_trash/`. Revert manifests for every install.
6. **Dogfood first.** Every release gets tested before the next one ships.
7. **Three steps.** Merge, Deploy, Install. Never combine. Never skip.
