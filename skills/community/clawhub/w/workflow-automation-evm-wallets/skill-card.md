## Description:

Creates, configures, simulates, deploys, monitors, and cancels on-chain automation workflows on supported EVM networks using the Ditto Network SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vladislavshad](https://clawhub.ai/user/vladislavshad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn requested EVM automation tasks into Ditto Network workflow scripts for recurring transfers, swaps, contract calls, event triggers, monitoring, and cancellation. It is intended for workflows that require wallet signing, IPFS upload, smart account funding, and on-chain registration on supported testnet or production chains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-signing automation can expose real funds if used with a primary or high-value wallet.

Mitigation: Use a dedicated low-value wallet, keep private keys in environment variables, and review every generated workflow before signing or deployment.

Risk: Unpinned SDK or tooling versions can change generated workflow behavior over time.

Mitigation: Pin and verify package versions with a lockfile before installing or running generated commands.

Risk: Production-chain deployment can move or approve real assets.

Mitigation: Test on a supported testnet first and require explicit user confirmation before setting production deployment options or funding a production smart account.

Risk: The production swap recipe uses unsafe placeholder bounds such as zero minimum output and a long deadline.

Mitigation: Replace the example with verified token and router addresses, bounded slippage, short deadlines, and clear spend limits before any production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/vladislavshad/skills/workflow-automation-evm-wallets)
- [Ditto Workflow SDK repository referenced by artifact](https://github.com/dittonetwork/ditto-workflow-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include environment configuration, package installation commands, workflow scripts, simulation, deployment, monitoring, and cancellation steps.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-03-20; artifact metadata reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
