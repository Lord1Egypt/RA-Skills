## Description:

为微信公众号制作并发布整篇 SVG 互动图文，支持视差滑动、滑动上色、计分答题、选择展开和场景转场。

This skill is ready for commercial/non-commercial use.

## Publisher:

[weipaiban](https://clawhub.ai/user/weipaiban)

### License/Terms of Use:

MIT-0

## Use Case:

公众号内容创作者和编辑可用它把主题或稿件制作成完整的互动 SVG 图文，并发布到微排版预览。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated API requests may expose the API key if a request is redirected.

Mitigation: Use the official HTTPS weipaiban.cn service endpoint and avoid intermediary or redirecting endpoints for authenticated requests.

Risk: User-provided images may be sent to external hosting when uploaded.

Mitigation: Upload only images the user has approved for transfer to the service.

Risk: Broad trigger wording may activate the skill for loosely related requests.

Mitigation: Use the skill when the request is specifically about creating or publishing interactive SVG content for WeChat.

## Reference(s):

- [微排版技能详情](https://clawhub.ai/weipaiban/skills/weipaiban)
- [微排版服务](https://weipaiban.cn)
- [API 密钥设置](https://weipaiban.cn/settings/api-keys)

## Skill Output:

**Output Type(s):** [HTML/SVG code, Interactive article, Published preview link]

**Output Format:** [Complete interactive HTML/SVG article with text and image assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Publishes the finished article to a microtypesetting preview.]

## Skill Version(s):

2.0.2 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
