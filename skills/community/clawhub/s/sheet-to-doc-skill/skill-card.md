## Description:

Generate Word documents from Word templates and JSON data. Supports basic placeholder replacement ({field} format) and placeholder extraction for data validation. Best for batch-generating contracts, invitations, certificates, and mail-merge style docs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[he-yang](https://clawhub.ai/user/he-yang)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and document-automation teams use this skill to generate Word .docx files from templates and JSON data, extract required placeholders, and validate data keys before generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Word documents include Sheet-to-Doc promotional footer text and modified lastModifiedBy metadata.

Mitigation: Inspect and clean generated files before using them as official, contractual, certificate, or client-facing documents.

Risk: The skill depends on npm packages and a lockfile that should be reviewed before installation.

Mitigation: Review the package lockfile source and dependency versions before installing or running the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/he-yang/skills/sheet-to-doc-skill)
- [Sheet-to-Doc homepage](https://sheet-to-doc.wtsolutions.cn)
- [Sheet-to-Doc documentation](https://sheet-to-doc.wtsolutions.cn/en/latest/index.html)
- [Full Sheet-to-Doc version](https://s.wtsolutions.cn/sheet-to-doc.html)

## Skill Output:

**Output Type(s):** [Files, JSON, Shell commands, Code, Guidance]

**Output Format:** [Word .docx files, JSON placeholder lists, and Markdown guidance with shell or JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated documents include Sheet-to-Doc footer text and modified lastModifiedBy metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
