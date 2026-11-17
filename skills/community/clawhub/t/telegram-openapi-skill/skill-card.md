## Description:

Operate Telegram Bot API through UXC with a curated OpenAPI schema, bot-token path auth, polling-based reads, and webhook management guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure UXC authentication and execute a lean Telegram Bot API surface for bot identity checks, chat lookup, messaging, polling, and webhook management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate with a Telegram bot token and perform write actions such as sending messages or media and changing webhook state.

Mitigation: Store the bot token in the configured environment variable and require explicit confirmation before sends, local uploads, webhook changes, or dropping pending updates.

Risk: Polling output and checkpoints may contain bot update data.

Mitigation: Store polling output in a private per-user directory with restrictive permissions and prefer the bundled schema or a pinned schema URL.

Risk: Local multipart uploads can send explicitly provided local files to Telegram.

Mitigation: Confirm each local file path before execution and limit uploads to files intentionally selected for the bot workflow.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/telegram-bot.openapi.json)
- [Telegram Bot API docs](https://core.telegram.org/bots/api)
- [Local Bot API server](https://github.com/tdlib/telegram-bot-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API operation names, JSON request examples, and local file paths for explicit multipart uploads.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
