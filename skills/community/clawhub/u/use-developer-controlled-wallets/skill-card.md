## Description: <br>
Create and manage Circle developer-controlled wallets where an application retains custody of wallet keys on behalf of end users, covering wallet sets, entity secret registration, token transfers, and balance checks via Circle's developer-controlled wallets SDK. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mscandlen3](https://clawhub.ai/user/mscandlen3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement Circle developer-controlled wallet workflows, including wallet creation, entity secret registration guidance, receiving funds, transfers, and balance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles custody credentials, Circle API keys, entity secrets, and recovery files. <br>
Mitigation: Keep credentials and recovery files out of chat, logs, and repositories; use environment variables or a secrets manager and store recovery files outside the project root. <br>
Risk: A reference example may print sensitive recovery-file contents. <br>
Mitigation: Remove or avoid logging recovery-file data before using the workflow with real wallets. <br>
Risk: Wallet transfers can move real funds, especially on mainnet. <br>
Mitigation: Start on testnet and require explicit human confirmation of destination, amount, network, and token before any mainnet transfer. <br>
Risk: Unpinned SDK dependencies can change wallet behavior or supply-chain exposure. <br>
Mitigation: Pin the Circle SDK dependency and review dependency updates before deployment. <br>


## Reference(s): <br>
- [Register Your Entity Secret](references/register-secret.md) <br>
- [Create Your First Developer-Controlled Wallet](references/create-dev-wallet.md) <br>
- [Receive an Inbound Transfer](references/receive-transfer.md) <br>
- [Transfer Tokens Across Wallets](references/check-balance-and-transfer-tokens.md) <br>
- [Circle Developer Docs](https://developers.circle.com/llms.txt) <br>
- [Register Entity Secret](https://developers.circle.com/wallets/dev-controlled/register-entity-secret) <br>
- [Circle Wallet Account Types](https://developers.circle.com/wallets/account-types) <br>
- [USDC Token IDs](https://developers.circle.com/wallets/monitored-tokens#usdc-token-ids) <br>
- [List Wallet Balance API](https://developers.circle.com/api-reference/wallets/developer-controlled-wallets/list-wallet-balance) <br>
- [Circle Faucet](https://faucet.circle.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SDK calls that require Circle API credentials and explicit human confirmation before fund transfers.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
