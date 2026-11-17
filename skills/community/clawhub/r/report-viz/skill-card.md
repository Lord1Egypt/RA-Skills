## Description:

财报可视化分析 helps agents parse financial reports, extract key indicators, and generate SVG mini charts, radar charts, and multi-format financial analysis outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business teams use this skill to turn financial report data into structured analysis, visual charts, and exportable report artifacts for finance, investment, and market research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial reports, generated outputs, and data-source credentials may contain sensitive business information.

Mitigation: Provide only the files and API credentials needed for the task, and keep credentials scoped to the intended data source.

Risk: Generated SVG, PDF, Word, or image files could overwrite or expose sensitive material if written to broad or ambiguous paths.

Mitigation: Ask the agent to write outputs to a specific workspace path before generation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration]

**Output Format:** [Structured JSON and human-readable analysis, with generated SVG, PDF, Word, or image files when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user-provided financial data or data-source API credentials; generated files should be written to a user-specified workspace path.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
