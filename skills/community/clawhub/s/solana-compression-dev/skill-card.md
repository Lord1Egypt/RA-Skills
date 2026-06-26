## Description: <br>
For client and program development on Solana compression, including rent-free per-user state, DePIN registrations, custom compressed accounts, and create, update, close, burn, and reinitialize workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tilo-14](https://clawhub.ai/user/tilo-14) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to build Solana client and program workflows with Light Protocol compressed accounts, compressed PDAs, nullifier PDAs, and ZK Compression SDKs. It helps generate implementation guidance, code patterns, shell commands, and troubleshooting references for TypeScript, Rust, Anchor, and native Solana projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live-network examples may use a Solana keypair, RPC API key, or transaction instructions that affect wallet funds or deployed programs. <br>
Mitigation: Prefer localnet or devnet, use a low-balance development wallet, keep RPC keys private, review generated edits and dependency installs, and explicitly approve any mainnet transaction, deployment, close, burn, or reinitialize action before it runs. <br>


## Reference(s): <br>
- [ZK Compression documentation](https://www.zkcompression.com) <br>
- [Compressed PDAs](references/compressed-pdas.md) <br>
- [Client guide](references/client.md) <br>
- [Nullifier PDAs](references/nullifier-pdas.md) <br>
- [Error codes reference](references/error-codes.md) <br>
- [light-sdk API docs](https://docs.rs/light-sdk/latest/light_sdk/) <br>
- [light-client API docs](https://docs.rs/light-client/latest/light_client/) <br>
- [@lightprotocol/stateless.js API docs](https://lightprotocol.github.io/light-protocol/stateless.js/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference project files, Solana wallets, RPC keys, CLI tools, SDK versions, and network-specific transaction steps.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
