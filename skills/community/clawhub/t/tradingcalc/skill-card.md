## Description:

Compute trading math with exact numbers instead of estimates, through TradingCalc's MCP tools. Options (Black-Scholes price and Greeks, payoff and breakeven, covered call, implied volatility), forex (position size, pip value, margin, swap, currency conversion, correlation), risk statistics (VaR, Sharpe ratio, Kelly, GARCH, tearsheet) and crypto futures (PnL, liquidation price, breakeven, funding cost). Use whenever a question needs a number a person might act on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skalinin909](https://clawhub.ai/user/skalinin909)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and analysts use this skill to obtain calculations for options, forex, portfolio risk, crypto futures, token checks, and prediction markets. It routes calculation requests to TradingCalc tools and presents the returned figures for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs sent to TradingCalc may include sensitive financial or account information; the remote implementation and MCP-specific retention were not audited.

Mitigation: Send only necessary inputs and exclude passwords, private keys, and identifying account details.

Risk: Calculated results may rely on fee and margin assumptions and do not validate a user's specific trading setup.

Mitigation: Confirm the assumptions before relying on a result, and treat formula checks or signatures as checks of the calculation response rather than validation of the particular trading setup.

## Reference(s):

- [TradingCalc API documentation](https://docs.tradingcalc.io/api)
- [TradingCalc calculator verification](https://tradingcalc.io/verify)
- [TradingCalc on ClawHub](https://clawhub.ai/skalinin909/skills/tradingcalc)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Plain text with calculated values and brief explanatory sentences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the inputs and fee or margin assumptions supplied.]

## Skill Version(s):

2.15.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
