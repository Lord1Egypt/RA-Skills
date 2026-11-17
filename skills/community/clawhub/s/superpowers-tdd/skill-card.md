## Description:

Use when implementing any feature or bugfix before writing implementation code; it enforces the RED-GREEN-REFACTOR cycle by requiring a failing test first, verifying the failure, writing minimal code, verifying the pass, then refactoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to enforce a strict test-driven development workflow for feature work and bug fixes: write a real failing test, verify it fails for the expected reason, implement only enough code to pass, then refactor while keeping tests green.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may encourage deleting or replacing implementation code written before tests without approval or recovery safeguards.

Mitigation: Agents should ask before deleting or replacing code, preserve recoverable changes, and constrain deletion guidance during installation or runtime policy review.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown with code examples and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
