## Description: <br>
Telegram Alert helps agents configure and operate multi-channel trading alerts with Telegram group delivery, compound trigger conditions, rich-media messages, scheduled reports, and team notification workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Trading teams and developers use this skill to send market signals, scheduled summaries, and priority alerts across Telegram and optional enterprise channels. It is best suited for notification workflows that require configured chat IDs, credentials, templates, routing, and alert history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad read, write, and execution authority could let the agent perform actions beyond routine notification setup. <br>
Mitigation: Limit the skill to trusted workspaces, review any generated command or script path before execution, and require explicit approval for commands that touch local files or external services. <br>
Risk: Misconfigured chat IDs, webhooks, or credentials could send sensitive alerts to the wrong audience or expose notification secrets. <br>
Mitigation: Verify all channel identifiers and credential sources before use, keep tokens in environment variables or protected local configuration, and avoid sending secrets in alert content. <br>
Risk: Alert history and rich notification content may contain sensitive trading or operational information. <br>
Mitigation: Set a retention policy appropriate for the team, restrict access to history storage, and review message templates before enabling automated or scheduled broadcasts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/telegram-alert) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, YAML configuration snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe message content, channel configuration, trigger rules, schedule settings, delivery status, and alert history handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
