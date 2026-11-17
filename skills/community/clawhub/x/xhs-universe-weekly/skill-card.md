## Description:

生成小红书人群宇宙投放追踪周报，拉取 RedBI 数据，对比人群宇宙与整体种草效果，分层客户优先级，并输出 HTML 周报和 Redoc 在线文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[peike-boop](https://clawhub.ai/user/peike-boop)

### License/Terms of Use:

MIT-0

## Use Case:

Internal marketing, operations, and commercial users use this skill to generate weekly audience-campaign performance reports for a selected industry and time period. The skill supports data retrieval, CSV analysis, customer priority segmentation, visual report generation, and Redoc publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable SSO cookies and internal RedBI report data.

Mitigation: Install only in a trusted internal environment, require explicit confirmation before SSO use, avoid raw reusable cookies, and serve previews through authenticated HTTPS or loopback-only access.

Risk: Downloaded CSV files and cover-image URLs may expose sensitive data or retrieve unintended content.

Mitigation: Validate download and image URLs against trusted RedBI and Xiaohongshu domains, check response type and size before saving or embedding, and retain generated files only where internal data handling is approved.

Risk: Published Redoc reports can expose campaign, client, and performance data beyond the intended audience.

Mitigation: Confirm publication scope, recipient access, and document permissions before creating or updating Redoc pages.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/peike-boop/skills/xhs-universe-weekly)
- [RedBI Dashboard Reference](artifact/references/dashboard.md)
- [HTML Generation Rules](artifact/references/html-rules.md)
- [RedBI Dashboard](https://redbi.devops.xiaohongshu.com/dashboard/list?dashboardId=45500&pageId=page_pWvbwhxFPz&projectId=4)
- [Skill Usage Guide](https://docs.xiaohongshu.com/doc/86833739ca1981f4212f3c1adcc87d33)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands, generated HTML report files, Redoc documents, JSON analysis, and CSV-derived tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local preview links and Redoc links; embeds report cover images as base64 when available.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
