## Description:

The X Platform Agent provides public X/Twitter social listening, post analytics, profile extraction, and network intelligence through the Teneo Protocol SDK.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agents, businesses, researchers, and marketers use this skill to retrieve and analyze public X/Twitter posts, profiles, engagement, sentiment, trends, and network data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet payment flows and spending limits can expose users to unintended USDC transactions.

Mitigation: Use a dedicated low-balance wallet, confirm every payment prompt, and verify spending limits before connecting.

Risk: The npm dependency supply chain can introduce package or version risks.

Mitigation: Pin and review npm dependency versions before installing or running the SDK.

Risk: Private keys or seed phrases could be exposed if entered into an unsafe runtime or configuration flow.

Mitigation: Do not expose seed phrases or private keys to the SDK process; use wallet signing flows and environment isolation.

## Reference(s):

- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [Teneo Protocol](https://teneo-protocol.ai)
- [Teneo Agent SDK NPM Package](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [Teneo Agent SDK GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require wallet signing and USDC payment configuration for Base, Peaq, or Avalanche.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
