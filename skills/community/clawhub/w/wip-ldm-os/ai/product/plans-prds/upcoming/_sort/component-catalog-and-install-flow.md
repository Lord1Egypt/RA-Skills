# Spec: Component Catalog and Install Flow

**Date:** 2026-03-12
**Authors:** Parker Todd Brooks, Claude Code (cc-mini)
**Status:** Spec
**Repos involved:** wip-ldm-os-private, memory-crystal-private, wip-ai-devops-toolbox-private

---

## Problem

Three products exist. None of them know about each other at install time. If someone finds LDM OS first, there's no way to discover Memory Crystal or the DevOps Toolbox. If someone finds Memory Crystal first, they don't know LDM OS exists (until it bootstraps silently). There's no catalog, no picker, no "here's what's available."

## The Three Products

| Product | What it is | npm | Repo |
|---------|-----------|-----|------|
| **LDM OS** | The runtime. Extensions, identity, boot, harness wiring. | `@wipcomputer/wip-ldm-os` | `wipcomputer/wip-ldm-os` |
| **Memory Crystal** | Memory. Persistent search, capture, Dream Weaver. | `@wipcomputer/memory-crystal` | `wipcomputer/memory-crystal` |
| **AI DevOps Toolbox** | Dev tools. Release, deploy, license, repo management, file guard. | `@wipcomputer/universal-installer` | `wipcomputer/wip-ai-devops-toolbox` |

Agent Pay exists but isn't installable yet. It shows in the catalog as "coming soon."

## Three Entry Points, All Work

### Path A: Find LDM OS first

User pastes the "Teach Your AI" prompt. AI reads SKILL.md. User says install.

```
$ ldm init

LDM OS v0.2.0
Scaffolded ~/.ldm/

Available components:

  1. Memory Crystal (recommended)
     Persistent memory for your AI. Search, capture, consolidation.

  2. AI DevOps Toolbox
     Release pipeline, license compliance, repo management, identity file protection.

  3. Agent Pay (coming soon)
     Micropayments for AI agents. Apple Pay approval.

Install components? [1,2,all,none]: 1

Installing Memory Crystal...
  [OK] Deployed to ~/.ldm/extensions/memory-crystal/
  [OK] CC hook configured (Stop)
  [OK] MCP server registered
  [OK] Backup cron installed
  [OK] Memory Crystal v0.7.4 ready

Run "crystal doctor" to verify. Run "ldm install" anytime to add more components.
```

### Path B: Find Memory Crystal first

User reads Memory Crystal's README. Runs `crystal init`.

```
$ crystal init

Bootstrapping LDM OS...
  [OK] LDM OS v0.2.0 scaffolded at ~/.ldm/

Installing Memory Crystal v0.7.4...
  [OK] Deployed to ~/.ldm/extensions/memory-crystal/
  [OK] CC hook configured
  [OK] MCP server registered
  [OK] Backup cron installed

Memory Crystal is ready. Run "crystal doctor" to verify.

Tip: Run "ldm install" to see more components you can add.
```

### Path C: Find DevOps Toolbox first

User reads the Toolbox README. Says "install."

```
$ wip-install wipcomputer/wip-ai-devops-toolbox

Bootstrapping LDM OS...
  [OK] LDM OS v0.2.0 scaffolded at ~/.ldm/

Installing AI DevOps Toolbox (13 tools)...
  [OK] 7 CLIs installed
  [OK] 3 MCP servers registered
  [OK] 2 CC hooks configured
  [OK] 2 OpenClaw plugins deployed
  [OK] 1 Skill copied

AI DevOps Toolbox is ready.

Tip: Run "ldm install" to see more components you can add.
```

### Every path ends the same way

No matter which product the user found first, they now have LDM OS + their chosen component. Running `ldm install` shows the catalog with what's already installed checked off:

```
$ ldm install

Installed components:
  [x] Memory Crystal v0.7.4

Available components:
  [ ] AI DevOps Toolbox
  [ ] Agent Pay (coming soon)

Install more? [number,all,none]:
```

## Component Catalog

LDM OS ships with a built-in catalog file. Not a remote registry. A local JSON that ships with the npm package and gets updated with each LDM OS release.

### `catalog.json`

```json
{
  "version": "0.1.0",
  "components": [
    {
      "id": "memory-crystal",
      "name": "Memory Crystal",
      "description": "Persistent memory for your AI. Search, capture, consolidation.",
      "npm": "@wipcomputer/memory-crystal",
      "repo": "wipcomputer/memory-crystal",
      "recommended": true,
      "status": "stable",
      "postInstall": "crystal doctor"
    },
    {
      "id": "wip-ai-devops-toolbox",
      "name": "AI DevOps Toolbox",
      "description": "Release pipeline, license compliance, repo management, identity file protection.",
      "npm": "@wipcomputer/universal-installer",
      "repo": "wipcomputer/wip-ai-devops-toolbox",
      "recommended": false,
      "status": "stable",
      "postInstall": null
    },
    {
      "id": "agent-pay",
      "name": "Agent Pay",
      "description": "Micropayments for AI agents. Apple Pay approval.",
      "npm": "@wipcomputer/wip-agent-pay",
      "repo": "wipcomputer/wip-agent-pay",
      "recommended": false,
      "status": "coming-soon",
      "postInstall": null
    }
  ]
}
```

