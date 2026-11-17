## Description:

Create, read, edit Excel spreadsheets (.xlsx, .xlsm, .csv). Supports formulas, formatting, charts, pivot tables, and data analysis with pandas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weaglewang](https://clawhub.ai/user/weaglewang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to generate, inspect, transform, format, and analyze Excel-compatible spreadsheets with Python libraries such as pandas, openpyxl, and xlsxwriter.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet examples can create or overwrite local Excel files when run with existing output paths.

Mitigation: Review input and output paths before execution and run examples in a disposable working directory when possible.

Risk: The skill depends on Python spreadsheet packages whose installed versions may vary across environments.

Mitigation: Install dependencies in an isolated environment and pin package versions when reproducibility or enterprise control is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weaglewang/skills/xlsx-skill)
- [Publisher profile](https://clawhub.ai/user/weaglewang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide the agent to create, read, modify, or overwrite local spreadsheet files.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
