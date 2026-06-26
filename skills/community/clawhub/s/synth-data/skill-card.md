## Description: <br>
Query volatility forecasts from Synthdata.co for crypto, commodities, and stocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emsin44](https://clawhub.ai/user/emsin44) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External developers, traders, and market analysts use this skill to query Synthdata volatility forecasts, compare supported assets, and generate short-horizon Monte Carlo price ranges for market monitoring and research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends selected asset tickers to the Synthdata API using a SYNTHDATA_API_KEY. <br>
Mitigation: Use a revocable Synthdata API key and avoid exposing the key in shared terminals, logs, or generated reports. <br>
Risk: Scheduled cron, Slack, Telegram, or alert integrations can continue sending market reports after initial setup. <br>
Mitigation: Create integrations deliberately, document where they run, and disable schedules or webhooks when reporting is no longer needed. <br>
Risk: Volatility forecasts and Monte Carlo ranges may be misread as financial advice or guaranteed outcomes. <br>
Mitigation: Treat outputs as market-data analysis inputs and review any trading, options, or portfolio decisions separately before acting. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/emsin44/synth-data) <br>
- [Synthdata](https://synthdata.co) <br>
- [Synthdata API Reference](references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Terminal text tables, JSON API responses, and Markdown instructions with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3.8+ and SYNTHDATA_API_KEY; simulations are capped to the Synthdata 24-hour forecast window.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
