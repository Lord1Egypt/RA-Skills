## Description:

A Chinese-language A-share and Hong Kong stock investment decision framework that combines a five-dimensional Bayesian research process, a six-layer decision matrix, and behavioral finance checks to produce structured investment diagnostic cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[managaman-ship-it](https://clawhub.ai/user/managaman-ship-it)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investing-focused agents use this skill to structure stock research, position sizing, holding reviews, and buy/sell decision checks for A-share and Hong Kong equity scenarios. It is intended to generate decision-support diagnostics, not licensed financial advice or automated trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat generated investment diagnostics as licensed financial advice.

Mitigation: Present outputs as decision-support guidance only and require independent review before acting on any recommendation.

Risk: Incorrect or stale market data can materially change stock-analysis conclusions.

Mitigation: Verify all prices, financial metrics, filings, and portfolio inputs against authoritative market data before using the diagnostic.

Risk: The framework includes 奇门遁甲 timing signals that are non-evidence-based.

Mitigation: Treat metaphysical timing outputs as optional context and do not let them override financial data, risk limits, or independent judgment.

Risk: Future Wind or MCP integrations could expand tool access beyond checklist generation.

Mitigation: Review and constrain any market-data or MCP tool permissions before granting access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/managaman-ship-it/skills/stock-investment-system)
- [Homepage from ClawHub metadata](https://github.com/guodong/stock-investment-system)
- [Six-layer decision matrix v1.0](references/six-layer-matrix-v1.0.md)
- [Five-dimensional Bayesian investment method v3.4](references/wuwei-bayesian-v3.4.md)
- [Foster 603806 holding health-check example](references/案例-福斯特603806.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown investment diagnostic card with structured checklists, decision gates, and scenario options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language decision-support output; may reference user-provided market data and portfolio context.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
