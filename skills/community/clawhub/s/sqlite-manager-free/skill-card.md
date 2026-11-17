## Description: <br>
Helps agents manage local SQLite databases with guidance for concurrency, foreign keys, schema changes, performance tuning, backups, and transaction workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to plan and execute local SQLite database tasks such as configuration, querying, export, backup, tuning, and safe write workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database-changing actions can modify, reset, import, export, vacuum, or alter local SQLite data. <br>
Mitigation: Review generated commands before execution, keep backups of important database files, and use transactions for write workflows. <br>
Risk: Network troubleshooting guidance is not needed for normal local SQLite management. <br>
Mitigation: Ignore network checks unless the user explicitly asks to diagnose connectivity. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/sqlite-manager-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with SQL, bash, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local sqlite3 commands that read or modify database files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
