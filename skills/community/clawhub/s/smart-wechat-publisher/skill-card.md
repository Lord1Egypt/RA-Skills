## Description: <br>
Creates WeChat Official Account draft posts from AI news content with configurable templates and scheduled publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[403914291](https://clawhub.ai/user/403914291) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
WeChat Official Account operators use this skill to prepare AI-news draft posts, apply an HTML template, and schedule draft creation for later review and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires powerful WeChat Official Account credentials and may read AppSecret from local configuration. <br>
Mitigation: Use environment variables or a secret manager for AppSecret, restrict permissions on configuration and memory directories, and rotate any exposed secret. <br>
Risk: Automatic draft workflows can publish inaccurate or unsuitable content if reviewed too late. <br>
Mitigation: Review generated drafts and content quality before enabling scheduled runs or publishing from the WeChat draft box. <br>
Risk: The included script appears to use fixed sample news content rather than collecting live items. <br>
Mitigation: Confirm the content source and update behavior before relying on the skill for current AI news coverage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/403914291/smart-wechat-publisher) <br>
- [WeChat Official Accounts platform](https://mp.weixin.qq.com) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, HTML, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON configuration, HTML article content, and WeChat draft creation results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WeChat Official Account AppID and AppSecret; generated drafts should be reviewed before publication.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
