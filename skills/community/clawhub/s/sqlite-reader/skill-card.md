## Description: <br>
Read and query SQLite database files for inspection and extraction, including basic SELECT queries, table listing, and schema inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SenKnight](https://clawhub.ai/user/SenKnight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local SQLite databases, list tables, view table schemas, run basic queries, and export query results while investigating application or OpenClaw data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The query mode can modify SQLite databases despite the read-oriented presentation. <br>
Mitigation: Use copies of important databases and run only SELECT-style queries unless write access is intentional. <br>
Risk: SQLite databases can contain sensitive OpenClaw memory or user data. <br>
Mitigation: Avoid exporting sensitive data unless you control and approve the output path. <br>


## Reference(s): <br>
- [SQLite Schema Reference](references/schema.md) <br>
- [ClawHub release page](https://clawhub.ai/SenKnight/sqlite-reader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and text or CSV query output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local CSV exports when the user supplies an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
