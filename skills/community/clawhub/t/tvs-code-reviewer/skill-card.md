## Description:

A stable, evidence-driven code review skill that requires a defined review scope, checks code through a fixed review process, and reports severity-ranked findings with concrete evidence, impact, confidence, and trigger conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[inksnowhailong](https://clawhub.ai/user/inksnowhailong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to perform scoped, evidence-driven code reviews in Chinese. It helps reviewers identify confirmed defects, validation gaps, and out-of-scope observations without modifying code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Findings may be misleading if the provided review scope, logs, or code context is incomplete.

Mitigation: Require an explicit scan scope, cite concrete evidence for each finding, and label uncertain issues as validation gaps or risks.

Risk: The skill may default to Chinese phrasing and a pointed review tone that is not appropriate for every audience.

Mitigation: Review the generated report before sharing it outside the review context and adjust wording for the intended audience.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/inksnowhailong/skills/tvs-code-reviewer)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown review report with severity-ranked findings, evidence, impact, confidence, and trigger conditions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an explicit review scope and does not produce code edits.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
