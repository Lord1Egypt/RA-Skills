## Description: <br>
Gives an AI agent a Sui wallet for account management, network switching, transaction review, and transaction signing through a local server and Chrome extension. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building or testing Sui DApps use this skill to let an agent operate a local wallet interface for accounts, networks, and signing workflows. It is especially relevant when an agent needs to inspect pending requests before approving or rejecting Sui transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated localhost endpoints expose seed phrases and signing controls that websites or local processes could abuse. <br>
Mitigation: Use only test wallets or throwaway funds unless the local server is hardened with authentication, strict origin checks, and explicit per-request approval. <br>
Risk: Direct signing and sign-and-execute endpoints can authorize Sui transactions without the protections expected from a production wallet. <br>
Mitigation: Review pending transaction details before approval and avoid using real SUI until the exposed signing APIs are secured. <br>


## Reference(s): <br>
- [Sui Agent Wallet on ClawHub](https://clawhub.ai/EasonC13/sui-agent-wallet) <br>
- [Sui Testnet Faucet](https://faucet.testnet.sui.io/) <br>
- [Sui Devnet Faucet](https://faucet.devnet.sui.io/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with shell commands, curl examples, and JSON API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes local HTTP and WebSocket wallet operations for Sui account, network, and signing workflows.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
