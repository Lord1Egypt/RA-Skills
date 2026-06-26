## Description: <br>
All-in-one release compatibility checking tool that analyzes Git diffs, identifies Java/configuration/SQL release changes, checks SQL compatibility, generates multi-database SQL variants, and outputs release TODO lists and Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qfann](https://clawhub.ai/user/qfann) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release engineers use this skill to inspect repository changes before a release, identify component-level compatibility work, convert MySQL SQL for PostgreSQL and Oracle when needed, and produce release readiness reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads changed source, configuration, and SQL files in target repositories. <br>
Mitigation: Install and run it only for repositories the user intentionally wants analyzed, and avoid using it on repositories that contain unmanaged secrets. <br>
Risk: The skill can write Markdown reports and converted SQL files to output paths. <br>
Mitigation: Use trusted branch names and output paths, and inspect generated files before committing or deploying them. <br>
Risk: SQL conversion and validation cover common MySQL to PostgreSQL/Oracle syntax but may miss complex SQL behavior or business logic issues. <br>
Mitigation: Review generated SQL manually and test it in a representative environment before applying it to production databases. <br>
Risk: The SQL conversion path depends on the external sqlglot package. <br>
Mitigation: Install sqlglot from a trusted package source and keep dependency versions under normal project review. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/qfann/release-checker) <br>
- [Publisher profile](https://clawhub.ai/user/qfann) <br>
- [Skill instructions](artifact/SKILL.EN.md) <br>
- [Release checker script](artifact/scripts/release_checker.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, TODO checklists, command guidance, and generated PostgreSQL/Oracle SQL files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read Git diffs and repository files, and may write Markdown reports or converted SQL files to user-selected paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
