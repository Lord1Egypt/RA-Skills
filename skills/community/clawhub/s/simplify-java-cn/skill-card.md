## Description:

代码能跑，但读起来费劲时使用。简化 Java / Spring Boot 代码，理清分支、命名与重复，保留原有行为；先弄清为什么这样写，再决定怎么改。

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticweb4](https://clawhub.ai/user/agenticweb4)

### License/Terms of Use:

MIT-0

## Use Case:

Java 和 Spring Boot 开发者可用此技能整理已能运行但难以阅读的代码。它帮助识别结构、命名和重复问题，并在简化时保留现有行为与项目约定。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proposed simplification could unintentionally change behavior or framework-level contracts.

Mitigation: Inspect the relevant call paths and project conventions, make small changes, and run the existing behavior and integration checks that cover affected boundaries.

## Reference(s):

- [Addy Osmani 的代码简化技能参考](https://github.com/addyosmani/agent-skills/tree/main/skills/code-simplification)
- [Oracle Java 安全编码指南](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [OWASP SQL 注入防护指南](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP 授权指南](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

## Skill Output:

**Output Type(s):** [Code, Guidance, Markdown]

**Output Format:** [Java code with concise text or Markdown explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Refactoring proposals should preserve existing behavior and follow the project's conventions.]

## Skill Version(s):

0.2.1 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
