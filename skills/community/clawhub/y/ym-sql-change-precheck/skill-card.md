## Description:

Prechecks SQL change scripts before release by statically identifying destructive DML, locking risks, implicit type conversions, missing rollback plans, large-table DDL risks, and naming issues, then producing a risk checklist and rewrite guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database review teams use this skill to review SQL DDL and DML change scripts before deployment, identify risky statements, and prepare a Markdown risk report with rewrite, execution-order, and rollback guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated rollback SQL or rewrite suggestions may be mistaken for execution approval.

Mitigation: Treat the skill output as a review aid and require DBA or human approval before running any SQL or shell command.

Risk: Static analysis cannot confirm live schema, table size, locks, data distribution, or execution plans.

Mitigation: Validate findings against target database metadata and operational constraints before deployment.

Risk: Missing database dialect, version, table scale, or locking policy can make guidance conditional.

Mitigation: Provide database type and version, table scale, allowed lock window, and rollback requirements for more precise review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-sql-change-precheck)
- [Server-resolved source repository](https://github.com/liuyuming0823/ym-sql-change-precheck)
- [SQL change risk rules](artifact/references/风险规则清单.md)
- [Risk report template](artifact/templates/风险报告模板.md)
- [Rollback plan template](artifact/templates/回滚方案模板.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown risk report with tables, SQL snippets, execution-order guidance, and rollback-plan sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static review output only; generated SQL and shell commands require DBA or human approval before use.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
