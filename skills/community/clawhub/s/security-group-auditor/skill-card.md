## Description: <br>
Audit AWS Security Groups and VPC configurations for dangerous internet exposure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anmolnagpal](https://clawhub.ai/user/anmolnagpal) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, cloud engineers, and security reviewers use this skill to analyze user-provided AWS Security Group, EC2, VPC, and subnet exports for risky internet exposure and to draft tightened rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS network configuration exports may include sensitive infrastructure details or accidental secrets. <br>
Mitigation: Use read-only AWS permissions, review exported JSON before sharing it with the agent, and remove credentials, access keys, or unrelated secrets. <br>
Risk: Generated security group changes may be incomplete or disrupt intended access if applied without review. <br>
Mitigation: Manually review proposed rule changes, validate business-approved source ranges, and test changes before applying them in production. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/anmolnagpal/security-group-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Markdown findings with tables, AWS CLI examples, corrected security group JSON, AWS Config rule recommendations, and remediation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; analyzes user-provided exports and does not access AWS accounts or execute commands directly.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
