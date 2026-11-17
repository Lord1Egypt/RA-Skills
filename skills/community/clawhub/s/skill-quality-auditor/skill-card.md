## Description:

Evaluate and score AgentSkills on design, content, security, and usability, producing a detailed numeric scorecard with improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ann0501](https://clawhub.ai/user/ann0501)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to audit AgentSkill packages before release. It produces a four-dimension quality scorecard with pass-or-revise guidance and concrete improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the contents of the skill package being reviewed, so sensitive files in that package may enter the review context.

Mitigation: Point it only at intended skill directories and remove secrets or unrelated private files before review.

Risk: The default report examples are Chinese-formatted, which may not match every reviewer or release workflow.

Mitigation: Specify the desired report language or adapt the output template before using the result with another audience.

Risk: Rubric-based quality findings may miss project-specific policy, legal, or release requirements.

Mitigation: Use the scorecard as release-review input alongside human review and the platform's security evidence.

## Reference(s):

- [Weight Adjustment](references/weight-adjustment.md)
- [Design Quality](references/design-quality.md)
- [Content Quality](references/content-quality.md)
- [Security](references/security.md)
- [Usability](references/usability.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style scorecard with numeric ratings and improvement suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default report examples are Chinese-formatted unless the user requests another output language.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
