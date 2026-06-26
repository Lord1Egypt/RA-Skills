# Memory Crystal + Claude Code Native Memory: Integration Plan

*Written 2026-02-28 by Claude Code*

## The Problem

Claude Code has its own built-in memory system: CLAUDE.md files (user-written) and auto memory (Claude-written, stored at `~/.claude/projects/<project>/memory/`). Memory Crystal is a separate, deeper memory layer that already runs alongside it. But they don't talk to each other. They're two memory systems running in parallel, unaware of each other.

Memory Crystal needs to work as a standalone product across six surfaces: Claude Code CLI, Claude Desktop, Claude web, Claude iOS, ChatGPT macOS/iOS/web. Each surface has different native memory capabilities. The integration plan must account for all of them.

## What Each Surface Has Natively

| Surface | Native Memory | What's Missing |
|---------|--------------|----------------|
| Claude Code CLI | CLAUDE.md + auto memory (`~/.claude/projects/*/memory/`) | Cross-project search, cross-agent, cross-device |
| Claude Desktop | CLAUDE.md + auto memory (same as CLI) | Same gaps as CLI |
| Claude web | Project instructions only | No persistent memory across sessions |
| Claude iOS | Syncs from web setup | No persistent memory across sessions |
| ChatGPT macOS/iOS/web | ChatGPT's built-in memory (opaque, limited) | No structured memory, no search, no sovereignty |

Memory Crystal fills the gaps: cross-project, cross-agent, cross-device, sovereign, searchable.

## Current State (What Already Works)

### Claude Code CLI Integration (local)
- **cc-hook.ts** runs as a Stop hook after every session
- Captures conversation turns from session JSONL transcripts
- Ingests into crystal.db (local) or relays to Mini (remote)
- Archives transcripts to `~/.ldm/agents/cc-mini/memory/transcripts/`
- Writes daily breadcrumbs to `~/.ldm/agents/cc-mini/memory/daily/`
- Generates session summaries

### MCP Server (local)
- Runs via `.mcp.json` as stdio MCP server
- Provides crystal_search, crystal_remember, crystal_forget, crystal_status, crystal_sources_*
- Available in Claude Code CLI and Claude Desktop

### OpenClaw Plugin
- Captures Lesa's conversations via agent_end hook
- Same tools as MCP server
- Runs continuously (gateway process)

### Cloud MCP Server (in progress, PR #10)
- Remote HTTP MCP server on Cloudflare Workers
- OAuth 2.1 + DCR for ChatGPT and Claude connector auth
- 6 tools: memory_search, memory_remember, memory_forget, memory_status, memory_log, memory_upload
- Encrypted relay to Mini (Tier 1) or cloud search (Tier 2)

## What Needs to Be Built

### 1. Index Claude Code's Auto Memory Files

Claude Code writes auto memory to `~/.claude/projects/<project>/memory/`. These are markdown files with build commands, debugging insights, preferences, patterns. Memory Crystal should index them so they become searchable across all agents and devices.

**Implementation:**

```
crystal sources add ~/.claude/projects/ --name claude-auto-memory
crystal sources sync claude-auto-memory
```

This already works with existing `crystal_sources_add` / `crystal_sources_sync`. But it needs to be:

- **Automated.** The cc-hook.ts Stop hook should trigger a sync after ingesting conversation turns. Not a full sync every time... just check if any files changed since last sync.
- **Incremental.** The sources system already does SHA-256 hash comparison. Only re-index changed files.
- **Filtered.** Only index `.md` files. Skip JSONL session files in `~/.claude/projects/*/` (those are raw transcripts, already captured by cc-hook).

**Changes needed:**
- `cc-hook.ts`: After conversation ingest, call `crystal.sourcesSync('claude-auto-memory', { quick: true })` if the collection exists
- `core.ts`: Add a `quick` sync option that only checks mtime, not full directory scan
- `cli.ts`: Add `crystal auto-sync` command for manual trigger

**File tree indexed:**
```
~/.claude/projects/
├── -Users-lesa--openclaw/memory/
│   ├── MEMORY.md
│   ├── debugging.md
│   └── patterns.md
├── -Users-lesa-Documents-Projects-*/memory/
│   └── MEMORY.md
└── ... (all project auto memories)
```

