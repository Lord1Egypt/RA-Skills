## Description: <br>
Superior Trade Hyperliquid helps agents backtest, configure, and manage Hyperliquid trading strategies through Superior Trade's managed cloud. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superior-ai](https://clawhub.ai/user/superior-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Use this skill when an agent needs to create trading strategy code and configuration, run and compare backtests, inspect results, check Hyperliquid balances, and manage Superior Trade deployments including live starts, stops, exits, and supported deposits after explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Online use where Superior Trade, Hyperliquid, and the user's local financial and digital-asset rules permit the activity. <br>

## Known Risks and Mitigations: <br>
Risk: The API key can start live deployments that trade with real funds and can initiate supported Arbitrum USDC deposits into Hyperliquid. <br>
Mitigation: Treat the API key as a financial credential, review each live deployment or deposit summary, and require explicit user confirmation before executing fund-affecting actions. <br>
Risk: Incorrect strategy settings, balance assumptions, or unresolved positions can cause unexpected trading behavior or financial loss. <br>
Mitigation: Run backtests first, verify balances and deployment readiness with current API responses, and review open positions, stake sizing, and risk controls before live deployment. <br>
Risk: The artifact states that the API key cannot withdraw funds or export private keys, but it still grants broad authority over the user's own backtests and deployments. <br>
Mitigation: Limit use to intended Superior Trade operations, avoid collecting wallet secrets, and confirm high-impact stop, exit, transfer, delete, and deposit actions with the user. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/superior-ai/superior-trade-hyperliquid) <br>
- [Publisher profile](https://clawhub.ai/user/superior-ai) <br>
- [Superior Trade account](https://account.superior.trade) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, text] <br>
**Output Format:** [Conversational guidance with API request details, trading strategy code, JSON-style deployment configuration, and backtest or deployment summaries.] <br>
**Output Parameters:** [Requires SUPERIOR_TRADE_API_KEY for protected Superior Trade operations; user-provided strategy goals, pairs, timeframe, trading mode, stake sizing, and confirmation are needed for live or fund-moving actions.] <br>
**Other Properties Related to Output:** [Outputs should distinguish simulated backtests from live trading, use current API responses for balances and deployment status, and avoid displaying or requesting private keys, seed phrases, or wallet credentials.] <br>

## Skill Version(s): <br>
4.5.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
