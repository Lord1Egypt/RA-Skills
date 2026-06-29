## Description: <br>
Generate topic briefings from Telegram channels and compile channel messages into structured summaries for Telegram or Gmail delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[telyclaw](https://clawhub.ai/user/telyclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to collect Telegram channel messages over a chosen time range, generate Markdown briefings, and optionally deliver them through Telegram or Gmail. It supports recurring briefing workflows when scheduling tools are available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access sensitive Telegram channels and Gmail accounts through OAuth, browser sessions, MCP servers, or platform tools. <br>
Mitigation: Install only when that access is acceptable, use the narrowest available integration, and complete authorization intentionally. <br>
Risk: Briefings can be sent to Telegram or Gmail recipients, creating accidental disclosure risk if recipients are wrong. <br>
Mitigation: Preview the generated briefing and review recipients before any send. <br>
Risk: Scheduled briefings may repeatedly generate and deliver summaries without fresh review. <br>
Mitigation: Use scheduling only for briefing configurations and recipients approved for repeated delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/telyclaw/tg-message-assistant) <br>
- [TelyClaw skill homepage](https://github.com/TelyAgent/telyclaw-skills) <br>
- [TelyClaw Gmail plugin](https://github.com/TelyAgent/telyclaw-plugin-gmail) <br>
- [Multi-platform research](artifact/references/multi-platform-research.md) <br>
- [Telegram Web](https://web.telegram.org/) <br>
- [Telegram API credentials](https://my.telegram.org/apps) <br>
- [BotFather](https://t.me/BotFather) <br>
- [Gmail Web](https://mail.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings, delivery guidance, configuration snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May split Telegram delivery into 4096-character message segments; email delivery requires user review and confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
