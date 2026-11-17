## Description:

Generate warehouse analytics charts, table images, and report-ready visuals from SQLite/CSV data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinmayagit](https://clawhub.ai/user/chinmayagit)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to generate warehouse reporting visuals and summary files from local SQLite or CSV-backed warehouse data for PDF or slide reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Python scripts read the selected warehouse database and write files to the chosen output directory.

Mitigation: Run the skill only against intended local databases and choose an output directory where generated report files are expected.

Risk: Generated CSV files may carry spreadsheet risks when product data comes from untrusted sources.

Mitigation: Sanitize generated CSV content before opening it in spreadsheet software.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; generated report files include PNG images, CSV data, and text summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a selected warehouse database and writes report assets to the chosen local output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
