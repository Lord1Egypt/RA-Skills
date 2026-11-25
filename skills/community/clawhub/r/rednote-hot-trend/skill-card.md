## Description:

搜索和分析小红书公开笔记、评论及创作者数据，支持关键词发现、笔记详情、评论和博主作品查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and operators use the skill to research public Xiaohongshu content, follow competitor posts, review comments, and assess creator activity. It returns structured results that an agent can summarize for topic research and internal analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and note or creator links are sent to the service to retrieve public data.

Mitigation: Use only public links and non-sensitive search terms.

Risk: Results may be saved in the system temporary directory.

Mitigation: Set XHS_GUAIKEI_DISABLE_LOG=1 to disable local result logging, and avoid sensitive queries.

Risk: The security analysis was partial, so some behavior remains unverified.

Mitigation: Review the release before use and keep requests within the documented public-data scope.

## Reference(s):

- [Command options and supported inputs](references/options.md)
- [Troubleshooting](references/troubleshooting.md)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured JSON results with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover public search, note details, comments, or creator activity; responses can be empty or report an error.]

## Skill Version(s):

1.2.0 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
