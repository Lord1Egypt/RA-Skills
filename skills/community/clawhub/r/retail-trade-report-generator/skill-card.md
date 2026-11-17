## Description:

Generates a consolidated weekly retail trade report from 12 Excel sales files with regional, channel, product, ADA, and week-over-week analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuminmin](https://clawhub.ai/user/wuminmin)

### License/Terms of Use:


## Use Case:

Business analysts and retail operations teams use this skill to consolidate weekly channel sales spreadsheets into a formatted Excel report with regional ADA metrics, WoW comparisons, and charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads all matching spreadsheets from the configured sales-report folder and writes an output workbook to the requested path.

Mitigation: Use a dedicated input folder containing only the intended 12 spreadsheets and choose a unique output filename to avoid processing unrelated workbooks or overwriting an existing report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuminmin/skills/retail-trade-report-generator)
- [SKILL.md](artifact/SKILL.md)
- [README_CN.md](artifact/README_CN.md)
- [store_mapping.csv](artifact/references/store_mapping.csv)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and Python code that generates a formatted Excel workbook]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires 12 weekly input Excel files, a store mapping CSV, and an output workbook path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
