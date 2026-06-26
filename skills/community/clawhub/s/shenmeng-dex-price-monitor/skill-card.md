## Description: <br>
DEX价格监控与差价追踪助手，当用户需要实时监控多个DEX的代币价格、发现套利价差、设置价格预警、分析价格趋势或获取最优交易路径时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and crypto monitoring operators use this skill to compare token prices across DEXs, configure alerts, analyze spreads and trends, and generate monitoring or route-finding scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The SkillPay helper can automatically charge 0.01 USDT using an environment-derived user identity, with an anonymous fallback if no user ID is set. <br>
Mitigation: Deploy only where the billing model is accepted, set and verify SKILLPAY_USER_ID explicitly, and confirm user consent and balance before invoking paid behavior. <br>
Risk: The payment helper includes an embedded billing key and sends billing requests to an external SkillPay service. <br>
Mitigation: Review, rotate, or remove embedded billing credentials before deployment, and restrict outbound billing access to approved environments. <br>
Risk: DEX monitoring or alert outputs may rely on delayed, unavailable, or simulated price data and can mislead trading decisions. <br>
Mitigation: Cross-check live data sources, validate API configuration, and require human review before using outputs for trades or financial alerts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-dex-price-monitor) <br>
- [Price data sources guide](references/data-sources.md) <br>
- [API documentation quick reference](references/api-documentation.md) <br>
- [Monitoring tools guide](references/monitoring-tools.md) <br>
- [Alert configuration guide](references/alert-configuration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with tables, alerts, code snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include price comparisons, alert settings, monitoring script templates, historical analysis, and route-finding guidance.] <br>

## Skill Version(s): <br>
2025.4.12 (source: server release metadata; artifact _meta.json reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
