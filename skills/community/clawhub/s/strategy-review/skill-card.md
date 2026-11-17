## Description:

Use when reviewing, critiquing, or stress-testing an existing strategy document. Evaluates seven dimensions -- diagnosis quality, guiding policy strength, action coherence, assumption exposure, falsifiability -- with optional 7S, Five Forces, Balanced Scorecard, and Hoshin Kanri lenses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external reviewers, and strategy authors use this skill to pressure-test existing strategy documents for structural gaps, hidden assumptions, failure paths, and weak links between diagnosis, guiding policy, and actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Strategy documents may contain sensitive business information, and long or judge-mode reviews can leave review notes and JSON artifacts on disk.

Mitigation: Review inputs for sensitivity before use and clean local review artifacts when retained copies are not desired.

Risk: The skill produces critical strategic guidance that could be mistaken for a final decision rather than review input.

Mitigation: Treat findings as decision support and have accountable business owners verify evidence, assumptions, and recommendations before acting.

## Reference(s):

- [Review Dimensions](artifact/references/review-dimensions.md)
- [Review Lenses](artifact/references/review-lenses.md)
- [Interview Lens Audit](artifact/references/interview-lens-audit.md)
- [Review Output Template](artifact/references/review-template.md)
- [Judge Artifact Schema](artifact/references/judge-artifact-schema.md)
- [Pressure-test Scenarios](artifact/references/pressure-tests.md)
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/strategy-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Guidance]

**Output Format:** [Markdown reviews, optional JSON judge artifacts, and concise chat summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce strategy-review.md, optional strategy-review.json, and local review state for long reviews.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
