## Description:

The Amazon Agent extracts Amazon product details, marketplace search results, and customer reviews through Teneo Protocol for e-commerce pricing, catalog, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teneoprotocoldev](https://clawhub.ai/user/teneoprotocoldev)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agents, businesses, and e-commerce researchers use this skill to query the Teneo Amazon agent for product details, marketplace searches, and reviews. It is intended for e-commerce pricing intelligence, catalog audits, and customer sentiment analysis using wallet-backed USDC payments through the Teneo SDK.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet-backed automatic USDC payments may cause unintended charges if authorization limits and revocation paths are unclear.

Mitigation: Use a dedicated low-balance wallet and confirm how each payment is authorized, capped, and revoked before use.

Risk: The installation command uses an unpinned SDK dependency that may change behavior over time.

Mitigation: Pin and review the @teneo-protocol/sdk version before deploying the skill.

Risk: Wallet credentials or private keys could be exposed if placed directly in application configuration.

Mitigation: Keep private keys out of checked-in configuration and use secret management appropriate for the deployment environment.

## Reference(s):

- [Amazon Agent on ClawHub](https://clawhub.ai/teneoprotocoldev/skills/teneo-agent-amazon)
- [Teneo Protocol](https://teneo-protocol.ai)
- [Teneo Agent SDK on ClawHub](https://clawhub.ai/teneoprotocoldev/teneo-agent-sdk)
- [@teneo-protocol/sdk on npm](https://www.npmjs.com/package/@teneo-protocol/sdk)
- [Teneo Agent SDK GitHub Repository](https://github.com/TeneoProtocolAI/teneo-agent-sdk)

## Skill Output:

**Output Type(s):** [text, structured data, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command syntax and TypeScript examples; runtime responses are text or structured data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid per-query commands require the Teneo SDK, Node.js 18+, wallet authentication, and USDC on a supported network.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
