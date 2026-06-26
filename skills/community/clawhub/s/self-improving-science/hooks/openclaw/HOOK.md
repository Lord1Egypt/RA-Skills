---
name: self-improving-science
description: "Injects science-specific self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🔬","events":["agent:bootstrap"]}}
---

# Self-Improving Science Hook

Injects a reminder to evaluate experiment learnings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a reminder block to check `.learnings/` for relevant experiment entries
- Prompts the agent to log methodology flaws, data quality issues, statistical errors, and reproducibility failures

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-science
```
