## Description: <br>
Execute cryptocurrency trades on exchanges (Binance, OKX) with risk controls, user confirmation, and audit logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[patches429](https://clawhub.ai/user/patches429) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare and execute user-confirmed cryptocurrency trades on Binance or OKX while applying risk checks, stop-loss requirements, and audit logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live cryptocurrency orders when installed with exchange credentials. <br>
Mitigation: Install only when agent-assisted live trading is intended, require explicit confirmation for every order, and keep exchange-side trading limits small. <br>
Risk: Exchange API keys could allow broader account actions than the skill requires. <br>
Mitigation: Use API keys restricted to trading and disable withdrawals, transfers, and permission changes. <br>
Risk: A user may approve an incorrect order preview or miss unfavorable order parameters. <br>
Mitigation: Verify the exchange, pair, side, type, quantity, price, stop-loss, take-profit, and estimated amount before confirming. <br>
Risk: Audit logs and risk-tracking records may contain sensitive trading activity. <br>
Mitigation: Confirm where gateway audit logs and risk-tracking data are stored and restrict access according to the user's operational requirements. <br>


## Reference(s): <br>
- [Trade Executor on ClawHub](https://clawhub.ai/patches429/trade-executor) <br>
- [Publisher profile: patches429](https://clawhub.ai/user/patches429) <br>
- [Binance](https://www.binance.com) <br>
- [Binance order API](https://api.binance.com/api/v3/order) <br>
- [Binance OCO order API](https://api.binance.com/api/v3/order/oco) <br>
- [OKX order API](https://api.okx.com/api/v5/trade/order) <br>
- [OKX algorithmic order API](https://api.okx.com/api/v5/trade/order-algo) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration, text, JSON] <br>
**Output Format:** [Markdown and structured order or audit records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires exchange API credentials and explicit order confirmation before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
