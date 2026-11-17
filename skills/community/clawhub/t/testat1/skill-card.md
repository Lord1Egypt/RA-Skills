## Description:

Use when you need to control Slack from Clawdbot via the slack tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaunceyliu](https://clawhub.ai/user/chaunceyliu)

### License/Terms of Use:


## Use Case:

Employees, external collaborators, and developers use this skill to direct Clawdbot to perform Slack actions such as reacting to messages, managing pins, sending or editing messages, reading recent messages, fetching member info, and listing custom emoji.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to read private Slack conversations or modify workspace messages, pins, and reactions through the configured bot token.

Mitigation: Install only with least-privilege Slack scopes and require explicit user direction before reading private conversations or changing messages.

Risk: Incorrect channel IDs, message timestamps, user IDs, or content could cause the agent to act on the wrong Slack item.

Mitigation: Confirm the target channel, message timestamp, user, and message content before sending, editing, deleting, pinning, or unpinning Slack items.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chaunceyliu/skills/testat1)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [Markdown guidance with JSON action payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Slack action guidance for an agent; execution depends on a configured Clawdbot Slack token and user-supplied channel, message, user, emoji, or content values.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
