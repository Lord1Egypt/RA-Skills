## Description:

Monitors competitor pricing, market price trends, price alerts, and B2B export pricing strategy reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and pricing analysts use this skill to compare competitor prices, monitor market movement, configure alerts, and prepare pricing strategy reports for B2B export sales.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses external YunlvAI-related APIs and may send product, competitor, market, and pricing context outside the local environment.

Mitigation: Install only when that data sharing is acceptable, protect the TRADEGPT_API_KEY, and limit submitted context to what is needed for the analysis.

Risk: Price alerts may disclose competitive or commercial information to unintended recipients.

Mitigation: Configure email and WhatsApp alerts only for recipients the user controls and review recipient lists before enabling automated notifications.

Risk: Generated pricing recommendations can be incomplete or misleading if source prices are delayed, estimated, or not actual transaction prices.

Mitigation: Review recommendations against current source data, costs, order terms, and business constraints before changing prices.

## Reference(s):

- [Competitor Monitoring Template](references/competitor_list_template.md)
- [Price Analysis Report Template](references/price_analysis_report.md)
- [Pricing Strategy Guide](references/pricing_strategy_guide.md)
- [YunlvAI Homepage](https://yunlvai.com)
- [YunlvAI TradeGPT API](https://api.yunlvai.com)
- [Customs Price Data API](https://data.yunlvai.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured JSON-style report examples and configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include price-monitoring setup, alert recommendations, and pricing reports that should be reviewed before business action.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
