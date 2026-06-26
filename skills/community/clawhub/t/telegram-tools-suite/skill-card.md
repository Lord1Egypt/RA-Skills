## Description: <br>
Telegram Tools Suite helps agents configure and run Telegram automation workflows for group monitoring, group search, batch joining, scheduled sending, account inspection, member export, and message-history export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[testman2025](https://clawhub.ai/user/testman2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up Telegram API credentials, configure local task files, and run CLI commands for group monitoring, group discovery, scheduled messaging, batch joining, and data export. It is intended for lawful Telegram group automation where the user controls the account, targets, and message content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Telegram account and creates local session files containing authentication state. <br>
Mitigation: Install only from a trusted publisher, prefer a test account, and keep .env plus userdata/*.session files private. <br>
Risk: Batch joining and scheduled sending can trigger platform enforcement or abuse concerns if configured carelessly. <br>
Mitigation: Keep high-risk operations disabled until intentionally needed, review join and send-schedule configuration files before running them, and follow Telegram terms and local laws. <br>
Risk: Member lists, message history, and generated Excel or JSON reports can contain sensitive group data. <br>
Mitigation: Store exported files locally with appropriate access controls and avoid sharing reports unless the recipients are authorized. <br>
Risk: Long-running monitor, search, join, and send-schedule tasks can leave stale processes or session-lock issues after abnormal exits. <br>
Mitigation: Track running processes, stop stale Python tasks before retrying, and rely on the documented temporary-session cleanup behavior where applicable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/testman2025/telegram-tools-suite) <br>
- [Publisher profile](https://clawhub.ai/user/testman2025) <br>
- [Telegram API development tools](https://my.telegram.org) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown-style operational guidance with inline shell commands; runtime commands can emit console text and local Excel, JSON, or session-related files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local environment variables and user-created configuration files; scheduled behavior is documented in Beijing Time (UTC+8).] <br>

## Skill Version(s): <br>
1.3.3 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
