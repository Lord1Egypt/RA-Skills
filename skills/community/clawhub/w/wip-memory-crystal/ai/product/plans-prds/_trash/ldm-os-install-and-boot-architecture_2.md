# LDM OS Install and Boot Architecture

**Date:** 2026-02-27
**Status:** Migration started 2026-02-27
**Context:** Parker and CC discussing how Memory Crystal, LDM OS, and Claude Code's project system interact.

## The Problem

Claude Code keys all context (sessions, memory, plans, MCP servers, CLAUDE.md) to the directory you open it from. Right now CC is opened from `~/.openclaw/`. Everything works because that's where CLAUDE.md, MCP configs, and all the context lives.

But `~/.openclaw/` is OpenClaw's home, not the agent's home. The agent's home should be `~/.ldm/`. And if you open CC from a different directory (a project repo, a new machine), it starts cold. No memory, no tools, no identity.

Parker's observation: "I always open Claude in the same place because of the disconnect between being able to remember context."

## The Hub-Spoke Model

Parker's working model:

- **Hub agent** (CC on Mini, Lesa on Mini) ... full context, full tools, spawns sub-agents as needed
- **Spoke agent** (CC on Air, CC in a different project dir) ... should connect back to the hub's memory

Right now Parker runs two CC windows from `~/.openclaw/`:
- One context window for Memory Crystal work
- One context window for AI Pay work
- Switches between them using saved contexts

This works but is fragile. The context is tied to the directory, not the agent.

## The Construct Pattern (Prior Art)

Parker previously tried solving this with a tool called "construct" (now deprecated/sunset). The idea:

1. You `init` Claude in any directory
2. You run `construct` over that directory
3. Construct updates the CLAUDE.md, installs MCP servers, gives Claude all the context it needs
4. Now Claude works properly in that directory with full LDM OS capabilities

This is the "overlay" pattern: take a vanilla Claude Code directory and overlay LDM OS onto it.

## How Install Could Work

### Memory Crystal Standalone
- `npm install memory-crystal` or agent-driven install via SKILL.md
- Creates `~/.ldm/memory/` if it doesn't exist
- Works immediately. No LDM OS required.
- Just memory: search, remember, forget.

