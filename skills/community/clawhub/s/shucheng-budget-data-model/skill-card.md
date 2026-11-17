## Description:

Provides a Chinese-language budget-system data model reference, including table names, field names, data types, constraints, and query examples for 68 tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lan2898408767](https://clawhub.ai/user/lan2898408767)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to answer budget-system schema questions and draft narrow database query snippets from the bundled table and field definitions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated queries against real budget or finance data could expose unauthorized or excessive data if used too broadly.

Mitigation: Confirm authorization, keep queries narrow, and avoid exporting unrelated bulk data.

Risk: Static schema references may differ from the current production database.

Mitigation: Validate table names, field names, and required fields against the current system before executing generated scripts.

Risk: Generated scripts can still have operational impact even though the skill contains no executable payload.

Mitigation: Review generated scripts before execution and test against non-production data when possible.

## Reference(s):

- [Budget data model definitions](references/data_models.json)
- [ClawHub skill page](https://clawhub.ai/lan2898408767/skills/shucheng-budget-data-model)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown text with Groovy and SQL query examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a static Chinese-language schema reference; no bundled executables, credentials, network payloads, or persistence behavior are reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
