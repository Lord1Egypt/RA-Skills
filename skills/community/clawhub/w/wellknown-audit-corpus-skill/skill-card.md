## Description: <br>
Audit an agent/API origin for well-known discovery, x402 pricing, OpenAPI/MCP readiness, and install blockers before an agent integrates it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebastiancoombs](https://clawhub.ai/user/sebastiancoombs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to evaluate whether an agent/API origin is ready for integration, payment, or troubleshooting before relying on it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid x402 calls can spend funds when an agent follows the workflow against backend endpoints. <br>
Mitigation: Use wallet spend limits, approval controls, and review the 402 payment requirement before signing. <br>
Risk: The optional installer writes files into a buyer-selected skills directory and can overwrite an existing copy when forced. <br>
Mitigation: Install to an explicit target directory, run package verification, and avoid --force unless replacement is intentional. <br>
Risk: External discovery and API content can be incomplete, unavailable, or misleading. <br>
Mitigation: Treat external responses as evidence, report uncertainty, and avoid treating a missing or failed upstream as proof of safety. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sebastiancoombs/wellknown-audit-corpus-skill) <br>
- [Backend readiness service](https://wellknown-audit-corpus.mtree.workers.dev) <br>
- [Package security notes](PACKAGE_SECURITY.md) <br>
- [Capability manifest](CAPABILITIES.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with optional JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include allow/fix/reject decisions, missing readiness surfaces, x402 cost evidence, and setup friction.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
