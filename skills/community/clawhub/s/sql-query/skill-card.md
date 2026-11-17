## Description: <br>
Sql Query helps teams manage SQL query workflows, including slow-query collection, result caching, cross-database SQL conversion, performance baselines, and read/write routing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, DBAs, and operations teams use this skill to produce guidance, code examples, shell commands, and configuration for SQL query execution, caching, monitoring, dialect conversion, benchmarking, and routing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests broad read, write, and execution authority while discussing real database access. <br>
Mitigation: Review before installation, grant only the minimum database and filesystem permissions required, and prefer read-only database accounts unless writes are explicitly needed. <br>
Risk: SQL text, query parameters, credentials, or operational alerts may contain sensitive information. <br>
Mitigation: Inject credentials through managed secrets or environment variables, avoid hardcoding secrets, and avoid sending sensitive SQL or parameters to webhook destinations. <br>
Risk: Disk caches, benchmark baselines, and slow-query records may retain private operational data. <br>
Mitigation: Confirm cache and baseline storage locations, retention periods, access controls, and cleanup procedures before use with private or production databases. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sql-query) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code blocks and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQL workflow guidance, configuration notes, and operational safeguards.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
