## Description: <br>
Telegram Notify helps agents send Telegram direct message alerts for trade entry, exit, and self-heal events with rate limiting and customizable templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[motivationationdaily](https://clawhub.ai/user/motivationationdaily) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading automation operators use this skill to add consistent Telegram DM notifications for trade lifecycle events and self-heal or restart alerts while limiting alert spam. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot details and trading-event information may leave the local environment through Telegram notifications. <br>
Mitigation: Keep the bot token scoped to this use, use a private chat or channel, and avoid including secrets, account balances, or order details unless that disclosure is intended. <br>
Risk: High-frequency trading events could create notification spam. <br>
Mitigation: Use the skill's cooldown or rate limiting behavior for noisy event streams. <br>


## Reference(s): <br>
- [Telegram Notify on ClawHub](https://clawhub.ai/motivationationdaily/telegram-notify) <br>
- [motivationationdaily publisher profile](https://clawhub.ai/user/motivationationdaily) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and Telegram alert templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [DM-only notification posture unless explicitly configured otherwise; optional cooldown or rate limiting to reduce spam.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