### 2. Ship .claude/rules/memory-crystal.md

When someone installs Memory Crystal for Claude Code, they need instructions loaded into every session telling Claude how to use the tools. Instead of asking users to edit their CLAUDE.md, ship a rules file.

**File: `.claude/rules/memory-crystal.md`** (installed to the user's project or home)

```markdown
# Memory Crystal

You have access to Memory Crystal, a persistent memory system that works across
all your projects, devices, and AI agents.

## Tools available (via MCP)

- crystal_search: Search all stored memories semantically. Use this before
  starting work on any topic to check for existing context.
- crystal_remember: Store important facts, preferences, decisions. Use after
  significant conversations or discoveries.
- crystal_forget: Deprecate a memory by ID if it's wrong or outdated.
- crystal_status: Check memory system health and stats.

## When to search

- Before starting a new task (check for prior work)
- When the user references something from a previous session
- When you need context about the project's history

## When to remember

- Architectural decisions
- User preferences confirmed across multiple sessions
- Solutions to recurring problems
- Key facts about the project that aren't in code
```

**Installation:** `crystal init` should offer to install this file at `~/.claude/rules/memory-crystal.md` (user-level, applies to all projects).

**Changes needed:**
- `cli.ts`: Extend `crystal init` to create the rules file
- Ship the rules file as a template in the package

### 3. Standalone Installation Path (No OpenClaw Required)

Memory Crystal must work with a bare Claude Code CLI installation. No OpenClaw, no gateway, no extensions directory. Just:

```bash
npm install -g memory-crystal
crystal init
```

**What `crystal init` does:**

1. Scaffold `~/.ldm/` directory structure (already implemented in ldm.ts)
2. Create `~/.ldm/memory/crystal.db` (empty, ready for use)
3. Register MCP server in Claude Code's config:
   - Write to `~/.claude/settings.json` (add to `mcpServers` section)
   - Or create project-level `.mcp.json` if user prefers
4. Install Stop hook in `~/.claude/settings.json` for cc-hook.ts
5. Install `.claude/rules/memory-crystal.md`
6. Prompt for OpenAI API key (for embeddings) or offer Ollama local alternative
7. Store API key in `~/.ldm/secrets/openai-api-key` (or 1Password reference)

**What `crystal init` does NOT do:**
- Touch `~/.openclaw/` anything
- Require OpenClaw to be installed
- Require a running gateway

**Changes needed:**
- `cli.ts`: Major expansion of `init` command
- New file: `src/installer.ts` with installation logic
- Template files for rules, MCP config, hook config

### 4. MCP Server Registration

The MCP server needs to be registered so Claude Code discovers it. Two paths:

**Option A: Global registration (recommended for standalone)**
Add to `~/.claude/settings.json`:
```json
{
  "mcpServers": {
    "memory-crystal": {
      "command": "crystal",
      "args": ["mcp-serve"],
      "env": {}
    }
  }
}
```

**Option B: Project-level registration**
Create `.mcp.json` in project root:
```json
{
  "mcpServers": {
    "memory-crystal": {
      "command": "crystal",
      "args": ["mcp-serve"],
      "env": {}
    }
  }
}
```

Currently, the MCP server entry point is `dist/mcp-server.js` (requires knowing the install path). For standalone, the `crystal` CLI binary should have a `mcp-serve` subcommand that launches the MCP server.

**Changes needed:**
- `cli.ts`: Add `crystal mcp-serve` command (just imports and runs mcp-server.ts logic)
- `installer.ts`: Register in Claude Code settings

### 5. Stop Hook Registration

The cc-hook.ts captures conversations. It needs to be registered as a Claude Code Stop hook:

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "crystal cc-hook",
            "timeout": 30000
          }
        ]
      }
    ]
  }
}
```

Currently registered as `node /path/to/dist/cc-hook.js`. For standalone, use the `crystal` binary:

**Changes needed:**
- `cli.ts`: Add `crystal cc-hook` command (reads stdin, runs cc-hook logic)
- `installer.ts`: Register hook in Claude Code settings

### 6. Claude Desktop Integration

Claude Desktop supports both local stdio MCP and remote HTTP MCP. Users get both:

- **Local MCP** (stdio): Same as CLI. Full Crystal access. `crystal mcp-serve`.
- **Remote MCP** (connector): Cloud worker. For when the user is away from their machine.

Claude Desktop auto-discovers MCP servers from `~/.claude/settings.json`. No extra work needed beyond the CLI registration.

### 7. Claude Web + iOS Integration

These surfaces only support remote HTTP MCP (connectors). Users connect to the cloud worker:

- Go to Settings > Connectors in Claude web
- Add Memory Crystal (URL: `https://memory-crystal.wipcomputer.workers.dev/mcp`)
- OAuth flow, consent page, token issued
- Tools appear in Claude web/iOS sessions

