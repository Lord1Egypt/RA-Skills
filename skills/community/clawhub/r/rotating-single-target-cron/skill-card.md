## Description:

Create or update recurring chat cron jobs that select exactly one configured @ID per run, avoid immediately repeating the previous target when possible, persist the last-picked target in workspace state, and post one single-target message to chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakullla](https://clawhub.ai/user/sakullla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and chat workspace operators use this skill to create or update recurring scheduled chat prompts that rotate through a roster and mention one person per run. It is suited for daily or weekly single-target messages such as story prompts, wake-up messages, teasing posts, or fortune-style rotations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A recurring chat job can post to the wrong destination, mention the wrong roster member, or use an unintended schedule or timezone.

Mitigation: Review the roster, destination, schedule, timezone, and message style before enabling or updating the job.

Risk: The skill stores the last mentioned @ID in a workspace memory file.

Mitigation: Confirm the workspace state-file path is acceptable and remains under the intended memory location.

Risk: Live tests in an active group chat will post a message and advance the rotation state.

Mitigation: Run a live test only after explicitly confirming the post and state change are acceptable.

## Reference(s):

- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/sakullla/skills/rotating-single-target-cron)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with prompt skeletons and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include guidance for a workspace state file that stores the last selected @ID.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
