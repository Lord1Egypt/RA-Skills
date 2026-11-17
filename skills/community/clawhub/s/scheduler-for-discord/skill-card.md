## Description:

Create and manage scheduled reminders and posts for Moltbot, especially messages delivered later or on a recurring schedule to the current Discord channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronwander](https://clawhub.ai/user/aaronwander)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn natural-language reminder or recurring-post requests into scheduled Moltbot jobs that deliver messages back to a Discord channel or another configured destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-written reminder text may be inserted into shell commands in a way that could run unintended commands.

Mitigation: Use only with trusted inputs until cron arguments are passed through a structured API or safely escaped argument array.

Risk: Incorrect or unvalidated delivery targets could send scheduled content to the wrong destination.

Mitigation: Validate channel IDs and job names, and prefer explicit channel:<id> or user:<id> targets.

Risk: Recurring jobs may continue running longer than intended if users cannot easily audit or remove them.

Mitigation: Provide clear list and delete workflows for recurring jobs before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaronwander/skills/scheduler-for-discord)
- [Publisher profile](https://clawhub.ai/user/aaronwander)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create one-shot or recurring scheduled jobs that deliver generated or user-provided messages to explicit channel or user destinations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
