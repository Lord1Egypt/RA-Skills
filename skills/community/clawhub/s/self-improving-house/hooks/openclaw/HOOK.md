---
name: self-improving-domotics
description: "Injects domotics self-improvement reminder during agent bootstrap"
metadata: {"openclaw":{"emoji":"🏠","events":["agent:bootstrap"]}}
---

# Self-Improving Domotics Hook

Injects a reminder to evaluate domotics learnings at bootstrap.

## What It Does

- Fires on `agent:bootstrap`
- Adds reminder content for logging `LRN` / `DOM` / `FEAT` entries
- Highlights reliability, safety, integration, and energy patterns
- Reinforces safe defaults and human confirmation for high-impact routines

## Safety Boundary

This hook is reminder-only and documentation-only.
It does not execute direct actuator actions (locks, alarms, gas/water shutoff, heaters).

## Configuration

Enable with:

```bash
openclaw hooks enable self-improving-domotics
```
