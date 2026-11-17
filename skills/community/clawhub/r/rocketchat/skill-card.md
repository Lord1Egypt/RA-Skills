## Description:

Rocket.Chat team messaging - channels, messages, users, integrations via REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zenjabba](https://clawhub.ai/user/zenjabba)

### License/Terms of Use:


## Use Case:

Developers and workspace operators use this skill to generate Rocket.Chat REST API commands for managing channels, messages, users, integrations, and server statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A powerful Rocket.Chat token can let an agent read or change workspace data.

Mitigation: Install only for a workspace the agent is intended to manage and prefer a limited-scope token when possible.

Risk: Generated commands can delete messages, archive channels, create users, post messages, or invoke webhooks.

Mitigation: Review commands before execution, especially destructive, administrative, posting, and webhook actions.

## Reference(s):

- [Rocket.Chat REST API Documentation](https://developer.rocket.chat/reference/api/rest-api)
- [Rocket.Chat API Documentation](https://developer.rocket.chat/reference/api)
- [ClawHub Skill Page](https://clawhub.ai/zenjabba/skills/rocketchat)
- [Publisher Profile](https://clawhub.ai/user/zenjabba)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces REST API command guidance that depends on RC_URL, RC_TOKEN, RC_USER_ID, curl, and optionally jq.]

## Skill Version(s):

1.0.2 (source: server release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
