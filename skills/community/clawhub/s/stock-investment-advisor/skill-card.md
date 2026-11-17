## Description:

提供沪深北港美股实时行情、多源信息搜索、图表解读和多角色投资分析，并生成专业投资报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gouyujun](https://clawhub.ai/user/gouyujun)

### License/Terms of Use:

MIT-0

## Use Case:

External investors, analysts, and agent users use this skill to gather current market data, compare securities, interpret stock charts, and draft structured stock analysis reports with risks and disclaimers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive stock names, screenshots, holdings details, or generated analysis may be sent to external data providers or Feishu cloud documents.

Mitigation: Ask the agent to confirm before creating any Feishu document, avoid entering account credentials or private portfolio details unless needed, and prefer pinned or already-installed ClawHub tooling over the unpinned npx command.

Risk: Market data, news, and generated investment analysis may be incomplete, stale, or mistaken.

Mitigation: Verify key claims against current primary market sources, keep the report disclaimer, and treat generated analysis as informational rather than personalized financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gouyujun/skills/stock-investment-advisor)
- [Publisher profile](https://clawhub.ai/user/gouyujun)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries and investment-report content, with optional Feishu cloud document output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sourced market data, chart analysis, risk notes, and disclaimers; Feishu document creation should be confirmed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
