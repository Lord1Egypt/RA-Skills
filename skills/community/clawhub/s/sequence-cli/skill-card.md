## Description:

Manage Sequence smart wallets, projects, API keys, ERC20 transfers, and query blockchain data using the Sequence Builder CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jameslawton](https://clawhub.ai/user/jameslawton)

### License/Terms of Use:


## Use Case:

Developers and automation agents use this skill to manage Sequence smart wallets, Builder projects, API keys, balances, transaction history, and ERC20 transfers across supported EVM chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blockchain transfers can move real assets and may be irreversible.

Mitigation: Use isolated wallets with limited funds and require explicit human confirmation of chain, token, amount, and recipient before any transfer.

Risk: Private keys and access keys may be exposed through command lines, logs, or chat transcripts.

Mitigation: Avoid putting secrets in command lines or chat logs; use protected local storage where appropriate and redact keys from outputs.

Risk: The skill runs a Node CLI through npx.

Mitigation: Pin and verify the CLI package version before use.

## Reference(s):

- [Sequence Builder CLI repository](https://github.com/0xsequence/builder-cli)
- [Sequence supported networks and status](https://status.sequence.info/)
- [ClawHub sequence-cli release page](https://clawhub.ai/jameslawton/skills/sequence-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-oriented CLI examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands commonly use --json output and may require Node.js, npx, wallet private keys, access keys, token addresses, recipient addresses, amounts, and chain IDs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
