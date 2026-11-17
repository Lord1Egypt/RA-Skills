## Description:

将任意文章 HTML 页面或纯文本，自动切片生成小红书风格图文卡片组（封面 + 内容图 + 金句图），输出单个可直接在浏览器预览的 HTML 文件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangchao228](https://clawhub.ai/user/yangchao228)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and knowledge workers use this skill to convert articles or plain text into Xiaohongshu-style visual card sets for previewing, screenshotting, and publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML may contain errors or unsuitable content for publication.

Mitigation: Review the generated HTML preview before opening broadly, screenshotting, or publishing.

Risk: Input articles may contain sensitive private content.

Mitigation: Avoid feeding sensitive private articles unless that content is necessary for the card-generation task.

Risk: Browser previews may contact Google Fonts.

Mitigation: Replace the Google Fonts link with local fonts when network contact is not acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangchao228/skills/redbook-cards-skill)
- [Publisher profile](https://clawhub.ai/user/yangchao228)
- [Google Fonts stylesheet](https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap)
- [Example](artifact/EXAMPLE.md)
- [Prompt](artifact/PROMPT.md)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Single complete HTML document as a string]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 5 to 7 visual cards with inline CSS and no JavaScript; generated previews may contact Google Fonts unless local fonts are substituted.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
