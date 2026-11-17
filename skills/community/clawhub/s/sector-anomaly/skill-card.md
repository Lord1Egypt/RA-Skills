## Description:

分析A股板块异动（放量、资金流入、涨停潮、个股联动），输出板块异动评分、强势/出货判断和操作建议，并可接入本地 SQLite 行情库和 stock-pool-v2.json 板块映射。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

External analysts, developers, and agent users can use this skill to run local A-share sector anomaly analysis for research, review, and personal trading-system optimization. It summarizes sector momentum, capital-flow signals, limit-up activity, leadership stocks, and cautionary interpretations without providing investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outputs may be mistaken for investment advice.

Mitigation: Keep the included disclaimer with any shared report and treat the analysis as research that requires independent judgment.

Risk: The skill reads local market-data files that may contain sensitive or unintended project data.

Mitigation: Install and run it only in projects where the referenced SQLite database and stock-pool mapping are intended for analysis, and do not package personal holdings or sensitive databases with the skill.

Risk: Optional refresh commands may update local market data or call network-backed project tooling.

Mitigation: Run refresh commands deliberately and review the surrounding project tooling before use.

## Reference(s):

- [板块异动指标体系](artifact/references/indicators.md)
- [ClawHub skill page](https://clawhub.ai/wwumit/skills/sector-anomaly)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with ranking tables, sector details, bullet-point judgments, command examples, and disclaimer text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an intended local stock_analyzer.db SQLite database and stock-pool-v2.json sector mapping; analysis can be filtered by date, minimum sector members, and top-N result count.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
