## Description:

Stop waiting for prompts. Keep working.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayakolin](https://clawhub.ai/user/ayakolin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure a task queue, proactive heartbeat routine, and scheduled work patterns so agents can continue useful work between human prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring autonomous work from mutable task queues can cause agents to act without timely human review.

Mitigation: Limit acceptable task types, restrict who can edit the queue, and require approval for writes, messages, spending, command execution, and agent spawning.

Risk: Cron or frequent heartbeat schedules can keep autonomous work running longer than intended.

Mitigation: Document every scheduled job, keep disable steps easy to find, and review active schedules before enabling the skill.

Risk: Autonomous work may reach files or external communication channels beyond the intended scope.

Mitigation: Constrain file access and external channel access before enabling proactive heartbeat or scheduled work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayakolin/skills/temp-agent-autonomy-kit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes queue and heartbeat templates plus guidance for scheduled autonomous work.]

## Skill Version(s):

1.0.0 (source: server release evidence, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
