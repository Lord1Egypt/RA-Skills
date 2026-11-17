## Description:

A Chinese-language resume coaching skill that analyzes a target job description, gathers user career details through multi-turn questioning, and generates tailored resume and interview-strategy Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[page-wong](https://clawhub.ai/user/page-wong)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers and career coaches use this skill to analyze a target job description, identify relevant strengths and achievements, and prepare customized resume and interview materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to save sensitive personal career and contact details for later use.

Mitigation: Obtain explicit user consent before retaining information, avoid persistence when not needed, and redact unnecessary personal data from saved context.

Risk: Generated interview materials may include an author donation section or remote image.

Mitigation: Review generated documents before sharing and remove any donation section, image, or external link that is not appropriate for the user's context.

## Reference(s):

- [Workflow Guide](references/workflow.md)
- [Resume Template](references/resume-template.md)
- [Interview Strategy Template](references/interview-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown documents for a tailored resume and interview strategy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The interview strategy may include an author donation section with a remote image/link.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
