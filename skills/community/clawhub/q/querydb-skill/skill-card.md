## Description:

Database query skill for connecting to MySQL or PostgreSQL databases, retrieving test data, and validating API response data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squidtestgary](https://clawhub.ai/user/squidtestgary)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to query MySQL or PostgreSQL data sources, map database rows into API request fields, and generate JSON test cases for invoice-related API validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes live-looking database credentials and business identifiers.

Mitigation: Rotate the exposed credential, replace examples with environment variables or a secret manager, and avoid exporting real invoice or taxpayer data unless explicitly approved.

Risk: The skill can execute database queries and write generated test data to files.

Mitigation: Use a read-only least-privilege database account, review SQL before execution, prefer parameterized queries, and restrict output paths to approved locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squidtestgary/skills/querydb-skill)
- [Artifact skill documentation](artifact/SKILL.md)
- [Database query helper script](artifact/scripts/db_query.py)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with Python code examples, shell commands, and JSON test case output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated test cases to JSON files when export paths are provided.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
