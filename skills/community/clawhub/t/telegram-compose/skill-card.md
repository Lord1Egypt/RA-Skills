## Description:

Format and deliver rich Telegram messages with HTML formatting through the Telegram API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tmchow](https://clawhub.ai/user/tmchow)

### License/Terms of Use:


## Use Case:

Agents and operators use this skill to turn substantive updates, reports, alerts, and briefings into scannable Telegram messages and send them to a specified chat or topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically transmit substantive content to Telegram using a local bot token.

Mitigation: Install only when Telegram delivery is intended, keep the bot limited to intended chats, and avoid sending secrets or sensitive reports.

Risk: Token handling and local config access may expose Telegram credentials if used in a high-sensitivity environment.

Mitigation: Protect OpenClaw config files, use scoped bot tokens, rotate tokens if exposed, and review token handling before high-sensitivity use.

Risk: Invalid topic fallback can route messages outside the intended Telegram thread.

Mitigation: Confirm chat and thread IDs before use and review fallback behavior before sensitive deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tmchow/skills/telegram-compose)
- [Publisher Profile](https://clawhub.ai/user/tmchow)
- [Telegram Bot API endpoint](https://api.telegram.org)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Telegram HTML message content with shell/API delivery steps and a message_id or error result.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an explicit Telegram bot account, chat ID, and optional thread ID; messages over Telegram limits are split before delivery.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
