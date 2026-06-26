## Description: <br>
Use weavmail CLI to manage emails for the current task. Use when you need to read, send, reply to, or move emails as part of completing a task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yankeguo](https://clawhub.ai/user/yankeguo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to configure weavmail accounts, sync inboxes, read local Markdown copies of messages, and prepare explicit user-approved email actions such as sending, replying, archiving, trashing, or moving messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can sync private mailboxes and store email contents locally. <br>
Mitigation: Use only trusted accounts, prefer app-specific revocable credentials, scope syncs with account and limit options where practical, and protect or delete the local mails/ cache after use. <br>
Risk: The skill can send, reply to, archive, trash, or move real emails. <br>
Mitigation: Require explicit user approval before any mail-changing action and review every command before it runs. <br>


## Reference(s): <br>
- [ClawHub weavmail skill page](https://clawhub.ai/yankeguo/weavmail) <br>
- [HEARTBEAT.md](artifact/HEARTBEAT.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown email cache files under mails/ after the weavmail CLI syncs mailboxes.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
