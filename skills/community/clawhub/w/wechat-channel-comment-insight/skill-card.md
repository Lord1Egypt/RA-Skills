## Description:

采集视频号公开评论并整理带证据的用户需求洞察、选题建议和可导出报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dunkong](https://clawhub.ai/user/dunkong)

### License/Terms of Use:

MIT-0

## Use Case:

内容运营与市场调研人员使用此技能收集视频号公开评论，核查用户反馈并制定选题和回复建议。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running the skill uses a local API key for paid requests to api.we-media.cn.

Mitigation: Keep the key in local environment variables and review the cost estimate and budget before collection.

Risk: Generated workspace reports contain collected public comments.

Mitigation: Store and share reports appropriately; review samples and cited comments before relying on conclusions.

Risk: The package contains an inactive official-account competitor-analysis workflow not described in the main skill text.

Mitigation: Review the additional workflow before using it; restrict execution to the requested comment-analysis workflow.

## Reference(s):

- [ClawHub 技能页面](https://clawhub.ai/dunkong/skills/wechat-channel-comment-insight)
- [采集计划与分析规范](references/workflow.md)
- [曼格云 API 产品文档](https://api.we-media.cn/client/products)

## Skill Output:

**Output Type(s):** [Text, Markdown, Excel files, HTML files, JSON files]

**Output Format:** [Evidence-linked analysis and downloadable Excel, Markdown, HTML, and JSON reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports cite sampled comments; collection is subject to user-approved scope and budget.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
