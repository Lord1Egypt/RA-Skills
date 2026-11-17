## Description:

Generate secure random string tokens for API keys, session tokens, password reset links, and related authentication use cases through AgentPMT-hosted remote tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request configurable random tokens for API keys, session identifiers, password reset links, 2FA codes, secure URLs, and cryptographic nonces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party service may generate values that become credentials or other sensitive authentication material.

Mitigation: For production secrets, prefer local OS CSPRNG generation or provider-blind designs; when using this skill, keep requests minimal, avoid logging tokens, and verify provider retention and logging controls.

Risk: Setup paths can rely on mutable remote installs such as npx-based skill installation.

Mitigation: Pin or audit setup skills and install commands before use in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/quantum-secure-token-generator)
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/quantum-secure-token-generator)
- [Quantum Secure Token Generator schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON responses containing generated token strings and request metadata, with Markdown instructions for tool invocation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Token length is configurable from 8 to 256 characters; charset options are alphanumeric, hex, base64, and printable ASCII without whitespace.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
