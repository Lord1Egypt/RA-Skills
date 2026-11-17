## Description:

Forward trading alerts and webhook events from TradingView to Telegram instantly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shinzzyak](https://clawhub.ai/user/shinzzyak)

### License/Terms of Use:

MIT

## Use Case:

Developers, traders, and operators use this skill to configure a self-hosted webhook relay that forwards TradingView alerts or other webhook events into Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The relay can be exposed broadly, and one message-forwarding endpoint is unauthenticated.

Mitigation: Require a non-empty WEBHOOK_SECRET on every POST endpoint, including /webhook/raw, before exposing the service beyond localhost.

Risk: Webhook payloads may contain secrets or private incident data and full webhook bodies are logged.

Mitigation: Avoid sending sensitive data in webhook payloads and restrict access to service logs.

Risk: A publicly reachable deployment can forward unwanted messages to the configured Telegram chat.

Mitigation: Bind locally or place the service behind a protected reverse proxy with access controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shinzzyak/skills/signallink)
- [SignalLink homepage](https://github.com/Shinzzyak/SignalLink)
- [Telegram BotFather](https://t.me/BotFather)
- [Telegram userinfobot](https://t.me/userinfobot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Telegram bot and chat configuration; optional webhook secret is recommended before exposure beyond localhost.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter and changelog state 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
