## Description:

Create and manage Circle developer-controlled wallets where the application retains full custody of wallet keys on behalf of end-users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mscandlen3](https://clawhub.ai/user/mscandlen3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to implement Circle developer-controlled wallet workflows, including entity secret registration, wallet set and wallet creation, inbound funding checks, balance lookup, and token transfers. It is intended for applications where the developer retains custody of wallet keys on behalf of end users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles custody credentials and wallet recovery material.

Mitigation: Require secrets manager or environment variable handling, keep recovery files outside the repository, and remove any logging of recovery-file contents before production use.

Risk: The skill can help create value-moving wallet transactions.

Mitigation: Require explicit human confirmation of destination, amount, network, and token before every transfer, with extra warning for mainnet or larger transfers.

Risk: Mutating wallet API calls can be duplicated if they lack idempotency controls.

Mitigation: Use UUID v4 idempotency keys for every mutating request.

Risk: Broad activation could apply wallet guidance outside explicit Circle developer-controlled wallet requests.

Mitigation: Use the skill only for explicit Circle developer-controlled wallet workflows and route other wallet custody models to the appropriate skill.

## Reference(s):

- [Register Your Entity Secret](references/register-secret.md)
- [Create Your First Developer-Controlled Wallet](references/create-dev-wallet.md)
- [Receive an Inbound Transfer](references/receive-transfer.md)
- [Transfer Tokens Across Wallets](references/check-balance-and-transfer-tokens.md)
- [Circle Developer Docs](https://developers.circle.com/llms.txt)
- [Register Entity Secret](https://developers.circle.com/wallets/dev-controlled/register-entity-secret)
- [Circle Account Types](https://developers.circle.com/wallets/account-types)
- [List Wallet Balance API](https://developers.circle.com/api-reference/wallets/developer-controlled-wallets/list-wallet-balance)
- [USDC Token IDs](https://developers.circle.com/wallets/monitored-tokens#usdc-token-ids)
- [Circle Faucet](https://faucet.circle.com)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet setup steps, SDK usage snippets, environment variable guidance, transfer confirmation checks, and security warnings.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
