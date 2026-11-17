## Description:

按关键词、TikTok账号或视频链接查询公开视频、账号作品和评论，并将结果整理为结构化 JSON，供后续分析使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

TikTok创作者、营销团队和研究人员可用它检索公开视频、账号作品和视频评论，再进行选题调研、竞品跟踪或评论分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release description suggests batch video downloads, while the skill documentation says it retrieves public data and does not download video files; the security review also notes that script inspection was partial.

Mitigation: Confirm the documented search, creator-post, and comment capabilities meet the task before relying on the download wording.

Risk: Search terms or TikTok links and the API token are sent to the third-party data service to retrieve results.

Mitigation: Use only public TikTok material, avoid sending sensitive query text, and confirm the service's data handling is acceptable before configuring a token.

## Reference(s):

- [参数与命令说明](artifact/references/options.md)
- [版本更新记录](artifact/references/changelog.md)
- [数据服务与支持](https://www.guaikei.com)
- [ClawHub 技能发布页](https://clawhub.ai/why20261/skills/tiktok-batch-downloader)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results, with natural-language summaries or analysis when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public video, creator, and comment data; it does not download video files. Requires a GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
