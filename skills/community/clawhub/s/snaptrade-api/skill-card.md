## Description: <br>
Execute trades and retrieve account data via the SnapTrade API using the snaptrade-python-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[player-1101](https://clawhub.ai/user/player-1101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to SnapTrade for brokerage account data, balances, positions, quotes, order history, order placement, order cancellation, and account refresh workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place or cancel real brokerage orders through connected SnapTrade accounts. <br>
Mitigation: Require explicit confirmation of account, symbol, side, quantity, order type, price, and cancellation target before each live action. <br>
Risk: SnapTrade credentials and per-user secrets can expose account data and trading permissions if mishandled. <br>
Mitigation: Store credentials in a secret manager or private .env file, avoid logging them, and rotate any exposed user secret through SnapTrade. <br>
Risk: Automated or broad routing could trade beyond the user's intended limits. <br>
Mitigation: Prefer paper trading or a low-limit dedicated account first, and use allowlists, notional caps, position limits, and daily loss limits before enabling automation. <br>
Risk: Account data, quotes, brokerage support, and order impact checks may be stale, delayed, unsupported, or expire before execution. <br>
Mitigation: Resolve symbols fresh, check brokerage trading support and connection health, place orders promptly after impact checks, and refresh holdings after orders or cancellations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/player-1101/snaptrade-api) <br>
- [SnapTrade API documentation](https://docs.snaptrade.com) <br>
- [SnapTrade getting started guide](https://docs.snaptrade.com/docs/getting-started) <br>
- [SnapTrade register user API reference](https://docs.snaptrade.com/reference/Authentication/Authentication_registerSnapTradeUser) <br>
- [Account Data](references/account-data.md) <br>
- [Cancel Orders & Refresh Holdings](references/cancel-refresh.md) <br>
- [Crypto Trading](references/crypto-trading.md) <br>
- [Historical Data](references/historical-data.md) <br>
- [Options Trading](references/options-trading.md) <br>
- [Place Orders](references/place-orders.md) <br>
- [Symbol Resolution](references/symbol-resolution.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell code snippets plus configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SnapTrade credentials and can guide real account-data access, order placement, order cancellation, and manual account refresh operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
