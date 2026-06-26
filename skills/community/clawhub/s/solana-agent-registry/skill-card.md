## Description: <br>
TypeScript SDK guidance for the 8004 Trustless Agent Registry on Solana, covering agent registration, feedback and SEAL v1, ATOM reputation, signing, indexer queries, x402 payment feedback, and skipSend server-mode patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MonteCrypto999](https://clawhub.ai/user/MonteCrypto999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to configure and use the 8004-solana TypeScript SDK for Solana agent registration, wallet-backed signing, feedback, reputation, and registry queries. It is intended for agents that need guidance for read-only registry access or write-enabled on-chain operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet signing and on-chain registry operations can cause high-impact or irreversible changes. <br>
Mitigation: Start on devnet, use a dedicated low-balance wallet, and manually approve every transaction, delete, transfer, or immutable metadata action. <br>
Risk: IPFS and on-chain metadata may expose secrets or private details permanently. <br>
Mitigation: Review all metadata before upload or submission and keep private keys, API keys, and sensitive operational details out of published content. <br>
Risk: Dependency or RPC/indexer behavior can affect registry reads, signing flows, and feedback operations. <br>
Mitigation: Pin and verify npm dependencies, review RPC and indexer configuration, and prefer verified on-chain reads when indexer trust is uncertain. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/MonteCrypto999/solana-agent-registry) <br>
- [8004-solana TypeScript SDK homepage](https://github.com/QuantuLabs/8004-solana-ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and SOLANA_PRIVATE_KEY for write-enabled operations; read-only SDK setup can be used without a wallet.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; SDK version 0.6.3 from artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
