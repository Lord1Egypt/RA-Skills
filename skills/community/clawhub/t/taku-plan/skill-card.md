## Description:

Turn an approved design into an executable implementation plan using a three-step pipeline for scope and architecture review, UI design review when applicable, and plan writing with automatic step detection from project state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kkenny0](https://clawhub.ai/user/kkenny0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill after a design is approved to review scope, architecture, and UI quality, then produce a concrete implementation plan. It is intended to keep review artifacts in DESIGN.md and execution tasks in PLAN.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move from planning into implementation without a clear user approval step.

Mitigation: Review generated PLAN.md before build handoff and require explicit user confirmation before invoking implementation workflows such as /taku-build.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kkenny0/skills/taku-plan)
- [Plan Review Reference](references/plan-review.md)
- [Design Review Reference](references/design-review.md)
- [Implementation Plan Scaffold](references/plan.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Guidance]

**Output Format:** [Markdown review sections appended to DESIGN.md and a Markdown implementation plan saved to PLAN.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scope decisions, architecture notes, design scorecards, task dependency annotations, TDD anchors, and execution hints.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
