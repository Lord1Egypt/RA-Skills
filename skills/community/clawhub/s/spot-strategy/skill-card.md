## Description: <br>
Design an interruption-resilient EC2 Spot instance strategy with fallback configurations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps teams use this skill to evaluate exported AWS EC2 inventory, Auto Scaling, and cost data and plan a resilient Spot, On-Demand, and Savings Plan mix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS inventory, Auto Scaling, and cost exports may contain sensitive environment details. <br>
Mitigation: Share only sanitized exports with the agent, run AWS CLI commands yourself using a least-privilege read-only role, and do not paste access keys, secret keys, session tokens, or unrelated sensitive data. <br>
Risk: Spot migration recommendations can affect workload availability if applied to stateful or interruption-sensitive systems without review. <br>
Mitigation: Review the generated eligibility matrix and fallback architecture before implementation, keep stateful workloads off Spot, and test interruption handling such as graceful shutdown and checkpoint patterns. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, AWS CLI command examples, and optional Karpenter NodePool YAML] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided exported AWS data and does not require credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
