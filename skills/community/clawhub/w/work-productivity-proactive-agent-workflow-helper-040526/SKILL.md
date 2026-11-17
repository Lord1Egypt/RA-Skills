---
name: work-productivity-proactive-agent-workflow-helper
description: >-
  Design proactive agent workflows that notice recurring needs, propose timely actions, and stay bounded by permissions, evidence, and user control. Use when a user asks for proactive agent, automation, notifications, workflow, approval gates, or needs practical workflow, code, checklist, documentation, or review support for this job.
---

# Proactive Agent Workflow Helper

## Purpose

Use this skill when a user wants an agent to monitor signals, suggest next actions, or prepare work before being asked, without becoming noisy, unsafe, or hard to audit.

Audience: agent builders, operations teams, productivity system designers, and skill authors adding proactive behavior to assistant workflows.

Read `references/requirement-plan.md` when demand evidence, source links, scoring rationale, or review criteria are needed.

## Workflow

1. Define trigger signals, user benefit, allowed data sources, action boundaries, opt-out rules, and what must never happen automatically.
2. Separate observe, decide, prepare, ask, and act stages so the agent can gather context without silently mutating important state.
3. Design thresholds for notification, confidence, freshness, duplication, and cooldown to prevent spam.
4. Specify approval gates for external sends, purchases, destructive file changes, account changes, and public publishing.
5. Create audit records that show signal, decision reason, proposed action, user response, and final outcome.
6. Test quiet periods, conflicting signals, stale data, user denial, and repeated-trigger scenarios.

## Expected Outputs

- A proactive workflow spec with triggers, thresholds, and approval gates.
- Notification copy and escalation rules.
- A state model for cooldowns, duplicate suppression, and audit logging.
- A test checklist for safe proactive behavior.

## Validation

- The user remains in control of sensitive, destructive, or public actions.
- Triggers are specific enough to avoid repeated low-value notifications.
- The workflow records why each proactive suggestion happened.
- Failure, stale data, and opt-out paths are explicit.

## Triggers

Keywords: `proactive agent`, `automation`, `notifications`, `workflow`, `approval gates`, `monitoring`, `audit log`

Example trigger sentences:

- `Use $work-productivity-proactive-agent-workflow-helper to design a proactive follow-up agent.`
- `Add approval gates and cooldowns to this monitoring workflow.`
- `Turn this recurring manual check into a safe proactive assistant flow.`
