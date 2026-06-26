## Description: <br>
Monitors competitor pricing, tracks market price trends, configures price alerts, and prepares pricing strategy reports for B2B export businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External business users and pricing analysts use this skill to monitor competitor prices, analyze market price changes, configure alerts, and draft pricing strategy reports for B2B export products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires TRADEGPT_API_KEY and sends business pricing context to external YunlvAI APIs. <br>
Mitigation: Install only if the user trusts YunlvAI with the API key and pricing context, and store the credential in the intended environment variable. <br>
Risk: Competitor monitoring may involve data sources the user is not authorized to access. <br>
Mitigation: Configure monitored products, competitors, alert recipients, frequency, retention, and data sources deliberately, and avoid unauthorized monitoring sources. <br>
Risk: Pricing recommendations can be wrong or incomplete if source data is delayed, noisy, or only indicative. <br>
Mitigation: Review generated recommendations against original data sources, costs, order terms, and business constraints before changing prices. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/yunlv-price-monitor) <br>
- [YunlvAI Homepage](https://yunlvai.com) <br>
- [YunlvAI TradeGPT API](https://api.yunlvai.com) <br>
- [Customs Price Data API](https://data.yunlvai.com) <br>
- [Competitor List Template](references/competitor_list_template.md) <br>
- [Price Analysis Report Template](references/price_analysis_report.md) <br>
- [Pricing Strategy Guide](references/pricing_strategy_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, configuration, guidance] <br>
**Output Format:** [Markdown reports and guidance with structured JSON examples and monitoring configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference external pricing APIs, local monitoring data, generated reports, and alert configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
