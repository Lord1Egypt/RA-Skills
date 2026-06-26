## Description: <br>
Analyzes event sequences to produce causal dependency graphs, risk-weighted paths, and responsibility-chain attribution against protocol constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to analyze failure-event chains, map causal dependencies, estimate path risk, and identify the protocol constraint most responsible for a failure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to send causal-event and protocol data to an unverified external API using a public/shared key or self-registered key. <br>
Mitigation: Use only if the endpoint is trusted, avoid confidential or regulated data, and prefer a user-owned endpoint with a dedicated low-privilege key. <br>
Risk: External causal attribution and remediation suggestions may be incomplete or misleading for real incidents. <br>
Mitigation: Treat results as decision support and validate responsibility findings against incident records, protocol owners, and operational review before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/v19-causal-dependency-analyzer) <br>
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>
- [V19 Trust Engine](https://clawhub.com/skills/v19-trust-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown guidance with curl examples and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts event sequences and protocol constraints; responses may include causal paths, risk weights, responsibility chains, and suggested remediation.] <br>

## Skill Version(s): <br>
1.3.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
