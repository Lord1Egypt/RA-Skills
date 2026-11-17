## Description:

Convert MySQL CREATE TABLE statements to Go structs with form, json, and xorm tags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weirubo](https://clawhub.ai/user/weirubo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn MySQL table definitions into Go model structs with form, JSON, and XORM tags. It is intended for schema-to-code conversion, ORM model generation, and consistent MySQL-to-Go type mapping.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Go structs may not reflect application-specific choices for nullable fields, decimal precision, time handling, tags, or comments.

Mitigation: Review generated structs against the source schema and application requirements before using them in production code.

Risk: Database schema text can reveal sensitive business details when shared with an agent.

Mitigation: Remove or anonymize sensitive table, column, comment, and default-value details before submitting schema text.

## Reference(s):

- [MySQL to Go Type Mappings](references/type_mappings.md)
- [ClawHub skill page](https://clawhub.ai/weirubo/skills/sql-to-go)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Markdown with Go code blocks and concise conversion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated structs should be reviewed for application-specific nullable fields, decimal precision, time handling, tags, and comments.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
