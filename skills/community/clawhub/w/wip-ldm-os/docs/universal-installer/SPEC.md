# The Universal Interface Specification

Every tool is a sensor, an actuator, or both. Every tool should be accessible through multiple interfaces. We call this the Universal Interface.

This is the spec.

## Architecture Layers

Five layers. Each one does one job. Together they let any AI safely consume any product.

| Layer | What it is | Where it lives |
|-------|-----------|----------------|
| **Interface** | What a product exposes (CLI, MCP, Skill, etc.). Eight kinds, listed below in canonical order. | The product repo. |
| **Installer** | Detects a product's interfaces and installs them all. `ldm install`. Stable, alpha, and beta tracks via flags. | `wip-ldm-os` (`bin/ldm.js`). |
| **Catalog** | Slug→source resolver (npm package, repo, registry/CLI matches, status) **plus** the trust surface: provenance, version pinning, permission scopes, audits, install/update/revocation. Stays human-readable and browseable as a fallback discovery surface; not the primary steering wheel. | `catalog.json` at the LDM OS root. |
| **Install Spec** | Agent-readable install runbook published at `wip.computer/install/<slug>.txt`. Track-neutral. Teaches an AI to safely check, explain, dry-run, install, update, and pair the product. | `https://wip.computer/install/<slug>.txt`. See [Install Spec](#install-spec). |
| **Stacks** | Multi-product bundles. One install brings up several products and their MCP servers. | `catalog.json.stacks`. |

Use the install spec URL to learn the safe install flow; use catalog to resolve the slug; use `ldm install` with stable/alpha/beta track flags; installer detects and installs the product's declared interfaces; stacks install bundles.

### Primary flow

The user's path is **outcome → agent resolves services → install specs / catalog / auth → bespoke artifact**. Not "browse a plugin store and pick one." The catalog stays browseable for the times a user wants to look around, but it is no longer the steering wheel. The steering wheel is the user's stated outcome and the agent's composition.

**Personal context** (goals, preferences, prior experiments, constraints) does not come from this spec. It comes from **Memory Crystal**, a sibling LDM OS component. The universal-installer spec describes how *services* expose themselves; Memory Crystal describes how the *agent* knows you. Both feed the bespoke composition.

## The Eight Interfaces

The canonical order is fixed: CLI (1), Module (2), MCP Server local stdio (3), Remote MCP (4), OpenClaw Plugin (5), Skill (6), Claude Code Hook (7), Claude Code Plugin (8). Local and Remote MCP sit next to each other because they are sibling transports of the same protocol. Claude Code Plugin sits last because it bundles the others.

### 1. CLI

A shell command. The most universal interface. If it has a terminal, it works.

**Convention:** `package.json` with a `bin` field.

**Detection:** `pkg.bin` exists.

**Install:** `npm install -g .` or `npm link`.

```json
{
  "bin": {
    "wip-grok": "./cli.mjs"
  }
}
```

### 2. Module

An importable ES module. The programmatic interface. Other tools compose with it.

**Convention:** `package.json` with `main` or `exports` field. File is `core.mjs` by convention.

**Detection:** `pkg.main` or `pkg.exports` exists.

**Install:** `npm install <package>` or import directly from path.

```json
{
  "type": "module",
  "main": "core.mjs",
  "exports": {
    ".": "./core.mjs",
    "./cli": "./cli.mjs"
  }
}
```

### 3. MCP Server (local stdio)

A JSON-RPC server implementing the Model Context Protocol over stdio. Spawned as a child process by the agent (Claude Code, Cursor, OpenClaw). For the HTTP/SSE sibling, see [#4 Remote MCP](#4-remote-mcp).

**Convention:** `mcp-server.mjs` (or `.js`, `.ts`) at the repo root. Uses `@modelcontextprotocol/sdk`.

**Detection:** One of `mcp-server.mjs`, `mcp-server.js`, `mcp-server.ts`, `dist/mcp-server.js` exists.

**Install:** Add to `.mcp.json` with `command` + `args`:

```json
{
  "tool-name": {
    "command": "node",
    "args": ["/path/to/mcp-server.mjs"]
  }
}
```

### 4. Remote MCP

The HTTP/SSE (or streamable HTTP) sibling of #3. Hosted at an HTTPS endpoint, not spawned locally. The transport that lights up Claude Desktop connectors, web, and mobile clients.

**Contract:** Remote MCP endpoint is **declared by package/catalog metadata** and **registered by `ldm install`**. No filesystem-sniffing fallback.

**Convention:** `mcp.remote` field in `package.json`:

```json
{
  "mcp": {
    "remote": {
      "url": "https://example.com/mcp",
      "transport": "streamable-http",
      "auth": "oauth"
    }
  }
}
```

`url` may be a placeholder (`"https://__DEPLOYED_URL__"`) when the repo ships the server code and the URL is supplied by the catalog at install time.

**Detection:** `package.json.mcp.remote.url` is a string.

**Install:** Add to `.mcp.json` as a remote entry (`url` + `transport` instead of `command` + `args`). Print a one-line Claude Desktop hint so the user can also add it under Connectors. Implementation tracked in [bugs/installer/](../../ai/product/bugs/installer/2026-04-28--cc-mini--installer-remote-mcp-install.md).

```json
{
  "tool-name": {
    "url": "https://example.com/mcp",
    "transport": "streamable-http"
  }
}
```

**How it differs from #3:** sibling transport, not a flag on #3.

| | #3 Local stdio | #4 Remote |
|---|---|---|
| Transport | stdio (child process) | HTTPS + SSE or streamable HTTP |
| Process model | Per-session spawn | Long-running, multi-tenant |
| Auth | Trust the local process | OAuth or shared secret |
| Surfaces | Claude Code, Cursor, OpenClaw | Claude Desktop, web, mobile |

### 5. OpenClaw Plugin

A plugin for OpenClaw agents. Lifecycle hooks, tool registration, settings.

**Convention:** `openclaw.plugin.json` at the repo root.

**Detection:** `openclaw.plugin.json` exists.

**Install:** Copy to `~/.openclaw/extensions/<name>/`, run `npm install --omit=dev`.

### 6. Skill (SKILL.md)

A markdown file that teaches agents when and how to use the tool. The instruction interface. Follows the [Agent Skills Spec](https://agentskills.io/specification).

**Convention:** `SKILL.md` at the repo root. YAML frontmatter with name, description. Optional `references/` directory for context files.

**Platform variants:** Codex CLI reads `AGENTS.md` instead of `SKILL.md`, with the same role and the same content shape. Treat `AGENTS.md` as the Codex-flavored filename for this same interface, not a separate interface. A repo may ship both (or symlink one to the other) so it works in Codex and SKILL.md-aware agents.

**Detection:** `SKILL.md` exists.

**Install:** `SKILL.md` deployed to `~/.openclaw/skills/<name>/`. If `references/` exists, deployed alongside SKILL.md and to `settings/docs/skills/<name>/` in the workspace.

**Structure:**
```
repo/
├── SKILL.md          # < 150 lines. Process only. Imperative instructions.
└── references/       # Optional. Context files loaded on demand.
    ├── PRODUCT.md    # What the product is
    ├── TOOLS.md      # MCP tools, CLI commands
    └── ...
```

**Key rules (from Agent Skills Spec):**
- SKILL.md body < 5000 tokens. Process goes in SKILL.md, context goes in references/.
- Imperative language: "Run this command" not "This product enables..."
- Progressive disclosure: metadata loaded at startup, body on activation, references on demand.

```yaml
---
name: wip-grok
description: >
  xAI Grok API. Search the web, search X, generate images.
  Use when asked to search, browse, or generate images.
metadata:
  category: search,media
  capabilities:
    - web-search
    - image-generation
---
```

### 7. Claude Code Hook

A hook that runs during Claude Code's tool lifecycle (PreToolUse, Stop, etc.).

**Convention:** `guard.mjs` at repo root, or `claudeCode.hook` in `package.json`.

**Detection:** `guard.mjs` exists, or `pkg.claudeCode.hook` is defined.

**Install:** Added to `~/.claude/settings.json` under `hooks`.

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Edit|Write",
      "hooks": [{
        "type": "command",
        "command": "node /path/to/guard.mjs",
        "timeout": 5
      }]
    }]
  }
}
```

### 8. Claude Code Plugin

A distributable plugin for Claude Code. Bundles skills, agents, hooks, MCP servers, and LSP servers into one installable package. Shareable via marketplaces.

**Convention:** `.claude-plugin/plugin.json` at the repo root.

**Detection:** `.claude-plugin/plugin.json` exists.

**Install:** Registered with Claude Code via `/plugin install` or marketplace.

```
your-plugin/
├── .claude-plugin/
│   └── plugin.json   # manifest (name, version, description)
├── skills/           # SKILL.md files
├── agents/           # subagent definitions
├── hooks/
│   └── hooks.json    # event handlers
├── .mcp.json         # MCP server configs
└── .lsp.json         # LSP server configs
```

```json
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "What it does",
  "author": { "name": "Your Name" }
}
```

### Out of scope by design

**Disposable, agent-generated artifacts** (custom dashboards, ephemeral scripts, one-off automations, the 300-line cardio tracker someone vibe-codes in an hour) are out of scope for this spec. They are products of an agent, not Universal Interface products. The eight interfaces describe what the agent has to *compose with*. The composition output is not itself a numbered interface and never will be.

### Worked example (compact sketch)

User says: *"Help me track my resting heart rate over the next 8 weeks. Goal: 50 → 45 bpm. Zone 2 cardio + 1 HIIT/week."*

The agent:

1. Reads personal context from Memory Crystal (RHR baseline, prior experiments, units preference).
2. Resolves the treadmill via catalog → install spec URL → declared Remote MCP (#4) for workout data.
3. Pulls calendar/time semantics for the 8-week window.
4. Composes a disposable dashboard (~300 lines).

The dashboard is **not** a Universal Interface product. It is the agent's output, assembled from agent-native sensors and actuators. Full version of this example is tracked separately ... see [bugs/installer/2026-04-28--cc-mini--installer-cardio-tracker-worked-example.md](../../ai/product/bugs/installer/2026-04-28--cc-mini--installer-cardio-tracker-worked-example.md).

### Future considerations

*LSP as a standalone interface (#9).* LSP servers are currently surfaced via Claude Code Plugin bundles (#8) ... `.lsp.json` is part of the plugin shape. If a product ships a standalone LSP server outside a CC Plugin, we will add it as a numbered interface. Not added today because no WIP product ships one yet, and the spec should describe interfaces we install and use, not interfaces software could theoretically have.

## Architecture

Every repo that follows this spec has the same basic structure:

```
your-tool/
  core.mjs            pure logic, zero or minimal deps
  cli.mjs             thin CLI wrapper around core
  mcp-server.mjs      MCP server wrapping core functions as tools
  SKILL.md            agent instructions with YAML frontmatter
  package.json         name, bin, main, exports, type: module
  README.md            human documentation
  ai/                  development process (plans, todos, notes)
