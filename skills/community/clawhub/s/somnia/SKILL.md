---
name: somnia
description: Run overnight skill health reviews, replay-case availability checks, feedback triage, and proposal-only maintenance reports for OpenClaw agents. Use when the user asks for nightly review, sleep-time skill maintenance, skill bug scanning, replay regression checks, or safe skill-maintenance proposals.
---

# Somnia

## Overview

Somnia is the sleep-cycle maintenance layer for OpenClaw skills. It provides a repeatable review workflow that checks installed skills during quiet hours, summarizes health risks, and writes proposal artifacts without silently mutating runtime skills.

Current version: `v0.4.3 "Standalone Safety"`.

## Trigger Cues

Use this skill when the user mentions:

- `nightly skill review`
- `sleep-time maintenance`
- `skill health report`
- `skill bug scanning`
- `replay regression check`
- `feedback-driven upgrade`
- `proposal-based update`
- `Somnia`

## Default Workflow

1. Confirm the review scope: managed skills, feedback-related skills, or all installed skills.
2. Run lightweight package validation, feedback summary, and replay-case availability checks for each selected skill.
3. Write JSON and Markdown health reports under the configured learning/report directory.
4. Write proposal artifacts only when feedback or quality gates justify the change.
5. Hand proposal artifacts to Skill Forge or a human maintainer before any install decision.
6. Keep simulated evaluation details hidden from user-facing reports.

## Output Contract

The final answer or artifact should include:

- Review scope and schedule assumption
- Skills checked and health summary
- Issues found, grouped by skill
- Update candidates proposed or blocked
- Replay and hidden-evaluation pass/fail summary
- Next action: no-op, review proposal, approve install, or adjust schedule

## Quality Gates

- Never auto-install skill changes; Somnia writes proposals and reports only.
- Keep hidden evaluation and replay case details out of user-facing Telegram reports.
- Redact feedback-derived content before it becomes a replay case or report item.
- Prefer proposal files and manifests over direct mutation of installed skills.
- Keep Somnia self-contained; do not execute out-of-package Skill Forge code.

## Resources

References:
- `references/somnia-architecture.md`
- `references/schedule-and-policy.md`

Scripts:
- `scripts/nightly_skill_review.py`
- `scripts/schedule_nightly_review.py`
