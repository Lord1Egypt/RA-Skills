## Description:

Helps agents analyze table DDL and slow SQL for MySQL, Oracle, and PostgreSQL, then generate candidate index recommendations and database-specific CREATE INDEX statements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houyalei](https://clawhub.ai/user/houyalei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database engineers, and agent operators use this skill to turn schema files and slow SQL examples into index optimization suggestions for review. It is intended to speed up candidate-index discovery, not to replace execution-plan validation or DBA approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper reads local schema and slow-query files, which may contain sensitive database structure or query details.

Mitigation: Use non-sensitive copies where possible and provide only the specific local files needed for analysis.

Risk: Generated index DDL may be incomplete or unsuitable because recommendations are static heuristics.

Mitigation: Review recommendations with a DBA and validate them using execution-plan tooling before production use.

Risk: The selected output path may create or overwrite a local recommendation file.

Mitigation: Choose an output path that is safe to create or replace before running the helper.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houyalei/skills/sql-index-optimizer-multi-db)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown or JSON files containing candidate indexes, reasons, counts, and CREATE INDEX SQL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports mysql, oracle, and postgresql dialects; reads local DDL and slow SQL files and writes recommendations to a selected output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
