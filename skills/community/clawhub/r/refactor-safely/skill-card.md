## Description:

Plans and executes safe refactors with small steps, tests, and rollback strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan and carry out behavior-preserving refactors, especially when cleaning technical debt or improving code structure without changing external behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refactor proposals may accidentally change behavior, especially during deletion of dead code or structural changes.

Mitigation: Review proposed edits before accepting them and verify each step with tests, builds, type checks, or targeted manual checks.

Risk: The skill's workflow may ask for deletion of unused or deprecated code after reference checks, which can be risky in codebases with implicit entry points.

Mitigation: Confirm references and runtime entry points before deletion, and keep each refactor step independently revertible in version control.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/skills/refactor-safely)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown refactor plan with step-by-step validation and rollback notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed code edits, verification commands, and rollback guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
