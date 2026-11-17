## Description:

Guides agents through a deep refactoring workflow covering characterization tests, incremental changes, behavior preservation, design direction, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and execute refactoring work while preserving external behavior. It is suited for reducing coupling, clarifying module boundaries, preparing code for future features, and paying down technical debt with a reviewable safety net.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested refactoring edits can unintentionally change behavior if accepted without review.

Mitigation: Keep changes incremental and verify behavior with tests, golden outputs, CI, or focused manual checks before merging.

Risk: Weak test coverage may leave behavior drift undetected during structural changes.

Mitigation: Establish a safety net with characterization tests, approval tests, exploratory scripts, or domain-expert review before larger refactors.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mike47512/skills/refactoring)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with possible code, shell command, and configuration suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Textual recommendations should be reviewed before applying changes to a codebase.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
