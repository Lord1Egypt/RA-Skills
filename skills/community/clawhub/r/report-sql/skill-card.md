## Description: <br>
Report Sql documents report-service SQL template variables, conditional SQL blocks, array loops, and result transformation rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[23396599](https://clawhub.ai/user/23396599) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers who maintain report-service report queries use this skill to author SQL templates with precise option.where variables, empty-safe conditional fragments, multi-value loops, and JSON-based result transformations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQL templates may be unsafe if report-service does not validate types and escape or parameterize substituted values. <br>
Mitigation: Confirm report-service validation and escaping behavior before using these patterns with real databases. <br>
Risk: Generated SQL could affect sensitive or production data if reviewed insufficiently. <br>
Mitigation: Review generated SQL before execution and prefer least-privilege or read-only database accounts. <br>


## Reference(s): <br>
- [Report Sql ClawHub release](https://clawhub.ai/23396599/report-sql) <br>
- [Transform reference](artifact/references/transform.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, configuration] <br>
**Output Format:** [Markdown with SQL and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; no executable code is included.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
