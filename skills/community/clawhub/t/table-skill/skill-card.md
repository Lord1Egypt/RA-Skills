## Description:

Processes tabular data end to end by splitting Excel and CSV tables, cleaning CSV data, merging multi-row headers, describing table schema and statistics, and supporting controlled exploratory analysis, visualization, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutesxy](https://clawhub.ai/user/cutesxy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and agents use this skill to prepare messy spreadsheets and CSV files for downstream analysis. It helps split multi-table files, clean and normalize table structure, merge complex headers, generate table descriptions, and produce controlled EDA outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Spreadsheet-derived samples, schema, and category values may be sent to the configured remote LLM provider when abstract generation or header merging is enabled.

Mitigation: Use local-only modes for sensitive data, including disabling abstracts with --no-abstract and disabling or skipping header merging unless the user explicitly authorizes remote LLM use.

Risk: Unsafe CSV output handling may preserve spreadsheet formulas or risky cell contents.

Mitigation: Avoid untrusted spreadsheets until CSV formula neutralization is fixed, and review generated CSV files before opening them in spreadsheet software.

Risk: Processing broad workspaces or unspecified output locations can expose unrelated data or create files in unexpected directories.

Mitigation: Run the skill in a restricted workspace, process only the required input files, and choose an explicit output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cutesxy/skills/table-skill)
- [Skill source instructions](artifact/SKILL.md)
- [Table skill documentation index](artifact/script/docs/README.md)
- [Split table documentation](artifact/script/docs/01_split_table_skill.md)
- [Clean table documentation](artifact/script/docs/02_clean_table_skill.md)
- [Describe table documentation](artifact/script/docs/03_describe_table_skill.md)
- [Merge header documentation](artifact/script/docs/04_merge_header_skill.md)
- [EDA and visualization guidance](artifact/script/docs/05_eda_mining_skill.md)

## Skill Output:

**Output Type(s):** [files, text, code, shell commands, configuration, guidance]

**Output Format:** [CSV files, JSON descriptions, chart or report files, and Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include cleaned CSV files, split table CSV files, merged-header CSV files, JSON table descriptions, static visualizations, and HTML reports depending on the workflow.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
