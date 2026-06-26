## Description: <br>
Wecom Deep Op gives agents a unified OpenClaw interface for WeCom documents, schedules, meetings, todos, and contacts through the WeCom OpenClaw plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Bingbox](https://clawhub.ai/user/Bingbox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, operators, and developers use this skill to let an agent create, read, update, cancel, and delete WeCom work items across documents, calendars, meetings, todos, and visible contacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify or delete real WeCom documents, schedules, meetings, todos, and contact-related records through a bot credential. <br>
Mitigation: Require human confirmation before edit, cancel, delete, or bulk contact actions, and use a dedicated bot with least-privilege MCP permissions. <br>
Risk: uaKey values grant access to enterprise WeCom MCP endpoints if exposed. <br>
Mitigation: Keep uaKey values out of source control, logs, screenshots, and shell history; store them only in protected environment variables or local configuration. <br>
Risk: Misconfigured WECOM_*_BASE_URL values can send enterprise data to an unintended endpoint. <br>
Mitigation: Verify every configured base URL points to the intended WeCom endpoint before enabling the skill. <br>
Risk: Contact operations may expose more people data than intended if the bot has broad visibility. <br>
Mitigation: Restrict the bot's contact visibility in the WeCom admin console before use. <br>


## Reference(s): <br>
- [Wecom Deep Op on ClawHub](https://clawhub.ai/Bingbox/wecom-deep-op) <br>
- [Bingbox publisher profile](https://clawhub.ai/user/Bingbox) <br>
- [WeCom admin console](https://work.weixin.qq.com/) <br>
- [Tencent WeCom OpenClaw plugin](https://github.com/WecomTeam/wecom-openclaw-plugin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON API results and Markdown or text content, with shell commands and configuration snippets in documentation-oriented flows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return WeCom document content, schedule and meeting records, todo records, contact search results, health-check status, and configuration diagnostics.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence, SKILL.md frontmatter, skill.yml, and changelog released 2026-03-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
