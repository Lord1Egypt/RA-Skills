## Description: <br>
微信公众号文章发布工具 v1.0。基于官方 API，支持智能配图、模板渲染、草稿/发布双模式。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucesongs](https://clawhub.ai/user/brucesongs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, WeChat official account operators, and developers use this skill to prepare Markdown-based articles, generate or select supporting images, create WeChat drafts, and optionally publish to a configured public account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect a live WeChat public account by creating drafts or publishing content. <br>
Mitigation: Test with a dedicated WeChat account first and use draft mode until a human verifies the account, content, images, and audience. <br>
Risk: Credential handling guidance may be unsafe if secrets are stored in config.yaml or committed to version control. <br>
Mitigation: Keep config.yaml out of version control and use environment variables or a secret store for AppSecret and image-provider API keys. <br>
Risk: Browser automation in publish.js is under-disclosed and may operate an administrative WeChat session. <br>
Mitigation: Avoid publish.js unless browser-based admin automation is intentional and has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucesongs/wechat-mp-publish-skill) <br>
- [Publisher profile](https://clawhub.ai/user/brucesongs) <br>
- [WeChat image upload API](https://api.weixin.qq.com/cgi-bin/media/uploadimg) <br>
- [WeChat draft API](https://api.weixin.qq.com/cgi-bin/draft/add) <br>
- [WeChat mass send API](https://api.weixin.qq.com/cgi-bin/message/mass/sendall) <br>
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com/) <br>
- [Unsplash Developers](https://unsplash.com/developers) <br>
- [DashScope Console](https://dashscope.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown, HTML article content, shell commands, Python snippets, configuration values, and WeChat API side effects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create WeChat drafts or publish to a configured account and can generate or upload article images.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and VERSION.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
