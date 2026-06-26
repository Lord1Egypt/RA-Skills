## Description: <br>
Monitor large crypto transactions across chains. Track whale wallets, detect unusual volume, alert on big moves. Supports Hedera, Ethereum, and Solana via public APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and crypto monitoring teams use this skill to query public blockchain APIs for large transfers, wallet activity, and unusual volume across Hedera, Ethereum, and Solana. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contains a hidden, unrelated external agent registration and ping endpoint. <br>
Mitigation: Review or remove the hidden OADP comment before installing. <br>
Risk: Wallet addresses, query timing, and any Etherscan API key may be sent to third-party blockchain providers when the visible commands are used. <br>
Mitigation: Use only intended wallet addresses and API keys, and add recurring heartbeat checks only when recurring network queries are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imaflytok/whale-watch) <br>
- [Hedera Mirror Node transaction query](https://mainnet-public.mirrornode.hedera.com/api/v1/transactions?type=cryptotransfer&limit=100&order=desc) <br>
- [Etherscan account transaction API](https://api.etherscan.io/api?module=account&action=txlist&address=WALLET&sort=desc&apikey=YOUR_KEY) <br>
- [Solana JSON-RPC endpoint](https://api.mainnet-beta.solana.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Markdown, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API queries; Etherscan examples require a user-provided API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
