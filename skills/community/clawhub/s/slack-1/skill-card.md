## Description:

Use when you need to control Slack from Clawdbot via the slack tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rumengkai](https://clawhub.ai/user/rumengkai)

### License/Terms of Use:


## Use Case:

Developers and workspace operators use this skill to have an agent manage Slack messages, reactions, pins, member lookup, and custom emoji through Clawdbot. It is useful when an agent needs to take explicit Slack actions with provided channel, message, or user IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, send, edit, delete, pin, and unpin Slack messages, which may affect sensitive workplace conversations.

Mitigation: Install only where Clawdbot should act in Slack, restrict access to appropriate channels, and review destructive actions before execution.

Risk: The configured Slack bot token may grant broader workspace access than the intended use case requires.

Mitigation: Use least-privilege Slack scopes for the bot token and periodically review granted permissions.

Risk: Member lookup, direct messages, and message reads can expose personal or confidential workspace data.

Mitigation: Limit use to approved workspaces and channels, and handle retrieved Slack data according to organizational data policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rumengkai/skills/slack-1)

## Skill Output:

**Output Type(s):** [guidance, JSON, API calls]

**Output Format:** [Markdown instructions with JSON action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Slack channel, message, or user identifiers and a configured Clawdbot Slack bot token.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
