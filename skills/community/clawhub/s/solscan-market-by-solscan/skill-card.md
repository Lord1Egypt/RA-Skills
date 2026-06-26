## Description: <br>
Use this skill to query Solana blockchain data via the Solscan Pro API across accounts, tokens, NFTs, transactions, blocks, markets, DeFi activity, programs, and API usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tiennv3](https://clawhub.ai/user/tiennv3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to retrieve read-only Solana on-chain data for wallet, token, transaction, NFT, DeFi, block, program, and market investigations through Solscan Pro. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Solana addresses, token mints, transaction signatures, query filters, and the Solscan API key are sent to Solscan Pro. <br>
Mitigation: Use a dedicated Solscan API key, avoid logging request headers, and limit lookups tied to real people or sensitive investigations. <br>
Risk: Blockchain lookup results may be used in privacy-sensitive investigations. <br>
Mitigation: Review outputs before sharing and avoid exposing wallet activity that can identify people or sensitive activity. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tiennv3/solscan-market-by-solscan) <br>
- [Solscan Pro API documentation](https://pro-api.solscan.io/pro-api-docs/v2.0) <br>
- [Solscan Pro API FAQ](https://pro-api.solscan.io/pro-api-docs/v2.0/faq.md) <br>
- [Solscan Pro API base URL](https://pro-api.solscan.io/v2.0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with Python CLI commands, JSON API responses, and CSV export data where supported.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Solscan Pro lookups require a SOLSCAN_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
