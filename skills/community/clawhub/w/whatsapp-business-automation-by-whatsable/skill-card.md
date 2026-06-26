## Description: <br>
Full three-phase agent skills suite for Notifyer by WhatsAble covering account setup, WhatsApp automation infrastructure, and live chat operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whatsable](https://clawhub.ai/user/whatsable) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, developers, and operations staff use this skill to let an agent configure a Notifyer workspace, manage WhatsApp Business automation, send broadcasts, operate live conversations, and inspect messaging analytics through scripted workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send customer WhatsApp messages, schedule broadcasts, and change automation settings. <br>
Mitigation: Review proposed message content, recipient lists, broadcast schedules, destructive actions, and team changes before execution. <br>
Risk: The skill requires sensitive credentials and may expose JWTs, Developer API keys, webhook signature secrets, analytics exports, and conversation logs. <br>
Mitigation: Use tokens only from trusted Notifyer workspaces, avoid shared terminals and logs, and treat exported data and secrets as sensitive. <br>
Risk: Security evidence reports documented backend endpoints with weak authorization controls. <br>
Mitigation: Avoid the documented public or weakly authorized raw endpoints until backend authorization issues are fixed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/whatsable/whatsapp-business-automation-by-whatsable) <br>
- [Project homepage](https://github.com/Whatsable/whatsapp-business-agent-skills) <br>
- [Notifyer by WhatsAble](https://notifyer-systems.com) <br>
- [README](artifact/README.md) <br>
- [Setup Notifyer reference](artifact/skills/setup-notifyer/SKILL.md) <br>
- [Automate Notifyer reference](artifact/skills/automate-notifyer/SKILL.md) <br>
- [Chat Notifyer reference](artifact/skills/chat-notifyer/SKILL.md) <br>
- [Account and authentication reference](artifact/skills/setup-notifyer/references/account-reference.md) <br>
- [Developer API key reference](artifact/skills/setup-notifyer/references/api-key-reference.md) <br>
- [Templates reference](artifact/skills/automate-notifyer/references/templates-reference.md) <br>
- [Broadcasts API reference](artifact/skills/automate-notifyer/references/broadcasts-reference.md) <br>
- [Messaging reference](artifact/skills/chat-notifyer/references/messaging-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Node.js script invocations, JSON outputs, and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute API-backed scripts that send WhatsApp messages, manage team and automation settings, read conversation logs, and retrieve sensitive credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
