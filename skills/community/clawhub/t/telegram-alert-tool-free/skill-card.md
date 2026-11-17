## Description: <br>
Helps an agent guide personal traders through sending basic trading alerts to a single Telegram chat or group with simple price thresholds and Markdown-formatted messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and personal trading users can use this skill to configure Telegram bot alerts for trading signals, market reminders, and simple above-or-below price threshold notifications to one target group. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may lead an agent to send messages or alert content to Telegram outside the intended trading-alert scenario. <br>
Mitigation: Use the skill only for trading alerts to an explicitly selected Telegram chat or group, and confirm message content and destination before sending. <br>
Risk: Telegram alert content and local alert history may contain sensitive trading information. <br>
Mitigation: Avoid sending sensitive content unless Telegram delivery and any local history retention are acceptable for the use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/telegram-alert-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash and YAML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Telegram bot setup steps, alert configuration examples, and command snippets for sending or monitoring alerts.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
