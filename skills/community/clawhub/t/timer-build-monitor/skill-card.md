## Description:

Set, list, and cancel one-shot async timers specialized for build monitoring and long-running task checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to schedule a single delayed check for an asynchronous build or long-running task, then review the resulting timer status without setting up cron or repeated reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Timer requests may pass broader conversation context to delayed subagents.

Mitigation: Use minimal task descriptions and avoid including secrets or unrelated sensitive details in timer requests.

Risk: The cancel command marks timer state as cancelled but does not stop already delayed subagent work.

Mitigation: Treat cancellation as local status only until session termination is implemented; do not rely on it for sensitive or time-critical cancellation.

Risk: Timer metadata is retained in a local JSON state file.

Mitigation: Avoid sensitive task names and clear local timer metadata when it is no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/space-cadet/skills/timer-build-monitor)
- [Publisher profile](https://clawhub.ai/user/space-cadet)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and plain-text timer status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local timer metadata under ~/.openclaw/timers/ when used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
