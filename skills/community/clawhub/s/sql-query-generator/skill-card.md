## Description: <br>
Generate secure SQL queries with validation, pagination helpers, risk analysis, and audit-focused safeguards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to draft SQL from natural-language requests, add validation and pagination patterns, and review query risk before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill overstates its safety while including unsafe query-building patterns. <br>
Mitigation: Treat generated SQL as draft output, review every query, avoid user-controlled raw WHERE, JOIN, or HAVING strings, and require parameterized values with allowlisted identifiers. <br>
Risk: Generated write or DDL statements can change or destroy data if executed without controls. <br>
Mitigation: Use least-privilege or read-only database roles by default and require explicit confirmation before writes or DDL. <br>
Risk: Audit logging can create sensitive records if retention and access controls are not defined. <br>
Mitigation: Disable or protect audit logs unless a retention and access-control plan is in place. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cerbug45/sql-query-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, Python, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated queries require review before execution; safety controls are advisory.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