```

Not every tool needs all eight interfaces. Build the ones that make sense.

The minimum viable agent-native tool has two interfaces: **Module** (importable) and **Skill** (agent instructions). Add CLI for humans. Add local MCP (#3) for agents that speak MCP over stdio. Add Remote MCP (#4) when you want Claude Desktop / web / mobile to reach the same server. Add OpenClaw Plugin / CC Hook / CC Plugin for specific platforms.

## The `ai/` Folder

Every repo should have an `ai/` folder. This is where agents and humans collaborate on the project ... plans, todos, dev updates, research notes, conversations.

```
ai/
  plan/              architecture plans, roadmaps
  dev-updates/       what was built, session logs
  todos/
    PUNCHLIST.md     blockers to ship
    inboxes/         per-agent action items
  notes/             research, references, raw conversation logs
```

The `ai/` folder is the development process. It is not part of the published product.

**Public/private split:** If a repo is public, the `ai/` folder should not ship. The recommended pattern is to maintain a private working repo (with `ai/`) and a public repo (everything except `ai/`). The public repo has everything an LLM or human needs to understand and use the tool. The `ai/` folder is operational context for the team building it.

## The Installer

`ldm install` is the primary installer (part of LDM OS). `wip-install` is the standalone fallback. Both scan a repo or slug, detect which interfaces exist, and install them all. One command.

```bash
ldm install /path/to/repo               # local (via LDM OS)
ldm install org/repo                    # from GitHub
ldm install <slug>                      # from catalog (stable, default)
ldm install --alpha <slug>              # alpha (validation track)
ldm install --beta <slug>               # beta (validation track)
ldm install <slug> --dry-run            # detect only, no changes
wip-install /path/to/repo               # standalone fallback (bootstraps LDM OS if needed)
wip-install --json /path/to/repo        # JSON output
```

Tracks select the npm dist-tag (or git ref) the installer pulls from. The same install spec URL covers all three; the AI follows the spec, the user (or releasing agent) picks the track via flag.

For toolbox repos (with a `tools/` directory containing sub-tools), the installer enters toolbox mode and installs each sub-tool.

## Install Spec

An **install spec** is an agent-readable install runbook published at a stable URL:

```
https://wip.computer/install/<slug>.txt
```

The contract is the URL and the behavior, not the file origin. An install spec can be generated from `SKILL.md`, mirrored from it, or live alongside it. What matters is that any AI can fetch it, read it, and walk a user through a safe install.

### Behavior contract

The spec teaches an AI to:

1. **Check** whether the product is already installed and at what version.
2. **Explain** what the product is, what it installs, and what changes for this AI and the user's other AIs.
3. **Dry-run** so the user sees what will change before anything is touched.
4. **Install** only after explicit user consent.
5. **Update** an existing install (skip steps the user already did).
6. **Pair** any post-install steps (passkey, device pairing, gateway start, etc.) with explicit consent at each step.

### Tracks

One install spec covers all release tracks. The user picks via flag:

| Track | Flag | Audience |
|-------|------|----------|
| Stable | (default) `ldm install <slug>` | End users. Owner-dogfooded. |
| Beta | `ldm install --beta <slug>` | Validation; agents may install. |
| Alpha | `ldm install --alpha <slug>` | Validation; agents may install. |

The spec text itself is track-neutral. Tracks are an installer concern, not a copy concern.

### Install spec vs `agent.txt`

These are related, not the same. Both are agent-readable. They sit at different scopes:

- **`agent.txt`** ... site- or product-level entrypoint for agents. "What can agents do here? What routes exist? What policies apply?" Lives at the root of a site or product (e.g. `wip.computer/agent.txt`).
- **`install/<slug>.txt`** ... per-product install runbook. "How should an agent safely check, explain, dry-run, install, update, and pair this product?" Lives under `wip.computer/install/`.

`agent.txt` can point agents at install specs. An install spec does not replace `agent.txt`.

### Worked example: Codex Remote Control

Install spec: [`https://wip.computer/install/wip-codex-remote-control.txt`](https://wip.computer/install/wip-codex-remote-control.txt).

