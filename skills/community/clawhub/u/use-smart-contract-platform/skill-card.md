## Description:

Helps agents deploy, import, interact with, and monitor smart contracts through Circle Smart Contract Platform APIs, including template deployments, ABI calls, bytecode deployments, and webhook event monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mscandlen3](https://clawhub.ai/user/mscandlen3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build Circle Smart Contract Platform workflows for testnet-first smart contract deployment, contract imports, ABI reads and writes, and event monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Smart contract deployments and write transactions can trigger high-impact blockchain actions.

Mitigation: Install only where Circle credentials stay server-side, use testnet by default, and require manual confirmation before mainnet or value-moving actions.

Risk: Deployment examples can be unsafe to reuse directly if retry and idempotency handling is incomplete.

Mitigation: Add UUID v4 idempotency keys to mutating requests and review retry behavior before production use.

Risk: Dependency or credential handling mistakes could expose Circle API keys or entity secrets.

Mitigation: Pin and review npm dependencies and keep API keys and entity secrets out of frontend code, logs, and committed files.

## Reference(s):

- [Deploy Smart Contract with Bytecode](references/deploy-bytecode.md)
- [Deploy ERC-1155 Template](references/deploy-erc-1155.md)
- [Interact with a Deployed Contract](references/interact.md)
- [Monitor Smart Contract Events](references/monitor-events.md)
- [Contracts Templates](references/templates.md)
- [Circle Developer Docs](https://developers.circle.com/llms.txt)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, shell, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes testnet-first workflows, credential-handling guidance, idempotency requirements, and transaction confirmation checkpoints.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
