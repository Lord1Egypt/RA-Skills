# TRAE Memory System Reference Guide

> This document guides the new session's agent on how to recover cross-session memory.
> TRAE IDE auto-injects some memory via `<memory_item>` system reminders, but explicit file reads are more reliable.
>
> **Consent required**: Reading memory files (user profile, project memory, session history) may expose personal preferences and project-internal information. The agent should inform the user before reading these files and respect the user's choice to decline.

---

## Memory System Architecture

```
~/.trae-cn/memory/
├── projects/
│   └── <project-key>/              # Project path encoded as directory name
│       ├── project_memory.md        # Project-level persistent memory (all sessions share)
│       ├── <YYYYMMDD>/               # Date-grouped session memories
│       │   ├── topics.md            # All session topic summaries for that day
│       │   ├── session_memory_<id>.jsonl  # Per-session granular memory
│       │   └── session_memory_<id>.jsonl
│       └── <YYYYMMDD>/
│           └── topics.md
└── user_profile.md                  # Cross-project user preferences (global)
```

---

## Three Memory Layers

### 1. User-Level Memory (Global, Cross-Project)

**File**: `~/.trae-cn/memory/user_profile.md`

**Contents**: User preferences, communication language, code style, tech stack, workflows, constraints.

**When to read**: Read at session start **only with explicit user consent** (skip if declined). This file is global — it applies to all projects.

**How TRAE uses it**: Auto-injected via `<memory_item type="user_profile">` in system reminders. The new session can rely on auto-injection; explicit file reads require user opt-in.

### 2. Project-Level Memory (Shared Within Project)

**File**: `~/.trae-cn/memory/projects/<project-key>/project_memory.md`

**Contents**: Project-specific engineering conventions, hard constraints, lessons learned.

**When to read**: Read at session start **only with explicit user consent** for the current project.

**How TRAE uses it**: Auto-injected via `<memory_item type="project_memory">` in system reminders.

**Project key encoding**: The `<project-key>` is the project path with special characters replaced. Example: `c:\Users\<your-username>\Documents\<project-name>` becomes `-c-Users-<your-username>-Documents-<project-name>` (special chars replaced with hyphens).

### 3. Topic-Level Memory (Recent Sessions)

**File**: `~/.trae-cn/memory/projects/<project-key>/<YYYYMMDD>/topics.md`

**Contents**: Per-session topic summaries, timestamped with session ID.

**Format**:
```
[session_id: 6a2a4044f1a95b585d79fbb9 | topic_summary_time: 2026-06-11 14:51:59]
User requested extracting and transcribing content from...
```

**When to read**: Read the last 2 days of `topics.md` files for recent context **only with explicit user consent**.

### 4. Message-Level Memory (Granular, Per-Session)

**File**: `~/.trae-cn/memory/projects/<project-key>/<YYYYMMDD>/session_memory_<session_id>.jsonl`

**Contents**: Per-message metadata — tasks, TODOs, related files, actions taken.

**When to read**: Do NOT read upfront (too large). Instead, use Grep to search by keywords relevant to the current task.

**How TRAE uses it**: Auto-injected via `<memory_item type="recent_topic">` — only the most recent topic summaries are injected.

---

## Quick Memory Lookup (For New Session Agent)

When the new session's agent receives the startup prompt, it should:

1. **Ask the user for explicit consent** before reading any memory files — explain that memory files may contain personal preferences and project-internal information
2. **If consent is granted**, read `user_profile.md` — understand user preferences (language, code style, constraints)
3. **If consent is granted**, read `project_memory.md` — understand project conventions and lessons learned
4. **If consent is granted**, read recent `topics.md` — scan last 2 days for relevant session topics
5. **If consent is granted**, grep `session_memory` files — search by keywords from the handoff doc if deeper context is needed
6. **If consent is declined**, rely on TRAE's auto-injected `<memory_item>` tags and the handoff doc only — do NOT silently read memory files

### Example Grep Search

To find all session memories mentioning a specific file or concept:
```
Grep pattern: "session-handoff|handoff|branch|fork"
path: ~/.trae-cn/memory/projects/<project-key>/
output_mode: content
```

---

## Important Notes

- **Read-shared, write-independent**: The new session reads the same memory files as the original session. New memories are written to a new `session_memory_<new_id>.jsonl` file, not overwriting the original.
- **Auto-injection is partial**: TRAE injects `<memory_item>` tags with recent topics and project/user memory. But it may not include all relevant entries — explicit reads are more reliable.
- **No env var values**: Memory files may reference env var names, but never contain values. The handoff doc should follow the same rule.
- **Project key discovery**: If the project-key is unknown, the agent can list `~/.trae-cn/memory/projects/` and match by path segments.
