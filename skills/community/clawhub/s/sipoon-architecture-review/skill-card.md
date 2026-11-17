## Description:

Performs periodic architecture quality reviews of codebases to identify cyclic dependencies, dead code, oversized modules, high cyclomatic complexity, unclear interfaces, and technical debt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipoon](https://clawhub.ai/user/sipoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to audit unfamiliar, aging, pre-release, or refactoring-bound codebases and prioritize architecture cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may execute project-controlled npm scripts during broad architecture scans.

Mitigation: Run reviews in a sandbox, inspect commands before execution, and avoid exposing credentials in the scanned environment.

Risk: The workflow may download analyzer CLIs dynamically at runtime.

Mitigation: Prefer pinned or already-installed local analysis tools and verify package sources before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sipoon/skills/sipoon-architecture-review)
- [ClawHub Publisher Profile](https://clawhub.ai/user/sipoon)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables and prioritized recommendations, plus inline shell commands when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized findings for module structure, dead code, complexity, interface design, and technical debt.]

## Skill Version(s):

0.1.0 (source: release evidence and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
