## Description:

检索 TikTok 公开的关键词搜索结果、博主作品和视频评论，并返回结构化数据，供需求挖掘、竞品研究和评论分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

面向 TikTok 创作者、跨境营销人员和产品研究团队，检索公开视频、博主作品及视频评论，并据此整理内容趋势、用户痛点与需求机会。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rated the skill benign but fully inspected only 21 of 33 components, leaving some uncertainty about its purpose and environment use.

Mitigation: Review the skill's GUAIKEI_API_TOKEN use before installation and keep the token private in the runtime environment.

## Reference(s):

- [GUAIKEI service and token access](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/tiktok-demand-mining)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON envelope with status, request, metadata, and TikTok video, creator, or comment records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields and record counts depend on available public data and the service plan; zero or empty fields may be omitted.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
