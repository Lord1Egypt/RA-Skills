## Description:

股票综合分析，融合基本面分析、技术分析、量化与行为金融分析三大体系，为投资者提供多维度的选股和择时建议。当用户询问某只股票（给出股票代码或名称）、市场整体情况、个股看法、能否买入/卖出、选股建议时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chris3cano-ship-it](https://clawhub.ai/user/chris3cano-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and market researchers use this skill to request structured stock or market analysis covering fundamentals, technical indicators, quantitative signals, market sentiment, and risk reminders. It is intended to produce decision-support analysis, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to automatically create local HTML/PDF reports and start a Python HTTP server after each analysis.

Mitigation: Require explicit user consent before file writes, browser actions, or local server startup; constrain output directories and shut down any server after use.

Risk: Stock analysis can be mistaken for financial advice or can rely on stale or incomplete market data.

Mitigation: Present the output as decision-support analysis only, cite current data sources when used, state missing data clearly, and preserve the investment-risk disclaimer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chris3cano-ship-it/skills/stock-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, files]

**Output Format:** [Markdown stock analysis report, with possible HTML/PDF file generation behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a risk disclaimer and may attempt local report generation after each analysis.]

## Skill Version(s):

1.0.0 (source: target metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
