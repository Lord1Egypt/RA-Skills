## Description: <br>
Stock Monitor Pro helps agents set up and operate a local stock-monitoring system for A-shares and ETFs with price, cost, volume, moving-average, RSI, gap, trailing-stop, daily-report, and error alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EaveLuo](https://clawhub.ai/user/EaveLuo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Investors and agent operators use this skill to configure watchlists, cost bases, thresholds, and daemon controls for local market monitoring. The skill supports alert review and reporting workflows, but users remain responsible for validating market data and investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a persistent local stock-monitoring daemon that continues polling until stopped. <br>
Mitigation: Start it only when continuous monitoring is intended, check its status and logs, and stop it with ./control.sh stop when monitoring is no longer needed. <br>
Risk: Configured stock symbols, watchlists, costs, and thresholds may be sent to external finance data providers during polling. <br>
Mitigation: Review and edit the watchlist before running the daemon, avoid adding sensitive holdings unless acceptable, and confirm use of each data source fits the provider's terms. <br>
Risk: Market alerts and technical indicators can be stale, incomplete, or misleading. <br>
Mitigation: Treat alerts as informational signals, validate against trusted market data, and do not use the output as the sole basis for investment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/EaveLuo/stock-monitor-pro) <br>
- [Sina Finance Quote Endpoint](https://hq.sinajs.cn/) <br>
- [Eastmoney Historical Quote Endpoint](https://push2his.eastmoney.com/api/qt/stock/kline/get) <br>
- [Tencent Quote Endpoint](https://qt.gtimg.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text, markdown] <br>
**Output Format:** [Markdown guidance with shell commands and Python configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and operation guidance for scripts that poll public market-data sources and write daemon logs under the user's home directory.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
