## Description:

Helps developers simplify and refactor existing code while preserving behavior and public APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkxzhou](https://clawhub.ai/user/linkxzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to make existing code easier to read and maintain through scoped, behavior-preserving edits or read-only assessments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may bring unrelated code into a refactoring request.

Mitigation: Confirm the requested scope and review the resulting diff and command report.

Risk: A simplification can unintentionally change behavior or public APIs.

Mitigation: Make small scoped edits, run available project checks, and review any unverified changes before use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/linkxzhou/skills/simplify-code-all)
- [Behavior traps](references/behavior-traps.md)
- [Simplification rules](references/rules.md)
- [Read-only assessment guidance](references/assessment.md)

## Skill Output:

**Output Type(s):** [Code, Markdown, Guidance]

**Output Format:** [Code edits or a concise Markdown report with a diff or rewritten code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports scope, changes, and the checks actually run; read-only assessments propose edits without applying them.]

## Skill Version(s):

1.1.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
