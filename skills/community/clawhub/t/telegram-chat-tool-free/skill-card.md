## Description: <br>
电报聊天工具免费版 helps personal users and small teams configure Telegram bots for group messaging, @mentions, cross-bot chat, and basic message tracing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, personal users, and small teams use this skill to set up a Telegram bot, configure allowed chats, test group message handling, and coordinate lightweight notifications through bot mentions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens grant messaging access if exposed. <br>
Mitigation: Keep the bot token private, rotate it through BotFather if leaked, and store it only in the intended configuration. <br>
Risk: Bots with group privacy disabled can read ordinary group messages. <br>
Mitigation: Disable privacy mode only for groups where members understand the bot can read messages, and restrict allowed_chats to intended groups. <br>
Risk: The skill may be misapplied to unrelated messaging channels or bulk-notification workflows. <br>
Mitigation: Use it only for Telegram bot administration and group chat workflows, and do not route unrelated email or SMS tasks through it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/telegram-chat-tool-free) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with YAML, text, shell command, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Telegram bot configuration snippets, allowed chat lists, message test steps, and result/status JSON examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