This is already covered by the cloud MCP server (PR #10). No additional work for this plan.

### 8. ChatGPT Integration

Same cloud MCP server as Claude. ChatGPT supports MCP via Developer Mode and Apps connector:

- Same URL, same OAuth, same tools
- Submit to ChatGPT Apps Directory separately
- Custom GPT with system instructions (already written in PR #10)

Already covered by cloud MCP server. No additional work for this plan.

### 9. Two-Way Sync Between Auto Memory and Crystal

This is the most interesting integration. Claude Code's auto memory learns things. Crystal learns things. They should inform each other.

**Crystal -> Auto Memory (warm-starting sessions):**

When a new Claude Code session starts, Crystal could pre-populate relevant context. But Claude Code doesn't have a "start" hook... only Stop. And CLAUDE.md / auto memory are already loaded at session start.

The better approach: the `.claude/rules/memory-crystal.md` file tells Claude to `crystal_search` proactively. Claude reads the rule, searches Crystal at the start of complex tasks, and gets cross-project context.

**Auto Memory -> Crystal (capturing Claude's learnings):**

The sources indexing (item 1 above) handles this. Claude writes to auto memory. Crystal indexes auto memory files. The learnings become searchable globally.

**No active sync needed.** The existing tools handle both directions:
- Claude's auto memory -> Crystal via source indexing (periodic)
- Crystal -> Claude sessions via crystal_search (on demand, guided by rules file)

### 10. Cross-Device Memory Flow

The full picture of how memory flows:

```
Claude Code CLI (Mac Mini)
  ↓ cc-hook (Stop hook)
  ↓ Ingest conversation turns
  ↓ Index auto memory files
  → crystal.db (local, primary)

Claude Code CLI (MacBook Air)
  ↓ cc-hook (Stop hook)
  ↓ Encrypt + relay
  → Relay Worker (R2) → Mini poller → crystal.db

Claude Desktop (any machine)
  ↓ MCP server (local stdio)
  → crystal.db (same as CLI)

Claude Web / iOS
  ↓ Cloud MCP server
  ↓ Encrypt + relay (Tier 1) or D1 + Vectorize (Tier 2)
  → Relay Worker → Mini poller → crystal.db

ChatGPT (macOS / iOS / web)
  ↓ Cloud MCP server
  ↓ Encrypt + relay
  → Relay Worker → Mini poller → crystal.db

OpenClaw (Lesa)
  ↓ agent_end hook
  → crystal.db (local, same DB)
```

All roads lead to crystal.db on the Mini. Every surface, every agent, every device.

## Build Phases

### Phase A: Standalone CLI (3-4 days)

Make Memory Crystal installable and functional without OpenClaw.

1. Add `crystal mcp-serve` subcommand
2. Add `crystal cc-hook` subcommand (stdin-based, like current cc-hook.ts)
3. Expand `crystal init` to:
   - Scaffold ~/.ldm/
   - Register MCP server in ~/.claude/settings.json
   - Register Stop hook in ~/.claude/settings.json
   - Install .claude/rules/memory-crystal.md
   - Prompt for embedding API key (OpenAI or Ollama)
4. Add `crystal auto-sync` command for manual auto-memory indexing
5. Test: fresh machine, no OpenClaw, `npm install -g memory-crystal && crystal init`

### Phase B: Auto Memory Indexing (1-2 days)

Index Claude Code's auto memory files into Crystal.

1. Add quick-sync option to sourcesSync (mtime-only check)
2. Auto-register `~/.claude/projects/` as source collection during `crystal init`
3. Trigger quick-sync in cc-hook after conversation ingest
4. Test: Claude writes to auto memory, Crystal indexes it, searchable via crystal_search

### Phase C: Rules File + Behavior Tuning (1 day)

Ship the memory-crystal.md rules file and tune Claude's behavior.

1. Write the rules file template
2. Install during `crystal init`
3. Test: Claude proactively searches Crystal, remembers important facts
4. Iterate on the rules based on real usage

### Phase D: Cloud MCP Server (already in progress, PR #10)

This is the existing cloud work. Continues in parallel.

1. Deploy cloud Worker
2. Connect ChatGPT + Claude web/iOS
3. Test end-to-end relay flow

### Phase E: npm Package + Distribution (2-3 days)

Package for public distribution.

1. Publish to npm as `memory-crystal` (or `@wipcomputer/memory-crystal`)
2. README with installation instructions
3. `npx memory-crystal init` one-liner
4. Homebrew formula (optional, for non-Node users)
5. Landing page with setup video

## File Map (New / Changed)

```
src/
  cli.ts            ← Add mcp-serve, cc-hook, auto-sync, expand init
  installer.ts      ← NEW: installation logic (MCP registration, hook setup, rules)
  cc-hook.ts        ← Add auto-memory sync trigger after ingest
  core.ts           ← Add quick-sync option to sourcesSync
  mcp-server.ts     ← No changes needed
  ldm.ts            ← No changes needed (already standalone)

templates/
  rules/
    memory-crystal.md   ← NEW: shipped rules file for Claude Code
  mcp-config.json       ← NEW: template for .mcp.json registration
  hook-config.json      ← NEW: template for Stop hook registration

cloud/                  ← Existing cloud MCP work (PR #10)
```

## Key Design Decisions

1. **`crystal` CLI is the universal entry point.** Not `node dist/mcp-server.js`. Not `npx`. Just `crystal`. This means the npm package installs a global binary.

2. **`crystal init` is the one command.** Users run it once. It sets up everything: directories, MCP registration, hooks, rules, API key. Idempotent... safe to run again.

3. **No OpenClaw dependency.** `~/.ldm/` is the home. If OpenClaw is installed, Crystal detects it and uses shared state. If not, Crystal works alone.

4. **Auto memory indexing is opt-in but recommended.** `crystal init` offers to index `~/.claude/projects/`. Users can decline. The sync is lightweight (mtime check, incremental).

5. **Rules file over CLAUDE.md modifications.** Don't touch the user's CLAUDE.md. Ship a `.claude/rules/memory-crystal.md` that loads automatically. Clean, modular, removable.

6. **Same DB, every surface.** crystal.db on the Mini is the single source of truth. Cloud, relay, local hooks... all feed into it. Search is always local (Tier 1) or mirrored (Tier 2).

## Verification Checklist

```
Phase A:
[ ] crystal init works on clean machine (no OpenClaw)
[ ] MCP server registered and functional in Claude Code
[ ] Stop hook registered and capturing conversations
[ ] Rules file installed and Claude uses Crystal tools
[ ] API key stored securely in ~/.ldm/secrets/

Phase B:
[ ] Auto memory files indexed after crystal init
[ ] Quick-sync runs after each cc-hook capture
[ ] Auto memory content searchable via crystal_search
[ ] No duplicate indexing (hash-based dedup works)

Phase C:
[ ] Claude proactively searches Crystal for context
[ ] Claude remembers significant facts without being told
[ ] Rules file doesn't conflict with existing CLAUDE.md

Phase D:
[ ] Cloud MCP server deployed
[ ] ChatGPT connects and uses all 6 tools
[ ] Claude web/iOS connects as connector
[ ] Relay drops arrive on Mini and ingest correctly

Phase E:
[ ] npm package published and installable
[ ] npx memory-crystal init works
[ ] README covers all installation scenarios
[ ] Works on macOS and Linux
```
