## Description:

Helps agents coordinate in Telegram group chats by using structured session keys and message parameters for multi-bot communication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1227cwx](https://clawhub.ai/user/1227cwx)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure multi-agent coordination in Telegram group chats, including how one bot should address another through session keys and how replies should be sent with the correct bot account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deployment guidance can copy every installed skill across matching OpenClaw workspaces, expanding the effect of an operator mistake.

Mitigation: Review deployment commands before running them, copy only the intended telegram-bot-chat skill, and use explicitly chosen bot workspaces.

Risk: Telegram group messages may expose credentials, internal prompts, or sensitive user data to group participants or bot infrastructure.

Mitigation: Do not send credentials, tokens, internal prompts, or sensitive user data through Telegram groups.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1227cwx/skills/telegram-bot-chat)
- [Publisher profile](https://clawhub.ai/user/1227cwx)
- [Telegram homepage](https://telegram.org)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline code blocks and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes session key patterns, message parameter examples, deployment commands, and troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
