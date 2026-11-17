## Description:

Generates professional Python matplotlib visualization code by selecting chart types from the data and applying BCG, The Economist, or McKinsey-style templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezvg](https://clawhub.ai/user/veezvg)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts, consultants, researchers, and content creators use this skill to turn tabular or survey-style data requests into runnable matplotlib scripts for report-style charts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example scripts write chart image files to local output paths.

Mitigation: Review and adjust generated or example output filenames before running scripts in a working directory.

Risk: Generated code may reference a hard-coded macOS Chinese font path.

Mitigation: Change the font path for non-macOS environments or when Chinese labels are not needed.

## Reference(s):

- [Chart Selection Guide](references/chart_selection.md)
- [Visualization Specification](references/visualization_spec.md)
- [Making Economist-Style Plots in Matplotlib](https://medium.com/data-science/making-economist-style-plots-in-matplotlib-e7de6d679739)

## Skill Output:

**Output Type(s):** [code, markdown, guidance]

**Output Format:** [Markdown containing runnable Python matplotlib code blocks and brief chart-selection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scripts may save image files to local output paths and may require environment-specific font adjustments.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
