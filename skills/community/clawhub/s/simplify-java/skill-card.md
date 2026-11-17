## Description:

Use when Java / Spring Boot code works but is hard to follow. Clarify branches, names, and duplication without changing behavior. Understand why the code exists before deciding how to simplify it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agenticweb4](https://clawhub.ai/user/agenticweb4)

### License/Terms of Use:

MIT-0

## Use Case:

Java developers use this skill to make working Java and Spring Boot code easier to understand while preserving behavior. It guides focused refactoring of requested or recently changed code after checking project conventions, contracts, and relevant tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A simplification may unintentionally change observable behavior, error handling, or framework contracts.

Mitigation: Check equivalence against the project conventions and affected tests before applying changes; keep the original when equivalence is unclear.

## Reference(s):

- [ClawHub release page: Java Code Simplification](https://clawhub.ai/agenticweb4/skills/simplify-java)
- [Inspiration: Addy Osmani code simplification skill](https://github.com/addyosmani/agent-skills/tree/main/skills/code-simplification)
- [Oracle Secure Coding Guidelines for Java SE](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)

## Skill Output:

**Output Type(s):** [Code, Guidance]

**Output Format:** [Markdown with code snippets and concise rationale]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focused refactoring suggestions or edits that aim to preserve behavior.]

## Skill Version(s):

0.2.1 (source: frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
