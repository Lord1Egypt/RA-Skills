# Plan: Adopt Agent Skills Spec for SKILL.md

**Date:** 2026-03-25
**Author:** cc-mini (with Parker)
**Issues:** #113, #211, #204, #207
**Related:** Single Source of Truth plan (same date), Agent Skills Spec (agentskills.io)

## Context

We shipped v0.4.42-v0.4.47 today trying to make the install SKILL.md work better. Six releases. AIs still ignore the instructions. They show a version table, say "Want to install?", and skip everything else: no release notes per component, no skill descriptions, no user-language explanations.

The root cause: our SKILL.md is 16KB / 390 lines mixing product pitch with operational instructions. The Agent Skills Spec says SKILL.md body should be < 5000 tokens (~150 lines). "Process goes in SKILL.md, context goes in reference files."

Evidence from other projects that work:
- **AgentCard** (agentcard.sh/agent.txt): pure instructions, no pitch, AIs follow it
- **gstack** (Garry Tan): template-generated, preamble gathers state, behavioral directives only
- **Anthropic skills repo**: template is 6 lines (frontmatter + "Insert instructions below")

## The Problem

```
Our SKILL.md (16KB, 390 lines):
  - Product pitch ("Learning Dreaming Machines. All your AIs. One system.")
  - Included skills descriptions (Bridge, Shared Workspace, Recall, etc.)
  - Optional skills descriptions (Memory Crystal, AI DevOps Toolbox, etc.)
  - Check-if-installed flow
  - Already-installed: status, table, release notes, install commands
  - Not-installed: explainer, directory listing, setup walkthrough
  - Platform compatibility table
  - Operating rules
  - Commands reference table
  - Interface detection table
  - Repo list

AI reads this and:
  1. Gets the general shape (check -> table -> ask)
  2. Ignores everything specific (release notes, user language, skill descriptions)
  3. Produces thin, generic output every time
```

## The Fix: Agent Skills Spec Compliance

### Architecture: Three Layers (Source -> Runtime -> Home)

```
LAYER 1: SOURCE (repo, checked into git)
wip-ldm-os-private/
├── SKILL.md                    # < 150 lines. Pure instructions only.
├── README.md                   # Product pitch (already exists, no change)
├── references/
│   ├── PRODUCT.md              # What LDM OS is (for "not installed" path)
│   ├── SKILLS-CATALOG.md       # Included + optional skills with descriptions
│   ├── COMMANDS.md             # Command reference table
│   └── INTERFACES.md           # Interface detection table
└── docs/                       # Already exists, no change

LAYER 2: RUNTIME (.ldm, deployed by ldm install)
~/.ldm/
├── skills/
│   └── wip-ldm-os/
│       ├── SKILL.md            # Deployed from npm package
│       └── references/         # Deployed from npm package
│           ├── PRODUCT.md
│           ├── SKILLS-CATALOG.md
│           ├── COMMANDS.md
│           └── INTERFACES.md
└── extensions/                 # Already exists (CLI tools, hooks, plugins)

LAYER 3: HOME (~/wipcomputerinc/, shared workspace)
~/wipcomputerinc/settings/
├── docs/
│   └── skills/                 # ldm install deploys skill references here
│       └── wip-ldm-os/        # so all agents (CC, Lesa, any AI) can read them
│           ├── PRODUCT.md
│           ├── SKILLS-CATALOG.md
│           ├── COMMANDS.md
│           └── INTERFACES.md
└── templates/                  # Already exists

FLOW:
  Repo (source) -> npm publish -> npm package
  npm install -g -> /opt/homebrew/lib/node_modules/
  ldm install -> deploys to ~/.ldm/skills/ AND ~/wipcomputerinc/settings/docs/skills/
  SKILL.md references: "Read references/PRODUCT.md" resolves to settings/docs/skills/wip-ldm-os/PRODUCT.md
```

