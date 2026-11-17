## Description:

Analyze AWS Cost & Usage Reports to identify top cost drivers, waste, and anomalies across all linked accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmolnagpal](https://clawhub.ai/user/anmolnagpal)

### License/Terms of Use:


## Use Case:

FinOps practitioners, cloud engineers, and account owners use this skill to analyze exported AWS billing data, identify cost drivers and anomalies, and prioritize savings actions without granting account access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: AWS billing exports and Cost Explorer output can reveal account names, service usage, spending patterns, and business activity.

Mitigation: Use only exported billing data or redacted read-only command output, and remove sensitive account details that are not needed for analysis.

Risk: Providing AWS credentials or secret keys would expose account access unnecessarily.

Mitigation: Do not provide credentials, access keys, or secret keys; the skill is instruction-only and does not require direct AWS access.

## Reference(s):

- [Spend Analyzer ClawHub listing](https://clawhub.ai/anmolnagpal/skills/spend-analyzer)
- [Anmol Nagpal ClawHub profile](https://clawhub.ai/user/anmolnagpal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with tables, bullet lists, and optional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an executive summary, top cost drivers table, anomaly flags, and a ranked savings action list.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
