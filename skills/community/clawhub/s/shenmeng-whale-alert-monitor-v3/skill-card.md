## Description: <br>
Whale Alert Monitor 大户监控 helps agents configure and run crypto whale wallet monitoring, large-transfer alerts, exchange-flow tracking, and holding-change analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenmeng](https://clawhub.ai/user/shenmeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto operations analysts use this skill to configure wallet monitoring, transfer thresholds, exchange flow tracking, and alert notifications. It is intended for informational monitoring and report generation, not investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes paid SkillPay billing behavior and may attempt per-use charges. <br>
Mitigation: Install only after confirming the billing terms, configured user identity, and account balance; review payment behavior before execution. <br>
Risk: The security summary says generated crypto reports or alerts should be treated as demo or simulated unless real, auditable data sources are provided. <br>
Mitigation: Validate monitoring results against trusted blockchain APIs and do not use generated alerts as investment advice. <br>
Risk: Alert details and credentials may be sent to Telegram, Discord, webhook, and blockchain API services. <br>
Mitigation: Keep API keys, bot tokens, and webhook URLs in environment variables or secret stores, and avoid sharing configuration files that contain them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shenmeng/shenmeng-whale-alert-monitor-v3) <br>
- [API data source configuration](artifact/references/api-configuration.md) <br>
- [Whale wallet label library](artifact/references/wallet-labels.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce wallet monitoring reports, alert setup guidance, and command examples that depend on configured blockchain APIs and notification endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
