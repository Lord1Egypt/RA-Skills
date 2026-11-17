## Description:

微信公众号文章发布工具 v1.0。基于官方 API，支持智能配图、模板渲染、草稿/发布双模式。当用户说"发公众号"、"发布微信公众号"时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucesongs](https://clawhub.ai/user/brucesongs)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, and operators use this skill to prepare Markdown-based WeChat Official Account articles, generate or attach images, render templates, and save drafts or publish through the official API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires WeChat publishing credentials and optional image-provider API keys.

Mitigation: Use a credential manager or environment-managed secrets, avoid committing local configuration, and grant only credentials acceptable for this publishing workflow.

Risk: Bundled tests and helper scripts may perform live account-changing actions unexpectedly.

Mitigation: Remove or quarantine live tests before installation, do not run pytest with production credentials, and validate first with a test WeChat account.

Risk: Browser automation and image-processing behavior may add operational and dependency risk.

Mitigation: Disable or document browser automation before deployment and upgrade the image-processing dependency before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brucesongs/skills/wechat-mp-publish-skill)
- [WeChat Official Account Platform](https://mp.weixin.qq.com/)
- [WeChat upload image API](https://api.weixin.qq.com/cgi-bin/media/uploadimg)
- [WeChat add draft API](https://api.weixin.qq.com/cgi-bin/draft/add)
- [WeChat mass publish API](https://api.weixin.qq.com/cgi-bin/message/mass/sendall)
- [Unsplash Developers](https://unsplash.com/developers)
- [Alibaba Cloud DashScope Console](https://dashscope.console.aliyun.com/)
- [User Guide](artifact/USER_GUIDE.md)
- [Version History](artifact/VERSION.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, API Calls, Files]

**Output Format:** [Markdown guidance with inline shell commands, Python usage snippets, configuration examples, rendered HTML, and generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WeChat publishing credentials and optional image-provider API keys.]

## Skill Version(s):

1.0.2 (source: release evidence and VERSION.md, released 2026-03-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
