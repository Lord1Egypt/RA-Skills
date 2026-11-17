## Description:

SQL Database Toolkit helps agents connect to databases or local files, run and optimize SQL, create visualizations, generate statistical insights, and assemble HTML reports and dashboards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moniq888](https://clawhub.ai/user/moniq888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to connect SQL databases or local tabular files, run SQL analysis, and produce charts, insights, dashboards, and HTML reports for business data workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database access and generated SQL can expose, modify, or delete sensitive data when run with broad privileges.

Mitigation: Use read-only, least-privilege database accounts and review generated SQL before execution.

Risk: Loading untrusted data files, especially pickle formats, can create security and data-integrity risk.

Mitigation: Use trusted input files only and avoid loading .pkl or .pickle files from untrusted sources.

Risk: Generated HTML reports and interactive charts can disclose sensitive data or rely on external chart assets.

Mitigation: Review generated HTML before sharing or hosting it, and prefer offline or pinned chart assets for sensitive reports.

Risk: Dependency installation guidance may alter pip mirror configuration in ways that persist beyond this skill.

Mitigation: Avoid permanent pip mirror changes unless they are intentional and the user knows how to reverse them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moniq888/skills/sql-database-toolkit)
- [Installation guide](references/INSTALLATION.md)
- [Integration guide](references/INTEGRATION_GUIDE.md)
- [SQL security guide](references/sql-security.md)
- [SQL generation guide](references/sql-generation.md)
- [Query optimization guide](references/query-optimization.md)
- [Visualization guide](references/visualization-guide.md)
- [Dashboard guide](references/dashboard.md)
- [Templates index](references/templates-index.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with SQL, Python, and bash snippets, plus generated tabular data, PNG base64 chart strings, interactive HTML charts, and HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include executable SQL and shareable HTML artifacts; review them before running against production data or publishing.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
