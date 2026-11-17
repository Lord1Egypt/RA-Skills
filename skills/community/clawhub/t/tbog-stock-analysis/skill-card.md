## Description:

股票深度分析（18维度融合版）：基本面估值+实战交易双重视角，支持A股/港股/美股，输出完整9部分飞书文档报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisxiaoding](https://clawhub.ai/user/dennisxiaoding)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to generate Chinese stock-analysis reports for A-share, Hong Kong, and U.S. equities. It combines valuation, trading posture, shareholder checks, news, financials, technical levels, risk notes, and Feishu document output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial analysis may be inaccurate or mistaken for personalized investment advice.

Mitigation: Treat reports as informational, verify sources independently, and keep explicit non-advice risk disclosures in user-facing output.

Risk: Reports are written to Feishu and may expose investment research if document links are shared too broadly.

Mitigation: Review Feishu document content and access settings before sharing links with users.

Risk: Chinese-language output and visible '田伯光' branding may not fit every workflow or audience.

Mitigation: Use only in workflows that accept Chinese reports and the disclosed branding.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dennisxiaoding/skills/tbog-stock-analysis)
- [18维度分析框架详细说明](references/analysis-framework.md)
- [数据源说明](references/data-sources.md)
- [9部分报告结构详细规范](references/report-structure.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Chinese Markdown report, concise text conclusion, and Feishu document link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires source attribution, data-completeness checks, explicit risk disclosure, and Feishu document validation before sharing.]

## Skill Version(s):

1.2.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
