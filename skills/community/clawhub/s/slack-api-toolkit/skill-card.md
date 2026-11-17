## Description:

Provides Slack API access through Maton managed OAuth for sending messages, managing channels, listing users, searching conversations and files, and automating Slack workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, workspace operators, and agent users use this skill to perform Slack API tasks through Maton managed OAuth, including message, channel, user, reaction, pin, star, bot, file, and search operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Slack write operations can send messages or modify workspace resources through the connected account.

Mitigation: Require explicit user approval and confirm the target resource and intended effect before create, update, or delete calls.

Risk: The Maton API key and OAuth connection can provide access to Slack workspace data and actions.

Mitigation: Review the Slack scopes on the connected account, store the API key securely, and clarify where the Maton API key and OAuth connection are stored before sensitive workspace use.

Risk: Read and search operations can expose Slack messages, files, users, channels, and related workspace metadata.

Mitigation: Limit use to authorized workspace content and avoid retrieving sensitive data unless the user has explicitly approved the operation.

## Reference(s):

- [ClawHub Slack Skill](https://clawhub.ai/thcjp/skills/slack-api-toolkit)
- [Maton Slack API Base URL](https://api.maton.ai/slack/{method})
- [Maton Connection Management](https://api.maton.ai)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Configuration instructions]

**Output Format:** [Markdown guidance with shell, HTTP, JavaScript, and Python examples; live API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MATON_API_KEY and a connected Slack OAuth account for live Slack API operations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
