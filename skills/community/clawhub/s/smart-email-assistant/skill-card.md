## Description: <br>
Smart Email helps an agent configure and operate an AI-assisted email workflow that retrieves supported IMAP mailboxes, archives messages locally, classifies urgent email, and sends urgent alerts or daily digests to configured delivery channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bu-bu-xxx](https://clawhub.ai/user/bu-bu-xxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Smart Email to set up mailbox monitoring, AI-based urgency analysis, local archiving, scheduled digests, and delivery of urgent email summaries to channels such as Telegram, DingTalk, WeCom, or Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to configured mailboxes. <br>
Mitigation: Install only when the publisher is trusted, and use a dedicated mailbox or app password where possible. <br>
Risk: Email content, attachments, logs, and tracking data may be stored under the Smart Email data directory. <br>
Mitigation: Use an appropriate local storage location and review retention, cleanup, and access controls before enabling routine use. <br>
Risk: Email content or inline images may be sent to the configured AI provider or subagent mode. <br>
Mitigation: Choose trusted AI endpoints and avoid connecting mailboxes that contain content unsuitable for the configured provider. <br>
Risk: Cron jobs can repeatedly fetch, analyze, and dispatch email-derived messages. <br>
Mitigation: Review the scheduled jobs before applying them, test the workflow first, and confirm delivery targets are correct. <br>
Risk: Running from directories with untrusted environment files can expose or alter mailbox, AI provider, and delivery settings. <br>
Mitigation: Run from a trusted workspace and inspect environment configuration before initialization. <br>


## Reference(s): <br>
- [Smart Email ClawHub Listing](https://clawhub.ai/bu-bu-xxx/smart-email-assistant) <br>
- [Smart Email User Guide](references/USER_GUIDE.md) <br>
- [Smart Email Installation Guide](references/INSTALL.md) <br>
- [OpenClaw Platform](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON-style outbox message payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local email archives, logs, a tracking database, and queued outbox messages when installed and executed.] <br>

## Skill Version(s): <br>
2.5.2 (source: release evidence and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
