## Description:

Create and send native Slack Block Kit messages, including tables, code cards, structured layouts, buttons, inputs, and rich Slack blocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bill492](https://clawhub.ai/user/bill492)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to compose rich Slack-native messages when plain mrkdwn is not enough. It supports portable OpenClaw presentation messages, Slack-specific Block Kit JSON, local sample validation, and direct Slack API posting guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help compose and post Slack messages, so content may be sent to the wrong channel or thread if destinations are not checked.

Mitigation: Confirm the destination channel, thread, and message content before using direct Slack API posting.

Risk: Slack bot tokens are required for direct posting and could be exposed if pasted into chat, logs, or generated commands.

Mitigation: Keep Slack bot tokens in configured secrets and avoid printing token values while copying or debugging commands.

Risk: Local sample validation is lightweight and does not replace full Slack schema or runtime validation.

Mitigation: Run the bundled sample validator and verify important messages with Slack readback when testing or investigating incidents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bill492/skills/slack-block-kit)
- [Slack chat.postMessage API](https://slack.com/api/chat.postMessage)
- [Slack Block Kit reference](https://api.slack.com/block-kit/reference)
- [Slack thinking steps partner guide](https://api.slack.com/partners/thinking-steps)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Slack Block Kit JSON examples and optional shell commands or API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes reusable sample JSON files and a table generator; direct Slack posting requires a Slack bot token and confirmed channel or thread destination.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
