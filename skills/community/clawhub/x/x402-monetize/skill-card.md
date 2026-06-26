## Description: <br>
Creates paid API endpoints using the x402 micropayment protocol by wrapping existing Zo skills and tools behind per-request payment walls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to expose existing scripts, Zo skills, or tools as paid HTTP API endpoints using x402 payment middleware. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes running an always-available paid API service from the user's environment. <br>
Mitigation: Review whether that service exposure is intended before installation or deployment. <br>
Risk: x402 payment configuration, wallet or payout settings, endpoint data sources, and financial outputs can affect real payments or user-facing financial results. <br>
Mitigation: Verify payment configuration, payout details, endpoint data sources, and financial outputs before making endpoints available to others. <br>


## Reference(s): <br>
- [x402 quickstart for sellers](https://docs.x402.org/getting-started/quickstart-for-sellers) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JavaScript code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance describes paid endpoint setup, example routes, payment flow, and service operation.] <br>

## Skill Version(s): <br>
1.0.15 (source: evidence release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
