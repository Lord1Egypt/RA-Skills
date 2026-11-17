## Description:

Sheetsmith helps agents inspect, summarize, filter, transform, and convert CSV, TSV, and Excel files with pandas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crimsondevil333333](https://clawhub.ai/user/crimsondevil333333)

### License/Terms of Use:


## Use Case:

Developers, analysts, and agents use Sheetsmith to inspect spreadsheet structure, preview rows, compute summaries, filter data, add or rename columns, and convert CSV, TSV, and Excel files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet inputs may contain confidential or regulated data.

Mitigation: Process only files the agent is authorized to access and avoid sharing results through personal messaging channels unless policy permits.

Risk: In-place transformations can overwrite source data.

Mitigation: Prefer --output and keep backups before using --inplace.

Risk: Unreviewed pandas query or transform expressions may produce incorrect filtered or derived data.

Mitigation: Review expressions before execution and preview results before writing files.

## Reference(s):

- [Sheetsmith usage reference](references/usage.md)
- [Sheetsmith ClawHub skill page](https://clawhub.ai/crimsondevil333333/skills/sheetsmith)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown text, shell commands, and generated CSV, TSV, or Excel files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write spreadsheet files when the agent runs the provided CLI; use --output to avoid overwriting source files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
