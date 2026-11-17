## Description:

Slack messaging skill for sending messages, managing channels, uploading files, adding reactions, and automating team notifications through the Slack Web API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to prepare Slack Web API commands for workspace messaging, channel administration, file sharing, reactions, and notification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broad Slack token can allow the agent to post messages or read workspace data beyond the intended workflow.

Mitigation: Use a bot token with only the scopes needed for the workflow, and avoid user tokens unless a user-level action is required.

Risk: Messages, file links, or uploaded content may disclose confidential information if sent to the wrong channel.

Mitigation: Review channel IDs, message content, and file links before posting, and do not use the skill on confidential channels without approval.

Risk: Automated Slack calls may be throttled or fail when rate limits are exceeded.

Mitigation: Respect Slack rate limits and Retry-After headers when automating repeated messages or channel operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/charlie-morrison/skills/slack-messaging)
- [Slack App Configuration](https://api.slack.com/apps)
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage)
- [Slack conversations.list API](https://slack.com/api/conversations.list)
- [Slack files.getUploadURLExternal API](https://slack.com/api/files.getUploadURLExternal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Slack token supplied through SLACK_TOKEN.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
