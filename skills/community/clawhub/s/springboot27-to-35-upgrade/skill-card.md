## Description:

将 Spring Boot 2.7 项目升级到 Spring Boot 3.5 的实战流程，覆盖版本基线、依赖坐标替换、Jakarta 迁移、配置兼容、异步上下文传递改造与验证门禁。

This skill is ready for commercial/non-commercial use.

## Publisher:

[k2-code](https://clawhub.ai/user/k2-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, execute, and validate enterprise multi-module Maven upgrades from Spring Boot 2.7 to Spring Boot 3.5. It helps identify baseline requirements, dependency replacements, Jakarta migration work, configuration changes, common pitfalls, and verification gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed code and dependency changes may introduce regressions or misleading migration guidance if accepted without review.

Mitigation: Review proposed changes before execution and run compile, startup, smoke-test, and log checks before accepting the upgrade.

Risk: The optional OpenRewrite/Maven plugin step can make broad automated edits across a project.

Mitigation: Run automated rewrite steps only on an upgrade branch, inspect the diff, and keep manual rollback options available.

Risk: Enterprise-specific dependency coordinates and parent POM guidance may not apply to every Spring Boot project.

Mitigation: Confirm internal repository availability, approved parent versions, and dependency-management policy before applying enterprise-specific coordinates.

## Reference(s):

- [Upgrade Checklist](references/upgrade-checklist.md)
- [Dependency Replacement Matrix](references/dependency-replacement-matrix.md)
- [Pitfall Cookbook](references/pitfall-cookbook.md)
- [Enterprise Parent Security](references/enterprise-parent-security.md)
- [ClawHub Skill Page](https://clawhub.ai/k2-code/skills/springboot27-to-35-upgrade)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include changed files, reasons for changes, dependency replacement results, verification commands and results, remaining issues, and follow-up recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
