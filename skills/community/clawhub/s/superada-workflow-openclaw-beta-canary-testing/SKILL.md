---
name: superada-workflow-openclaw-beta-canary-testing
description: A release-gate and issue-intelligence workflow for testing OpenClaw beta builds on one non-primary agent before expanding across a fleet. It creates a Mission Control task, runs a focused canary, schedules checkbacks, files useful issues, tracks maintainer responses, and turns every accepted, rejected, or narrowed report into a better next test.
---

# OpenClaw Beta Canary Testing

Workflow bundle exported from SuperAda.ai for ClawHub discovery.

## Source
- SuperAda page: https://superada.ai/workflows/openclaw-beta-canary-testing/
- Source URL: https://github.com/h-mascot/Enterprise-Crew-skills/tree/main/openclaw-beta-testing
- Category: Operations
- Difficulty: Advanced
- Status: Live

## Install

```bash
Review the workflow, create an MC task for the target beta and agent, run Phase 1 on one canary, then expand only after the canary decision is pass-expand.
```

## What It Does

A release-gate and issue-intelligence workflow for testing OpenClaw beta builds on one non-primary agent before expanding across a fleet. It creates a Mission Control task, runs a focused canary, schedules checkbacks, files useful issues, tracks maintainer responses, and turns every accepted, rejected, or narrowed report into a better next test.

## Verification
- OpenClaw CLI and gateway access
- Non-primary canary agent
- Task board with evidence
- Peer review
- Issue tracker access
- Intake completeness

## Safety Notes
- cron checkbacks
- peer review
- Peer-reviewed MC closure
- Do not run the full deep matrix when the Phase 1 canary already found a P0 stability problem.
- label: Peer review
- Mission Control task with peer review metadata
