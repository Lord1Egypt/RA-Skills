## Description:

Skytekx namespace for Netsnek e.U. cloud infrastructure monitoring dashboard. Tracks resource usage, alerts on anomalies, visualizes costs, and provides optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kleberbaum](https://clawhub.ai/user/kleberbaum)

### License/Terms of Use:

MIT

## Use Case:

Developers and cloud operations teams use Skytekx to monitor AWS, GCP, Azure, or multi-cloud infrastructure, inspect alert activity during incidents, and generate cost reports with optimization recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud monitoring workflows may involve cloud credentials, alert rule changes, or incident notifications.

Mitigation: Review future implementations before granting cloud credentials, and require explicit approval before changing production alert rules or sending incident notifications.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kleberbaum/skills/skytekx)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe dashboard, alert, and cost-report workflows for cloud monitoring.]

## Skill Version(s):

0.1.0 (source: frontmatter, claw.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
