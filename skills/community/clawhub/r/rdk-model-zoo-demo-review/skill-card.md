## Description:

Use when reviewing a new, changed, migrated, or pre-merge RDK Model Zoo sample/demo for repository compliance or delivery completeness across RDK X3, X5, and RDK S branches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maxma615](https://clawhub.ai/user/maxma615)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to assess RDK Model Zoo demos against repository standards and stated delivery requirements across RDK X3, X5, and RDK S branches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads repository files related to the demo under review and may inspect more context than intended if the target is ambiguous.

Mitigation: Provide a clear repository path and sample path so the review remains focused on the intended demo.

Risk: The skill produces compliance findings that could be misleading if they are based on incomplete target evidence.

Mitigation: Review cited paths, command output, and verification level before using findings for release decisions.

Risk: Board-execution status can be overstated if hardware evidence is not available.

Mitigation: Treat board execution as unverified unless the stated command, board, model artifact, input, and result were observed on target hardware.

## Reference(s):

- [Branch and Family Matrix](artifact/references/branch-matrix.md)
- [Family Patterns](artifact/references/family-patterns.md)
- [Review Checklist](artifact/references/review-checklist.md)
- [Review Report Template](artifact/references/review-report-template.md)
- [ClawHub Skill Page](https://clawhub.ai/maxma615/skills/rdk-model-zoo-demo-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown review report with findings, passed checks, open questions, verification level, and overall verdict.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include severity, review axis, location, rule or requirement, evidence, impact, and smallest corrective action.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
