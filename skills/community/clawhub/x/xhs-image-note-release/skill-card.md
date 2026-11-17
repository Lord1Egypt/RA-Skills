## Description:

通过已登录的浏览器自动发布或暂存小红书图文与视频笔记，并可生成多种样式的卡片图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT

## Use Case:

面向小红书内容创作者，用于生成样式卡片并通过已登录的浏览器发布图文或视频笔记、保存草稿，或准备页面供人工检查。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the release suspicious, citing sandbox-isolation and browser-rendering risks; its analysis is incomplete.

Mitigation: Review the incomplete script analysis and install only if you accept the reported risks, as the scanner guidance advises.

Risk: Publish mode submits content through the user's logged-in XiaoHongShu account.

Mitigation: Use stage or draft mode to review the content in the platform before publishing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/songhonglei/skills/xhs-image-note-release)
- [Card generator usage](references/card-generator-usage.md)
- [Photo background cards](references/photo-background.md)
- [Error handling](references/error-handling.md)

## Skill Output:

**Output Type(s):** [Images, Browser actions, Shell commands, Guidance]

**Output Format:** [PNG card images, browser-driven publishing or draft staging, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Card images use configurable themes and layouts; note publishing supports image or video inputs.]

## Skill Version(s):

2.0.7 (source: frontmatter; server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
