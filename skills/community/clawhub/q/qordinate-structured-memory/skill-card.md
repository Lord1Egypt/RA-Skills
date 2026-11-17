## Description:

Qordinate is a chat-native assistant that acts as structured memory for OpenClaw agents by letting them offload long-term facts, tasks, and reminders over WhatsApp, Telegram, or Slack.

This skill is ready for commercial/non-commercial use.

## Publisher:

[singhcoder](https://clawhub.ai/user/singhcoder)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to let an OpenClaw agent save, update, and query durable facts, list items, tasks, contacts, leads, links, and reminders through a Qordinate chat account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent broad discretion to send durable personal or business information to Qordinate through the user's chat accounts.

Mitigation: Require explicit confirmation before saving sensitive items and use the integration only when the user is comfortable with selected information being stored durably.

Risk: Passwords, tokens, private communications, regulated data, or confidential file contents could be forwarded if the agent treats Qordinate as general memory.

Mitigation: Exclude secrets, regulated data, confidential file contents, and private communications from Qordinate messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/singhcoder/skills/qordinate-structured-memory)
- [Qordinate website](https://qordinate.ai)
- [Qordinate Slack setup](https://qordinate.ai/slack)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown instructions with structured natural-language message examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an existing Qordinate account and access to an enabled WhatsApp, Telegram, or Slack channel.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
