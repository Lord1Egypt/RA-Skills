## Description:

通过关键词、创作者主页和视频链接查询 TikTok 公开视频及评论，并以结构化 JSON 提供选题、竞品和舆情分析依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

创作者、营销团队和研究人员可用它搜索 TikTok 关键词视频、查看创作者公开作品或读取视频评论，再据此整理内容趋势、竞品动态和评论观点。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports medium confidence and partial coverage: 20 of 32 components were fully inspected.

Mitigation: Review the release files and obtain a complete scan before relying on it in a production workflow.

Risk: The security guidance flags possible environment-variable scope and fixed Beijing-time timestamp concerns.

Mitigation: Verify the variables the scripts need, provide credentials through a narrowly scoped environment, and confirm Beijing-time timestamps fit the workflow.

Risk: The skill sends its API token to the Guaikei service to retrieve data.

Mitigation: Use the service only when it is an approved data recipient, and avoid sending sensitive query content.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/why20261/skills/tiktok-yunying-zhushou)
- [Provider and API access](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis, Shell commands]

**Output Format:** [Structured JSON results with optional concise text analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover publicly available TikTok content and depend on the configured API access and plan limits.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
