---
name: self-improving-meta
description: "Injects meta self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🔧","events":["agent:bootstrap"]}}
---

# Meta Self-Improvement Hook

Injects a reminder to evaluate agent infrastructure learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a meta-specific reminder block to check `.learnings/` for infrastructure entries
- Prompts the agent to log prompt file issues, hook failures, skill activation problems, rule conflicts, context bloat, and memory staleness
- Skips subagent sessions to avoid noise
- Reminder-only behavior: does not modify files or call network resources

## Reminder Content

The hook injects reminders to log to the appropriate file based on what occurred:

| Trigger | Target File | Category |
|---------|-------------|----------|
| Agent misinterprets prompt file instruction | `LEARNINGS.md` | `instruction_ambiguity` |
| Hook fails or produces no output | `META_ISSUES.md` | hook_failure |
| Skill doesn't activate when expected | `META_ISSUES.md` | skill_gap |
| Two rules contradict each other | `LEARNINGS.md` | `rule_conflict` |
| Context window feels cramped/truncated | `LEARNINGS.md` | `context_bloat` |
| Memory entry is stale or wrong | `LEARNINGS.md` | `prompt_drift` |
| Missing skill capability | `FEATURE_REQUESTS.md` | feature request |

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-meta
```
