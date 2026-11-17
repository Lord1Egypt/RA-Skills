## Description:

Browser screenshots and vision over MCP Streamable HTTP with x402 USDC micropayments; paid tools require an x402-aware MCP client and funded wallet, and URLs and page-derived data are processed off-host.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildinhk](https://clawhub.ai/user/buildinhk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect agents to a remote MCP service that captures public HTTPS page screenshots and can return vision analysis after x402 USDC payment authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid endpoints require x402 payment authorization from a funded signer.

Mitigation: Verify discovery.json pricing and payment network before use, and use a limited funded wallet or controlled signer.

Risk: Submitted URLs, screenshots, prompts, and page-derived data are processed off-host.

Mitigation: Use only public, non-sensitive HTTPS URLs and avoid private, internal, auth-gated, or secret-bearing content.

Risk: Clients that cannot attach x402 payment proofs cannot complete paid screenshot or analysis calls.

Mitigation: Use an x402-aware MCP client for paid tools, or limit usage to free discovery and health checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/buildinhk/skills/screenshots-for-ai-agents)
- [Screenshot x402 homepage](https://screenshotx402.com)
- [Screenshot x402 discovery](https://screenshotx402.com/discovery.json)
- [Screenshot x402 API reference](https://screenshotx402.com/docs)
- [x402](https://www.x402.org/)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [images, text, configuration, guidance]

**Output Format:** [MCP tool results with image content, JSON strings, and optional text analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid screenshot and analysis tools require x402 payment authorization; the free health check returns a JSON string.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
