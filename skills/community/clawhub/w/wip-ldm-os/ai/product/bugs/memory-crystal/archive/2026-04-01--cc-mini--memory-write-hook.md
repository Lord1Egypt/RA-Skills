# Bug: Agent memory writes don't sync to Memory Crystal

**Date:** 2026-04-01
**Reporter:** Parker
**Status:** Open
**Severity:** High
**Repos:** memory-crystal-private, wip-ldm-os-private, wip-ai-devops-toolbox-private

---

## Problem

When Claude Code writes to its auto-memory files (`~/.claude/projects/*/memory/*.md`), those memories stay local. Lesa writes to her workspace memory (`workspace/MEMORY.md`, `workspace/memory/*.md`). Those also stay local. Neither agent's memories are visible to the other through Memory Crystal search.

Memory Crystal should be the shared memory that all agents can search. Right now it only captures conversation turns (via hooks). It does not capture the structured memories that agents write to their own file-based systems.

## Two bugs

### Bug 1: Guard blocks memory file writes

The branch guard checks the CWD's git branch and blocks all Writes when on main. But Claude Code's auto-memory files live at `~/.claude/projects/*/memory/` which is NOT in a git repo. The guard should check whether the TARGET path is inside a git repo on main, not just whether the CWD is on main.

**Repo:** wip-ai-devops-toolbox-private (tools/wip-branch-guard/guard.mjs)

### Bug 2: Memory writes need a hook to sync to Crystal

When any agent writes a memory (file-based), that memory should also be written to Memory Crystal with the correct type metadata. This makes all memories searchable across all agents through one system.

**Repo:** memory-crystal-private (new hook), wip-ldm-os-private (hook wiring)

---

## The Four Memory Types

Reference: Claude Code source analysis (`cc-src-private/ai/product/notes/2026-03-31--cc-mini--influence-analysis.md`)

These are the four structured memory types that Claude Code uses. The hook should tag each memory with its type when writing to Crystal.

### 1. `user`
Who the person is. Role, goals, preferences, knowledge level.
- Example: "Parker is the founder, based in LA, prefers no em dashes"
- Example: "User is a data scientist investigating logging"
- Purpose: tailor responses to the person's perspective

### 2. `feedback`
Corrections AND confirmations. What to avoid and what to keep doing.
- Example: "Don't mock the database in tests"
- Example: "Single bundled PR was the right call here"
- Purpose: agent doesn't repeat mistakes, doesn't drift from validated approaches

### 3. `project`
Ongoing work, goals, decisions, deadlines. Context behind the work.
- Example: "Merge freeze begins March 5 for mobile release"
- Example: "Auth rewrite is driven by legal compliance, not tech debt"
- Purpose: understand motivation and constraints behind requests
- Decays fast. Relative dates must be converted to absolute.

### 4. `reference`
Pointers to external systems. Where to find information.
- Example: "Pipeline bugs tracked in Linear project INGEST"
- Example: "Oncall latency dashboard at grafana.internal/d/api-latency"
- Purpose: know where to look without being told every time

---

## Hook Design

### For Claude Code (PreToolUse or Stop hook)

When Claude Code writes to a memory file (`~/.claude/projects/*/memory/*.md`), fire a hook that:

1. Reads the memory file content (frontmatter + body)
2. Extracts: `name`, `description`, `type` (user/feedback/project/reference)
3. Calls `crystal remember` with the content and type as metadata
4. Tags with `agent_id: "claude-code"` and the memory type

Hook location: Claude Code Stop hook or a file watcher on the memory directory.

### For Lesa (OpenClaw agent_end hook)

When Lesa writes to her workspace memory files, the existing `agent_end` hook should also:

1. Check if any workspace memory files changed this turn
2. If so, read the changed content
3. Call `crystal remember` with the content, tagged `agent_id: "lesa"`
4. Classify into one of the four types based on content

### For Open Claude / future agents

Same pattern. Any agent that writes structured memories fires a hook that syncs to Crystal with the four-type taxonomy.

---

## What this enables

- `crystal_search "user preferences"` finds memories from ALL agents
- Claude Code can search what Lesa learned. Lesa can search what CC learned.
- The four types allow filtered search: "show me all feedback memories" or "what project context exists for Q3?"
- Memory Crystal becomes the single shared memory. File-based memories are the local cache. Crystal is the index.

---

## Upstream tickets

This bug rolls up from:
- memory-crystal-private (hook implementation)
- wip-ai-devops-toolbox-private (guard fix for memory path)
- wip-ldm-os-private (hook wiring in boot/install)
