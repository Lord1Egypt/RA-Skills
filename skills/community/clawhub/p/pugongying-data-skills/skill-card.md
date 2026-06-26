## Description: <br>
A data-engineering skill suite for requirements analysis, architecture design, data modeling, SQL development, ETL pipeline work, data quality checks, and data testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shixiangyu2](https://clawhub.ai/user/shixiangyu2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data engineers and developers use this skill to plan and produce end-to-end data warehouse and data pipeline artifacts, including requirement packages, architecture packages, model designs, SQL, ETL plans, quality rules, and test packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill suite can produce shell, database, deployment, and data-modifying guidance across multiple modules. <br>
Mitigation: Use it first in a disposable or development workspace and require manual approval before running database writes, replace/upsert operations, DELETE/UPDATE repairs, package handoffs, or deployment steps. <br>
Risk: Generated SQL, ETL code, and test or quality automation may be incorrect or unsafe for production data. <br>
Mitigation: Review generated SQL, ETL code, quality rules, and deployment instructions before execution, and keep production credentials out of prompts and generated files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shixiangyu2/pugongying-data-skills) <br>
- [README](README.md) <br>
- [Skill Connections](skill-connections.yaml) <br>
- [Skill Hub](skill-hub.md) <br>
- [Requirement Standards](requirement-analyst/references/requirement-standards.md) <br>
- [Architecture Standards](architecture-designer/references/architecture-standards.md) <br>
- [Data Modeling Standards](modeling-assistant/references/data-modeling-standards.md) <br>
- [SQL Standards](sql-assistant/references/sql-standards.md) <br>
- [ETL Standards](etl-assistant/references/etl-standards.md) <br>
- [Data Quality Standards](dq-assistant/references/data-quality-standards.md) <br>
- [Test Standards](test-engineer/references/test-standards.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with YAML, SQL, shell, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces standardized YAML package artifacts and human-reviewable implementation guidance across the suite modules.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release, package.json, CHANGELOG released 2026-04-10) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
