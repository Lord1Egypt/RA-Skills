## Description: <br>
Analyzes AWS infrastructure for cost savings. Right-sizing, Reserved Instances, Savings Plans, unused resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, cloud engineers, and FinOps teams use this skill to review AWS infrastructure for cost savings opportunities while preserving security, scalability, and maintainability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AWS cost recommendations can lead to real infrastructure changes, commitments, or purchases if followed without review. <br>
Mitigation: Review generated AWS CLI, IaC, Reserved Instance, and Savings Plan recommendations before running commands or purchasing commitments. <br>
Risk: AWS cost analysis may involve sensitive account, architecture, and billing data. <br>
Mitigation: Use least-privilege AWS access and do not paste real AWS credentials into chat. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/sovereign-aws-cost-optimizer-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/sovereign-aws-cost-optimizer) <br>
- [Safety evaluation artifact](artifact/SAFETY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with analysis, code examples, configuration snippets, shell commands, and architecture guidance where relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses artificial placeholders in examples and avoids exposing real AWS credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
