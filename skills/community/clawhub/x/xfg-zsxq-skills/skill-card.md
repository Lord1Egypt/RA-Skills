## Description: <br>
Automates ZSXQ posting, replies, browsing, notification checks, scheduled checks, and browser-assisted reply workflows using locally stored group configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzhengwei](https://clawhub.ai/user/fuzhengwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators who manage ZSXQ communities use this skill to post content, review activity, reply to topics, and configure recurring notification checks from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles full ZSXQ cookies and access tokens and can use them for authenticated account actions. <br>
Mitigation: Treat cookies and tokens as passwords, avoid pasting them into visible logs, rotate them if exposed, and keep local credential files private. <br>
Risk: Posting, replying, notification checks, and scheduled tasks can create recurring or unintended account activity. <br>
Mitigation: Verify the target group and message content before execution, remove hard-coded defaults, and enable scheduled checks or auto-replies only when recurring actions are intended. <br>
Risk: The server security verdict is suspicious because the skill performs unofficial ZSXQ account automation with weak guardrails. <br>
Mitigation: Install only when the publisher is trusted and this specific account automation behavior is desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fuzhengwei/xfg-zsxq-skills) <br>
- [ZSXQ web app](https://wx.zsxq.com) <br>
- [ZSXQ API reference](references/api.md) <br>
- [Usage guide](references/usage.md) <br>
- [Token configuration](references/token-config.md) <br>
- [Browser automation guide](references/puppeteer.md) <br>
- [Puppeteer documentation](https://pptr.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and JavaScript automation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce authenticated ZSXQ API calls, browser automation steps, local configuration files, and cron setup commands.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
