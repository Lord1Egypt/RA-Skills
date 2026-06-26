## Description: <br>
Real-time crypto trading signal generator that connects to Bybit WebSocket price feeds, runs configurable strategies on live candle data, and sends alerts to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunnyztj](https://clawhub.ai/user/Sunnyztj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and traders use this skill to run a local market-monitoring bot that watches configured crypto pairs, evaluates technical strategies, and sends Telegram alerts with entry, stop-loss, and take-profit levels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and chat identifiers can be exposed if copied into committed configuration files. <br>
Mitigation: Store credentials as secrets or environment variables, keep config.py out of version control, and rotate any token that may have been exposed. <br>
Risk: The bot can run as a persistent local service that writes logs and state while connecting to external market and messaging APIs. <br>
Mitigation: Run it in a virtual environment under a dedicated non-root user, review systemd settings before enabling persistence, and monitor generated log and state files. <br>
Risk: The optional hosted signal API requires trusting a third-party provider with email and API usage. <br>
Mitigation: Skip the hosted Tinyore API unless that provider is acceptable for the user's data-sharing and operational requirements. <br>
Risk: Trading alerts and backtest claims may be incorrect or unsuitable for a user's financial situation. <br>
Mitigation: Treat alerts as informational, review strategy settings and market assumptions, and avoid automated trading decisions without independent validation. <br>


## Reference(s): <br>
- [Telegram Bot Setup](references/telegram_setup.md) <br>
- [ClawHub skill page](https://clawhub.ai/Sunnyztj/trading-signals-ws) <br>
- [Tinyore free signals API](https://api.tinyore.com/signals/free) <br>
- [Tinyore market status API](https://api.tinyore.com/status) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python configuration and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to edit config.py, run a Python WebSocket bot, and configure Telegram credentials.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
