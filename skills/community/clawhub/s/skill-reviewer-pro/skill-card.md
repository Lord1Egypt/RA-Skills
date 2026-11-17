## Description:

Skill Reviewer Pro reviews OpenClaw skills for format validity, writing quality, functional alignment, best practices, optimization opportunities, and workflow completeness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykaixu](https://clawhub.ai/user/ykaixu)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to audit OpenClaw skills before publishing, evaluate downloaded skills, and identify concrete improvements to structure, validation, functional coverage, and workflow guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Language auto-adaptation may be over-applied as a hard instruction.

Mitigation: Treat language matching as a user-experience preference while preserving higher-priority safety, system, and developer instructions.

Risk: The review workflow includes a local validation command path that may not exist in every OpenClaw installation.

Mitigation: Verify the local OpenClaw validator path before running validation commands against skill files.

Risk: Review findings and recommendations can be incomplete or incorrect if accepted without human review.

Mitigation: Have a maintainer review the generated findings and scan the skill before publishing or deployment.

## Reference(s):

- [ClawHub Skill Reviewer Pro release page](https://clawhub.ai/ykaixu/skills/skill-reviewer-pro)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review report with checklists, scorecards, findings, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts response language to the user's request.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
