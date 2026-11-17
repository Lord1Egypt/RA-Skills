## Description:

Provides launch verification and watchdog discipline for delegated, backgrounded, browser-driven, and long-running tasks, preventing false "running" claims, clarifying failed_to_start vs failed_after_work_started, and treating heartbeat as a watchdog rather than the main progress loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike-alford](https://clawhub.ai/user/mike-alford)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage delegated, backgrounded, browser-driven, or long-running work with verified startup, truthful status reporting, and clear failure classification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may incorrectly report delegated or backgrounded work as running before startup is verified.

Mitigation: Require startup health checks before using the running state, and classify startup failures as failed_to_start.

Risk: Long-running or delegated tasks may stall or fail after meaningful work begins.

Mitigation: Use heartbeat as a watchdog for overdue or stalled work and report failed_after_work_started when execution began before failure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mike-alford/skills/subagent-sheepdog)
- [Publisher profile](https://clawhub.ai/user/mike-alford)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance and concise status language]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
