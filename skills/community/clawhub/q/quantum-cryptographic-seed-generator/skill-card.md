## Description: <br>
Generate cryptographic seeds, UUIDs, tokens, passwords, and prime numbers using quantum-derived or standard cryptographic randomness through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to request AgentPMT-generated seeds, UUIDs, tokens, passwords, and prime numbers for cryptographic workflows, API/session credentials, database identifiers, and auditable randomness. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated passwords, tokens, seeds, or primes are produced through AgentPMT's remote service rather than entirely local execution. <br>
Mitigation: Use this skill only when remote generation is acceptable for the intended secret material; require local generation for secrets that must never leave the local environment. <br>
Risk: Broad prompts about passwords or tokens may activate this skill when a different credential workflow was intended. <br>
Mitigation: Confirm the intended tool and action before invoking the remote service, especially for credential-related requests. <br>
Risk: Account secrets, wallet keys, mnemonics, signatures, or payment headers could be exposed if included in prompts or logs. <br>
Mitigation: Keep inputs scoped to the minimum required parameters and use the AgentPMT setup skills for credential handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/quantum-cryptographic-seed-generator) <br>
- [AgentPMT marketplace product](https://www.agentpmt.com/marketplace/quantum-cryptographic-seed-generator) <br>
- [Generated action schema](artifact/schema.md) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown guidance with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes remote AgentPMT tool calls; the remote service returns JSON responses and no local command runtime is declared.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
