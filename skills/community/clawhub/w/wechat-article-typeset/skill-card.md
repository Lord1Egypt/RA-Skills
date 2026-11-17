## Description:

公众号文章预设主题排版--Markdown 一键渲染主题并生成复制页预览链接（不含 AI 结构化预览）

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiker1996](https://clawhub.ai/user/shiker1996)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operators use this skill to convert a Markdown article into preset-themed WeChat-ready HTML and a copy-page preview link. It is intended for preset theme rendering, not AI rewriting or custom structured HTML design.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full rendered article HTML is uploaded to edit.shiker.tech to create the copy-page preview.

Mitigation: Do not use this skill on confidential drafts unless the user accepts that upload.

Risk: Generated HTML may include undisclosed branded mini-program content.

Mitigation: Inspect article.preset.html and the preview page before publication, and remove or disclose promotional content as appropriate.

Risk: Unsafe link or image URI schemes from untrusted Markdown may pass through into generated HTML.

Mitigation: Use trusted Markdown sources and inspect generated links and images before copying the article into WeChat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiker1996/skills/wechat-article-typeset)
- [Publisher profile](https://clawhub.ai/user/shiker1996)
- [Skill instructions](artifact/SKILL.md)
- [Skill README](artifact/README.md)
- [Copy preview API](https://edit.shiker.tech/api/copy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, a preview URL, generated HTML, and a text file containing the preview URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces article.preset.html and wechat-preview-url.txt in the Markdown file directory when the copy script succeeds.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
