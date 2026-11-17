## Description:

Generates 40-minute, three-part vocational classroom lesson plans in Markdown and DOCX formats, adapting to either uniform or layered student contexts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flyboat403](https://clawhub.ai/user/flyboat403)

### License/Terms of Use:

MIT-0

## Use Case:

Teachers and education staff use this skill to turn course details, student context, and optional reference materials into a structured 21-field lesson plan for vocational education classes. It supports differentiated planning by selecting either a uniform-class or layered-class workflow before producing Markdown and DOCX outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process teaching documents, local paths, or knowledge-base items supplied by the user.

Mitigation: Confirm each source before parsing and avoid providing materials that should not be used for lesson-plan generation.

Risk: The skill relies on document parsing and optional OCR packages whose behavior depends on the local environment.

Mitigation: Install dependencies from a trusted, pinned environment and review generated Markdown and DOCX lesson plans before classroom use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/flyboat403/skills/teaching-plan-generator)
- [Server-Resolved GitHub Source](https://github.com/flyboat403/teaching-plan-generator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown preview plus Markdown and DOCX lesson-plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a teacher-confirmed 21-field lesson plan with quality checks for timing, structure, measurable objectives, and differentiation.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
