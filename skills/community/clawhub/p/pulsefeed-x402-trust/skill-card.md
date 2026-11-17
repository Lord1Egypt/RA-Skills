## Description:

Checks whether an x402 payment endpoint is safe to pay and whether an npm or MCP package is safe to install before an agent spends USDC or runs unknown code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikolife2016](https://clawhub.ai/user/nikolife2016)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before paying unknown x402 endpoints, installing MCP servers or npm packages, or checking current x402 security incidents. It provides verification workflows and command examples for endpoint trust checks, package risk checks, and incident review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional npm commands may run unpinned package code when using npx or npm install.

Mitigation: Pin package versions and verify package provenance before executing optional npm commands.

Risk: Endpoint URLs and package names are sent to pulsefeed.dev during verification.

Mitigation: Avoid submitting private or sensitive endpoint and package identifiers unless disclosure to PulseFeed is acceptable.

Risk: The live deep check is paid via x402.

Mitigation: Confirm the x402 payment challenge and expected cost before authorizing the paid check.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nikolife2016/skills/pulsefeed-x402-trust)
- [PulseFeed Methodology](https://pulsefeed.dev/methodology)
- [PulseFeed A2A Agent Card](https://pulsefeed.dev/.well-known/agent-card.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown guidance with inline shell and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No API key required for the basic checks described by the skill; live deep checks are paid via x402.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
