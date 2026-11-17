## Description:

Helps users lightly polish and prepare WeChat Official Account articles, including title and summary suggestions, cover and illustration generation, article files, and publishing support for mp.weixin.qq.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianshuo](https://clawhub.ai/user/jianshuo)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to turn rough notes, drafts, or speech transcripts into WeChat Official Account article packages while preserving the author's voice. It prepares markdown, HTML, metadata, AI-generated images, and upload or paste guidance for publication workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpublished article text, titles, and generated assets may be sent to external AI and WeChat services.

Mitigation: Redact sensitive drafts before use and confirm that content is appropriate for external processing before image generation or draft upload.

Risk: The workflow depends on an unpinned third-party image-generation wrapper and persistent Codex authentication.

Mitigation: Pin and inspect the gpt-image-2-skill dependency before running it, and review local authentication handling before enabling the image scripts.

Risk: Publishing helpers can upload assets or drafts to a configured WeChat Official Account.

Mitigation: Run upload steps manually, verify the target account configuration, and preview the resulting draft in mp.weixin.qq.com before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jianshuo/skills/wjs-publishing-wechat)
- [Publisher profile](https://clawhub.ai/user/jianshuo)
- [WeChat Official Account platform](https://mp.weixin.qq.com)
- [gpt-image-2-skill dependency](https://github.com/Wangnov/gpt-image-2-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands, article markdown, HTML, JSON metadata, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates article folders containing original.md, article.md, article.html, cover.png, illustration.png, meta.json, and optional draft upload artifacts.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
