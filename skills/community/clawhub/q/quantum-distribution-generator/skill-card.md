## Description: <br>
Quantum Distribution Generator guides agents in calling AgentPMT-hosted tools for sampling probability distributions, Monte Carlo samples, and random walks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate AgentPMT MCP or REST calls for statistical sampling tasks such as risk analysis, queue modeling, A/B testing, stochastic simulation, Bayesian sampling, and random walk modeling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AgentPMT calls send requests to a remote paid service and may consume credits. <br>
Mitigation: Use the skill only when remote AgentPMT statistical sampling is intended, confirm account setup, and review request parameters before execution. <br>
Risk: Credential, token, wallet, or payment details could be exposed if placed in prompts or logs during setup. <br>
Mitigation: Use the separate AgentPMT setup guidance for credential handling and keep secrets out of prompts, logs, and product-specific requests. <br>
Risk: Cached schemas or examples can become stale for production integrations. <br>
Mitigation: Fetch live schema or instructions before production use or when parameters, outputs, enum values, or examples are unclear. <br>


## Reference(s): <br>
- [Quantum Distribution Generator marketplace page](https://www.agentpmt.com/marketplace/quantum-distribution-generator) <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/quantum-distribution-generator) <br>
- [Quantum Distribution Generator Schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, API calls] <br>
**Output Format:** [Markdown with JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes MCP and REST invocation shapes, schema lookup steps, and supported action parameters; remote tool responses are JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
