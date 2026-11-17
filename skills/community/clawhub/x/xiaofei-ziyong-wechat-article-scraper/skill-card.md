## Description:

Scrapes public WeChat Official Account articles from mp.weixin.qq.com, extracts ordered text, image, and GIF/video-preview blocks, downloads images, and prepares content for Feishu knowledge-base import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengzi53](https://clawhub.ai/user/mengzi53)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operations users use this skill to capture public WeChat article text and media into local outputs that can be imported into Feishu knowledge-base documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch unsandboxed Chrome against weakly validated URLs.

Mitigation: Run only in a constrained environment, use trusted WeChat article URLs, and add strict HTTPS hostname and redirect allowlists before broader use.

Risk: The skill can download article images without strong size or count limits and write them to a cache directory.

Mitigation: Use a disposable cache directory, avoid important existing paths for --cache-dir, and cap image downloads before deployment.

Risk: Feishu media insertion appends images to the end of the document rather than placing them inline.

Mitigation: Review generated Feishu documents and manually move images into the intended positions after import.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengzi53/skills/xiaofei-ziyong-wechat-article-scraper)
- [WeChat Official Accounts article domain](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts can emit JSON, Markdown article content, and local image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and Google Chrome; image imports to Feishu may require manual repositioning after append-only media insertion.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
