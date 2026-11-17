## Description:

Connects to SQL Server to retrieve and generate monthly, quarterly, and yearly delivery order reports with performance comparisons and growth metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyawzo-ptcl](https://clawhub.ai/user/kyawzo-ptcl)

### License/Terms of Use:

MIT-0

## Use Case:

Warehouse managers and logistics teams use this skill to retrieve delivery order summaries and comparison reports without writing SQL manually.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release exposes database credentials.

Mitigation: Rotate the exposed database password, move credentials to a secure secret source, and restrict the database account to read-only least privilege before installation.

Risk: Unsupported commands can return broad internal delivery data.

Mitigation: Change unknown commands to fail closed and require specific authorized report commands and date filters.

Risk: Generic triggers may invoke reporting in unintended contexts.

Mitigation: Replace broad triggers with specific business-approved triggers for delivery reporting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyawzo-ptcl/skills/sql-reports)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text report tables with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces delivery summaries and comparisons from SQL Server data; unsupported commands may return broad delivery records.]

## Skill Version(s):

1.0.0 (source: skill.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
