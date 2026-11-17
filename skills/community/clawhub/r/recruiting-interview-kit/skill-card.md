## Description:

Generates interview questions, scoring dimensions, red flags, and interview record templates from job descriptions for recruiting and structured interview workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiters, hiring managers, and interview coordinators use this skill to turn job descriptions, levels, and key competencies into review-ready interview kits. It supports structured recruiting preparation without generating discriminatory questions or replacing final hiring decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is local and non-networked, but security evidence reports broader file-audit and secret-pattern scanning code that is not clearly part of interview preparation.

Mitigation: Review the script modes and path scope before installation, and use it with recruiting inputs or explicit dry-run review unless broader audit behavior is intended.

Risk: Recruiting materials can contain personal or sensitive candidate data.

Mitigation: Redact sensitive personal data where possible and review generated questions for legal, privacy, and anti-discrimination requirements before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/recruiting-interview-kit)
- [Output template](artifact/resources/template.md)
- [Structured specification](artifact/resources/spec.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON recruiting interview kit with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write output to a chosen local file; otherwise returns stdout.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
