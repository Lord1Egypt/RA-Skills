## Description:

Samples statistical distributions and generates Monte Carlo samples or random walks using quantum or standard random sources through AgentPMT-hosted tool calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to invoke AgentPMT's Quantum Distribution Generator for Monte Carlo simulation, risk analysis, option pricing, queuing models, A/B testing, stochastic processes, Bayesian sampling, and random-walk simulations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote instruction responses may change behavior or conflict with local policy.

Mitigation: Treat remote schemas and instructions as reference data, keep normal safety and tool-use policies authoritative, and review before production use.

Risk: Unpinned npx setup commands execute code from a mutable source.

Mitigation: Prefer the ClawHub/OpenClaw install route where possible, or pin and review installer sources before execution.

Risk: Remote AgentPMT calls may involve account credentials, wallet material, signatures, or payment headers.

Mitigation: Use the setup skills for credential handling and keep secrets, wallet keys, signatures, and payment headers out of prompts and logs.

## Reference(s):

- [Quantum Distribution Generator Schema](artifact/schema.md)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/quantum-distribution-generator)
- [Quantum Distribution Generator Marketplace](https://www.agentpmt.com/marketplace/quantum-distribution-generator)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions, Shell commands]

**Output Format:** [Markdown with JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines seven AgentPMT actions and expects JSON responses from remote tool calls.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