### How the catalog updates

The catalog ships inside the `@wipcomputer/wip-ldm-os` npm package. When LDM OS updates (`ldm update`), the catalog updates too. New components appear. Removed components disappear. No remote fetching required.

Future: the catalog could also check a remote registry for third-party components. That's the AI CASH marketplace. But v1 is local only.

## What `ldm install` Needs to Support

Currently `ldm install` takes a local repo path. For this to work publicly:

### Install from npm (new)

```bash
ldm install memory-crystal           # resolves via catalog.json to npm package
ldm install @wipcomputer/wip-ldm-os  # direct npm package
```

Flow:
1. Check catalog.json for the component id
2. If found, get npm package name
3. `npm install -g <package>` (or install to ~/.ldm/extensions/ directly)
4. Run interface detection on the installed package
5. Deploy, register MCP, configure hooks, write registry
6. Run postInstall command if specified

### Install from local path (existing)

```bash
ldm install /path/to/memory-crystal-private   # local dev install
```

Already works. No changes needed.

### Install from GitHub repo (new)

```bash
ldm install wipcomputer/memory-crystal   # clones, detects, installs
```

Flow:
1. Clone to temp dir (or use npx to pull)
2. Run interface detection
3. Deploy, register, configure
4. Clean up temp clone

### Bare `ldm install` (catalog picker)

```bash
ldm install   # no arguments = show catalog picker
```

Shows installed and available components. Interactive selection.

## How Each Product's Install Changes

### Memory Crystal (`crystal init`)

```
crystal init
  1. Check for ldm CLI
  2. If missing: import bootstrapLdm() from @wipcomputer/wip-ldm-os, run it
  3. If present: skip bootstrap
  4. Run ldm install memory-crystal (generic deployment)
  5. MC-specific setup:
     - Backup crystal.db if updating
     - Verify DB readable
     - Core/Node role setup
     - Pairing (if --pair)
     - Cron setup
     - Session discovery
  6. Print: "Tip: Run ldm install to see more components"
```

### DevOps Toolbox (`wip-install`)

```
wip-install wipcomputer/wip-ai-devops-toolbox
  1. Check for ldm CLI
  2. If missing: bootstrap LDM OS
  3. If present: delegate to ldm install
  4. Toolbox-specific: iterate sub-tools, install each interface
  5. Print: "Tip: Run ldm install to see more components"
```

### LDM OS (`ldm init`)

```
ldm init
  1. Scaffold ~/.ldm/
  2. Write version.json
  3. Install ldm CLI globally
  4. Write initial registry
  5. Show catalog picker
  6. Install selected components
```

## How the READMEs Connect

### LDM OS README

The hub. Lists all components. The "Teach Your AI" prompt leads to `ldm init` which shows the picker.

```
# LDM OS

## All your AIs. One system.

[tagline, problem statement]

## Teach Your AI

[install prompt]

## Components

Memory Crystal ... persistent memory. Search, capture, consolidation.
AI DevOps Toolbox ... release, deploy, license, repo management.
Agent Pay ... micropayments. Apple Pay. (coming soon)

Install all or pick what you need. ldm init walks you through it.

## More Info
...
```

### Memory Crystal README

Standalone. Mentions LDM OS as the runtime it installs into.

```
# Memory Crystal

## Your AI remembers.

[tagline, problem statement]

## Teach Your AI

[crystal-specific install prompt ... leads to crystal init]

## Part of LDM OS

Memory Crystal installs into LDM OS, the local runtime for AI agents.
Run "ldm install" to see other components.

## More Info
...
```

### DevOps Toolbox README

Standalone. Same pattern. Already follows this structure.

```
# AI DevOps Toolbox

## Want your AI to dev?

[existing README is already good]

## Part of LDM OS

AI DevOps Toolbox installs into LDM OS, the local runtime for AI agents.
Run "ldm install" to see other components.
```

### The cross-linking rule

Every component README has a "Part of LDM OS" section at the bottom. One sentence. One link. Not a sales pitch. Just: "this is part of a bigger system, here's how to find the rest."

## Implementation Order

1. **Add `catalog.json` to wip-ldm-os-private** (the component list)
2. **Add `ldm install` from npm support** (resolve catalog id to npm package)
3. **Add interactive picker to `ldm init`** (show catalog after scaffold)
4. **Update `crystal init` to bootstrap LDM + print tip**
5. **Update `wip-install` to bootstrap LDM + print tip**
6. **Update all three READMEs** (LDM OS as hub, components link back)
7. **Add "Part of LDM OS" section to Memory Crystal and Toolbox READMEs**

## What This Does NOT Include

- Remote registry (AI CASH marketplace). That's Layer 3. This is Layer 1 and 2.
- Third-party components. The catalog is WIP Computer components only for now.
- Payments. Agent Pay appears in the catalog as "coming soon" but doesn't install yet.
- Auto-update. `ldm update` is a separate feature.
