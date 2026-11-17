## Description:

Skill Builder guides an agent through Socratic questioning, first-principles analysis, complexity assessment, and packaging steps to help users design complete new skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dead1ine](https://clawhub.ai/user/dead1ine)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to turn an initial skill idea into a structured SKILL.md draft, supporting folder layout, publishing description, and follow-up guidance through a guided multi-turn design process.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask users to provide a ClawHub token in chat.

Mitigation: Use a secret manager or environment variable with a narrow, short-lived token instead of pasting secrets into chat.

Risk: Generated skills may be installed or published without enough review.

Mitigation: Review and scan generated skills before deployment, and require explicit confirmation before workspace install or publish actions.

## Reference(s):

- [Skill page](https://clawhub.ai/dead1ine/skills/socratic-skill-builder)
- [Complexity assessment matrix](references/complexity-matrix.md)
- [First-principles analysis framework](references/first-principles.md)
- [Socratic question library](references/socratic-questions.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with SKILL.md drafts, folder structures, publishing descriptions, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include candidate skill names, implementation boundaries, and review steps for generated skills.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
