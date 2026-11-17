## Description:

Pugongying Data Skill is a Chinese-language data-engineering skill suite that helps agents support requirements analysis, architecture design, data modeling, SQL development, ETL pipeline work, data quality checks, and data testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shixiangyu2](https://clawhub.ai/user/shixiangyu2)

### License/Terms of Use:

MIT-0

## Use Case:

Data engineers and developers use this skill suite to plan and produce data warehouse, ETL, SQL, data quality, and data testing artifacts across an end-to-end data development workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project initialization scripts can create or modify local project files.

Mitigation: Run init scripts only in a new or disposable project directory and use simple trusted project names.

Risk: Generated code, YAML packages, and deployment steps may be incorrect or unsuitable for a production environment.

Mitigation: Review generated artifacts before sharing or using them, and require explicit human approval before any production deployment.

Risk: Dependencies may change if installed without version constraints.

Mitigation: Pin dependencies before installing or running project tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shixiangyu2/skills/pugongying-data-skills)
- [README](README.md)
- [Skill connections](skill-connections.yaml)
- [Skill hub](skill-hub.md)
- [Requirement standards](requirement-analyst/references/requirement-standards.md)
- [Architecture standards](architecture-designer/references/architecture-standards.md)
- [Data modeling standards](modeling-assistant/references/data-modeling-standards.md)
- [SQL standards](sql-assistant/references/sql-standards.md)
- [ETL standards](etl-assistant/references/etl-standards.md)
- [Data quality standards](dq-assistant/references/data-quality-standards.md)
- [Test standards](test-engineer/references/test-standards.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured YAML-oriented guidance with code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are organized around standardized package files such as requirement_package.yaml, architecture_package.yaml, modeling_package.yaml, sql_package.yaml, etl_package.yaml, dq_package.yaml, and test_package.yaml.]

## Skill Version(s):

1.0.1 (source: server release evidence, package.json, CHANGELOG, released 2026-04-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
