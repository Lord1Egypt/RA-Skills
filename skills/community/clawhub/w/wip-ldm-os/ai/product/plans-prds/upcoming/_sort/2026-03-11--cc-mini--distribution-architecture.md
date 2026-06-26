# LDM OS Distribution Architecture

**Date:** 2026-03-11
**Author:** CC Mini
**Status:** Living document

---

## The Problem

An AI agent tries to read our SKILL.md from GitHub. Gets rate-limited. Can't tell the user what the tools do. The tools are invisible.

We build tools. We don't distribute them. wip-release says it publishes to npm, ClawHub, and GitHub. Most of it silently fails. 8 of 13 devops tools aren't on npm. 7 aren't on ClawHub. The two most important skills on ClawHub are stuck in "Scanning." Nobody knows because the errors are silent.

Documentation doesn't change behavior. Tools do. But tools nobody can find don't change anything either.

---

## Four Distribution Layers

In order of when they come online:

### Layer 1: wipcomputer.github.io (now)

Static CDN via GitHub Pages. No rate limits, no auth, free. Any AI can fetch from it.

- SKILL.md files for every tool
- `llms.txt` at the root (the convention for AI discovery, like robots.txt but inverted)
- `/skills/` index page listing everything
- Individual skill pages at `/skills/{tool-name}/`

This is the stopgap. It works today because GitHub Pages doesn't rate-limit like the GitHub API.

### Layer 2: wip.computer (the website)

Proper domain, proper branding, proper tools page. Not built yet.

- Landing pages for each product (Memory Crystal, Agent Pay, devops toolbox)
- `/tools/` or `/skills/` directory with full SKILL.md content
- `llms.txt` at the root
- Human-readable AND AI-readable
- SEO, social cards, the whole thing

This replaces github.io as the permanent home for discovery.

### Layer 3: WIP Cloud (mcp.wip.computer)

Remote MCP hosting on Cloudflare Workers. The commercial layer.

- Makes local tools available on every Claude surface (iOS, desktop, web)
- OAuth 2.1 with Dynamic Client Registration (required for Claude mobile)
- Tool documentation served alongside the actual MCP endpoints
- Stripe billing via Agent Pay

A developer builds a tool locally (MIT). WIP Cloud hosts it remotely (AGPLv3). Users on Claude iOS can use it without installing anything.

### Layer 4: Agent Pay Connectors (the store)

The marketplace. This is where it all converges.

- Developers publish capabilities behind 402 payment gates
- Agents discover tools, pay for them, use them
- Users tap Apple Pay. Agents handle the rest.
- Settlement via x402 protocol (USDC on Base/Solana)

Three products inside Agent Pay:

```
AGENT WALLET    ... sovereign wallet. User's own CDP/Privy keys. No fees. No limits.
AI CASH         ... pool mode. Apple Pay. $0.25/tx. $25 cap.
Connectors      ... marketplace. Paid capabilities. Agents discover and use them.
```

The Connectors marketplace is the ultimate distribution channel. Everything else feeds into it.

---

## Registries (Existing)

These are installation channels, not discovery channels. They work alongside the four layers above.

| Registry | Purpose | Status |
|----------|---------|--------|
| ClawHub (clawhub.ai) | OpenClaw skill registry | Exists. 6 skills published, 2 stuck in Scanning. Needs fixing. |
| npm (@wipcomputer) | Package registry | Exists. 7 packages, most stale. 8 tools missing. |
| GitHub Releases | Per-repo versioned releases | Working. deploy-public.sh creates these. |
| GitHub Packages | npm mirror on GitHub | Broken (404 scoping issue). |

---

## The Release Pipeline (What wip-release Should Do)

One command. Every channel.

```
wip-release patch --notes-file=RELEASE-NOTES-v1-9-2.md

  Pre-flight gates:
    ✓ License compliance
    ✓ Product docs up to date
    ✓ Release notes quality (from file, not one-liner)

  Version bump:
    ✓ package.json -> 1.9.2
    ✓ SKILL.md version synced
    ✓ CHANGELOG.md updated
    ✓ Git commit + tag v1.9.2

  Distribution:
    ✓ Git push
    ✓ npm publish (@wipcomputer/tool-name)
    ✓ GitHub Packages publish
    ✓ GitHub Release created
    ✓ ClawHub publish (each sub-tool SKILL.md individually)
    ✓ GitHub Pages updated (llms.txt, skill pages)

  Summary:
    npm:          @wipcomputer/wip-release@1.9.2    published
    ClawHub:      wip-release@1.9.2                 published
    GitHub:       v1.9.2                            created
    GitHub Pkgs:  @wipcomputer/wip-release@1.9.2    published
    Pages:        skills/wip-release updated         synced
```

If any distribution target fails, the summary shows it. No more silent failures.

---

## The Install Pipeline (What wip-install Should Do)

One command. Every interface.

```
wip-install wipcomputer/wip-ai-devops-toolbox

  Interfaces detected and deployed:
    ✓ CLI:        wip-release installed globally
    ✓ Module:     import from "core.mjs"
    ✓ MCP:        registered at user scope
    ✓ OpenClaw:   deployed to ~/.openclaw/extensions/
    ✓ Skill:      copied to ~/.openclaw/skills/
    ✓ CC Hook:    added to ~/.claude/settings.json
    ✓ ClawHub:    published (or verified current)
```

7 interfaces. ClawHub is the 7th.

---

## How It All Connects

```
Developer builds tool locally (MIT)
    |
    v
wip-release (one command)
    |
    +---> npm (package registry)
    +---> ClawHub (OpenClaw skill registry)
    +---> GitHub Release (versioned source)
    +---> GitHub Pages (AI-readable docs, llms.txt)
    |
    v
wip.computer (website, discovery)
    |
    v
WIP Cloud (remote MCP hosting, commercial)
    |
    v
Agent Pay Connectors (marketplace, paid capabilities)
    |
    v
Agent finds tool -> user taps Apple Pay -> tool unlocks -> agent uses it
```

Free tools flow through all layers without payment. Paid tools hit the Agent Pay gate. The architecture is the same either way. The only difference is whether there's a 402 in the middle.

---

## Current Bugs (wip-ai-devops-toolbox-private)

15 open issues blocking this architecture:

- #96: CLI binaries not executable after install
- #97: ClawHub publish broken for sub-tools
- #98: Installer missing ClawHub as interface
- #99-#104: npm, GitHub Packages, distribution audit, silent failures
- #105-#108: SKILL.md spec compliance, docs
- #109: Skills stuck in Scanning on ClawHub
- #110: Installer can't clone private repos

---

## Components

| Component | Repo | Role |
|-----------|------|------|
| wip-release | devops/wip-ai-devops-toolbox-private | Release pipeline (publish everywhere) |
| wip-install | devops/wip-ai-devops-toolbox-private | Install pipeline (all interfaces) |
| deploy-public | devops/wip-ai-devops-toolbox-private | Private-to-public sync |
| wip-homepage | wipcomputer.github.io | Layer 1 (github.io discovery) |
| wip-cloud | components/wip-cloud-private | Layer 3 (remote MCP hosting) |
| wip-agent-pay | components/wip-agent-pay-private | Layer 4 (payments + store) |
| Memory Crystal | components/memory-crystal-private | Product (distributed via all layers) |
| LDM OS | components/wip-ldm-os-private | The OS underneath everything |

---

Built by Parker Todd Brooks, Lesa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).
