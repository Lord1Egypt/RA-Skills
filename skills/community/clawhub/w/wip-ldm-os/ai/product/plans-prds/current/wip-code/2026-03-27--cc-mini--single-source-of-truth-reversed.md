# Plan: Single Source of Truth (REVERSED)

**Date:** 2026-03-27
**Author:** cc-mini (with Parker)
**Revises:** 2026-03-25--cc-mini--single-source-of-truth.md
**Save to:** wip-ldm-os-private/ai/product/plans-prds/current/wip-code/

## What went wrong with the original plan

We deployed Level 1 (thin ~/.claude/CLAUDE.md) FIRST, before Level 2 or Level 3 existed. CC lost system knowledge. The "on demand" pointers didn't work because CC doesn't proactively read docs. Two days of cascading bugs because the AI didn't understand the system it was coding on.

## The reverse approach

Build from the bottom up. Don't touch the global file until everything below it is proven.

```
ORDER OF OPERATIONS:
1. RESTORE: Put the full CLAUDE.md back at ~/.claude/ (undo the damage)
2. REPOS (Level 3): Add CLAUDE.md to each repo (for Claude Code iOS/web)
3. WORKSPACE (Level 2): ~/wipcomputerinc/ gets working docs + settings
4. USER HOME (Level 1): ~/.claude/CLAUDE.md gets trimmed LAST, only after 2+3 are proven
```

## Why reverse?

- Claude Code on iOS/web reads ONE repo at a time. No ~/.claude/, no ~/.openclaw/. If the repo doesn't have CLAUDE.md, the AI is blind.
- The workspace (~/wipcomputerinc/) is where all agents work. Settings, docs, templates live here.
- The user home (~/) is global. Change it last because it affects everything.
- Memory Crystal MCP (wip.computer/docs/mcp or local crystal_search) fills gaps. If something doesn't need to be inlined in the repo, Crystal can provide it on demand.

## Step 0: RESTORE (do now)

Restore ~/.claude/CLAUDE.md to the full 340-line version from backup.

**Source:** /Users/lesa/wipcomputerinc/team/cc-mini/documents/backups/2026-03-25-pre-level1/claude-CLAUDE.md
**Destination:** ~/.claude/CLAUDE.md

Then verify: open a fresh CC session anywhere. Does it know the system? Does it know the release pipeline? Does it know the repo structure?

**Installer question:** Does ldm install overwrite this? YES, currently ldm init deploys the Level 1 template to ~/.claude/CLAUDE.md. We need to DISABLE that until Level 3 and Level 2 are built. Otherwise the next ldm install wipes the restored file.

## Step 1: REPOS (Level 3)

Add CLAUDE.md to every product repo. This is for Claude Code on iOS/web where you open a single repo and that's all the AI sees.

Each repo's CLAUDE.md should contain:
- What this repo is (one paragraph)
- Build/test/lint commands
- Repo-specific conventions
- "For full system context, search Memory Crystal or read the Dev Guide at ~/wipcomputerinc/settings/docs/"
- "For other repos, use crystal_search to find context across all repos"

This is #166 (per-repo CLAUDE.md). Not generated yet, written manually for each repo.

**Repos to add CLAUDE.md:**
- wip-ldm-os-private
- memory-crystal-private
- wip-ai-devops-toolbox-private
- wip-1password-private
- wip-xai-grok-private
- wip-xai-x-private
- wip-markdown-viewer-private
- dream-weaver-protocol-private
- openclaw-tavily
- wip-healthcheck-private
- wip-bridge-private

**Installer question:** ldm install doesn't need to deploy these. They live in the repo. Git tracks them.

## Step 2: WORKSPACE (Level 2)

~/wipcomputerinc/ is home. All agents read from here.

Already built (from docs pipeline plan):
- settings/docs/ (14 personalized docs, deployed by ldm install from templates)
- settings/templates/ (dev guide, install prompt, claude-md template)
- settings/config.json (org identity, agents, paths)
- settings/docs/change-dependencies.json (what to update when X changes)

Still needed:
- ~/.openclaw/CLAUDE.md needs to be trimmed to ~150 lines (Level 2 content only)
- But NOT until Level 3 is in every repo and tested

**Installer question:** ldm install deploys settings/docs/ from templates. That's working (v0.4.57+).

## Step 3: USER HOME (Level 1) ... LAST

