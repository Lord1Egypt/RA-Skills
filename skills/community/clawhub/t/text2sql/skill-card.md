## Description: <br>
Supports generating SQL queries from natural language after configuring database or spreadsheet schema context and topic-specific YAML files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asksqlai](https://clawhub.ai/user/asksqlai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data teams, and agent users use this skill to configure database or Excel-backed semantic context, create topic YAML files, and request SQL from natural-language questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database schema details, sampled values or enum lists, natural-language questions, YAML topic files, and Excel workbook contents may be sent to the configured API provider. <br>
Mitigation: Use least-privilege read-only database access, avoid regulated or production data, and install only when that data handling is acceptable. <br>
Risk: Database credentials can be written to a local configuration file. <br>
Mitigation: Protect generated output files, remove plaintext credentials when no longer needed, and rotate credentials after use when appropriate. <br>
Risk: Generated SQL can be incorrect, incomplete, or too broad for the user's intent. <br>
Mitigation: Review generated SQL before execution and test against non-production data or read-only environments first. <br>


## Reference(s): <br>
- [Open Semantic Interchange field specification](references/open_semantic_interchange_description.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, YAML, SQL] <br>
**Output Format:** [Markdown guidance with shell commands, JSON status files, YAML topic files, and SQL text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local output files for database configuration, table metadata, column metadata, and topic-specific semantic YAML.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
