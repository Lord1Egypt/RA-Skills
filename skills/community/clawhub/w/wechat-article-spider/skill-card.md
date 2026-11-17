## Description:

微信公众号文章爬虫 - 将微信公号文章转换为 Markdown + 本地图片

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchaoqun](https://clawhub.ai/user/chenchaoqun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to fetch WeChat Official Account article pages, convert extracted article content to Markdown, and save referenced images locally with relative links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs and download unbounded content.

Mitigation: Use only trusted WeChat article URLs, run in a dedicated output directory, and prefer a sandbox or outbound network restrictions until domain validation, private-network blocking, and download size limits are added.

Risk: Downloaded article content and images are written to local disk.

Mitigation: Review the selected output directory before running and avoid paths that contain sensitive or unrelated project files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchaoqun/skills/wechat-article-spider)
- [WeChat Official Accounts article host](https://mp.weixin.qq.com/)

## Skill Output:

**Output Type(s):** [markdown, files, shell commands]

**Output Format:** [Markdown file, local image files, and command-line status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates one Markdown file and an images/ subdirectory in the selected output directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
