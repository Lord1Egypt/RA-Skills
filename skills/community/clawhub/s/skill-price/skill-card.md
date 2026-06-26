## Description: <br>
Skill Price helps B2B export teams monitor competitor pricing, track market price trends, configure price alerts, and prepare pricing strategy reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business operators use this skill to compare competitor prices, monitor market changes, and generate pricing recommendations for B2B export products. It can also help configure alerts and recurring price-monitoring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a TradeGPT API key and may submit business pricing context to YunlvAI services. <br>
Mitigation: Use a scoped API key when available and avoid sending confidential customer, margin, or strategy data unless approved. <br>
Risk: Monitoring reports and alerts may expose competitor, product, or pricing information through local storage, email, or WhatsApp recipients. <br>
Mitigation: Make monitoring targets, recipients, thresholds, and retention settings explicit before enabling alerts. <br>
Risk: Price recommendations can be affected by delayed customs data, reference-price differences, or incomplete market coverage. <br>
Mitigation: Treat recommendations as decision support and verify important pricing decisions against authorized data sources and business constraints. <br>


## Reference(s): <br>
- [Skill Price ClawHub page](https://clawhub.ai/wangm-a3/skill-price) <br>
- [YunlvAI homepage](https://yunlvai.com) <br>
- [YunlvAI TradeGPT API](https://api.yunlvai.com) <br>
- [YunlvAI customs price data](https://data.yunlvai.com) <br>
- [Competitor monitoring template](artifact/references/competitor_list_template.md) <br>
- [Price analysis report template](artifact/references/price_analysis_report.md) <br>
- [Pricing strategy guide](artifact/references/pricing_strategy_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with structured tables, JSON examples, alert configuration, and pricing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use TRADEGPT_API_KEY-backed API calls and may write monitoring configurations, reports, alerts, and logs under the documented local data path.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
