## Description:

Schedules recurring prompts or commands on a cadence, runs the task once immediately, and returns cancellation details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they want an agent to schedule a prompt or command on a recurring interval, such as polling deployment status or repeating a slash-command. It helps normalize the cadence, create the recurring schedule, run the task once immediately, and provide cancellation or update details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring scheduled commands can repeatedly change files, deploy systems, or access sensitive services if the cadence or task is wrong.

Mitigation: Review the cadence, cancellation details, and command scope before scheduling; use the generated cancellation or update instructions to stop or adjust the loop.

## Reference(s):

- [Recurring Loop Runner on ClawHub](https://clawhub.ai/wimi321/skills/recurring-loop-runner)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown text with cadence, schedule identifier, immediate run result, and cancellation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include an immediate task execution result when the cadence is accepted.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
