## Description:

Use when you need to control Slack from OpenClaw via the message tool, including reacting to messages or pinning/unpinning items in Slack channels or DMs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ailven](https://clawhub.ai/user/ailven)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Slack through OpenClaw message actions for channel and DM workflows, including sending, reading, reacting, editing, deleting, pinning, unpinning, listing pins, looking up member information, and listing custom emojis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Slack bot-token authority for reading, sending, editing, deleting, pinning, unpinning, direct messages, and member profile lookup.

Mitigation: Install only with the smallest needed Slack scopes and channel access, and manually confirm delete, edit, pin, unpin, DM, and member profile lookup actions before execution.

Risk: Slack reads and member-info lookups may expose workspace content or user profile data to the agent.

Mitigation: Limit use to approved channels and users, and avoid requesting member profile details unless they are needed for the current task.

## Reference(s):

- [Slack (Socket Mode) on ClawHub](https://clawhub.ai/ailven/skills/slack-socket)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with message action examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires configured Slack channel access through channels.slack.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
