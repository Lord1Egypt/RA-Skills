## Description:

一键将 Markdown 或 HTML 文章和封面图上传到微信公众号草稿箱，并生成适合公众号阅读的草稿内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qujingyang28](https://clawhub.ai/user/qujingyang28)

### License/Terms of Use:

MIT-0

## Use Case:

Content publishers and agent operators use this skill to prepare WeChat Official Account drafts from local Markdown or HTML articles, including cover image upload and basic formatting before manual review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles WeChat account secrets and can upload selected article text, title, and cover image to WeChat.

Mitigation: Use protected environment injection or a secret manager for APPSECRET, avoid passing secrets in prompts or shell history, and rotate exposed credentials.

Risk: Draft creation can publish incorrect or unreviewed article content into a WeChat account workflow.

Mitigation: Keep the draft-review step, preview on mobile, and complete the provided pre-publication accuracy checklist before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qujingyang28/skills/wechat-publisher-pro)
- [WeChat Official Accounts Platform](https://mp.weixin.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; runtime actions create WeChat draft API requests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an article path, cover image path, title, and WeChat APPID/APPSECRET supplied through protected configuration.]

## Skill Version(s):

3.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
