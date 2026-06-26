## Description: <br>
For token distribution on Solana 5000x cheaper than SPL (rewards, airdrops, depins, ...). @lightprotocol/compressed-token (TypeScript). Reference examples for custom claim support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tilo-14](https://clawhub.ai/user/tilo-14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to plan and implement Solana compressed-token distributions, including small airdrops, large batched distributions, and claim-based distribution patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example code can submit real Solana blockchain transactions if copied and run against mainnet. <br>
Mitigation: Confirm the network, mint, recipients, amounts, fees, and preflight settings before execution; test on devnet or localnet first. <br>
Risk: Production use requires RPC credentials and a payer keypair, which can expose funds or infrastructure access if mishandled. <br>
Mitigation: Keep private keys and HELIUS_API_KEY out of source and chat, use a secrets manager, and use a limited-balance payer wallet. <br>


## Reference(s): <br>
- [Simple Airdrop](references/simple-airdrop.md) <br>
- [Batched Airdrop](references/batched-airdrop.md) <br>
- [ZK Compression Documentation](https://www.zkcompression.com) <br>
- [Compressed Tokens Airdrop Guide](https://www.zkcompression.com/compressed-tokens/airdrop) <br>
- [@lightprotocol/stateless.js API Docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html) <br>
- [@lightprotocol/compressed-token API Docs](https://lightprotocol.github.io/light-protocol/compressed-token/index.html) <br>
- [Light Protocol Audits](https://github.com/Lightprotocol/light-protocol/tree/main/audits) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference required environment variables and runtime dependencies for Solana RPC access and transaction signing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
