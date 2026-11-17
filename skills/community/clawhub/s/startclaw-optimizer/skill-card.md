## Description:

StartClaw-Optimizer helps agents reduce context and model-cost overhead by routing tasks, compacting long context, scheduling automations, governing browser concurrency, and monitoring usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idanmann10](https://clawhub.ai/user/idanmann10)

### License/Terms of Use:

StartClaw Internal Use License

## Use Case:

Developers and agent operators use this skill to optimize Clawdbot-style subagent workflows with task routing, token compaction, automation scheduling, browser concurrency controls, and usage monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation authority may be under-scoped for workflows that mutate accounts, files, databases, payments, posts, or authenticated browser sessions.

Mitigation: Use the skill first with idempotent tasks and add explicit cancellation, retry, preflight, and postflight controls before production use.

Risk: Context telemetry can expose session identifiers, token counts, and detected task themes.

Mitigation: Minimize telemetry, redact or avoid persistent session identifiers, and define explicit handling for any logged context metadata.

Risk: Retries and fault-tolerant scheduling can repeat non-idempotent operations.

Mitigation: Gate scheduled work with idempotency checks, bounded retry policies, and operator-visible failure states.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include model-selection rationale, cost estimates, context-compaction recommendations, scheduler hooks, and dashboard commands.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
