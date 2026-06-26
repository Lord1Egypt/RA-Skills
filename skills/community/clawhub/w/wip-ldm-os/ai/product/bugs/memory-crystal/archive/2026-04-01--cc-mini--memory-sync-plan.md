# Plan: Memory Crystal Sync Hook + Guard Fix

**Date:** 2026-04-01
**Status:** Approved
**Repos:** memory-crystal-private, wip-ai-devops-toolbox-private, wip-ldm-os-private

## Context

Agents write structured memories to their own file-based systems (Claude Code writes to `~/.claude/projects/*/memory/*.md`, Lesa writes to `workspace/MEMORY.md`). These memories stay local. They don't sync to Memory Crystal, so agents can't search each other's memories.

Additionally, file guard's `/memory/i` pattern blocks Claude Code from writing to its OWN memory files. This fights the harness's built-in memory system.

### Parker's principles
1. Don't fight the harness's built-in memory. Let it do its thing.
2. Guard against massive destructive edits to identity files (SOUL.md, IDENTITY.md). That's what file guard is for.
3. Sync everything to Crystal so all agents can search all memories.
4. Tag memories with the four types: user, feedback, project, reference.

### Citizens (agents in the org)
- OpenClaw (Lesa)
- Anthropic (Claude Code)
- OpenAI (ChatGPT)
- xAI (Grok)
- Pi-based agents
- Hermes (Nous Research, MCP-native, MIT, to be installed and tested)

## What the exploration found

**Branch guard** (`guard.mjs`): NOT the blocker. It checks the TARGET file's repo, not CWD. Files outside git repos (like `~/.claude/`) are explicitly allowed (line 370-374: "File is outside any git repo... allow it").

**File guard** (`guard.mjs`): THIS is the blocker. The `/memory/i` pattern (line 20-37) matches `~/.claude/projects/*/memory/` paths. It blocks Write entirely and limits Edit to 2-line removals. These paths are NOT in SHARED_STATE_PATHS, so they get the strict limit.

**Crystal's remember()**: Takes `text` + `category` (fact/preference/event/opinion/skill). Creates both a memory record AND a chunk for vector search. The category enum doesn't include user/feedback/project/reference yet.

**Crystal's cc-hook** (Stop hook): Already captures conversation turns to Crystal. Does NOT scan for changed memory files. This is where the sync hook would go.

---

## Plan

### Fix 1: File guard ... allow harness memory writes

**File:** `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-file-guard/guard.mjs`

**Change:** Add `~/.claude/projects/*/memory/` to SHARED_STATE_PATHS (or a new HARNESS_MEMORY_PATHS allowlist). This gives the harness's built-in memory system the lenient limits (20-line removal, 30-line replacement) instead of the strict limits (2-line removal).

The harness needs to be able to manage its own memory. We should not block it. Identity files (SOUL.md, IDENTITY.md) stay protected under the strict limits.

Specifically:
- Add pattern: `~/.claude/projects/` to the lenient list
- Add pattern: `~/.claude/` memory-related paths
- Keep SOUL.md, IDENTITY.md, CONTEXT.md under strict protection regardless of path
- Keep SHARED-CONTEXT.md under strict protection (shared state)

### Fix 2: Crystal sync hook ... write memories to Crystal on session end

**File:** `repos/ldm-os/components/memory-crystal-private/src/cc-hook.ts` (extend existing Stop hook)

**Change:** After the existing conversation capture, add a step that:

1. Scans `~/.claude/projects/*/memory/*.md` for files modified since last capture
2. For each changed file, reads the YAML frontmatter (name, description, type)
3. Maps the CC memory type to Crystal category
4. Calls `crystal.remember(text, category)` with `agent_id: "claude-code"`
5. Updates watermark so unchanged files aren't re-ingested

### Fix 3: Lesa's hook ... sync workspace memories to Crystal

**File:** `repos/ldm-os/components/memory-crystal-private/src/openclaw.ts` (extend existing agent_end hook)

**Change:** After the existing conversation capture, add a step that:

1. Checks if any workspace memory files changed this turn (workspace/MEMORY.md, workspace/memory/*.md)
2. For each changed file, reads content
3. Classifies into one of the four types
4. Calls `crystal.remember(text, category)` with `agent_id: "lesa"`
5. Dedup: check text hash before ingesting to avoid duplicates

### Fix 4: Add four memory types to Crystal schema

**File:** `repos/ldm-os/components/memory-crystal-private/src/core.ts`

**Change:** Extend the Memory category type:

Current: `fact`, `preference`, `event`, `opinion`, `skill`
Add: `user`, `feedback`, `project`, `reference`

This allows `crystal_search` to filter by type: "show me all feedback memories."

---

## The Four Memory Types

Reference: Claude Code source analysis (`cc-src-private/ai/product/notes/2026-03-31--cc-mini--influence-analysis.md`)

### 1. `user`
Who the person is. Role, goals, preferences, knowledge level.
- Example: "Parker is the founder, based in LA, prefers no em dashes"
- Purpose: tailor responses to the person's perspective

### 2. `feedback`
Corrections AND confirmations. What to avoid and what to keep doing.
- Example: "Don't mock the database in tests"
- Example: "Single bundled PR was the right call here"
- Purpose: agent doesn't repeat mistakes, doesn't drift from validated approaches

### 3. `project`
Ongoing work, goals, decisions, deadlines.
- Example: "Merge freeze begins March 5 for mobile release"
- Purpose: understand motivation and constraints
- Decays fast. Relative dates must be converted to absolute.

### 4. `reference`
Pointers to external systems. Where to find information.
- Example: "Pipeline bugs tracked in Linear project INGEST"
- Purpose: know where to look without being told every time

---

## Files to modify

1. `repos/ldm-os/devops/wip-ai-devops-toolbox-private/tools/wip-file-guard/guard.mjs` ... add harness memory paths to lenient list
2. `repos/ldm-os/components/memory-crystal-private/src/cc-hook.ts` ... add memory file sync after conversation capture
3. `repos/ldm-os/components/memory-crystal-private/src/openclaw.ts` ... add workspace memory sync after conversation capture
4. `repos/ldm-os/components/memory-crystal-private/src/core.ts` ... extend Memory category type

## Verification

1. Write a test memory file to `~/.claude/projects/*/memory/test.md` ... file guard should allow it
2. End a Claude Code session ... Stop hook should pick up the new memory file and ingest to Crystal
3. `crystal search "test memory"` ... should find the memory with correct agent_id and category
4. From Lesa: `crystal_search "test memory"` ... should also find it (shared memory)
5. Verify identity files (SOUL.md, IDENTITY.md) are still protected

## Order of operations

1. Fix 1 first (file guard) ... unblocks memory writes immediately
2. Fix 4 (schema) ... add types before the hooks need them
3. Fix 2 (CC hook) ... sync CC memories to Crystal
4. Fix 3 (Lesa hook) ... sync Lesa memories to Crystal
5. Alpha release, install, test

## Hermes Research

Hermes Agent by Nous Research (https://github.com/NousResearch/hermes-agent) is a potential sixth citizen:
- MCP-native (first-class support, both stdio and HTTP)
- MIT licensed, model-agnostic (15+ providers including Anthropic, OpenAI, OpenRouter)
- Can serve as MCP server or consume MCP servers
- SQLite-based session persistence with memory
- Multi-platform gateway (Telegram, Discord, Slack, WhatsApp, Signal, CLI)
- Install: `curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash`
- Integration path: bidirectional MCP. Hermes consumes our Crystal MCP server, we consume Hermes tools.
- Status: to be installed and tested
