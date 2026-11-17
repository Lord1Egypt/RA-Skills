## Description:

Manage Tally forms, submissions, respondents, fields, and form workflow data via the Tally API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hith3sh](https://clawhub.ai/user/hith3sh)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage Tally forms, submissions, respondents, fields, notifications, and workflow data from an agent through ClawLink.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate on Tally forms, fields, workflows, notifications, submissions, and respondent data through the connected account.

Mitigation: Connect only the intended Tally account and confirm that requested operations match the user's intent before execution.

Risk: Write or delete actions can change or permanently remove forms, fields, notifications, workflow settings, or submissions.

Mitigation: Use previews and require explicit user confirmation before form, field, workflow, notification, submission, or delete operations.

Risk: Submission and respondent data may contain personal information.

Mitigation: Handle returned form data according to privacy best practices and limit access to data needed for the task.

## Reference(s):

- [ClawHub Tally Skill](https://clawhub.ai/hith3sh/skills/tally-forms)
- [Tally API Documentation](https://tally.so/help/webhooks)
- [Tally Developer Docs](https://tally.so/developers)
- [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=tally-forms)
- [ClawLink Docs](https://docs.claw-link.dev/openclaw)
- [ClawLink Verification](https://claw-link.dev/verify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown with inline bash commands and JSON tool parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Tally account through ClawLink; write and delete operations require explicit user confirmation.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
