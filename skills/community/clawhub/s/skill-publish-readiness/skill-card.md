## Description:

Reviews ClawHub skills and plugins before release using a quick launch checklist or deeper evidence-based review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bonniegeng-max](https://clawhub.ai/user/bonniegeng-max)

### License/Terms of Use:

MIT-0

## Use Case:

Skill and plugin publishers use this reviewer to check release readiness, identify blockers, and plan validation before publishing to ClawHub.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A dry run may be mistaken for proof that a release is published or installable.

Mitigation: Label unverified stages clearly and confirm publication and installation separately.

Risk: Suggested publishing commands may be run before the user has approved a live release.

Mitigation: Stop at validation or dry-run and obtain explicit confirmation before formal publishing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/bonniegeng-max/skills/skill-publish-readiness)
- [Project homepage (listed in package metadata)](https://github.com/bonniegeng-max/openclaw-publisher)
- [Consistency rules](references/consistency_rules.md)
- [Security review guide](references/security_review_guide.md)
- [Differentiation rubric](references/differentiation_rubric.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown report with checklists, tables, and suggested commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Quick or deep review; includes a release recommendation, supporting evidence, gaps, and next steps.]

## Skill Version(s):

2.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
