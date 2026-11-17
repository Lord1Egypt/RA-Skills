## Description:

Repo-wide structural-maintainability review focused on ambitious simplification, file-size discipline, anti-spaghetti branching, canonical-layer enforcement, anti-magic abstractions, and explicit type and boundary contracts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to perform strict, evidence-backed structural maintainability reviews of code changes. It emphasizes behavior-preserving simplification, clearer abstractions, canonical ownership boundaries, and maintainable file structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs the agent to read broadly across the repository, which can expose sensitive project context to the active review session.

Mitigation: Use it only where broad repository read access is appropriate and keep normal secret-handling controls in place.

Risk: Strict structural review guidance can lead to over-applied refactoring if findings are accepted without engineering judgment.

Mitigation: Review each finding against its cited code evidence and accept only behavior-preserving changes with clear maintainability value.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/review-structure)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown review report with file and line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires cited same-turn evidence before findings and uses read-only repository inspection when reviewing changes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
