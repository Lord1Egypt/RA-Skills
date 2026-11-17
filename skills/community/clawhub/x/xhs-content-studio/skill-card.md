## Description:

小红书博主运营助手，集成 AI 生图智能路由、爆款文案创作及草稿自动发布功能，支持未登录二维码扫码登录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shichao666](https://clawhub.ai/user/shichao666)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, Xiaohongshu bloggers, and social commerce operators use this skill to generate post imagery, draft Xiaohongshu-style titles and copy, and automate draft uploads for review or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Xiaohongshu creator session through a local OpenClaw browser and may handle MiniMax API configuration, generated images, temporary screenshots, and draft content.

Mitigation: Install only when comfortable with authenticated browser automation, keep MiniMax configuration pointed at the official API, avoid untrusted config or content files, review drafts before publishing, and clear generated images or temporary screenshots if they contain sensitive material.

## Reference(s):

- [小红书内容创作助手 README](README.md)
- [热门话题标签库](references/Hashtags.md)
- [小红书内容模板库](references/content-templates.md)
- [爆款标题公式](references/title-formulas.md)
- [MiniMax Platform](https://platform.minimaxi.com/)
- [Xiaohongshu Creator Platform](https://creator.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command examples, generated image files, and Xiaohongshu draft content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create image files under generated_images and use local browser automation to upload draft content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
