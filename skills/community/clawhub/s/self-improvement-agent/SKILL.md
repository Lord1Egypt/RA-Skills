---
name: self-improving-agent
description: "Captures learnings, errors, and corrections for continuous improvement. Use when: (1) A command fails unexpectedly, (2) User corrects you ('No, that's wrong...', 'Actually...'), (3) User requests a missing capability, (4) An external API or tool fails, (5) You realize your knowledge is outdated, (6) A better approach is found for a recurring task. Also review `.learnings/` before major tasks. Trigger words: 'actually', 'wrong', 'outdated', 'I wish you could', 'why can't you', non-zero exit code."
---

# Self-Improvement Skill

Log learnings and errors to markdown files. Important patterns get promoted to project memory files.

## Quick Reference

| Situation | Action |
|-----------|--------|
| Command/operation fails | Log to `.learnings/ERRORS.md` |
| User corrects you | Log to `.learnings/LEARNINGS.md` (category: `correction`) |
| User wants missing feature | Log to `.learnings/FEATURE_REQUESTS.md` |
| API/external tool fails | Log to `.learnings/ERRORS.md` |
| Knowledge was outdated | Log to `.learnings/LEARNINGS.md` (category: `knowledge_gap`) |
| Found better approach | Log to `.learnings/LEARNINGS.md` (category: `best_practice`) |
| Similar to existing entry | Link with `**See Also**`, bump priority |
| Broadly applicable learning | Promote to workspace files (see below) |

## Promotion Targets

When a learning proves broadly applicable, elevate it:

| Learning Type | Promote To |
|---------------|------------|
| Behavioral patterns | `SOUL.md` |
| Workflow patterns | `AGENTS.md` |
| Tool gotchas | `TOOLS.md` |
| Project facts | `CLAUDE.md` or workspace prompt files |

## Logging Format

### Learning Entry

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | resolved | promoted | in_progress

### Summary
One-line description of what was learned

### Details
Full context: what happened, what was wrong, what's correct

### Suggested Action
Concrete fix or improvement

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: LRN-YYYYMMDD-XXX (if related)
```

### Error Entry

```markdown
## [ERR-YYYYMMDD-XXX] command_or_tool

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending

### Summary
Brief description of what failed

### Error
```
Paste actual error output here
```

### Context
- Command/operation attempted
- Input or parameters used
- Environment details

### Suggested Fix
If identifiable, how to resolve it

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/file.ext
```

### Feature Request Entry

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending

### Requested Capability
What the user wanted to do

### User Context
Why they needed it

### Complexity Estimate
simple | medium | complex
```

## ID Generation

`TYPE-YYYYMMDD-XXX` — e.g. `LRN-20250322-001`, `ERR-20250322-A3F`

## Resolving Entries

When fixed:
1. Set **Status**: `resolved` or `promoted`
2. Add resolution block:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: What was done
```

## Promoting to Workspace Files

**When**: Learning applies across files, prevents recurring mistakes, or any contributor should know it.

**How**: Distill into a concise rule. Add to target file. Set original entry to `promoted`.

Example learning:
> Project uses pnpm workspaces. `npm install` fails because lock file is `pnpm-lock.yaml`.

Promote to `CLAUDE.md`:
```markdown
## Build & Dependencies
- Package manager: **pnpm** (not npm) — always use `pnpm install`
```

## Recurring Pattern Detection

Before logging, search for related entries:
```bash
grep -r "keyword" .learnings/
```

If similar entry exists:
- Link with `**See Also**: LRN-...`
- Increment `Recurrence-Count`
- Consider systemic fix (promote to AGENTS.md, create tech debt ticket)

**Promote to permanent prompt guidance** when a pattern:
- Occurs 3+ times
- Spans 2+ distinct tasks
- Within a 30-day window

## OpenClaw Inter-Session Tools

Share learnings across sessions:

| Tool | Use |
|------|-----|
| `sessions_list` | View active/recent sessions |
| `sessions_history(sessionKey, limit)` | Read another session's transcript |
| `sessions_send(sessionKey, message)` | Send a learning to another session |
| `sessions_spawn(task, label, mode)` | Spawn a background sub-agent |

**Example**: After a session ends, promote its key learnings to workspace files.
Use `sessions_history` to review what another session discovered.

## Periodic Review

Check `.learnings/` at natural breakpoints:
- Before starting a new major task
- After completing a feature
- Weekly during active development

Quick status:
```bash
grep -h "Status.*pending" .learnings/*.md | wc -l  # count pending
grep -B3 "Priority.*high" .learnings/*.md | grep "^##"  # high priority items
```

## Detection Triggers

**Log immediately when you notice:**

| Signal | → Entry |
|--------|---------|
| Non-zero exit code, exception, timeout | `ERRORS.md` |
| User says "No, that's wrong...", "Actually..." | `LEARNINGS.md` (correction) |
| User provides info you didn't know | `LEARNINGS.md` (knowledge_gap) |
| "Can you also...", "I wish you could..." | `FEATURE_REQUESTS.md` |
| Found a better approach mid-task | `LEARNINGS.md` (best_practice) |
| Repeated mistake (2+ times) | Promote to workspace file |

## Best Practices

1. **Log immediately** — context is freshest right after the issue
2. **Be specific** — future you needs to understand quickly
3. **Suggest concrete fixes** — not just "investigate"
4. **Link related files** — makes fixes easier
5. **Promote aggressively** — broadly applicable learnings belong in workspace files, not hidden in `.learnings/`
6. **Use consistent IDs** — enables `See Also` linking

## Installation (OpenClaw)

```bash
clawhub install self-improving-agent
```

Manual:
```bash
git clone https://github.com/pskoett/self-improving-agent.git ~/.openclaw/skills/self-improving-agent
```

Create log directory:
```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

## Detailed Topics

For complete documentation, see:
- **OpenClaw integration**: `references/openclaw-integration.md`
- **Hook setup**: `references/hooks-setup.md`
- **Full entry examples**: `references/examples.md`
- **Skill extraction workflow**: `references/skill-extraction.md`
- **Other agents (Claude Code, Codex, Copilot)**: `references/other-agents.md`
