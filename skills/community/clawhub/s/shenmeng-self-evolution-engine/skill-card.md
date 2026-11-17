## Description:

自我进化引擎 - 让AI Skill具备自我分析、自我改进、自我学习的能力。通过监控执行日志、分析用户反馈、自动发现优化点并生成改进方案，实现Skills的持续进化。适用于技能开发者希望自动化技能维护、优化和迭代的场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shenmeng](https://clawhub.ai/user/shenmeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to monitor execution metrics, analyze errors and feedback, generate improvement proposals, and manage skill version snapshots and rollbacks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic billing calls can submit charge requests using SKILLPAY_USER_ID.

Mitigation: Require explicit payment consent before execution and verify the billing account, amount, and user identifier in a controlled environment.

Risk: The packaged code contains an exposed SkillPay API credential.

Mitigation: Remove or rotate the exposed credential and load billing secrets only from a protected runtime secret or environment variable.

Risk: Snapshot and rollback scripts perform local file operations that may be under-scoped.

Mitigation: Constrain and validate all target paths to the intended skill workspace before allowing backups, snapshots, rollback, or generated changes.

Risk: Generated improvement proposals or patches can be incorrect or unsafe.

Mitigation: Keep human review, tests, and security scanning in the approval path before applying generated changes.

## Reference(s):

- [Architecture design](references/architecture.md)
- [ClawHub skill page](https://clawhub.ai/shenmeng/skills/shenmeng-self-evolution-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON reports with shell command examples and generated code or patch guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local logs, evolution proposal JSON files, backups, and version snapshots when its scripts are run.]

## Skill Version(s):

2025.4.15 (source: server release metadata; artifact _meta.json reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
