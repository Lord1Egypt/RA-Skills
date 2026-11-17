## Description:

抓取微信公众号文章并转换为 Markdown，提取正文内容后总结核心观点或输出完整文章。

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongym1234](https://clawhub.ai/user/kongym1234)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve a trusted WeChat Official Account article URL, convert the article body to Markdown, and summarize the core points or return the full article text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fetcher can make under-scoped network requests to arbitrary URLs.

Mitigation: Use only trusted WeChat article URLs and review before installing in environments that can reach private networks or sensitive internal services.

Risk: The --save-images option can download unbounded remote image content.

Mitigation: Avoid --save-images unless local image copies are needed, and review retained Markdown and image files before reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kongym1234/skills/wechat-summarize)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files]

**Output Format:** [Markdown summaries or full Markdown article text, with optional local Markdown and image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated Markdown files are deleted after summarization unless the user explicitly asks to keep them; --save-images can create local image files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
