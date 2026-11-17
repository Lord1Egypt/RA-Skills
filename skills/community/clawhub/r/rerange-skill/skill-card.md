## Description:

Build, preview, monitor, rerange, close, and risk-check non-custodial Rerange liquid orders using @rerange/wagmi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rerange](https://clawhub.ai/user/rerange)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, portfolio agents, treasury agents, wallet-connected assistants, and permissionless resolvers use this skill to discover Rerange deployments, construct and preview non-custodial liquidity orders, monitor order state, manage vault delegation, compose bounded strategies, and apply safety checks before transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can use arbitrary RPC endpoints, which could mislead DeFi reads and financial checks.

Mitigation: Use trusted RPC endpoints and compare critical reads across providers before opening, reranging, or closing orders.

Risk: State-changing Rerange actions depend on the calling agent and wallet runtime for safety controls.

Mitigation: Require fresh preview, wallet simulation, and explicit wallet confirmation before any transaction is submitted.

Risk: Autonomous agents with broad vault permissions could expose user assets.

Mitigation: Avoid giving agents withdrawal authority and limit delegation to scoped, time-limited order management.

Risk: Dependency updates can change SDK behavior used to encode calls and resolve deployment metadata.

Mitigation: Pin and review dependencies before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rerange/skills/rerange-skill)
- [Publisher profile](https://clawhub.ai/user/rerange)
- [Rerange homepage](https://rerange.xyz)
- [Rerange protocol deployments](https://github.com/rerange-xyz/info/tree/main/protocol/deployments)
- [Rerange protocol ABIs](https://github.com/rerange-xyz/info/tree/main/protocol/abi)
- [Rerange protocol interfaces](https://github.com/rerange-xyz/info/tree/main/protocol/interfaces)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance, JSON-shaped transaction and safety outputs, encoded calldata, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled Node helper can print deployments and ABIs, encode calldata, and perform read-only contract calls; write paths are represented as unsigned transaction intent for wallet simulation and confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
