## Description:

xlsx-data-wizard helps agents create, read, modify, format, merge, and visualize Excel workbooks using openpyxl-oriented workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and spreadsheet automation users use this skill to guide an agent through Excel report generation, template filling, batch workbook processing, formatting, charting, and workbook troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workbook write operations can overwrite files, delete sheets, or otherwise change important spreadsheet data.

Mitigation: Work on copies of important spreadsheets and require explicit confirmation before overwriting files or deleting sheets.

Risk: The artifact contains contradictory API credential guidance even though the inspected skill does not clearly define a legitimate external API integration.

Mitigation: Do not provide API keys or credentials based on this skill alone; require a separately validated integration need before handling credentials.

Risk: Spreadsheet contents may include sensitive business or personal data.

Mitigation: Avoid logging sensitive cell values, credentials, or tokens, and review generated code before running it on confidential workbooks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/xlsx-data-wizard)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate or modify .xlsx workbooks when the agent executes the proposed code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
