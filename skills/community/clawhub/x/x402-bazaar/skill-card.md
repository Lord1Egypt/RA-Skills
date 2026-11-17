## Description:

x402 Bazaar protocol guide for AgentPMT - implement the HTTP 402 two-step handshake, sign EIP-3009 TransferWithAuthorization, route through the AgentPMT facilitator, and settle USDC payments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build or debug AgentPMT x402 payment flows for credit purchases and agent-to-agent commerce using USDC on Base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet authorizations can move USDC if signed against the wrong challenge, payee, amount, token, chain, nonce, or endpoint.

Mitigation: Before signing, verify the payee, amount, token, chain, nonce, endpoint, and returned server challenge; do not reuse nonces.

Risk: Endpoint, schema, setup, or example guidance may be stale because the artifact's freshness date is older than seven days.

Mitigation: Refresh or reinstall the skill from ClawHub before relying on current AgentPMT endpoints, schemas, setup steps, or examples.

## Reference(s):

- [AgentPMT External Agent API](https://www.agentpmt.com/external-agent-api)
- [X402 Bazaar on ClawHub](https://clawhub.ai/agentpmt/skills/x402-bazaar)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown with inline code blocks, request examples, endpoint tables, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on x402 payment handshakes, EIP-3009 authorization signing, AgentPMT API endpoints, EIP-191 request messages, and payment-related error recovery.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
