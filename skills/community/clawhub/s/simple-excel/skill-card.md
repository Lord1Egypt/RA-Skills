## Description:

Simple Excel helps agents read, create, edit, and summarize .xlsx and .csv files for basic spreadsheet data tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anmu14641](https://clawhub.ai/user/anmu14641)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to guide agents through common Pandas-based Excel and CSV workflows, including reading files, exporting files, filtering rows, grouping data, sorting data, and basic summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet examples may lead an agent to read local Excel or CSV files and write exported files.

Mitigation: Use explicit input and output paths, review target filenames before execution, and avoid exporting over important existing files unless replacement is intended.

## Reference(s):

- [Simple Excel ClawHub Skill Page](https://clawhub.ai/anmu14641/skills/simple-excel)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with inline Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to read local Excel or CSV files and write exported .xlsx or .csv files.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
