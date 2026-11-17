## Description:

Cross-chain bridge operations using the xflows CLI (Wanchain XFlows) for wallet management, route discovery, quotes, cross-chain sends, same-chain transfers, status tracking, and address balance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lolieatapple](https://clawhub.ai/user/lolieatapple)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to prepare and execute EVM cross-chain bridge transactions, same-chain token transfers, and balance checks through the xflows CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent sensitive wallet and transaction authority.

Mitigation: Use only test or low-value wallets, require dry runs and explicit approval before real sends, and avoid granting broader wallet access than the task needs.

Risk: Private keys or wallet passwords may be exposed through chat, shell history, or command output.

Mitigation: Avoid pasting private keys or wallet passwords into chat or command arguments, and run wallet key export commands only when intentionally needed in a protected environment.

Risk: The xflows CLI dependency may change behavior or provenance across versions.

Mitigation: Pin and verify the xflows CLI source and version before use.

## Reference(s):

- [XFlows CLI command reference](artifact/references/commands.md)
- [xflows CLI](https://github.com/wandevs/xflows-cli)
- [ClawHub skill page](https://clawhub.ai/lolieatapple/skills/xflows-bridge-skills)
- [Publisher profile](https://clawhub.ai/user/lolieatapple)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and structured CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run xflows commands that create wallets, inspect balances, quote bridge routes, submit transactions, and poll status.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
