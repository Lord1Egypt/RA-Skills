## Description:

Analyzes AWS infrastructure for cost savings, including right-sizing, Reserved Instances, Savings Plans, and unused resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud engineers, FinOps practitioners, and AWS operators use this skill to identify cost-optimization opportunities and produce actionable recommendations while preserving security, scalability, and maintainability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS credentials or account data could be exposed if copied into chat or generated artifacts.

Mitigation: Do not paste credentials; use clearly artificial placeholders and verify AWS identity with safe commands such as aws sts get-caller-identity.

Risk: Cost-optimization advice could encourage cross-account data transfer or third-party reporting paths that expose AWS architecture or billing data.

Mitigation: Keep AWS access read-only or narrowly scoped, avoid agent-piped transfers to external APIs or cross-account buckets, and use vendor-native IAM role integrations when third-party tools are required.

Risk: Recommendations involving security controls or financial commitments could create operational, security, or budget impact.

Mitigation: Manually review generated commands and infrastructure changes before applying them, especially changes involving security controls, cross-account transfer, Reserved Instances, or Savings Plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/sovereign-aws-cost-optimizer-hardened)
- [Faberlens safety evaluation](https://faberlens.ai/explore/sovereign-aws-cost-optimizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration examples, and architecture guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses artificial placeholders for credentials and asks users to review generated commands or infrastructure changes before applying them.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
