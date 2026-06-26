---
name: self-improving-security
description: "Injects security self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🛡️","events":["agent:bootstrap"]}}
---

# Security Self-Improvement Hook

Injects a reminder to evaluate security findings during agent bootstrap.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Adds a reminder block to check `.learnings/` for security-relevant entries
- Prompts the agent to log vulnerabilities, misconfigurations, access violations, and incidents
- Emphasizes **NEVER logging actual secrets, credentials, or PII**

## Configuration

No configuration needed. Enable with:

```bash
openclaw hooks enable self-improving-security
```
