## Description: <br>
CLI for crypto portfolio tracking, market data, and CEX history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arein](https://clawhub.ai/user/arein) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to query crypto market data, wallet balances, portfolio values, centralized exchange history, and Polymarket predictions through the onchain CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet, exchange, and API-key data can expose sensitive financial information if pasted into chats, logs, or shared systems. <br>
Mitigation: Use read-only exchange API keys with trading and withdrawals disabled, avoid sharing secrets or wallet details in logs, and review the saved onchain configuration before use on shared machines. <br>
Risk: Installing or invoking an untrusted onchain CLI could expose credentials or produce unreliable crypto account data. <br>
Mitigation: Install only a trusted onchain CLI and verify commands before giving the tool access to wallet or exchange configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/arein/test) <br>
- [DeBank API](https://cloud.debank.com/) <br>
- [Helius](https://helius.xyz/) <br>
- [Coinbase API settings](https://www.coinbase.com/settings/api) <br>
- [Binance API management](https://www.binance.com/en/my/settings/api-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill recommends --json for programmatic agent use and relies on configured API keys for wallet and exchange data.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
