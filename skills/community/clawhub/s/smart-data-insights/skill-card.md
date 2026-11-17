## Description:

Enterprise-grade data analysis assistant that cleans, analyzes, and visualizes local CSV, Excel, JSON, and TSV data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuyandong8](https://clawhub.ai/user/wuyandong8)

### License/Terms of Use:

MIT-0

## Use Case:

Business analysts, data teams, and developers use this skill to inspect local tabular datasets, clean common data quality issues, generate statistical summaries, create charts, and produce Markdown reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package installation can affect the user's Python environment if run globally.

Mitigation: Install the skill in a virtual environment and avoid sudo pip.

Risk: Generated summaries, cleaned data, charts, and reports may overwrite similarly named files near the input dataset.

Mitigation: Run analysis in a dedicated working directory, review output paths before execution, and keep backups of original data.

Risk: Reports may contain sensitive or misleading information if source data is unauthorized, private, or misinterpreted.

Mitigation: Use only data the user is authorized to analyze and review generated reports before sharing, emailing, or uploading them.

## Reference(s):

- [Data Cleaning Reference](artifact/references/data_cleaning.md)
- [Data Analysis Reference](artifact/references/data_analysis.md)
- [Visualization Reference](artifact/references/visualization.md)
- [Report Generation Reference](artifact/references/report_generation.md)
- [ClawHub Skill Listing](https://clawhub.ai/wuyandong8/skills/smart-data-insights)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Console text, JSON summaries, CSV files, PNG charts, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python dependencies and writes generated files near the input dataset or requested output path.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
