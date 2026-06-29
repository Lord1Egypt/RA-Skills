## Description: <br>
帮助用户监控 BTC、ETH、SOL 等加密货币价格，设置价格突破或跌破告警，并生成市场概览和单币分析报告。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check cryptocurrency prices, configure monitoring alerts, and produce informational market reports. It is not intended for trade execution, wallet management, DeFi operations, or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market reports and risk-style analysis can be mistaken for financial advice. <br>
Mitigation: Treat generated reports and suggestions as informational only, and independently verify market data before making financial decisions. <br>
Risk: Users may act on alerts or risk scores without confirmation. <br>
Mitigation: Confirm alert settings, target prices, and any risk score before taking action outside the skill. <br>
Risk: External market APIs can be unavailable, delayed, or inconsistent. <br>
Mitigation: Check the displayed data source and timestamp, and compare critical values against another trusted source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/qqyougit-crypto-monitor) <br>
- [加密货币监控与告警 - 详细内容](references/details.md) <br>
- [CoinGecko markets API](https://api.coingecko.com/api/v3/coins/markets) <br>
- [CoinCap assets API](https://api.coincap.io/v2/assets) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-style text with command examples and alert configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include current price data, 24-hour changes, market report summaries, alert IDs, and data-source labels.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
