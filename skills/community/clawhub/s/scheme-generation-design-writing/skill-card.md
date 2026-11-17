## Description:

Generates concept proposal and design description documents from historical UI/UX project materials, local design images, and optional Figma inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaco223](https://clawhub.ai/user/shaco223)

### License/Terms of Use:

MIT

## Use Case:

Designers, product teams, and developers use this skill to match relevant historical projects, draft concept proposals, and produce structured design descriptions for UI/UX projects. It is intended for normal ClawHub release use with human review before generated documents are relied on.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guide includes Figma configuration guidance that weakens HTTPS certificate verification while handling design data and tokens.

Mitigation: Do not set verify=False or suppress HTTPS warnings; use a trusted CA or approved proxy configuration, keep Figma tokens read-only, and store tokens securely.

Risk: Historical project folders may contain confidential, regulated, or credential-bearing files.

Mitigation: Use only approved and sanitized historical-project folders, and exclude secrets, personal data, and regulated data before indexing or generation.

Risk: Generated proposals and design descriptions may be incomplete, incorrect, or misaligned with the source design.

Mitigation: Have a qualified reviewer compare generated documents with the original requirements, design assets, and organization-approved design standards before use.

## Reference(s):

- [Quick Start](references/quick-start.md)
- [Concept Plan Schema](references/concept_plan_schema.md)
- [Design Description Schema](references/design_desc_schema.md)
- [Examples](references/examples.md)
- [Figma](https://www.figma.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance and structured document drafts; host agents may render final proposal or design-description files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated content should be reviewed against source designs, project requirements, and approved design standards before use.]

## Skill Version(s):

1.0.1 (source: server release metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
