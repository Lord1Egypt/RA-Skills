---
name: self-improving-negotiation
description: "Injects negotiation self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🤝","events":["agent:bootstrap"]}}
---

# Self-Improving Negotiation Hook

Injects a negotiation reminder at bootstrap so agents remember to log patterns and risks.

## Behavior

- Fires on `agent:bootstrap`
- Adds a virtual reminder file for negotiation logging prompts
- Reminder-only behavior

## Safety

This hook does not execute agreement actions.

- No acceptance of terms
- No pricing commitments
- No legal or financial approvals
- No finalization of agreements

Human approval remains required for high-impact concessions and final terms.

## Enable

```bash
openclaw hooks enable self-improving-negotiation
```
