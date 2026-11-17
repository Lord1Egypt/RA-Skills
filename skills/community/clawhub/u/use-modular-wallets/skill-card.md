## Description:

Build crypto wallets using Circle Modular Wallets SDK with passkey authentication, gasless transactions, and extensible module architecture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mscandlen3](https://clawhub.ai/user/mscandlen3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to build Circle Modular Wallet integrations with passkey registration and login, gas-sponsored user operations, batch transfers, mnemonic-based passkey recovery, and modular smart account patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example snippets persist passkey credentials in localStorage, which is not appropriate for production wallet applications.

Mitigation: Use a production-safe session or storage design, such as httpOnly cookies or an equivalent secure credential storage pattern, before handling real funds.

Risk: Wallet transfer and recovery actions can move funds or change account control if executed without sufficient user review.

Mitigation: Require explicit confirmation for destination, amount, network, token, and recovery actions; default to testnets and warn before mainnet execution.

Risk: Recovery mnemonic exposure or reuse can compromise wallet recovery and account ownership.

Mitigation: Store recovery backups outside the repository, never commit recovery phrases, and require a unique mnemonic for each account.

Risk: Unsupported chain selection or malformed transaction inputs can lead to failed or unsafe wallet operations.

Mitigation: Validate addresses, amounts, chain identifiers, token decimals, and contract targets before submitting user operations.

## Reference(s):

- [Circle Smart Account with Passkey Authentication](artifact/references/circle-smart-account.md)
- [Passkey Recovery for Circle Smart Accounts](artifact/references/passkey-recovery.md)
- [Circle Developer Docs](https://developers.circle.com/llms.txt)
- [Circle Modular Wallet Console Setup](https://developers.circle.com/wallets/modular/console-setup)
- [Circle Wallet Account Types](https://developers.circle.com/wallets/account-types)
- [Circle Smart Account Example Source](https://github.com/circlefin/modularwallets-web-sdk/blob/master/examples/circle-smart-account/index.tsx)
- [Passkey Recovery Example Source](https://github.com/circlefin/modularwallets-web-sdk/blob/master/examples/passkey-recovery/index.tsx)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet safety constraints for credentials, recovery phrases, transfer confirmation, testnet defaults, and supported chains.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
