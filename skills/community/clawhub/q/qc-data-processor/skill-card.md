## Description:

Quality control data analysis MCP server for parsing QC data, running SPC control charts and process capability analysis, performing reliability and Weibull analysis, and generating QC reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daizehua-wq](https://clawhub.ai/user/daizehua-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Quality engineers, manufacturing teams, and developers use this skill to parse CSV or Excel QC datasets, run SPC and reliability analysis, and generate Markdown QC reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP tools can read CSV or Excel paths available to the server process without built-in path scoping.

Mitigation: Run the server with filesystem access limited to the intended QC data directory and avoid broad home, shared-drive, customer, finance, or HR locations unless authorized.

Risk: Dependencies are specified as version ranges rather than a reviewed lockfile.

Mitigation: Use pinned dependencies or a reviewed lockfile before production deployment.

Risk: Statistical outputs may influence quality or reliability decisions if source columns, specifications, or assumptions are wrong.

Mitigation: Have a qualified reviewer validate the dataset, selected columns, specification limits, and analysis assumptions before acting on the results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daizehua-wq/skills/qc-data-processor)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [JSON analysis results and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports CSV, XLSX, and XLS inputs; outputs text and JSON data without images or GUI.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
