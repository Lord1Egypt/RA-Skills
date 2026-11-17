## Description:

Generates software design documentation from uploaded requirement or technical specification files, with user confirmation before key decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlq54321](https://clawhub.ai/user/zlq54321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn uploaded requirements documents and technical notes into confirmed design-document structure, detailed design prose, and a starter project skeleton.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded document contents are inspected during use.

Mitigation: Use only files the user explicitly selected and avoid processing sensitive documents unless the user approves.

Risk: User- or file-derived folder names may affect shell file operations.

Mitigation: Require safe folder names and exact path confirmation before running directory or file commands.

Risk: Moving uploaded files can place them in an unintended project folder or remove them from the inbound area.

Mitigation: Prefer copying uploads, or confirm source and destination paths before moving files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlq54321/skills/skill-doc-design)
- [Publisher profile](https://clawhub.ai/user/zlq54321)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown documents, progress messages, and shell/file-operation command sequences]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation for folder name, technical findings, and document scope before generating files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
