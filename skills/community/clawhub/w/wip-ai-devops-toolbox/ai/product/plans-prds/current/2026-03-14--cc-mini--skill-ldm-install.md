# Plan: DevOps Toolbox Install Experience (Match Memory Crystal)

**Date:** 2026-03-14
**Issue:** Toolbox SKILL.md uses deprecated wip-install. Needs to match Memory Crystal pattern.
**Status:** In Progress
**Branch:** cc-mini/skill-ldm-install

## Context

The DevOps Toolbox SKILL.md still tells AIs to use `wip-install` (deprecated). The world moved to LDM OS. `ldm install` already has toolbox mode and works (12 sub-tools, 39 interfaces detected). The code in `install.js` already bootstraps LDM OS silently. But the SKILL.md (what AIs read and follow as instructions) still uses the old path.

Memory Crystal's SKILL.md is the gold standard: conversational, guided, asks questions, explains what's happening, gets consent. The AI becomes the installer. No standalone installer binary. The SKILL.md IS the installer script for the AI.

## The dogfooding loop

1. CC fixes on branch
2. CC merges to private main (PR, `gh pr merge --merge`)
3. CC deploys (`wip-release patch` + `deploy-public.sh`)
4. Parker dogfoods (runs the install prompt in a fresh session)
5. Parker sends transcript
6. CC iterates
7. CC never installs. Parker runs the prompt. Parker says "install."

## What changes

### 1. SKILL.md Install section rewrite (main work)

Replace the 3-line `wip-install` block with a conversational, Memory Crystal-style install flow:

- **Step 0: Check for LDM OS** ... `ldm --version`. If not installed, offer to install it.
- **Transparency block** ... explain exactly what will be created (CLI tools, MCP servers, hooks, plugins, registry)
- **Step 1: Dry run** ... `ldm install wipcomputer/wip-ai-devops-toolbox --dry-run`. Walk through each tool.
- **Step 2: Install** ... `ldm install wipcomputer/wip-ai-devops-toolbox`
- **Step 3: Verify** ... `ldm doctor`
- **Update section** ... for existing installs

### 2. Fix SKILL.md version corruption

Line 8: `"1.9.17".9.16".9.15".9.14"` -> `"1.9.17"`
Bug already fixed in core.mjs (commit f02ed62). This is artifact cleanup.

### 3. Update Universal Installer section in SKILL.md

Rename from "wip-universal-installer" to "Universal Installer (built into LDM OS)". Explain that `wip-install` delegates to `ldm install` when LDM OS is available, bootstraps LDM OS silently when it's not.

### 4. Update TECHNICAL.md Quick Start

Replace `wip-install` with `ldm install` commands.

### 5. Update README.md

Replace `wip-install` reference in "Teach your AI" block with `ldm install`.

### 6. Fix LDM OS SKILL.md version corruption (separate repo)

Line 8: `"0.2.11".2.10"` -> `"0.2.11"`. Separate branch + PR.

## Files modified

| File | Change |
|------|--------|
| `SKILL.md` | Rewrite Install section, fix version, update Universal Installer section |
| `README.md` | Update dry-run command in Teach your AI block |
| `TECHNICAL.md` | Update Quick Start |

## Depends on

- bootstrap-ldm-os.md (code already implemented in install.js, just needs release)

## Verify

Parker runs the install prompt in a fresh Claude Code session:

```
Read wip.computer/install/wip-ai-devops-toolbox.txt

Then explain:
1. What is AI DevOps Toolbox?
2. What does it install on my system?
3. What changes for us? (this AI)
4. What changes across all my AIs?

Check if AI DevOps Toolbox is already installed.
If it is, show me what I have and what's new.

Then ask:
- Do you have questions?
- Want to see a dry run?

If I say yes, run: ldm install wipcomputer/wip-ai-devops-toolbox --dry-run

Show me exactly what will change. Don't install anything until I say "install".
```

The AI should:
1. Read the SKILL.md (now with new Install section)
2. Check for LDM OS (`ldm --version`)
3. Explain what will change (transparency block)
4. Offer dry run (`ldm install ... --dry-run`)
5. Show all 12 sub-tools detected
6. Wait for user consent before installing
7. Verify with `ldm doctor`
