## Description:

Splits multi-object SQL files into separate object files, analyzes dependencies, and can generate dependency-ordered merge scripts and Dameng conversion outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fish1981bimmer](https://clawhub.ai/user/fish1981bimmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database migration engineers use this skill to split large SQL exports into object-level files, inspect dependencies, and convert SQL Server objects toward Dameng SQL syntax. It is most useful for database migration preparation, review, and repeatable split-convert workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A helper script dynamically patches and executes code from a hardcoded external skill path while bypassing limits.

Mitigation: Avoid scripts/unlimited_split.py and use the packaged splitter and converter scripts only after review.

Risk: The security guidance flags broad or sensitive directory access before dynamic execution and config-name path traversal issues are constrained.

Mitigation: Run the skill only on a narrow working directory with non-sensitive SQL inputs until those issues are removed or constrained.

Risk: Automated SQL dialect conversion can introduce semantic differences, such as TRUNCATE-to-DELETE behavior or temporary table handling.

Mitigation: Review converted SQL and run database-specific validation before applying generated scripts to production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fish1981bimmer/skills/sql-splitter)
- [Split and conversion workflow](references/split-convert-workflow-20260627.md)
- [Dameng converter design notes](references/dm-converter-design.md)
- [Document maintenance notes](references/document-maintenance.md)
- [v3.4.5 dbo and bracket handling notes](references/dm-converter-v345-fixes.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated SQL files when scripts are run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces object-level .sql files, merge_all.sql scripts, optional Dameng-converted SQL output, and workflow guidance.]

## Skill Version(s):

3.6.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