The user pastes one prompt into Codex (or any AI). The AI fetches the install spec, checks installed state, explains the product, runs `ldm install --dry-run wip-codex-remote-control`, and only installs (and starts the daemon, and pairs the phone) after the user says yes at each step. Tracks are selected by flag against the same URL.

## Examples

### AI DevOps Toolbox (this repo)

| # | Tool | Interfaces |
|---|------|------------|
| | **Repo Management** | |
| 1 | [Repo Visibility Guard](tools/wip-repo-permissions-hook/) | CLI + Module + MCP + OpenClaw + Skill + CC Hook |
| 2 | [Repo Manifest Reconciler](tools/wip-repos/) | CLI + Module + MCP + Skill |
| 3 | [Repo Init](tools/wip-repo-init/) | CLI + Skill |
| 4 | [README Formatter](tools/wip-readme-format/) | CLI + Skill |
| 5 | [Branch Guard](tools/wip-branch-guard/) | CLI + Module + CC Hook |
| | **License, Compliance, and Protection** | |
| 6 | [Identity File Protection](tools/wip-file-guard/) | CLI + Module + OpenClaw + Skill + CC Hook |
| 7 | [License Guard](tools/wip-license-guard/) | CLI + Skill |
| 8 | [License Rug-Pull Detection](tools/wip-license-hook/) | CLI + Module + MCP + Skill |
| | **Release & Deploy** | |
| 9 | [Release Pipeline](tools/wip-release/) | CLI + Module + MCP + Skill |
| 10 | [Private-to-Public Sync](tools/deploy-public/) | CLI + Skill |
| 11 | [Post-Merge Branch Naming](tools/post-merge-rename/) | CLI + Skill |
| 12 | [Universal Installer](tools/wip-universal-installer/) | CLI + Module + Skill |

### Other WIP Computer Tools

| Repo | Interfaces |
|------|------------|
| [Memory Crystal](https://github.com/wipcomputer/memory-crystal) | CLI + Module + MCP + OpenClaw + Skill |
| [LDM OS](https://github.com/wipcomputer/wip-ldm-os) | CLI + Module + Skill + CC Hook |
| [wip-grok](https://github.com/wipcomputer/wip-grok) | CLI + Module + MCP + Skill |
| [wip-x](https://github.com/wipcomputer/wip-x) | CLI + Module + MCP + Skill |
| [Markdown Viewer](https://github.com/wipcomputer/wip-markdown-viewer) | CLI + Module |
