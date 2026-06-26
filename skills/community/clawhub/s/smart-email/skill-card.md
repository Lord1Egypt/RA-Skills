## Description: <br>
Email assistant skill — check emails, AI summaries, daily digests. Supports Gmail, Outlook/M365, Google Workspace. Users interact through their chat platform (Telegram, Feishu, WhatsApp, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jundongGit](https://clawhub.ai/user/jundongGit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external users use this skill to check configured mailboxes, read messages, and receive AI-generated email summaries or daily digests from chat platforms. Developers and operators can also use its CLI and optional web UI to configure accounts, credentials, and provider settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mailbox contents may be sent to the configured AI provider for summaries and digests. <br>
Mitigation: Use only with mailboxes whose contents may be shared with that provider, and disclose this processing before enabling summaries. <br>
Risk: Credentials and tokens appear to be stored without real encryption. <br>
Mitigation: Prefer OAuth over app passwords, protect or delete the skill data directory when no longer needed, and avoid sharing the web UI token URL. <br>
Risk: Secrets can be exposed through chat or shell command history during setup. <br>
Mitigation: Avoid putting API keys, app passwords, or OAuth tokens in chat messages or shell command arguments when configuring the skill. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jundongGit/smart-email) <br>
- [Skill Homepage](https://clawhub.ai/skills/smart-email) <br>
- [Publisher Profile](https://clawhub.ai/user/jundongGit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON from CLI commands, with user-facing chat or Markdown summaries and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include email metadata, message previews, full message text, AI summaries, account lists, setup URLs, and configuration status.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
