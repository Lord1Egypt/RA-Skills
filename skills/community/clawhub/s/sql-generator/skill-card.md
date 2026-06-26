## Description: <br>
SQL Generator helps agents produce SQL queries, explanations, optimization suggestions, DDL, mock data, migration-oriented templates, and SQL reference guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, database users, and agents use this skill to draft SQL statements, schema templates, indexes, test data, and concise SQL learning or troubleshooting guidance before review and execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL may be incorrect, inefficient, or unsafe for a production schema. <br>
Mitigation: Review and test generated SQL before executing it against production databases. <br>
Risk: scripts/script.sh can store command arguments in a local history log. <br>
Mitigation: Do not pass secrets, private query text, tokens, or sensitive file paths to scripts/script.sh. <br>
Risk: The artifact includes local shell scripts from a third-party publisher. <br>
Mitigation: Install and run the scripts only after reviewing the artifact and accepting the publisher risk. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ckchzh/sql-generator) <br>
- [Publisher Profile](https://clawhub.ai/user/ckchzh) <br>
- [Homepage](https://bytesagain.com) <br>
- [Source](https://github.com/bytesagain/ai-skills) <br>
- [tips.md](artifact/tips.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with SQL code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated SQL and shell output should be reviewed before use against production databases.] <br>

## Skill Version(s): <br>
2.3.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
