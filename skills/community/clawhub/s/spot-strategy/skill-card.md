## Description:

Design an interruption-resilient EC2 Spot instance strategy with fallback configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

Developers and cloud infrastructure engineers use this skill to analyze exported AWS EC2 inventory, Auto Scaling configuration, and EC2 cost data, then design Spot, On-Demand, and Savings Plan fallback strategies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may share AWS inventory, Auto Scaling, and cost exports that contain sensitive account details.

Mitigation: Use exported read-only data only, limit shared data to the requested EC2 planning inputs, and remove unrelated account information before analysis.

Risk: Users may accidentally include credentials, access keys, secret keys, or unrelated secrets in pasted CLI or console output.

Mitigation: Do not provide credentials or secrets; confirm pasted data contains no credentials before processing it.

Risk: Spot planning recommendations can be unsuitable for stateful workloads or services without interruption handling.

Mitigation: Flag stateful or single-replica workloads as not Spot-safe and include graceful shutdown hooks, checkpoint patterns, and On-Demand fallback capacity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/anmolnagpal/skills/spot-strategy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with tables, inline bash examples, and optional YAML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Karpenter NodePool YAML when EKS context is detected.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
