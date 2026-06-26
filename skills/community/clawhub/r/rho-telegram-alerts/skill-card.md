## Description: <br>
Send formatted trading alerts, portfolio updates, and market signals via Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JamieRossouw](https://clawhub.ai/user/JamieRossouw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and traders use this skill to draft Telegram notifications for trade entries and exits, price thresholds, portfolio summaries, stop-loss warnings, win/loss streaks, and scheduled trading reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and chat IDs can expose notification channels if committed, logged, or shared. <br>
Mitigation: Use a dedicated bot, keep credentials in environment variables or a secrets manager, avoid logging them, and rotate the token if exposure is suspected. <br>
Risk: Trading alerts and portfolio summaries may disclose sensitive trading or portfolio details to the configured Telegram chat. <br>
Mitigation: Verify the chat ID before use and limit alert content to information appropriate for that Telegram recipient. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JamieRossouw/rho-telegram-alerts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text alert content with setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID for Telegram delivery.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
