# Proactive Agent Workflow Helper

## What It Does

Design proactive agent workflows that notice recurring needs, propose timely actions, and stay bounded by permissions, evidence, and user control.

This package was generated from demand signals in run `20260623-040526` and then rewritten for publication with domain-specific workflow guidance instead of generic task scaffolding.

## Best For

Agent builders, operations teams, productivity system designers, and skill authors adding proactive behavior to assistant workflows.

## Workflow Summary

1. Define trigger signals, user benefit, allowed data sources, action boundaries, opt-out rules, and what must never happen automatically.
2. Separate observe, decide, prepare, ask, and act stages so the agent can gather context without silently mutating important state.
3. Design thresholds for notification, confidence, freshness, duplication, and cooldown to prevent spam.
4. Specify approval gates for external sends, purchases, destructive file changes, account changes, and public publishing.
5. Create audit records that show signal, decision reason, proposed action, user response, and final outcome.
6. Test quiet periods, conflicting signals, stale data, user denial, and repeated-trigger scenarios.

## Deliverables

- A proactive workflow spec with triggers, thresholds, and approval gates.
- Notification copy and escalation rules.
- A state model for cooldowns, duplicate suppression, and audit logging.
- A test checklist for safe proactive behavior.

## Quality Bar

- The user remains in control of sensitive, destructive, or public actions.
- Triggers are specific enough to avoid repeated low-value notifications.
- The workflow records why each proactive suggestion happened.
- Failure, stale data, and opt-out paths are explicit.

## Trigger Examples

- `Use $work-productivity-proactive-agent-workflow-helper to design a proactive follow-up agent.`
- `Add approval gates and cooldowns to this monitoring workflow.`
- `Turn this recurring manual check into a safe proactive assistant flow.`

## Files

- `SKILL.md`: English skill instructions.
- `SKILL.zh-CN.md`: Chinese skill instructions.
- `README.md`: English user-facing guide.
- `README.zh-CN.md`: Chinese user-facing guide.
- `references/requirement-plan.md`: Demand evidence and scoring details.
- `agents/openai.yaml`: Default invocation metadata.
