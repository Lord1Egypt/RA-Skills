## Description: <br>
Places GTC limit orders on both sides of liquid Polymarket markets to quote bid/ask spreads around the CLOB midpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prysm96](https://clawhub.ai/user/prysm96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External traders and developers use this skill to run a configurable Polymarket market-making strategy that selects liquid markets, quotes both YES and NO sides, and reports dry-run or live execution results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real trades on the connected trading account. <br>
Mitigation: Review before installing, use dry run or TRADING_VENUE=sim first, and use --live only after confirming the account, venue, and strategy settings. <br>
Risk: Live execution can cancel all existing open orders on the connected account. <br>
Mitigation: Prefer a dedicated trading account or API key, and do not run --live on an account with manual orders or other strategies unless existing open-order cancellation is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/prysm96/simmer-market-maker) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Console text with optional automaton JSON status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and supports dry-run, live trading, position display, and configurable strategy parameters.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