This applies to ALL repos, not just wip-ldm-os. Every product that ships a SKILL.md:
- Source: `<repo>/SKILL.md` + `<repo>/references/`
- npm publish includes SKILL.md + references/ in the tarball
- `ldm install` deploys references/ to `settings/docs/skills/<product-name>/`
- The SKILL.md instruction "Read references/PRODUCT.md" works for any AI that can access home

### How this applies to all repos (the OS pattern)

LDM OS is the runtime. It defines HOW skills work. Every product follows the same structure:

```
Any product repo (e.g. memory-crystal-private):
├── SKILL.md                    # < 150 lines. Pure instructions.
├── references/
│   ├── PRODUCT.md              # What this product is
│   ├── TOOLS.md                # MCP tools, CLI commands specific to this product
│   └── EXAMPLES.md             # Usage examples (optional)
└── ...

ldm install wipcomputer/memory-crystal deploys:
  ~/.ldm/skills/memory-crystal/SKILL.md
  ~/.ldm/skills/memory-crystal/references/
  ~/wipcomputerinc/settings/docs/skills/memory-crystal/
```

The universal installer (#113) already defines this pattern:
1. Bootstrap (check ldm, npm install if needed)
2. Install (ldm install ... installs everything)
3. Enable product (ldm enable <product>)
4. Product-specific setup

This plan adds the SKILL.md + references/ structure to that pattern.

### SKILL.md Structure (target: ~120 lines)

```yaml
---
name: wip-ldm-os
description: >
  LDM OS installer and updater. Use when asked to install, update, or check
  status of LDM OS. Use when user pastes an install prompt mentioning
  wip.computer/install or ldm. Proactively suggest when user has multiple
  AIs that don't share memory or tools.
license: MIT
compatibility: Requires git, npm, node. Node.js 18+.
metadata:
  display-name: "LDM OS"
  version: "0.4.47"
  homepage: "https://github.com/wipcomputer/wip-ldm-os"
  author: "Parker Todd Brooks"
  category: infrastructure
  openclaw:
    requires:
      bins: [git, npm, node]
    install:
      - id: node
        kind: node
        package: "@wipcomputer/wip-ldm-os"
        bins: [ldm]
        label: "Install LDM OS via npm"
    emoji: "🧠"
---

## Step 1: Check if installed

(bash: which ldm && ldm --version)
(cloud AI fallback: tell user to open terminal AI)
Branch on result.

## Already installed

1. Run ldm status
2. Show update table (always a table, every component gets a row)
3. Fetch release notes per component (DO NOT SKIP)
4. Translate to user language (good/bad examples inline)
5. Ask: questions? dry run? install?
6. Install commands

## Not installed

1. Read references/PRODUCT.md for what to explain
2. Read references/SKILLS-CATALOG.md for what ships with it
3. Present: what is it, what installs, what changes for this AI, what changes across all AIs
4. Ask: questions? dry run?
5. Install commands

## Operating rules

- Dry-run first. Always.
- Never touch sacred data.
- Check before you run.
```

### Key Principles (from research)

1. **Process in SKILL.md, context in references/** ... the spec says < 5000 tokens for body
2. **Imperative language** ... "Run ldm status" not "LDM OS is a shared infrastructure layer"
3. **Progressive disclosure** ... metadata (~100 tokens) loaded at startup, body on activation, references on demand
4. **No product pitch in SKILL.md** ... that's what README.md is for
5. **References loaded on demand** ... AI reads PRODUCT.md only for "not installed" path, SKILLS-CATALOG.md only when presenting skills
6. **Good/bad examples inline** ... teach the AI the voice directly in the instruction (like gstack does)

## Existing Tickets

| # | Title | Status | Role in this plan |
|---|-------|--------|-------------------|
| #113 | Universal installer pattern: every SKILL.md installs LDM OS + enables its product | Open | The universal bootstrap pattern. Every product's SKILL.md uses the same install flow. |
| #211 | SKILL.md: tell AIs to present release notes in user language | Closed (v0.4.47) | Already addressed in instructions. Keep the good/bad examples. |
| #207 | SKILL.md: cloud-only AI path | Open | Already addressed: "tell user to open terminal AI" |
| #204 | Public docs site (Mintlify free tier) | Open | Separate. Not blocked by this. |
| #99 | Converge skill discovery paths | Open | Related. SKILL.md references/ dir needs to be discoverable. |
| #109 | ldm install should run crystal init as postInstall | Open | Related. Post-install hooks in catalog.json. |

## Universal Installer Docs Update

`docs/universal-installer/` needs to reference the Agent Skills Spec:
- SPEC.md: add "SKILL.md follows the Agent Skills Spec (agentskills.io/specification)"
- SPEC.md: update SKILL.md section with frontmatter requirements from the spec
- TECHNICAL.md: add references/ directory to the skill detection section
- README.md: add link to agentskills.io

## Implementation Steps

### Step 1: Create references/ directory

Split current SKILL.md content into reference files:

**references/PRODUCT.md** (~60 lines)
- "Learning Dreaming Machines. All your AIs. One system."
- The six pillars (Identity, Memory, Ownership, Collaboration, Compatibility, Payments)
- What it installs (~/.ldm/ directory listing)
- What changes for this AI
- What changes across all AIs

**references/SKILLS-CATALOG.md** (~80 lines)
- Included skills with full descriptions (Bridge, Universal Installer, Shared Workspace, System Pulse, Recall, LUME)
- Optional skills with full descriptions (Memory Crystal, AI DevOps Toolbox, 1Password, etc.)
- Install command per skill

**references/COMMANDS.md** (~30 lines)
- Command reference table (ldm init, install, doctor, status, etc.)
- --dry-run and --json flags

**references/INTERFACES.md** (~20 lines)
- Interface detection table (CLI, MCP Server, OpenClaw Plugin, Skill, CC Hook, Module)

### Step 2: Rewrite SKILL.md

Pure instructions. < 150 lines. Imperative voice.

- Frontmatter: name, description (with trigger phrases), license, compatibility, metadata
- Step 1: check if installed (with cloud AI fallback)
- Already installed path: status -> table -> release notes (with user-language examples) -> ask -> install
- Not installed path: read references/PRODUCT.md -> read references/SKILLS-CATALOG.md -> present -> ask -> install
- Operating rules (3 lines)
- No product pitch. No tables. No catalog. Just steps.

### Step 3: Update ldm install to deploy references/

The installer (`bin/ldm.js`) needs to:
1. When installing a skill (SKILL.md detected), also copy `references/` if it exists
2. Deploy to `~/.ldm/skills/<product-name>/references/`
3. Deploy to `~/wipcomputerinc/settings/docs/skills/<product-name>/` (home, shared workspace)
4. The home path comes from `~/.ldm/config.json` (workspace field), not hardcoded

This is an OS-level change. Once `ldm install` knows about references/, it works for every product automatically. No per-repo installer changes needed.

### Step 4: Update universal installer docs

- docs/universal-installer/SPEC.md: reference Agent Skills Spec (agentskills.io/specification)
- docs/universal-installer/SPEC.md: add references/ directory to Skill interface definition
- docs/universal-installer/TECHNICAL.md: add references/ to skill detection and deployment
- docs/universal-installer/README.md: link to agentskills.io, explain references/ pattern

### Step 5: Save reference docs to plan directory

Save these to `ai/product/plans-prds/current/skills/`:
- This plan
- Agent Skills Spec summary (from agentskills.io/specification)
- gstack patterns summary (from github.com/garrytan/gstack)
- AgentCard agent.txt analysis (from agentcard.sh)

### Step 6: Apply to other product SKILLs (#113)

After validating with wip-ldm-os, apply the same pattern to ALL product repos:
- memory-crystal-private SKILL.md + references/
- wip-ai-devops-toolbox-private SKILL.md + references/
- wip-1password-private SKILL.md + references/
- wip-xai-grok-private SKILL.md + references/
- wip-xai-x-private SKILL.md + references/
- wip-markdown-viewer-private SKILL.md + references/
- dream-weaver-protocol-private SKILL.md + references/

Each follows the universal pattern from #113:
1. Bootstrap (check ldm, npm install if needed)
2. Install (ldm install ... installs everything)
3. Enable product (ldm enable <product>)
4. Product-specific setup

And the new SKILL.md structure:
- < 150 lines of pure instructions
- references/ for product context, tool docs, examples
- Deployed by ldm install to .ldm and home

## Acknowledgements

- **Agent Skills Spec** ... agentskills.io (specification for SKILL.md format)
- **Anthropic** ... github.com/anthropics/skills (official skills repo, skill-creator meta-skill)
- **Garry Tan / gstack** ... github.com/garrytan/gstack (template system, preamble pattern, 28 skills showing how to write behavioral instructions AIs actually follow)
- **AgentCard** ... agentcard.sh/agent.txt (clean agent instruction file that works)
- **Ole Lehmann** ... "I deleted half my Claude setup and every output got BETTER" (addition by subtraction)
- **MindStudio** ... "Process goes in SKILL.md, context goes in reference files" (the rule we violated)

## Verification

```bash
# After implementation:
wc -l SKILL.md                          # should be < 150 lines
ls references/                          # PRODUCT.md, SKILLS-CATALOG.md, COMMANDS.md, INTERFACES.md
wc -l references/*                      # each < 100 lines

# Dogfood (fresh session):
# Read https://wip.computer/install/wip-ldm-os.txt
# AI should:
#   1. Check if installed
#   2. Show update table (if installed)
#   3. Show release notes per component IN USER LANGUAGE
#   4. Mention included skills by name (if not installed)
#   5. Not dump the entire SKILL.md as explanation
```

## What This Does NOT Cover

- Template generation system (like gstack's gen-skill-docs.ts) ... future
- Preamble scripts that gather state before instructions run ... future
- Per-product SKILL.md rewrites (Step 5 is scoped, not detailed) ... separate PRs
- Mintlify docs site (#204) ... separate plan
- CLAUDE.md consolidation ... separate plan (same date)

## Files to Modify

### wip-ldm-os-private (this release)
| File | Change |
|------|--------|
| `SKILL.md` | Rewrite to < 150 lines, pure instructions |
| `references/PRODUCT.md` | NEW: product pitch from current SKILL.md + README |
| `references/SKILLS-CATALOG.md` | NEW: included + optional skills with descriptions |
| `references/COMMANDS.md` | NEW: command reference table |
| `references/INTERFACES.md` | NEW: interface detection table |
| `bin/ldm.js` | Add references/ deployment to ldm install (deploy to .ldm + home) |
| `docs/universal-installer/SPEC.md` | Add Agent Skills Spec reference, references/ in Skill interface |
| `docs/universal-installer/TECHNICAL.md` | Add references/ to skill detection and deployment |
| `docs/universal-installer/README.md` | Link to agentskills.io |
| `ai/product/plans-prds/current/skills/` | NEW: this plan + research reference docs |

### All org repos with SKILL.md (Step 6, separate PRs after validation)

Every repo in the wipcomputer org that has a SKILL.md gets the same treatment:
SKILL.md rewrite (< 150 lines, pure instructions) + references/ directory.

This includes but is not limited to:
- memory-crystal-private
- wip-ai-devops-toolbox-private
- wip-1password-private
- wip-xai-grok-private
- wip-xai-x-private
- wip-markdown-viewer-private
- dream-weaver-protocol-private
- wip-bridge-private
- wip-healthcheck-private
- openclaw/openclaw
- Any future repo that ships a SKILL.md

The `ldm install` change (Step 3) makes references/ work for all repos automatically.
Each repo just needs: SKILL.md (instructions) + references/ (context). The OS handles deployment.

## Deployment

```bash
# Worktree for changes:
cd ~/wipcomputerinc/repos/ldm-os/wip-ldm-os-private
git worktree add ~/wipcomputerinc/_worktrees/wip-ldm-os-private--cc-mini--skills-spec -b cc-mini/skills-spec

# All changes + RELEASE-NOTES on the branch before merge.
# Then: merge -> git pull -> wip-release patch -> dogfood
```
