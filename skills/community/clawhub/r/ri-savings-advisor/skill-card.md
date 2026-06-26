## Description: <br>
Recommend optimal Reserved Instance and Savings Plan portfolio based on AWS usage patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Cloud finance, FinOps, and AWS infrastructure teams use this skill to analyze exported AWS cost, usage, Savings Plans, and Reserved Instance data and plan commitment-based discount coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste AWS access keys, secret keys, session tokens, account identifiers, or sensitive business details with billing exports. <br>
Mitigation: Review pasted data before analysis and remove credentials, tokens, account identifiers, and sensitive business details. <br>
Risk: Savings recommendations can influence financial commitments and may be wrong if the supplied usage data is incomplete or stale. <br>
Mitigation: Treat the output as planning guidance and have finance or cloud owners verify assumptions before making AWS purchasing decisions. <br>
Risk: Generating source reports may require AWS account access. <br>
Mitigation: Use a least-privilege read-only role or profile for Cost Explorer and reservation inventory exports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/ri-savings-advisor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables and inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-supplied exported AWS billing and reservation data; does not require credentials or direct AWS account access.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
