## Description:

ZenTao Project Management API Integration | 禅道-ZenTao 项目管理 API 集成。Query products, projects, executions, stories, tasks, bugs / 查询产品、项目、执行、需求、任务、缺陷等。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoyoalphax](https://clawhub.ai/user/yoyoalphax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project teams use this skill to query and manage ZenTao products, projects, executions, stories, tasks, bugs, tests, feedback, and tickets from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads ZenTao credentials from TOOLS.md and uses them to authenticate to a ZenTao server.

Mitigation: Keep TOOLS.md out of version control, use HTTPS-only ZenTao URLs, and prefer a least-privilege service account.

Risk: The skill can perform high-impact project-management changes such as create, update, delete, review, and test-run actions.

Mitigation: Require explicit confirmation before any mutating operation and review the target object, account, and ZenTao server before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yoyoalphax/skills/yoyoalphax-zentao)
- [Publisher profile](https://clawhub.ai/user/yoyoalphax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain-text command guidance with tabular query results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May issue authenticated ZenTao REST or legacy API operations after credentials are configured.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
