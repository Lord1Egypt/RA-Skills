## Description:

Quantum Cryptographic Seed Generator helps an agent generate cryptographic seeds, UUIDs, tokens, passwords, and prime numbers using AgentPMT-hosted remote tool calls with quantum-derived randomness or standard cryptographic randomness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to request secure passwords, API or session tokens, UUIDs, cryptographic seeds, and prime candidates from the AgentPMT-hosted Quantum Cryptographic Seed Generator. It is suited for workflows that need configurable random material and can accept the trust model of a remote generation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote generation can expose passwords, bearer tokens, encryption seeds, or RSA private-key factors to the service operator.

Mitigation: Use the skill only when AgentPMT is trusted with the generated secret material; for production secrets, prefer local generation or combine remote randomness with trusted local entropy.

Risk: Companion setup paths and endpoints may affect credential handling.

Mitigation: Review the setup skill before use and prefer pinned or verified installation paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/quantum-cryptographic-seed-generator)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/quantum-cryptographic-seed-generator)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill describes AgentPMT actions for password, token, UUID, seed, prime, and prime_pair generation.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
