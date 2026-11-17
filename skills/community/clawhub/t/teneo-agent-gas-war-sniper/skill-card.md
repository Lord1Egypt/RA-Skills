## Description:

Gas War Sniper monitors multi-chain gas prices block by block, detects sudden spikes and likely gas-war activity, identifies contracts by address, and returns alerts and status through the Teneo SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to query a Teneo-hosted gas monitoring agent for current gas prices, block details, supported networks, gas spike monitoring, historical gas trends, and contract identification across supported EVM networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires wallet signing and uses automatic USDC payment rails.

Mitigation: Use a dedicated low-balance wallet and require explicit confirmation before any transaction or signature.

Risk: Dependency or SDK substitution could affect wallet and payment behavior.

Mitigation: Verify the SDK package and version, pin dependencies, and use a lockfile before connecting a wallet.

## Reference(s):

- [Teneo Protocol](https://teneo-protocol.ai)
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [Teneo Agent SDK NPM Package](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [Teneo Agent SDK GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk)
- [Agent Console](https://agent-console.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline command examples and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include human-readable gas data, block metadata, monitoring status, ASCII charts, network lists, and raw or structured response content from the Teneo SDK.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
