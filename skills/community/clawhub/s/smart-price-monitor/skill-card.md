## Description: <br>
Monitors product prices, stock levels, and market data across websites or APIs, then produces alerts, trend analysis, reports, and dashboards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, shoppers, and business users use this skill to configure local price monitors, record price history, detect price drops or restocks, and generate markdown reports or HTML dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Monitored URLs, target prices, price history, alerts, and reports may contain sensitive purchase or competitor information. <br>
Mitigation: Store the local price-monitor-data directory in a controlled location and review generated files before sharing or syncing them. <br>
Risk: Website or API collection can violate source rules if the user monitors targets without permission. <br>
Mitigation: Use permitted APIs or scraping paths, respect site terms and rate limits, and avoid private targets unless authorized. <br>
Risk: Capability tags mention purchases, but the reviewed artifacts only support monitoring and recommendations. <br>
Mitigation: Do not grant purchase authority to this skill; keep buying decisions and transactions under explicit user control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chloepark85/smart-price-monitor) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands, markdown, JSON, HTML] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, Python command examples, generated Markdown reports, JSON history and alert files, and self-contained HTML dashboards.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local monitoring state under price-monitor-data by default; PRICE_MONITOR_DATA can override the data directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
