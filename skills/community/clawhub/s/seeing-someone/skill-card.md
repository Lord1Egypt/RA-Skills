## Description:

Early-stage rapport: phase updates, question relay, and summaries while things are still forming. Same official AILove agent API as loveq.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thesamething](https://clawhub.ai/user/thesamething)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to help an agent check AILove matching status, relay pending questions, summarize early-stage rapport updates, and configure scheduled morning and evening check-ins. The skill is intended to keep the human in control of answers and direct users to AILove for profile details or contact information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent scheduled jobs that read an AILove API key and send private relationship updates to a selected messaging destination.

Mitigation: Use an environment variable or secret store for the API key, choose a private destination, review cron jobs before enabling them, and confirm how to remove jobs and rotate the key.

Risk: Private relationship-status data may be exposed if credentials or scheduled delivery targets are misconfigured.

Mitigation: Send the AILove key only to the documented AILove API base URL, restrict credential file permissions, and avoid logging the full key in shared places.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thesamething/skills/seeing-someone)
- [Publisher profile](https://clawhub.ai/user/thesamething)
- [AILove homepage](https://heerweiyi.cc)
- [AILove Agent API base](https://heerweiyi.cc/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron configuration, credential-handling guidance, and API response summaries for private relationship-status updates.]

## Skill Version(s):

1.4.2 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
