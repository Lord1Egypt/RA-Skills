## Description:

Converts natural-language data requests plus a provided database schema into syntactically correct SQL queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to draft SQL from plain-English data questions when they can provide the relevant database schema. It can also produce commented queries or alternative query approaches for learning and comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SQL can be incorrect for the schema, SQL dialect, or user-supplied filter values.

Mitigation: Review the generated query before execution, verify table and column names, prefer bind parameters, and use a read-only database account where practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/text-to-sql)
- [Metadata source: MiniMax-AI skills](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with SQL code blocks and concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated SQL should be reviewed for schema accuracy, SQL dialect, and parameters before execution.]

## Skill Version(s):

999.0.0 (source: ClawHub release metadata; artifact frontmatter and changelog report 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
