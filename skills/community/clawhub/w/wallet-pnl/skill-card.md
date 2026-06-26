## Description: <br>
Analyze a Solana wallet's trading history to estimate win rate, realized PnL, trader type, and copy-trade rating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ultranumblol](https://clawhub.ai/user/ultranumblol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and trading-tool agents use this skill to inspect recent Solana wallet swap activity before deciding whether a wallet merits further copy-trading review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried Solana wallet addresses and transaction lookups may be sent to third-party RPC or API providers. <br>
Mitigation: Use the skill only for wallet addresses you are comfortable sharing with those providers and review provider terms before deployment. <br>
Risk: Paid API usage may incur x402 USDC charges. <br>
Mitigation: Confirm payment configuration, price, and spending controls before routing agent requests to the paid endpoint. <br>
Risk: Copy-trading ratings can be misleading if treated as investment advice. <br>
Mitigation: Present FOLLOW, NEUTRAL, and AVOID outputs as rough heuristics and require independent review before trading decisions. <br>
Risk: A Helius API key is required for transaction history and may be exposed through misconfiguration. <br>
Mitigation: Use a least-privilege key, store it as a secret, and avoid logging the key or full request URLs containing it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ultranumblol/wallet-pnl) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/ultranumblol) <br>
- [Declared Project Homepage](https://github.com/ultranumblol/wallet-pnl) <br>
- [Declared Support URL](https://github.com/ultranumblol/wallet-pnl/issues) <br>
- [Helius Transactions API Endpoint](https://api.helius.xyz/v0/addresses/{wallet}/transactions) <br>
- [x402 Facilitator Endpoint](https://x402.org/facilitator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON API responses and command-line text summaries, with Markdown documentation for setup and usage.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Solana wallet address; Helius-backed analysis needs HELIUS_API_KEY and the paid API can require x402 USDC payment.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
