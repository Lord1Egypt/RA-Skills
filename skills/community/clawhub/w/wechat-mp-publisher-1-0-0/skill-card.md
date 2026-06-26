## Description: <br>
Publishes articles to WeChat Official Accounts through the WeChat API using configured AppID, AppSecret, IP allowlisting, and access token management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Saaaa1aaaaS](https://clawhub.ai/user/Saaaa1aaaaS) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and content operators use this skill to publish Markdown or text articles to a configured WeChat Official Account, including token retrieval, optional cover upload, draft creation, and publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles real WeChat AppID, AppSecret, and access tokens. <br>
Mitigation: Use a test account first, keep secrets only in a local .env file, and do not share token command output. <br>
Risk: The publish workflow can create and publish content through a live WeChat Official Account. <br>
Mitigation: Require human review before running publish commands on production content or production accounts. <br>
Risk: The security review flags weak safeguards and unsafe credential examples. <br>
Mitigation: Replace all example credentials with local secrets and review the skill carefully before installing it with a real account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Saaaa1aaaaS/wechat-mp-publisher-1-0-0) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JavaScript code, and environment-variable configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May perform live WeChat API calls and can print access tokens when the token command is run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; package.json declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
