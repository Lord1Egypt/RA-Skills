## Description: <br>
Quantum Distribution Generator helps agents request probability distribution samples, Monte Carlo samples, and random walks through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill when an agent needs to generate exponential, Poisson, binomial, beta, gamma, Monte Carlo, or random-walk samples for simulation, risk analysis, queuing models, A/B testing, Bayesian estimation, or related statistical workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can invoke a paid external AgentPMT API. <br>
Mitigation: Enable it only for workflows that intentionally use AgentPMT sampling calls, and confirm account, credential, credit, or payment setup before invocation. <br>
Risk: The skill may require sensitive account, wallet, or payment credentials through the AgentPMT setup path. <br>
Mitigation: Use the setup guidance for credential handling and do not place secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>
Risk: Broad activation keywords such as beta, source, and count could trigger the skill for unrelated requests. <br>
Mitigation: Invoke it only when the user explicitly needs statistical sampling, simulation, or the named Quantum Distribution Generator operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/quantum-distribution-generator) <br>
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/quantum-distribution-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance, configuration] <br>
**Output Format:** [Markdown instructions with JSON request examples and JSON tool responses from AgentPMT calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill uses AgentPMT account setup and paid remote calls; supported operations include beta, binomial, exponential, gamma, montecarlo_sample, poisson, and randomwalk.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
