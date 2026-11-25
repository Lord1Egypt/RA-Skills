# SKILL.md Quick Security Check (free)

A fast five-pattern security check for a third-party SKILL.md, before
you install it:

1. Remote code piped into a shell
2. Destructive commands
3. Wildcard tool approvals
4. Hidden Unicode
5. Credential access and data exfiltration

It returns a short do-not-install / fix-first / safe-to-read-further
result with line numbers. Mechanical checks only — a file can pass all
five and still contain harmful instructions in plain language.

**Full version:** the SKILL.md Security Auditor adds the semantic
review (does every instruction serve the skill's stated purpose?),
permission-budget and data-flow analysis, persistence and
encoded-payload checks, and a written audit report with a fix for
every finding. €15 on SkillHQ:
https://skillhq.dev/skills/yuanqingsong/skill-md-security-auditor

**Companion tool:** [skillmdvalidator.com](https://skillmdvalidator.com)
— free SKILL.md format validation against the official Agent Skills
specification, plus this pattern scan, running entirely in your
browser. Your file is never uploaded.

MIT licensed. By the maker of skillmdvalidator.com.
