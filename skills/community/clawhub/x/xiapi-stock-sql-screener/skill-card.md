## Description:

Screens A-share stocks using Daxi API SQL conditions, including custom filters, logical combinations, sorting, and limits, and returns structured stock-screening analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksky521](https://clawhub.ai/user/ksky521)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market-analysis agents use this skill to construct SQL-style filters for A-share stock screening, retrieve matching records through the Daxi API CLI, and summarize results into a structured screening report. It is intended for technical and quantitative screening workflows, not deep fundamental analysis or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned external Daxi API CLI with an API token.

Mitigation: Use a pinned CLI version, run it in a minimal environment, and store only narrowly scoped, revocable tokens.

Risk: Free-form SQL conditions can become unsafe when interpolated into shell commands.

Mitigation: Validate SQL conditions against the documented grammar and avoid passing untrusted user input directly through a shell command.

Risk: Stock-screening outputs can be mistaken for investment advice.

Mitigation: Keep recommendations conditional, cite the data date, include risk notes, and retain the required disclaimer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ksky521/skills/xiapi-stock-sql-screener)
- [Daxi API](https://daxiapi.com)
- [SQL Syntax Guide](references/sql-syntax.md)
- [Field List](references/field-list.md)
- [Query Examples](references/query-examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and SQL condition examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include stock tables, sector summaries, strength metrics, risk notes, and disclaimers.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
