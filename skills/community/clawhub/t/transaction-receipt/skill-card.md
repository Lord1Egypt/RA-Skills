## Description: <br>
Transaction Receipt helps an agent turn valid BTC or EVM transaction hashes into human-readable on-chain receipts with status, fees, transfers, approvals, swaps, DeFi interactions, NFT activity, and clear fallback behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bevanding](https://clawhub.ai/user/bevanding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, wallet operators, support teams, and developers use this skill to explain blockchain transaction hashes in plain language, including whether a transaction succeeded, what assets moved, what fees were paid, and what contract interaction appears to have occurred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction hashes and request metadata may be sent to Tokenview or public blockchain endpoints during lookups. <br>
Mitigation: Use the skill only when sharing transaction lookup data with those endpoints is acceptable for the deployment environment. <br>
Risk: A configured Tokenview API key is sensitive and could be exposed if pasted into chat or logs. <br>
Mitigation: Provide TOKENVIEW_API_KEY through the agent environment or an approved secret store, rotate it if exposed, and do not paste full keys into prompts. <br>
Risk: On-chain data can be incomplete, unavailable, or difficult to decode for complex contract interactions. <br>
Mitigation: Treat the receipt as a best-effort explanation, avoid inventing missing amounts or counterparties, and fall back to clearly stating unavailable or not fully decoded fields. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bevanding/transaction-receipt) <br>
- [Publisher profile](https://clawhub.ai/user/bevanding) <br>
- [Repository listed in skill metadata](https://github.com/AntalphaAI/transaction-receipt) <br>
- [Tokenview](https://tokenview.io) <br>
- [Ethereum public RPC endpoint](https://ethereum.publicnode.com) <br>
- [Blockstream transaction API](https://blockstream.info/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown receipt summaries with concise status, overview, interaction, fee, and takeaway sections; setup guidance may include shell commands and environment-variable configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; TOKENVIEW_API_KEY is optional and fallback lookups use public read-only endpoints with rate limiting and response validation.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
