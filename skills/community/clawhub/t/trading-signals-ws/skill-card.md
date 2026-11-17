## Description:

Real-time crypto trading signal generator using WebSocket price feeds. Connects to Bybit (or any exchange) WebSocket, runs configurable strategies on live candle data, and pushes alerts to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyztj](https://clawhub.ai/user/sunnyztj)

### License/Terms of Use:


## Use Case:

Developers and traders use this skill to set up a WebSocket-based crypto market monitor that evaluates configured strategies and sends Telegram trading alerts with entry, stop-loss, and take-profit levels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment example encourages a root-level auto-start service.

Mitigation: Run the bot as an unprivileged user or user-level service and review the service configuration before enabling auto-start.

Risk: Telegram bot tokens and chat IDs may be exposed through plaintext configuration or logs.

Mitigation: Store credentials in protected environment variables or a secrets manager, restrict file permissions, and protect generated logs.

Risk: The optional hosted Tinyore subscription/API examples send requests to an external service.

Mitigation: Use those API examples only when you intentionally want to share the requested data with that service.

Risk: Trading alerts can be incomplete, stale, or misleading if market data, strategy configuration, or connectivity is unreliable.

Mitigation: Review strategy settings and signal outputs before acting on them, and avoid treating generated alerts as financial advice.

## Reference(s):

- [Telegram Bot Setup](references/telegram_setup.md)
- [Trading Signals Ws Skill Page](https://clawhub.ai/sunnyztj/skills/trading-signals-ws)
- [Publisher Profile](https://clawhub.ai/user/sunnyztj)
- [Tinyore Free Signals API](https://api.tinyore.com/signals/free)
- [Tinyore Subscribe API](https://api.tinyore.com/subscribe)
- [Tinyore Live Signals API](https://api.tinyore.com/signals/live)
- [Tinyore Status API](https://api.tinyore.com/status)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance and runnable bot/configuration files for Telegram-based trading alerts.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
