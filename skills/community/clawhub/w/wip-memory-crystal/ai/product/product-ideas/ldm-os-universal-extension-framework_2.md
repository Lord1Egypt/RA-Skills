# Product Idea: LDM OS Universal Extension Framework

**Date:** 2026-03-06
**Source:** Parker, during memory analysis walkthrough
**Status:** Architecture vision. This is the future of LDM OS.
**Priority:** High. This shapes everything.

---

## The Vision

LDM OS is the runtime. Extensions are the apps. The universal installer is the app store.

`~/.ldm/` is the single source of truth. Every agent lives in it. Every extension installs there once. Every agent runtime (Claude Code, OpenClaw, future agents) loads from there.

---

## How It Works

### 1. LDM OS is always the base

Every extension installer (`crystal init`, `op-secrets init`, etc.) triggers `ldm init` first. The OS is always there before anything else. `ldm init` scaffolds `~/.ldm/`, creates the agent registry, sets up the extension directory.

### 2. Extensions install once to a central location

```
~/.ldm/extensions/<name>/
```

Not copied to each agent's directory. Not duplicated between `~/.openclaw/extensions/` and `~/.ldm/extensions/`. One location. Agents point to it (symlinks or direct paths).

### 3. Agents register, extensions wire up per-agent

When you add an agent, LDM OS says: "Here's what's installed: memory-crystal, op-secrets, tavily. Which ones should this agent use?"

Each agent runtime loads extensions differently:

| Agent Runtime | How it loads extensions |
|--------------|----------------------|
| Claude Code | Hooks in `~/.claude/settings.json` + MCP server registrations |
| OpenClaw | Plugin entries in `openclaw.json` + `.mcp.json` |
| Future agents | Whatever they support |

LDM OS handles the wiring. The extension doesn't need to know about every runtime. The OS adapts.

### 4. Universal installer: point at any repo

The killer feature. You point the installer at any repo ... an MCP server someone made, a CLI tool, a Python script, an npm package. The installer:

1. Analyzes what it is (MCP server? CLI tool? skill? plugin?)
2. Packages it as an LDM OS extension in `~/.ldm/extensions/<name>/`
3. Figures out the best way to expose it to each registered agent:
   - For Claude Code: register as MCP server, or add as hook, or make available as CLI
   - For OpenClaw: wrap as plugin with lifecycle hooks, or register as MCP
   - For future agents: whatever format they need

Not all extensions are the same shape. An MCP server might be better as a CC hook for one use case, or an OC skill for another. The installer handles the conversion.

```bash
ldm install https://github.com/someone/cool-mcp-server
# -> Analyzes repo
# -> Packages to ~/.ldm/extensions/cool-mcp-server/
# -> "You have 2 agents: cc-mini, oc-lesa-mini. Wire up to both? [Y/n]"
# -> Registers MCP for CC, adds plugin entry for OC
```

### 5. Config tracks everything

`~/.ldm/config.json` knows:
- What agents exist (cc-mini, oc-lesa-mini, future agents)
- What extensions are installed
- Which extensions are enabled for which agents
- How each agent runtime loads each extension (hook, MCP, plugin, skill, CLI)

---

## What Changes From Today

### Today (broken)

- Extensions manually copied to both `~/.ldm/extensions/` and `~/.openclaw/extensions/`
- Most copies in `~/.ldm/extensions/` are dead (nothing loads them)
- Memory Crystal does double duty as both the OS installer and a memory component
- Each extension has its own install process (or no process ... just `cp`)
- MCP servers registered per-project in `.mcp.json`, not centrally
- Wiring is manual: edit settings.json, edit .mcp.json, edit openclaw.json

### Tomorrow (LDM OS)

- `~/.ldm/extensions/` is the single source
- `~/.openclaw/extensions/<name>` symlinks to `~/.ldm/extensions/<name>/`
- `ldm init` is the OS installer. `crystal init` calls `ldm init` first, then installs memory.
- `ldm install <repo>` is the universal installer
- `ldm wire <extension> <agent>` connects an extension to an agent
- `ldm doctor` shows all agents, all extensions, all wiring

