## Description:

Provides high-performance guidance for analyzing Excel datasets with 10,000 or more rows using openpyxl streaming reads, Parquet conversion, memory optimization, chunked processing, and large-file export patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data analysts use this skill when working with large Excel datasets that require memory-conscious inspection, conversion, analysis, visualization, or export. It helps agents choose streaming, Parquet, vectorized processing, and chunked writing patterns instead of loading oversized spreadsheets directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CSV or XLSX reports can preserve formula-like strings in headers or cells.

Mitigation: Sanitize formula-like strings before sharing generated spreadsheet reports with others.

Risk: Large Excel workflows may process workbooks supplied from outside the user's trust boundary.

Mitigation: Use the skill on files the user trusts, consistent with the server security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-da-large-file-analysis)

## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workflow patterns for streaming reads, Parquet conversion, memory optimization, vectorized operations, and large-file export.]

## Skill Version(s):

2026.8.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
