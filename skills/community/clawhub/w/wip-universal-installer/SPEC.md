# The Universal Interface Specification

Every tool is a sensor, an actuator, or both. Every tool should be accessible through multiple interfaces. We call this the Universal Interface.

This is the spec.

## The Six Interfaces

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

### 3. MCP Server

A JSON-RPC server implementing the Model Context Protocol. Any MCP-compatible agent can use it.

**Convention:** `mcp-server.mjs` (or `.js`, `.ts`) at the repo root. Uses `@modelcontextprotocol/sdk`.

**Detection:** One of `mcp-server.mjs`, `mcp-server.js`, `mcp-server.ts`, `dist/mcp-server.js` exists.

**Install:** Add to `.mcp.json`:

```json
{
  "tool-name": {
    "command": "node",
    "args": ["/path/to/mcp-server.mjs"]
  }
}
```

### 4. OpenClaw Plugin

A plugin for OpenClaw agents. Lifecycle hooks, tool registration, settings.

**Convention:** `openclaw.plugin.json` at the repo root.

**Detection:** `openclaw.plugin.json` exists.

**Install:** Copy to `~/.openclaw/extensions/<name>/`, run `npm install --omit=dev`.

### 5. Skill (SKILL.md)

A markdown file that teaches agents when and how to use the tool. The instruction interface.

**Convention:** `SKILL.md` at the repo root. YAML frontmatter with name, version, description, metadata.

**Detection:** `SKILL.md` exists.

**Install:** Referenced by path. Agents read it when they need the tool.

```yaml
---
name: wip-grok
version: 1.0.0
description: xAI Grok API. Search the web, search X, generate images.
metadata:
  category: search,media
  capabilities:
    - web-search
    - image-generation
---
```

### 6. Claude Code Hook

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

Not every tool needs all six interfaces. Build the ones that make sense.

The minimum viable agent-native tool has two interfaces: **Module** (importable) and **Skill** (agent instructions). Add CLI for humans. Add MCP for agents that speak MCP. Add OpenClaw/CC Hook for specific platforms.

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

## The Reference Installer

`ldm install` is the primary installer (part of LDM OS). `wip-install` is the standalone fallback. Both scan a repo, detect which interfaces exist, and install them all. One command.

```bash
ldm install /path/to/repo           # local (via LDM OS)
ldm install org/repo                # from GitHub
ldm install org/repo --dry-run      # detect only
wip-install /path/to/repo           # standalone fallback (bootstraps LDM OS if needed)
wip-install --json /path/to/repo    # JSON output
```

For toolbox repos (with a `tools/` directory containing sub-tools), the installer enters toolbox mode and installs each sub-tool.

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
