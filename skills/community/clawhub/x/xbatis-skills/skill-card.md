## Description: <br>
在使用 xbatis 的 Java 项目中实现、改写、审查或优化 ORM / Mapper / QueryChain / 联表 / 分页 / VO 映射 / 多租户 / 逻辑删除 / 乐观锁 / SQL 模板相关代码时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-010](https://clawhub.ai/user/ai-010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when adding, refactoring, reviewing, or troubleshooting xbatis-based Java persistence code. It guides agents toward xbatis-native Mapper, DAO, QueryChain, result mapping, pagination, multi-tenancy, logic delete, optimistic locking, and SQL-template patterns while limiting XML or raw SQL fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill tells agents to download mutable external xbatis framework repositories for reference. <br>
Mitigation: Require approval before network fetches and pin repository revisions when possible. <br>
Risk: The security summary notes insecure database credential examples. <br>
Mitigation: Replace sample database credentials with environment variables or project-local secret handling before use. <br>
Risk: The security verdict is suspicious, so generated guidance should be reviewed before execution. <br>
Mitigation: Review and scan the skill before deployment, especially any proposed shell commands, dependency changes, or configuration edits. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/xbatis/xbatis-skills) <br>
- [ClawHub skill page](https://clawhub.ai/ai-010/xbatis-skills) <br>
- [Xbatis framework source](https://github.com/xbatis/xbatis) <br>
- [Xbatis Spring Boot starter source](https://github.com/xbatis/xbatis-spring-boot-parent) <br>
- [Xbatis Solon plugin source](https://github.com/xbatis/xbatis-solon-plugin) <br>
- [Environment Setup](references/environment-setup.md) <br>
- [Mapper Modes](references/mapper-modes.md) <br>
- [Query Strategy](references/query-strategy.md) <br>
- [Framework Features](references/framework-features.md) <br>
- [Advanced SQL Decision](references/advanced-sql.md) <br>
- [XML Boundaries](references/xml-boundaries.md) <br>
- [Review Checklist](references/review-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project-specific recommendations that depend on local xbatis source verification.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
