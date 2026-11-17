## Description:

Support generating SQL queries through natural language; use when users need to configure Text-to-SQL database, manage data topics, or generate SQL with natural language questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asksqlai](https://clawhub.ai/user/asksqlai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data teams use TEXT2SQL to configure database or Excel-backed semantic topics, inspect table structures, generate topic YAML files, and request SQL from natural-language questions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect and upload database metadata, table samples, topic YAML, questions, or spreadsheet data to asksql.ai.

Mitigation: Use a least-privilege read-only database account, avoid confidential spreadsheets unless remote processing is accepted, and inspect or restrict what is sent to the remote service.

Risk: Database passwords may be passed on the command line and saved in a local configuration file.

Mitigation: Use temporary or scoped credentials, protect the output directory, and rotate credentials after use when handling sensitive environments.

Risk: Generated SQL may be incorrect for the intended business question or unsafe to run without review.

Mitigation: Review generated SQL before execution and run it first against non-production data or with read-only permissions.

## Reference(s):

- [Open Semantic Interchange field specification](references/open_semantic_interchange_description.md)
- [AskSqlAI SQL API service](https://asksql.ai/)
- [TEXT2SQL ClawHub release](https://clawhub.ai/asksqlai/skills/text2sql)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON status output, YAML configuration files, and SQL text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local output files for database configuration, table metadata, column metadata, and topic YAML; generated SQL is returned when the remote API call succeeds.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
