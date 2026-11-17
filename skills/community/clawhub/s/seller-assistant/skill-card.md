## Description:

帮助 Amazon 卖家采集和分析商品评论，形成消费者洞察、经营诊断和监控报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[funewa](https://clawhub.ai/user/funewa)

### License/Terms of Use:

MIT-0

## Use Case:

External Amazon sellers use this skill to collect and analyze product reviews, generate voice-of-customer reports, diagnose product performance, and monitor review trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands presented as previews may spend credits, and recurring-cost approval behavior is inconsistent.

Mitigation: Before report generation, require confirmation for every payment, disable and verify autoconfirm, quote costs, use manual collection for one-time jobs, and approve recurring costs separately. Do not assume omitting --confirm prevents spending; use a release that resolves the approval inconsistency.

## Reference(s):

- [ARI CLI 与 API 参考](artifact/references/reference.md)
- [ARI 使用指南](artifact/使用说明.md)
- [ARI 监控中心](https://ari.funewa.com/zh/monitor)
- [ARI 报告中心](https://ari.funewa.com/zh/reports)

## Skill Output:

**Output Type(s):** [Text, Markdown reports, CSV files, HTML reports]

**Output Format:** [Conversational analysis and Markdown reports, with optional CSV or HTML exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings depend on the selected Amazon product and marketplace, available review data, and account access.]

## Skill Version(s):

1.5.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
