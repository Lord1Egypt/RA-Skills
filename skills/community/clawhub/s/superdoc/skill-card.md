## Description:

Create, edit, and manipulate DOCX files using SuperDoc, a modern document editor with a custom rendering pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yebo-liu](https://clawhub.ai/user/yebo-liu)

### License/Terms of Use:

AGPLv3 for community use, commercial license available

## Use Case:

Developers and engineers use this skill to create, edit, format, and generate DOCX documents in browser, React, and headless Node.js workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and write local DOCX files, so accidental overwrites or unintended document changes are possible.

Mitigation: Use copies or backups for important documents and keep generated files in a deliberate output folder.

Risk: Template generation can process client data such as names and email addresses.

Mitigation: Limit input data to necessary fields and handle generated documents according to the applicable data handling policy.

Risk: Unpinned or global npm installs can make behavior harder to reproduce.

Mitigation: Prefer pinned, project-local npm dependencies for repeatable use.

## Reference(s):

- [SuperDoc reference](references/superdoc-reference.md)
- [SuperDoc repository](https://github.com/superdoc-dev/superdoc)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, JSX, and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include DOCX file paths, dependency setup steps, and document generation examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
