## Description:

Guides users through collecting tender project information and generating a package of standardized project documents from templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mama1234421](https://clawhub.ai/user/mama1234421)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect project, company, pricing, and technical inputs through a guided workflow, then generate tender document packages and supporting automation commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles banking details, contact information, company identifiers, and generated tender documents that may be sensitive.

Mitigation: Keep input JSON and generated ZIP/DOCX files out of version control and shared workspaces, and replace realistic sample data with placeholders before release.

Risk: Unsafe file-writing behavior may be exposed when generating ZIP filenames or output paths from user-provided project data.

Mitigation: Review generated filenames and avoid running the generator on untrusted JSON until ZIP filename handling is sanitized.

Risk: Generated tender documents may contain missing fields, incorrect formatting, or placeholders that are not ready for formal use.

Mitigation: Perform manual review of all generated documents, replace required scans or signatures, and verify technical parameters and pricing before submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mama1234421/skills/tender-generator-skill)
- [README](artifact/README.md)
- [Usage guide](artifact/USAGE.md)
- [Default template guide](artifact/templates/默认/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and generated DOCX/ZIP files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents require human review before formal submission.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
