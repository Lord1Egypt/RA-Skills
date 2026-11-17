## Description:

Generate and parse UUIDs (v1, v4, v5), with batch generation, validation, format conversion, and no API key requirement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to generate, validate, parse, and reformat UUID values in local workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: UUID v1 values can include timestamp and host-identifying metadata.

Mitigation: Prefer UUID v4 for general identifiers, and use UUID v1 only when that metadata is acceptable for the storage or sharing context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/uuid-generator-tool)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces UUID strings, validation status, and parsed UUID components using Python standard library behavior.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
