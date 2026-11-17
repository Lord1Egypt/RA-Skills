## Description:

Load, explore, clean, analyze, and visualize CSV data to provide statistical summaries, correlations, filtered views, and charts for insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[underbench2-gif](https://clawhub.ai/user/underbench2-gif)

### License/Terms of Use:


## Use Case:

Developers, analysts, and business users use this skill to have an agent inspect CSV datasets, clean data, compute descriptive statistics and correlations, create charts, and summarize findings in plain language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV files may contain private or sensitive data that could appear in summaries, charts, or exported cleaned datasets.

Mitigation: Use approved datasets, review generated outputs before sharing, and avoid retaining unnecessary derived files.

Risk: Generated charts or cleaned CSV exports may be written to the workspace.

Mitigation: Confirm output locations, inspect generated files, and remove exports that are not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/underbench2-gif/skills/ub2-csv-data-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown summaries with optional code or shell commands, plus generated PNG charts and cleaned CSV files when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a valid CSV input; Python with pandas and matplotlib should be available for analysis and visualization workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
