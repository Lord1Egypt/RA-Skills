## Description: <br>
社交媒体自动化运营助手。自动生成并发布小红书、微博、Twitter 内容，定时发送、互动回复。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anson125chen](https://clawhub.ai/user/anson125chen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to generate, schedule, list, and run posts for Twitter/X, Xiaohongshu, and Weibo, with optional comment auto-reply workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect public social media accounts through real posts, scheduled posts, and auto-replies. <br>
Mitigation: Require manual confirmation before any post, scheduled post, or auto-reply is sent. <br>
Risk: The skill asks users to configure sensitive platform credentials, including API secrets, access tokens, and cookies. <br>
Mitigation: Use scoped, revocable credentials; avoid cookie-based authentication where possible; and protect local configuration files. <br>
Risk: Cron configuration can create recurring automation that runs without an interactive user present. <br>
Mitigation: Do not install the cron job unless recurring automation is intended, and review scheduled tasks before enabling automated runs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/anson125chen/socialpost-auto) <br>
- [Publisher profile](https://clawhub.ai/user/anson125chen) <br>
- [Project website](https://asmartglobal.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create local scheduled-task records and execute posting commands when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
