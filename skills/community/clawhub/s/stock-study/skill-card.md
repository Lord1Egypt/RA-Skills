## Description:

Senior equity research analysis for single tickers. Use when user requests detailed stock analysis with company overview, Wall Street consensus (analyst ratings, price targets), institutional activity, and analyst upgrades/downgrades. Cite all metrics with source and date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickzhou](https://clawhub.ai/user/rickzhou)

### License/Terms of Use:


## Use Case:

External analysts, investors, and research-focused agents use this skill to produce cited single-ticker equity research with company overview, analyst consensus, price targets, institutional activity, and recent analyst actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial metrics, analyst ratings, price targets, and institutional holdings can be outdated or incorrect if not checked against current authoritative sources.

Mitigation: Verify all cited financial data from current authoritative sources before relying on the analysis, and retain the skill's requirement to cite each metric with source and date.

Risk: The generated analysis could be mistaken for investment advice.

Mitigation: Treat the output as research support only and require human review before any investment decision.

Risk: The skill asks for premium or current market data that may be unavailable to the executing agent.

Mitigation: When data is unavailable or potentially outdated, state that limitation explicitly instead of estimating or fabricating values.

## Reference(s):


## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown report with headers, tables, and inline source citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Flags unavailable data and metrics that may be more than 30 days old.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
