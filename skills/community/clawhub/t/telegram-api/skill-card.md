## Description:

Helps agents use the Telegram Bot API through Maton to manage chats, send messages, handle updates, and configure bot automations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and bot operators use this skill to interact with Telegram chats, messages, polls, commands, and updates through an authenticated Maton connection. It also guides user-approved webhooks and scheduled or event-driven automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message sends, edits, deletes, and other writes can affect chats or remove content.

Mitigation: Start with read-only calls and confirm recipients, payloads, and effects with the user before writes.

Risk: Webhooks and trigger destinations can forward future updates or events continuously.

Mitigation: Require separate approval for each destination, identify its operator and data scope, and restrict updates to those needed.

Risk: Hosted functions and event handlers can act on future events without a new prompt.

Mitigation: Review the handler and its side effects with the user before enabling automation.

Risk: Raw API keys and chat responses can expose credentials or personal data.

Mitigation: Prefer CLI-managed login, never print or store keys, and limit displayed or retained response data.

## Reference(s):

- [Telegram Bot API documentation](https://core.telegram.org/bots/api)
- [Maton CLI manual](https://cli.maton.ai/manual)
- [Maton](https://maton.ai)
- [Telegram Bot skill release](https://clawhub.ai/byungkyu/skills/telegram-api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Telegram Bot API responses; share only data needed for the task.]

## Skill Version(s):

1.2.9 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
