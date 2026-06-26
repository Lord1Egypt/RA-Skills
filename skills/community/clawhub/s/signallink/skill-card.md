## Description: <br>
Forward trading alerts and webhook events from TradingView to Telegram instantly. No subscriptions, no middlemen. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shinzzyak](https://clawhub.ai/user/Shinzzyak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers, traders, and operations teams use Signallink to self-host a webhook receiver that formats TradingView or generic alert payloads and forwards them to a configured Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says one reachable endpoint can allow arbitrary messages to be sent to the configured Telegram chat. <br>
Mitigation: Set WEBHOOK_SECRET, patch or disable /webhook/raw until it requires the same secret, and expose the service only behind HTTPS and network restrictions. <br>
Risk: Webhook payloads may contain secrets, personal data, or sensitive trading or incident details that are forwarded to Telegram and may appear in server logs. <br>
Mitigation: Use a dedicated Telegram bot, store the bot token in a local secret mechanism, and avoid sending sensitive data in webhook payloads. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Shinzzyak/signallink) <br>
- [SignalLink Homepage](https://github.com/Shinzzyak/SignalLink) <br>
- [README](artifact/README.md) <br>
- [Skill Instructions](artifact/SKILL.md) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON payload examples, and environment configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup of a FastAPI webhook service that forwards formatted alert messages to Telegram.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
