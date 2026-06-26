## Description: <br>
Portable Solana wallet operations for agents, including wallet creation, address lookup, balance checks, devnet airdrops, Ed25519 message signing, signature verification, and previewed RockPaperClaw deposits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhentan](https://clawhub.ai/user/zhentan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a local Solana wallet for devnet or explicitly selected mainnet workflows, including wallet setup, balance checks, airdrops, ownership-proof signatures, and carefully previewed RockPaperClaw deposit signing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use local Solana private key files and submit a RockPaperClaw deposit when explicitly executed. <br>
Mitigation: Use a dedicated devnet keypair where possible, explicitly set the keypair path and RPC URL, protect the keypair file, review preview output, and use --execute only after approving the exact transaction. <br>
Risk: Signing opaque payloads or running against the wrong network can produce unintended wallet actions. <br>
Mitigation: Default to devnet, require explicit approval for another network, sign only clear user-approved messages, and verify deposit metadata before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zhentan/solana-wallet-rpc) <br>
- [Circle Faucet](https://faucet.circle.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Wallet commands can create local keypair files, read configured keypairs, call Solana RPC endpoints, and return structured JSON fields such as address, balance, signatures, preview data, and transaction signatures.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