---

## Extension Audit (current state)

From today's analysis. What's real, what's dead, what needs conversion:

| Extension | Status | Needs OpenClaw? | Action |
|-----------|--------|----------------|--------|
| memory-crystal | Live, both runtimes | No | Keep. First LDM OS extension. |
| op-secrets | Live, OC only | No (needs op CLI + SA token) | Convert to LDM OS extension. Could be MCP for CC. |
| compaction-indicator | Live, OC only | Yes (OC lifecycle hooks) | Keep OC-only for now. CC equivalent would need different approach. |
| context-embeddings | **Dead.** Disabled in config. | Yes | Kill. Memory Crystal replaced it. 128 MB orphan DB. |
| private-mode | Live, OC only | Yes (OC plugin) | Convert. Could be MCP tool or CC hook. |
| root-key | Live, OC only | Yes (OC skill) | Convert. Could be MCP tool. |
| tavily | Live, OC only | No (just API wrapper) | Convert to LDM OS extension. MCP for CC. |
| lesa-bridge | Live, both | Needs OC gateway | Keep. Only useful when Lesa exists. |
| wip-agent-pay | Live, MCP | No | Already runtime-agnostic. Model LDM OS extension. |
| wip-file-guard | Live, CC only | No | Already a CC hook. LDM OS extension. |
| wip-repo-permissions-hook | Live, CC only | No | Already a CC hook. LDM OS extension. |
| cc-session-export | **Dead.** | No | Kill. Absorbed into memory-crystal cc-poller. |
| session-export | **Dead.** | Yes | Kill. Absorbed into memory-crystal openclaw.ts. |

---

## Workspace State Files (CONTEXT.md, SOUL.md, etc.)

OpenClaw auto-loads workspace files (CONTEXT.md, MEMORY.md, TOOLS.md, SOUL.md) into every session via the gateway. Claude Code has no equivalent ... CC relies on CLAUDE.md instructions telling it to manually read files from `~/.ldm/agents/cc-mini/`.

LDM OS should handle this for any agent. The workspace state files should be part of the OS framework:
- `~/.ldm/agents/<id>/CONTEXT.md` ... current state
- `~/.ldm/agents/<id>/SOUL.md` ... identity
- `~/.ldm/agents/<id>/IDENTITY.md` ... core facts

For OpenClaw: the gateway already loads these from its workspace path. Point it at `~/.ldm/agents/oc-lesa-mini/` (or symlink).
For Claude Code: a boot hook or the cc-hook could inject these. Or CLAUDE.md continues to instruct CC to read them (simpler, works today).

---

## Relationship to Memory Crystal

Memory Crystal is the first LDM OS extension. It's currently also acting as the OS installer (`crystal init` scaffolds `~/.ldm/`). That should separate:

- `ldm init` ... installs the OS (directories, config, agent registry)
- `crystal init` ... installs memory (calls `ldm init` first, then adds DB, capture, hooks)
- `ldm install <anything>` ... installs any extension

For now, Memory Crystal can continue to carry `ldm init` inside it (it's the only package that ships). But architecturally, they're separate concerns. The OS is the framework. Memory is the first app.

---

## WIP Agent Pay as Model Extension

Agent Pay is already close to the ideal LDM OS extension shape:
- It's an MCP server (runtime-agnostic)
- It doesn't depend on OpenClaw
- It installs to one location
- Any agent that supports MCP can use it

This is what every extension should look like. The universal installer would take a repo like agent-pay and say: "This is an MCP server. I'll register it for all your agents."

---

## Next Steps

1. Write the LDM OS init (can live in memory-crystal package for now)
2. Symlink `~/.openclaw/extensions/` entries to `~/.ldm/extensions/`
3. Kill dead extensions (context-embeddings, cc-session-export, session-export)
4. Build `ldm install` prototype (point at a repo, analyze, package, wire up)
5. Convert op-secrets to work as MCP server for CC (not just OC plugin)
6. Update memory-analysis.md with the new architecture
