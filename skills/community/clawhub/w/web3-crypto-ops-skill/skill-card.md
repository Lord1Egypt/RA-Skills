## Description: <br>
Universal Web3 and crypto operating skill for AI agents covering token discovery, market data, token safety scoring, wallet and portfolio analysis, DEX swaps, CEX spot trading, and smart-money or meme-market signals across supported providers and chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stanpoldark](https://clawhub.ai/user/stanpoldark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to guide AI agents through crypto market analysis, portfolio review, provider credential setup, and gated trading workflows with transaction safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live crypto trading and on-chain swaps can cause financial loss. <br>
Mitigation: Use testnet first, require manual review before every order or transaction, and start mainnet use with dedicated low-balance wallets. <br>
Risk: Exchange API keys or wallet private keys could expose funds if overprivileged or leaked. <br>
Mitigation: Disable withdrawal permissions, use trade-only exchange scopes, enable IP whitelisting where available, and keep signing keys in dedicated wallets or a vault. <br>
Risk: Provider, RPC, or quote failures can lead to stale decisions or unsafe retries. <br>
Mitigation: Check transaction and order status before retrying, block execution on quote failure, and use RPC health failover with explicit user confirmation for mainnet movement. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/stanpoldark/web3-crypto-ops-skill) <br>
- [OKX API key management](https://www.okx.com/account/my-api) <br>
- [Binance API management](https://www.binance.com/en/my/settings/api-management) <br>
- [Gate.io API keys](https://www.gate.io/myaccount/apikeys) <br>
- [Bitget API keys](https://www.bitget.com/account/newapi) <br>
- [Alchemy dashboard](https://dashboard.alchemy.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with tables, configuration snippets, and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Risk flags first; blocked trades include reasons and safer alternatives; credentials must remain outside chat and source control.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