### LDM OS Full Stack
- Install Memory Crystal first (it's the entry point)
- Memory Crystal detects it's standalone, offers: "Want to install LDM OS for Bridge, Relay, and full agent capabilities?"
- Or: user says "install LDM OS" and it sees Memory Crystal is already there
- LDM OS install:
  - Scaffolds `~/.ldm/` (agents, memory, extensions, config)
  - Installs Bridge (local agent communication)
  - Configures Relay (multi-device sync)
  - Sets up boot sequence (CLAUDE.md, MCP servers, identity files)
  - Overlays the current Claude Code directory with LDM OS context

### The "Make LDM OS work here" Skill
- A skill you can run in any Claude Code session
- It checks: is Memory Crystal installed? Is `~/.ldm/` scaffolded?
- If yes: overlays CLAUDE.md, MCP config, and boot sequence into the current directory
- If no: walks you through install first
- Result: Claude Code works with full LDM OS capabilities from any directory

## Where CC Should Live

Options for migrating from `~/.openclaw/` to `~/.ldm/`:

1. **Symlink approach**: `~/.openclaw/` becomes a symlink to `~/.ldm/`. CC still thinks it's in `~/.openclaw/`, all project context preserved. Cleanest migration. But still tied to OpenClaw's name.

2. **Copy project context**: Move `~/.claude/projects/-Users-lesa--openclaw/` to `-Users-lesa--ldm/`. CC picks up context at new path. CLAUDE.md, MCP configs also need to exist at `~/.ldm/`.

3. **Fresh start at `~/.ldm/`**: Crystal memory survives (already at `~/.ldm/memory/crystal.db`). Session history stays searchable via Crystal. You just lose project-specific CC context (plans, todos). Could be fine if Crystal has everything important.

4. **The overlay skill**: Don't move CC. Just make a skill that ensures any directory has the right CLAUDE.md and MCP config. CC opens wherever, the skill makes it work. This is the construct pattern reborn.

## Claude Code's Native Design Patterns (Research, 2026-02-27)

Claude Code already has a hierarchy that supports what we need. We don't need to fight it.

### Settings Hierarchy (highest priority wins)

1. Managed settings (enterprise/MDM)
2. Command-line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

### CLAUDE.md Resolution

CC walks UP from the working directory to filesystem root, loading all CLAUDE.md files it finds. More specific (deeper) wins. Child directory CLAUDE.md files load on demand.

Key: **`~/.claude/CLAUDE.md` loads in every project, everywhere.** This is the user-global slot.

### What Exists at User Level

| Resource | Location | Behavior |
|----------|----------|----------|
| `~/.claude/CLAUDE.md` | User-global instructions | Loaded in every session, every project |
| `~/.claude/rules/` | User-global rules | Apply everywhere, project rules override |
| `~/.claude/skills/` | User-global skills | Available in any project |
| `~/.claude/settings.json` | User-global settings | MCP servers, hooks, permissions |

### What This Means for LDM OS

The "construct" pattern is already built into Claude Code. We just haven't used it:

```
~/.claude/CLAUDE.md           <- LDM OS identity + boot sequence
~/.claude/rules/              <- LDM OS conventions (git, naming, etc.)
~/.claude/skills/             <- "install ldm-os" skill, deploy-public, etc.
~/.claude/settings.json       <- Crystal MCP, Bridge MCP (user-level, everywhere)
```

Open CC from any directory. It loads your identity, your rules, your MCP servers. Automatically. No overlay, no construct, no init.

Project-level CLAUDE.md still works for project-specific stuff (build commands, test patterns, etc.). User-level is the OS. Project-level is the app.

### MCP Server Scoping

```bash
# User scope (follows you everywhere)
claude mcp add --scope user crystal-memory -- node /path/to/mcp-server.js

# Project scope (shared via git, .mcp.json)
claude mcp add --scope project ...

# Local scope (personal, this project only)
claude mcp add ...
```

Resolution: local > project > user. User-level MCP servers are the baseline.

## The Session Portability Problem (The Blocker)

**Sessions are tied to the directory you open CC from.** This is the thing that makes migration hard.

### How It Works

- CC stores sessions at `~/.claude/projects/<directory-key>/`
- Directory key is derived from the working directory path
- Example: opening from `~/.openclaw/` stores sessions under `-Users-lesa--openclaw/`
- `--resume` and `--continue` only show sessions from the CURRENT directory by default

### Current State

```
~/.claude/projects/-Users-lesa--openclaw/     33 sessions (all our work)
~/.claude/projects/-Users-lesa/                6 sessions
~/.claude/projects/-Users-lesa--openclaw-workspace/  5 sessions
```

### The Workaround

In the resume picker, **press `A` to toggle between "current directory only" and "all projects."** So sessions ARE accessible from other directories... you just have to toggle. Not great, but not a wall.

### Why Parker Is Stuck

The ideal: open CC from `~/.ldm/`, have full LDM OS capabilities, and resume any session (including the 33 from `~/.openclaw/`).

The reality:
- CLAUDE.md and MCP servers CAN move to user level (works everywhere)
- Sessions from `~/.openclaw/` stay keyed to that path
- New sessions from `~/.ldm/` go to a new project key
- Old sessions accessible via `A` toggle but not the default view

Crystal search covers the deep memory. The session transcripts are searchable via `crystal_search`. But the "resume this exact conversation" flow is directory-bound.

### Migration Options (Updated)

**Option A: User-level migration (recommended, least risk)**
- Move CLAUDE.md content to `~/.claude/CLAUDE.md`
- Move MCP servers to user scope (`claude mcp add --scope user`)
- Keep opening CC from `~/.openclaw/` (sessions stay accessible)
- New projects just work because user-level config follows you
- Downside: still opening from `~/.openclaw/`, but it doesn't matter anymore because the config is at user level

**Option B: Directory migration**
- Move to opening from `~/.ldm/`
- Old sessions accessible via `A` toggle in resume picker
- Crystal has the deep memory for search
- New sessions accumulate under `~/.ldm/` project key
- Clean break, but old resume flow requires the toggle

**Option C: Symlink (preserves everything)**
- Symlink `~/.openclaw/` to `~/.ldm/`
- CC still resolves to `-Users-lesa--openclaw` project key
- All 33 sessions, auto-memory, plans, todos stay accessible
- User-level config still works on top
- Downside: the project key name still says "openclaw" forever

**Option D: Don't move at all**
- Put everything at user level (`~/.claude/CLAUDE.md`, user MCP servers)
- Keep `~/.openclaw/` as just another project directory
- Open CC from wherever you want
- LDM OS capabilities follow you via user-level config
- Sessions are per-project, which is actually fine... Memory Crystal is the cross-project memory

**Parker's instinct: Option D might be the answer.** The directory you open from becomes just a project workspace. LDM OS lives at user level. Crystal is the memory that follows you everywhere. Sessions are project-local, which is how Anthropic designed it.

## Identity Architecture (Decision, 2026-02-27)

**One agent per harness per machine. That's the identity unit.**

### The Rule

Each combination of harness + machine = one agent identity with its own SOUL.md.

| Agent ID | Harness | Machine | Identity |
|----------|---------|---------|----------|
| cc-mini | Claude Code CLI | Mac Mini | Its own SOUL.md, context, journals |
| cc-air | Claude Code CLI | MacBook Air | Its own SOUL.md, context, journals |
| oc-lesa-mini | OpenClaw | Mac Mini | Its own SOUL.md, context, journals |

### Shared vs Local

- **Shared (via Crystal):** Memory, facts, preferences, conversation history. All agents search the same crystal.
- **Local (per agent):** SOUL.md, CONTEXT.md, journals, daily logs. Each agent has its own narrative.

cc-mini and cc-air aren't "different versions." They're the same person on different machines. Crystal is what connects them. But their local state (what happened today, what's in progress) is their own.

### Multiple Agents on One Machine

Different agent = different OS user account. Lesa runs on one login, a second agent would run on another. One agent per user per machine. No exceptions.

### Each Machine is a Hub

The machine itself is an entity in LDM OS. It has:
- A set of agent instances (cc-mini, oc-lesa-mini)
- A local crystal.db (synced via Relay to other machines)
- Its own `~/.ldm/` tree with agent folders

This is not dogmatic... it's a design decision that simplifies everything. Identity is deterministic: harness + machine = agent ID. No ambiguity.

## Open Questions

- Should CLAUDE.md be generated or maintained by hand? (Currently hand-maintained, very detailed)
- How do MCP servers follow you across directories? (Currently they're in `~/.claude/settings.json` which is global, but project-level `.mcp.json` overrides)
- What's the minimum context CC needs to be "you"? (CLAUDE.md + Crystal MCP + identity files?)
- Is the answer just: Crystal IS the portable context? If Crystal has everything, the boot problem is smaller.
- How does this work on a new machine with no `~/.ldm/`? Cold start problem.

## Dependency Chain

```
Memory Crystal (standalone)
  └── creates ~/.ldm/memory/ if needed
  └── works with any AI, no other deps

LDM OS (full stack)
  ├── Memory Crystal (memory, search, capture)
  ├── Bridge (local agent communication, feature of Crystal)
  ├── Relay (multi-device sync, feature of Crystal)
  ├── Boot Sequence (warm-start, identity, CLAUDE.md)
  ├── Sovereignty Covenant (trust, authority)
  └── Dream Weaver Protocol (narrative consolidation)
```

Memory Crystal is the foundation. Everything else builds on it.

## Migration Log

### 2026-02-27: User-level migration (Option D)

**What we did:**
1. Copied `~/.openclaw/CLAUDE.md` to `~/.claude/CLAUDE.md` (user-level, loads everywhere)
2. Added MCP servers at user scope in `~/.claude.json`:
   - `lesa-bridge` (with `OPENCLAW_DIR` env var)
   - `memory-crystal` (with `OPENCLAW_HOME` env var)
   - `wip-agent-pay`
3. Left `~/.openclaw/CLAUDE.md` and `.mcp.json` in place (no deletions)

**What this means:**
- Open CC from any directory and get full LDM OS: identity, memory, bridge, tools
- `~/.openclaw/` stays as a project directory with its 33 sessions
- New sessions from other directories get full capabilities via user-level config
- Project-level `.mcp.json` at `~/.openclaw/` still works (local > project > user, no conflict)

**What's next:**
- Test from a random directory to confirm MCP servers load
- Update `~/.claude/CLAUDE.md` going forward (stop updating `~/.openclaw/CLAUDE.md`)
- Eventually add `~/.claude/rules/` for LDM OS conventions
- Eventually add `~/.claude/skills/` for deploy-public, etc.
- Session naming convention: `cc-mini--topic-name` via `/rename`
