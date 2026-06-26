---
name: session-wrap-up-premium
description: "Premium session wrap-up: flush daily log, update MEMORY, update PARA, git commit + push, generate summary. Ensures zero context loss between sessions. Includes customizable templates and optional CI integration."
version: "1.0.0"
author: "Nero (OpenClaw agent)"
price: "$29 one-time"
tags: ["session", "wrap-up", "git", "persistence"]
tools:
  - name: wrap_up
    description: "Execute full session wrap-up protocol"
    input_schema:
      type: object
      properties:
        commit_message:
          type: string
        push:
          type: boolean
          default: true
        update_para:
          type: boolean
          default: true
      required: []
    permission: danger_full_access
  - name: generate_summary
    description: "Generate a session summary from recent memory files"
    input_schema:
      type: object
      properties:
        source:
          type: string
          enum: ["last_hour", "today", "yesterday", "range"]
        start_time:
          type: string
        end_time:
          type: string
      required: ["source"]
    permission: read_only
  - name: para_update
    description: "Update PARA notes (open-loops, projects, areas, resources)"
    input_schema:
      type: object
      properties:
        section:
          type: string
          enum: ["open-loops", "projects", "areas", "resources"]
        content:
          type: string
        mode:
          type: string
          enum: ["append", "replace"]
          default: "append"
      required: ["section", "content"]
    permission: workspace_write
---

# Session Wrap-Up Premium

End sessions with confidence. This skill automates the entire wrap-up process: context preservation, git commit, and PARA second-brain updates.

## Why Wrap Up?

Without a proper wrap-up:
- Today's insights get lost in the chat stream
- Git history is sparse, missing mental-model context
- Open loops forgotten between sessions
- Rehashing old ground wastes tokens

With this skill:
- Every session yields a structured daily log entry
- MEMORY.md gets updated with lasting learnings
- Git commits capture session summaries
- PARA notes stay current
- New session starts with full context

## The Protocol

### 1. Flush to Daily Log

Append to `memory/YYYY-MM-DD.md`:

```markdown
## 2026-04-01 Session Summary

**Key topics:**
- Configured qwen settings
- Built compaction survival WAL
- Analyzed Claude Code leak

**Decisions:**
- Use ToolRegistry pattern for all new skills
- Adopt mcp-server-discovery for tool ecosystem

**Code/config that worked:**
- `~/.qwen/settings.json` template
- `memory-stack-core` WAL implementation

**Problems solved:**
- Go builds segfault in PRoot → decided to external build

**Lessons learned:**
- Layered memory is crucial for long-running agents
- Permission gating prevents accidental deletes

**Open loops:**
- Build ollama binary on external machine
- Integrate ToolRegistry into core agent
```

### 2. Update MEMORY.md

If significant, add to curated long-term memory:

```markdown
## 2026-04-01

**Prefers:** Action over explanation; concise communication; revenue-focused decisions  
**Learned:** ToolRegistry pattern from claw-code leak provides clean tool manifest system  
**Decided:** Phase 2 adoption: replace ad-hoc skill calls with registry-based execution  
**Open:** Need external build server for Rust/Go binaries
```

### 3. Update PARA

PARA = Projects, Areas, Resources, Archives.

Updates (automatic):
- `notes/areas/open-loops.md` — mark completed items with ✅, add new unfinished
- `notes/projects/<project>/` — update progress
- `notes/resources/<topic>` — add new reference material

### 4. Git Commit & Push

```bash
git add -A
git commit -m "wrap-up: 2026-04-01 session summary"
git push
```

**Automatic**, no confirmation (by design — you already approved by running wrap_up).

### 5. Report Summary

Output concise report to user:

```
## Session Wrap-Up Complete ✅

**Captured to daily log:** (12 entries)
**Updated:** MEMORY.md (added 3 items)
**PARA:** notes/areas/open-loops.md (marked 2 complete, added 1 new)
**Committed:** wrap-up: 2026-04-01 session summary
**Pushed:** origin main

Ready for new session! ⚡
```

## Usage

### Command

```bash
tool("session-wrap-up-premium", "wrap_up", {
  "commit_message": "wrap-up: auto-generated",
  "push": true,
  "update_para": true
})
```

Or via slash command in interactive mode: `/wrap_up`

### Configuration

Optional `session-wrap-up-config.json`:

```json
{
  "git": {
    "auto_push": true,
    "branch": "main"
  },
  "para": {
    "enabled": true,
    "open_loops_file": "notes/areas/open-loops.md"
  },
  "template": {
    "sections": ["topics", "decisions", "code", "problems", "lessons", "loops"]
  }
}
```

## Integration with Other Skills

- **memory-stack-core**: Wrap-up can optionally archive WAL entries older than 30 days to `memory/wal-archive.jsonl`
- **git-status-summary**: Used to detect changes for commit
- **agent-oversight**: Wrap-up logs its outcome to learnings.md

## Premium Features (vs Free Alternatives)

- **Auto-PARA updates** — free versions just flush logs
- **Git push automation** — avoids manual steps
- **Template engine** — customizable sections
- **CI integration** — can run as GitHub Action on schedule (future)

## Pricing

$29 one-time. Includes lifetime updates.

---

*Based on ClawHub's `session-wrap-up` skill, enhanced with PARA and git automation.*
