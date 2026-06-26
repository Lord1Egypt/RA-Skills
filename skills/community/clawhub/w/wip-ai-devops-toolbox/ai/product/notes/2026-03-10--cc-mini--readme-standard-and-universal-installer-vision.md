# README Standard, Universal Installer, and Interface System

Date: 2026-03-10 (created), 2026-03-11 (updated)
Source: Parker, across memory-crystal + wip-dev-tools + wip-ai-devops-toolbox sessions

---

## The Six Interfaces

Every tool can ship up to six interfaces. These are the ways humans and AIs interact with a tool.

| Interface | What it is | Where it deploys |
|-----------|-----------|-----------------|
| CLI | Shell commands | Global bin (`/opt/homebrew/bin/`) via `npm install -g` |
| Module | Node.js import | Already available via npm |
| MCP | Model Context Protocol server | `~/.claude/` (user scope) + `~/.openclaw/.mcp.json` |
| OC Plugin | OpenClaw agent runtime plugin | `~/.ldm/extensions/<name>/` + `~/.openclaw/extensions/<name>/` |
| Skill | SKILL.md file (works in both Claude Code and OpenClaw) | `~/.openclaw/skills/<tool>/SKILL.md` |
| CC Hook | PreToolUse hook in Claude Code | `~/.claude/settings.json` |

Detection is automatic. Universal Installer scans for signals:
- `package.json` has `bin`? -> CLI
- `package.json` has `main`/`exports`? -> Module
- `mcp-server.mjs` exists? -> MCP
- `openclaw.plugin.json` exists? -> OC Plugin
- `SKILL.md` exists? -> Skill
- `guard.mjs` or `claudeCode.hook` in package.json? -> CC Hook

Skills are one interface, one file format. The same SKILL.md works in Claude Code (reads it as a prompt) and OpenClaw (loaded from `~/.openclaw/skills/`). Universal Installer deploys to both.

---

## README Standard

Every repo follows this pattern. No exceptions.

### Structure

```
# Tool Name

Tagline. What it solves in human words. Not what it is technically.

## Teach Your AI to [verb]

Copy-paste prompt block. The AI reads the SKILL.md, explains itself,
asks if you want to install, runs the installer. That's onboarding.

## Features

Human-readable feature list. Name, plain description, stability tag.
No architecture diagrams. No config references. Just what it does
for you.

## Interface Coverage

Table showing which interfaces each tool ships (auto-generated from detection).

## More Info

- Technical Documentation ... link
- Universal Interface Spec ... link
- Other docs (Dev Guide, etc.)

## License
```

### Rules

- The tagline is NOT "a tool that does X". It's what it solves: "All your AI tools. One shared memory. Private, searchable, sovereign."
- "Teach Your AI" is the install section. User copies a prompt into their AI. The AI reads SKILL.md from GitHub, explains what it is, asks questions, offers to install. That's onboarding. Always dry-run first.
- Features are human-readable. Each has: name, plain-English description, stability tag (Stable, Beta, etc). No technical jargon.
- Interface Coverage shows what each tool ships. Column names match the six interfaces above.
- "More Info" links to technical documentation (architecture, API, config, design decisions). That stuff does NOT go in the README.
- License at the bottom. Standard dual MIT+AGPL block.
- That's it. Nothing else in the README.
- Everything else (build steps, dev setup, architecture, API surface, config options, design decisions) goes in TECHNICAL.md or linked docs.

### Reference Implementations

- AI DevOps Toolbox: `wipcomputer/wip-ai-devops-toolbox` (multi-tool toolbox pattern)
- Memory Crystal: `wipcomputer/memory-crystal` (single-tool pattern)

---

## Universal Installer

One command installs everything a repo ships. Run it over any repo and it:

1. Detects which interfaces the repo supports (scans for the signals above)
2. If the repo has a `tools/` directory with sub-tools, enters toolbox mode and installs each one
3. For each tool, deploys every detected interface to the right location
4. Smart update: detects what's already installed, skips identical versions, replaces stale symlinks, doesn't duplicate entries

### Dogfooding

wip-ai-devops-toolbox installs itself using the universal installer it ships. That's the test. If `wip-install wipcomputer/wip-ai-devops-toolbox` works clean, it works for everything.

### Interface Coverage (wip-ai-devops-toolbox, current as of v1.8.2+)

| # | Tool | CLI | Module | MCP | OC Plugin | Skill | CC Hook |
|---|------|-----|--------|-----|-----------|-------|---------|
| 1 | Universal Installer | Y | Y | | | Y | |
| 2 | Dev Guide | | | | | | |
| 3 | LDM Dev Tools.app | | | | | | |
| 4 | Release Pipeline | Y | Y | Y | | Y | |
| 5 | Private-to-Public Sync | Y | | | | Y | |
| 6 | Post-Merge Branch Naming | Y | | | | Y | |
| 7 | Identity File Protection | Y | Y | | Y | Y | Y |
| 8 | License Guard | Y | | | | | |
| 9 | License Rug-Pull Detection | Y | Y | Y | | Y | |
| 10 | Repo Visibility Guard | Y | Y | Y | Y | Y | Y |
| 11 | Repo Manifest Reconciler | Y | Y | Y | | Y | |
| 12 | Repo Init | Y | | | | Y | |

---

## README Formatter (future tool)

`wip-readme-format`. Point it at a repo and it:

1. Runs `wip-install --json` to detect all interfaces
2. Rewrites the README to match the standard above
3. Moves technical content to TECHNICAL.md
4. Generates the interface coverage table from detection results
5. Validates the structure matches the standard

Same pattern as wip-release enforcing the release pipeline. May be a standalone tool or part of the toolbox.
