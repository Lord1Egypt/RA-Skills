## Description:

面向 A股、港股、美股和 ETF 的中文股票分析技能，要求基于已核实市场数据、研报和新闻输出数据校验、综合结论和操作建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lin838465-ux](https://clawhub.ai/user/lin838465-ux)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents use this skill to analyze named stocks and ETFs across China A-share, Hong Kong, U.S., and ETF markets. It produces source-labeled market checks, ratings, and buy/sell/hold-style guidance for informational review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically read files under ~/Desktop/股票知识库/, which can expose unrelated or sensitive local content.

Mitigation: Keep sensitive or unrelated files out of that folder and review the skill's local-file behavior before enabling it.

Risk: The skill produces decisive buy/sell-style recommendations that may be affected by incomplete, stale, or unavailable market data.

Mitigation: Verify market data and cited sources independently, and treat outputs as informational rather than investment advice.

Risk: The security summary flags limited user control and data-integrity safeguards.

Mitigation: Use the skill only when those tradeoffs are acceptable, and review generated conclusions before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lin838465-ux/skills/stock-analysis-cn-full)
- [ClawHub publisher profile](https://clawhub.ai/user/lin838465-ux)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Chinese Markdown with a data validation checklist, source-labeled analysis, conclusion box, operation guidance, and disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cited market data, research-report references, news references, and Python data-access snippets; no fixed token cap specified.]

## Skill Version(s):

4.0.0 (source: server release metadata; artifact config files list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
