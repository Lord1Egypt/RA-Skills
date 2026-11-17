## Description:

Manage construction unit price databases: update prices, track vendors, apply location factors, maintain historical records. Essential for accurate estimating.

This skill is ready for commercial/non-commercial use.

## Publisher:

[datadrivenconstruction](https://clawhub.ai/user/datadrivenconstruction)

### License/Terms of Use:

MIT

## Use Case:

Construction estimators, cost engineers, and project teams use this skill to maintain unit price records, look up current and historical prices, compare vendor quotes, apply regional adjustments, and generate database status reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local CSV import/export and spreadsheet workflows can expose users to untrusted file content, formula-like text fields, dependency drift, or accidental file overwrites.

Mitigation: Install in an isolated environment with a pinned pandas version, import CSVs only from trusted sources, choose export paths deliberately, and sanitize spreadsheet formula characters before sharing or opening exported CSV files.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples, structured price records, CSV-oriented import/export guidance, and generated report text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include last-update dates for price lookups and flag prices older than 12 months as potentially stale.]

## Skill Version(s):

2.0.0 (source: server release metadata and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
