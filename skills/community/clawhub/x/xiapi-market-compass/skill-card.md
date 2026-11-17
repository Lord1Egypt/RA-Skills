## Description:

虾皮股市罗盘 analyzes Chinese A-share market structure across trend, valuation, and sentiment indicators to produce a market-state assessment and position-management guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to turn daxiapi market compass data into a Chinese A-share market structure report. It helps assess whether the current market environment supports holding equities, identify trend repair or deterioration signals, and frame position-management guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to run an unpinned remote CLI package that can change over time and execute local code.

Mitigation: Review and pin a trusted daxiapi-cli version, run it in a constrained environment, and expose only the required API token.

Risk: Finance-oriented market guidance can be misleading if treated as investment advice or if generated from stale or incorrect data.

Mitigation: Review generated reports against the source data, keep the disclaimer visible, and treat outputs as informational support rather than trading instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksky521/skills/xiapi-market-compass)
- [字段说明](references/field-descriptions.md)
- [分析框架详解](references/analysis-framework.md)
- [报告模板](assets/report-template.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables and concise Chinese prose; may include inline shell commands for retrieving market compass data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses daxiapi market compass data and is scoped to broad Chinese A-share market analysis, not individual stock, sector, short-term timing, or bond fund analysis.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
