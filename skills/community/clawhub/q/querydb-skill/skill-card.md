## Description: <br>
QueryDB Skill helps agents connect to MySQL or PostgreSQL databases, run SQL queries, inject database fixture data, and generate API test cases from database scenarios. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squidtestgary](https://clawhub.ai/user/squidtestgary) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to retrieve database-backed test data, map invoice records into API request parameters, and generate JSON test cases from database scenarios. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes live-looking database credentials. <br>
Mitigation: Remove the embedded credentials, rotate any exposed database account secrets, and replace examples with placeholders or secure secret loading before installation. <br>
Risk: The database helper can execute write-capable SQL. <br>
Mitigation: Use read-only database accounts by default and require explicit user confirmation before running any non-SELECT SQL. <br>
Risk: Generated case exports may contain database-derived business or tax data. <br>
Mitigation: Confirm export destinations and data handling requirements before writing generated JSON files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squidtestgary/querydb-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples, shell install commands, SQL snippets, and JSON test case output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated test cases can be exported as JSON; database access depends on user-supplied connection settings and driver dependencies.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
