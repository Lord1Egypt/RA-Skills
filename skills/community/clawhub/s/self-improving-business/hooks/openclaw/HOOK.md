---
name: self-improving-business
description: "Injects business self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"📊","events":["agent:bootstrap"]}}
---

# Business Self-Improvement Hook

Injects a reminder to evaluate business administration findings during agent bootstrap.

## What It Does

- fires on `agent:bootstrap`
- injects a lightweight reminder for logging LRN/BUS/FEAT entries
- highlights high-signal business triggers (SLA miss, approval delay, KPI variance)
- enforces reminder-only behavior
- states no transactional or approval execution

## Safety Boundary

This hook outputs reminder text only.
It does not execute approvals, spending, vendor commitments, payroll, or legal actions.

## Enable

```bash
openclaw hooks enable self-improving-business
```
