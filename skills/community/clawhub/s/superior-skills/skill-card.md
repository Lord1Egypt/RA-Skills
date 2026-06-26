## Description: <br>
Backtest and deploy trading strategies on Superior Trade's managed cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, backtest, evaluate, and deploy crypto trading strategies through Superior Trade. It supports normal trading workflows, including live deployments and deposits, with explicit confirmation expected before real-funds actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start live trading deployments and initiate supported USDC deposits using a sensitive API key. <br>
Mitigation: Treat SUPERIOR_TRADE_API_KEY as a financial credential, keep it in a credential manager or environment variable, and confirm every live deployment or deposit before execution. <br>
Risk: Trading strategies can lose real funds if deployed without enough testing, conservative sizing, or clear stoploss rules. <br>
Mitigation: Prefer dry runs and backtests first, then set conservative stake amounts, stoploss settings, and wallet exposure limits before using real funds. <br>
Risk: The skill's authority includes financial actions that are intentional for this release but high impact. <br>
Mitigation: Install only when the agent is expected to manage Superior Trade backtests and live trading, and review the deployment summary before approving real-funds activity. <br>


## Reference(s): <br>
- [Superior Trade account and API key setup](https://account.superior.trade) <br>
- [Superior Trade API base endpoint](https://api.superior.trade) <br>
- [Superior Trade skill listing](https://clawhub.ai/superior-ai/superior-skills) <br>
- [Hyperliquid public info endpoint](https://api.hyperliquid.xyz/info) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON, Python strategy code, API request examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading strategy templates, backtest interpretation, deployment checklists, and explicit confirmation prompts for live trading or deposits.] <br>

## Skill Version(s): <br>
4.5.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
