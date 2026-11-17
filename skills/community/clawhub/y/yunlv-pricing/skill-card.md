## Description:

Yunlv Pricing helps B2B export businesses generate pricing strategy suggestions, market pricing reference reports, competitive positioning advice, and dynamic pricing recommendations from market context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and developers use this skill to prepare B2B export pricing reference reports, compare competitor price positioning, calculate FOB/CIF/CFR pricing, simulate margins, and draft pricing recommendations for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pricing prompts may disclose product context or pricing strategy to the Yunlv/TradeGPT API.

Mitigation: Avoid sending confidential customer lists, negotiated prices, sensitive margin targets, or internal pricing strategy unless disclosure to the provider is acceptable.

Risk: Generated pricing recommendations may be incomplete, stale, or unsuitable as final pricing decisions.

Mitigation: Use the output as business guidance only; validate source data, costs, market assumptions, and margin impact before changing prices.

Risk: The skill requires a TRADEGPT_API_KEY for API-backed functionality.

Mitigation: Store the API key in the agent environment, restrict access to it, and avoid pasting credentials into prompts, reports, logs, or shared outputs.

Risk: Referenced B2B platform quotes, customs data, and industry reports can lag or differ from actual transaction prices.

Mitigation: Sample-check important market references against original sources and combine market data with product cost, payment terms, order size, and customer relationship context.

## Reference(s):

- [Yunlv Homepage](https://yunlvai.com)
- [Yunlv AI TradeGPT API](https://api.yunlvai.com)
- [Competitor List Template](references/competitor_list_template.md)
- [Price Analysis Report Template](references/price_analysis_report.md)
- [Pricing Strategy Guide](references/pricing_strategy_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON report examples and optional JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use TRADEGPT_API_KEY for API-backed pricing guidance; local calculator commands return JSON for pricing, positioning, and profit simulations.]

## Skill Version(s):

1.1.0 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
