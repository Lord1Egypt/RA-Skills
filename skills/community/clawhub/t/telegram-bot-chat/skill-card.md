## Description: <br>
Guides agents in coordinating multiple Telegram bots in group chats by using the correct sessionKey format, message parameters, and bot account configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1227cwx](https://clawhub.ai/user/1227cwx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up multi-agent coordination among Telegram bots in group chats. It provides deployment notes, sessionKey patterns, message tool examples, and configuration checks for bot-to-bot communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The deployment loop can copy every installed skill into every bot workspace, which may spread unwanted agent behavior beyond the intended Telegram bot chat skill. <br>
Mitigation: Review deployment commands before use and copy only telegram-bot-chat into explicitly selected bot workspaces. <br>
Risk: Telegram bot tokens and group messages may expose sensitive access or coordination data if broad permissions or secrets are used. <br>
Mitigation: Use dedicated Telegram bot tokens with minimal group permissions and avoid sending secrets through inter-agent messages or Telegram group chats. <br>


## Reference(s): <br>
- [Telegram](https://telegram.org) <br>
- [ClawHub skill page](https://clawhub.ai/1227cwx/telegram-bot-chat) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands and JavaScript-style tool call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes sessionKey patterns, Telegram bot account configuration checks, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
