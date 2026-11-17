## Description:

Generate professional data reports (HTML/PDF-ready) with KPI summaries, charts, tables, executive insights, and recommendations from CSV, Excel, or JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plgonzalezrx8](https://clawhub.ai/user/plgonzalezrx8)

### License/Terms of Use:


## Use Case:

Business analysts, operators, and executives use this skill to turn structured CSV, Excel, or JSON data into concise KPI reports, dashboards, charts, and recommendations for recurring business reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports and chart images may contain sensitive data from the supplied input file.

Mitigation: Provide only data files intended for analysis and review generated HTML and chart files before sharing them.

Risk: Dirty, missing, or mismapped fields can produce misleading KPI summaries or charts.

Mitigation: Validate input columns, request mappings when required numeric fields are missing, and sanity-check numbers and narrative consistency before using the report.

Risk: The bundled script supports only CSV, Excel, or JSON input and writes local HTML output rather than a complete PDF workflow.

Mitigation: Use supported structured inputs, keep file operations within the intended workspace, and apply a separate reviewed conversion step if PDF output is required.

## Reference(s):

- [Report Templates](references/report-templates.md)
- [Chart Guidelines](references/chart-guidelines.md)
- [ClawHub Skill Page](https://clawhub.ai/plgonzalezrx8/skills/report-generator-pedro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and optional local HTML report files with chart images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script writes a local HTML report and companion chart image when supplied with a supported CSV, Excel, or JSON input file.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
