## Description:

Saves WeChat Official Account articles and image-note pages from mp.weixin.qq.com into a user-specified local folder as Markdown with local assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and content archivists use this skill to save supported WeChat article or image-note URLs, or browser-saved final HTML, as local Markdown with copied images. It is intended for local archiving and verification of article content, not cloud upload, knowledge-base import, or message sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded image URLs can be downloaded into the archive without host, scheme, size, or network-safety limits.

Mitigation: Use the skill only with WeChat URLs and output folders you choose, consider --skip-images for untrusted content, and run it in a sandboxed environment without access to internal networks or sensitive local files.

Risk: Browser-saved HTML from an untrusted source may contain asset references that affect what the downloader fetches.

Mitigation: Review saved HTML before use or disable image downloading for untrusted inputs until asset URL and size limits are added.

## Reference(s):

- [WeChat Article Archive on ClawHub](https://clawhub.ai/harven-droid/skills/wechat-article-archive)
- [Publisher profile: harven-droid](https://clawhub.ai/user/harven-droid)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance]

**Output Format:** [Markdown article file, local asset files, JSON run summary, and concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or reuses the requested destination folder and assets directory; image downloads can be skipped with --skip-images.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
