# Release Notes: LDM OS v0.2.0

## The Product Page

LDM OS now tells its own story. The README is the product page for the entire ecosystem.

Six pillars: Identity, Memory, Ownership, Collaboration, Compatibility, Payments. Everything WIP Computer builds either ships with LDM OS or plugs into it.

## Included Skills

These ship with LDM OS. You get them on `ldm init`.

- **Universal Installer** ... point any skill, application, or plugin at any AI running LDM OS, and it will convert those skills to work with all of your AIs. Engine moved from DevOps Toolbox to LDM OS.
- **Shared Workspace** ... one directory for all your AIs. Memories, tools, identity files, boot config. Lives in one folder on your computer. Easy to back up, easy to move, easy to own.
- **System Pulse** ... is everything working? What's installed? What needs fixing? A complete picture of your AI setup in seconds.
- **Recall** ... every session, your AI starts with full context. Identity, memory, tools, what happened yesterday. No blank slates.
- **LUME** ... Language for Unified Memory and Emergence. A memory language for AI agents to document their own learning and maintain continuity across sessions.

Each included skill has its own technical docs page in `docs/`.

## Optional Skills

The OS connects your AIs. Skills are what they actually use. Each one is a full product that plugs into LDM OS.

Memory Crystal, AI DevOps Toolbox, Agent Pay, Dream Weaver Protocol, Bridge. Plus 1Password, Markdown Viewer, xAI Grok, X Platform, OpenClaw. Full catalog at `docs/optional-skills.md`.

## The `ldm` CLI

Five commands for a full extension lifecycle:

- `ldm init` ... scaffold `~/.ldm/`, write version.json, seed the extension registry. Interactive catalog picker shows available skills.
- `ldm install <org/repo>` ... clone, detect interfaces, deploy, register. Also resolves catalog IDs (e.g. `ldm install memory-crystal`).
- `ldm install` (bare) ... show what's installed, what's available, update all.
- `ldm doctor` ... check health of every extension.
- `ldm status` ... show version, extension count, installed skills.

All commands support `--dry-run` and `--json`.

## Interface Detection

The installer automatically detects six interface types in any repo:

| Interface | Detection | Deployment |
|-----------|----------|------------|
| CLI | `bin` entries in package.json | `npm install -g` |
| MCP Server | `mcp-server.mjs` or `mcp-server.js` | `claude mcp add --scope user` |
| OpenClaw Plugin | `openclaw.plugin.json` | `~/.ldm/extensions/` + `~/.openclaw/extensions/` |
| Skill | `SKILL.md` or `skills/` | `~/.openclaw/skills/` |
| CC Hook | `guard.mjs` or `claudeCode.hook` | `~/.claude/settings.json` |
| Module | `main`/`exports` in package.json | importable |

## Safe Deployment

Three bugs from the original `wip-install` are fixed:

1. **TypeScript build** ... detects `tsconfig.json` or `build` script and runs build before deploying.
2. **Atomic swap** ... deploys to a temp directory first, verifies, then swaps. Old install stays intact if new one fails.
3. **OpenClaw plugin naming** ... checks `openclaw.plugin.json` for the expected directory name.

## Skill Catalog

`catalog.json` ships with the package. Nine skills across core, utilities, apps, and APIs. Catalog IDs resolve automatically in `ldm install`.

## SKILL.md

Teaches any AI how to install LDM OS. Same "Teach Your AI" pattern as Memory Crystal and the DevOps Toolbox.

## Cross-linking

All three products now know about each other. Memory Crystal and DevOps Toolbox READMEs link back to LDM OS. Both installers delegate to `ldm install` when available, fall back to standalone when not.
