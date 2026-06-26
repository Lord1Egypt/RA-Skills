## Description: <br>
将 Spring Boot 2.7 项目升级到 Spring Boot 3.5 的实战流程，覆盖版本基线、依赖坐标替换、Jakarta 迁移、配置兼容、异步上下文传递改造与验证门禁。用于企业多模块 Maven 项目升级与排障。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k2-code](https://clawhub.ai/user/k2-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to plan and execute Spring Boot 2.7 to 3.5 upgrades in enterprise multi-module Maven projects, including dependency replacement, Jakarta migration, configuration updates, and validation gates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Upgrade guidance can lead to substantial repository edits, dependency changes, and Maven or OpenRewrite runs. <br>
Mitigation: Apply the skill on a feature branch, review generated changes before merge, and run the stated compile, package, startup, and smoke-validation gates. <br>
Risk: Enterprise-specific parent POMs, internal starters, or rewrite recipes may be unavailable or untrusted in a target environment. <br>
Mitigation: Confirm enterprise dependencies and recipes are trusted and resolvable before applying them; pause migration and document blockers when compatible internal artifacts are missing. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/k2-code/springboot27-to-35-upgrade) <br>
- [Upgrade checklist](artifact/references/upgrade-checklist.md) <br>
- [Dependency replacement matrix](artifact/references/dependency-replacement-matrix.md) <br>
- [Pitfall cookbook](artifact/references/pitfall-cookbook.md) <br>
- [Enterprise parent security guidance](artifact/references/enterprise-parent-security.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces upgrade plans, change summaries, dependency replacement guidance, validation commands, and follow-up recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
