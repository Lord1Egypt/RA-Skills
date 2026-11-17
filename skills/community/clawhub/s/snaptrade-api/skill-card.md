## Description:

Execute trades and retrieve account data through the SnapTrade API using the snaptrade-python-sdk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[player-1101](https://clawhub.ai/user/player-1101)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent inspect SnapTrade-connected brokerage accounts, retrieve balances and positions, resolve symbols, place or cancel supported orders, and refresh account state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive brokerage account data and execute live trades when SnapTrade credentials are provided.

Mitigation: Install only when brokerage interaction is intended, keep SnapTrade secrets in a secret manager or uncommitted .env file, and require explicit confirmation for live orders and cancellations.

Risk: Automated trading can cause unintended financial loss if orders are placed without guardrails.

Mitigation: Use paper trading or a low-limit account first, and enable automation only with symbol allowlists, notional caps, position limits, and daily loss limits.

Risk: Brokerage support, delayed quotes, stale symbol identifiers, and data refresh timing can make account or order guidance inaccurate.

Mitigation: Check connection health and brokerage capabilities, resolve symbols fresh before trading, use dedicated market data for real-time strategy inputs, and refresh holdings after order placement or cancellation.

## Reference(s):

- [SnapTrade API Documentation](https://docs.snaptrade.com)
- [SnapTrade Getting Started Guide](https://docs.snaptrade.com/docs/getting-started)
- [SnapTrade Register User API Reference](https://docs.snaptrade.com/reference/Authentication/Authentication_registerSnapTradeUser)
- [Account Data](references/account-data.md)
- [Symbol Resolution](references/symbol-resolution.md)
- [Placing Orders](references/place-orders.md)
- [Options Trading](references/options-trading.md)
- [Crypto Trading](references/crypto-trading.md)
- [Cancel Orders and Refresh Holdings](references/cancel-refresh.md)
- [Historical Data](references/historical-data.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SnapTrade credentials and a connected brokerage account before account data or trading calls can run.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
