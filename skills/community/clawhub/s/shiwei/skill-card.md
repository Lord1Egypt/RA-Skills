## Description:

十维 is a Chinese-language stock value analysis workflow that guides an agent through ten fundamental analysis modules and produces a scored investment-quality report with risk reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lsh9630](https://clawhub.ai/user/lsh9630)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and agents use this skill to structure stock fundamental analysis across revenue, profit, ROE, balance sheet, cash flow, shareholder returns, industry context, peer benchmarking, ownership changes, shareholding concentration, and valuation. It is intended to produce an informational value-analysis report, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce investment-facing conclusions such as configuration, observation, or exclusion recommendations.

Mitigation: Treat the report as informational analysis only and do not use it as personalized investment advice.

Risk: Outdated or incorrect financial, market, industry, or ownership data can make the scoring misleading.

Mitigation: Verify all financial data independently and refresh the analysis with current filings and market information before relying on conclusions.

## Reference(s):

- [十维 ClawHub skill page](https://clawhub.ai/lsh9630/skills/shiwei)
- [Scoring template](artifact/references/scoring_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with a stock profile, ten-module scoring table, core conclusion, and risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current, independently verified financial, market, industry, and ownership data supplied by the user or other tools.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