Only after Steps 1 and 2 are proven:
- Trim ~/.claude/CLAUDE.md to ~30 lines
- Test: open CC in a repo. Does Level 3 (repo) + Level 1 (global) give enough context?
- Test: open CC in ~/wipcomputerinc/. Does Level 2 (workspace) + Level 1 (global) give enough context?
- If anything breaks, add it back before shipping

**Installer question:** ldm install generates Level 1 from template + config.json. This is the LAST thing we enable, not the first.

## The rule for every change (ENFORCED, not optional)

The 5 questions are GATES. wip-release should check for them before publishing. Not documentation. Not suggestions. Hooks.

1. What source files change? (in the repo)
2. What does ldm install deploy?
3. Fresh vs existing install?
4. What docs need updating?
5. What files does the installer touch?

**Enforcement:** wip-release checks the RELEASE-NOTES file for these answers. If they're not there, the release is blocked. Same pattern as "no release notes, no release." No answers to the 5 questions, no release.

This is a ticket: add 5-question gate to wip-release. Not a hook (hooks are for CC). This is a check inside wip-release itself.

## Memory Crystal as the bridge

Repos don't need to inline everything. The CLAUDE.md in each repo says:
"For context beyond this repo, use crystal_search."

Memory Crystal MCP at wip.computer/docs/mcp is available to any AI (including iOS/web).
Local crystal_search is available to CC and Lesa via MCP.

This means: repo CLAUDE.md stays lean. System knowledge lives in Crystal and settings/docs. The CLAUDE.md just points to where to find it.

## 5 Questions for Each Step

### Step 0: RESTORE

1. **Source files:** backup at team/cc-mini/documents/backups/2026-03-25-pre-level1/claude-CLAUDE.md
2. **ldm install deploys:** YES, ldm init currently overwrites ~/.claude/CLAUDE.md with Level 1 template. MUST DISABLE this in bin/ldm.js until Step 3 is complete.
3. **Fresh vs existing:** Fresh install gets Level 1 (thin). Existing install should NOT overwrite a restored full file. Need a flag or version check.
4. **Docs to update:** settings/docs/how-install-works.md (note that CLAUDE.md deployment is paused)
5. **Files touched:** ~/.claude/CLAUDE.md (restored from backup)

### Step 1: REPOS

1. **Source files:** new CLAUDE.md in each of 11 repos
2. **ldm install deploys:** No. These are in git. Not deployed by installer.
3. **Fresh vs existing:** No difference. File is in the repo.
4. **Docs to update:** dev guide (add "every repo must have CLAUDE.md")
5. **Files touched:** <repo>/CLAUDE.md (one per repo, 11 total)

### Step 2: WORKSPACE

1. **Source files:** ~/.openclaw/CLAUDE.md (trim to ~150 lines)
2. **ldm install deploys:** This file is in the openclaw repo, not deployed by ldm install. It's tracked by git.
3. **Fresh vs existing:** No difference. Git tracks it.
4. **Docs to update:** settings/docs/how-agents-work.md (note Level 2 content)
5. **Files touched:** ~/.openclaw/CLAUDE.md

### Step 3: USER HOME (last)

1. **Source files:** wip-ldm-os-private/shared/templates/claude-md-level1.md
2. **ldm install deploys:** YES. This is what ldm init writes to ~/.claude/CLAUDE.md. Re-enable the deployment.
3. **Fresh vs existing:** Fresh gets Level 1. Existing gets Level 1 (replacing the restored full file, but only AFTER Level 3 and Level 2 are proven).
4. **Docs to update:** settings/docs/how-install-works.md, dev guide
5. **Files touched:** ~/.claude/CLAUDE.md (generated from template + config.json)

## Verification

```
Step 0: Restore
  wc -l ~/.claude/CLAUDE.md   # should be 340 lines (restored)
  Open fresh CC session. Ask: "what's the release pipeline?" Should know.

Step 1: Repos
  ls <each-repo>/CLAUDE.md    # should exist in every repo
  Open CC on iOS with one repo. Ask: "what does this repo do?" Should know.

Step 2: Workspace
  wc -l ~/.openclaw/CLAUDE.md  # should be ~150 lines (trimmed)
  Open CC in ~/wipcomputerinc/. Should know the full system.

Step 3: User home (LAST)
  wc -l ~/.claude/CLAUDE.md    # should be ~30 lines
  Open CC anywhere. Level 1 + Level 3 or Level 2 should give full context.
  If not, DON'T SHIP. Add back what's missing.
```
