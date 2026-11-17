## Description:

生成传输单边故障日报报表，按考核周期统计，包含原始清单。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wede375](https://clawhub.ai/user/wede375)

### License/Terms of Use:

MIT-0

## Use Case:

Operations and network-reporting teams use this skill to generate Chinese-language Excel daily reports for transmission single-sided fault data. The report groups records by assessment period, calculates ticket counts, durations, timeout counts, timely rates, and keeps the source rows for audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input and generated Excel workbooks may contain sensitive operational fault records, and the output includes a raw-data sheet.

Mitigation: Review the raw-data sheet before sharing generated workbooks and handle input and output files under the same data-access controls as the source fault records.

Risk: The script uses hardcoded local input and output paths and a fixed workbook filename.

Mitigation: Review or adjust the paths before running the skill in a new workspace.

Risk: Dependency installation may pull unpinned package versions.

Mitigation: Install pandas and openpyxl in a virtual environment with pinned versions appropriate for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wede375/skills/transmission-daily-report-generator)
- [Usage README](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [Files, Analysis, Shell commands, Guidance]

**Output Format:** [Excel workbook with console status text and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a timestamped .xlsx workbook with an annual summary sheet, one sheet per assessment period with data, and a raw-data sheet.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
