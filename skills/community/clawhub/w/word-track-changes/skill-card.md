## Description:

Enables agents to edit DOCX files with Microsoft Word Track Changes using native OOXML revision elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elio-huang-15](https://clawhub.ai/user/elio-huang-15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-editing agents use this skill to apply auditable replacements, insertions, deletion marks, and batch revisions to Microsoft Word documents while preserving Word's review workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies user-provided DOCX files and can overwrite the input when no explicit output path is used.

Mitigation: Use explicit output paths and keep originals unchanged until the tracked revision output is reviewed.

Risk: Processing untrusted or unusually large DOCX files may consume excessive local resources because archive extraction is not size-limited.

Mitigation: Run only on trusted, reasonably sized documents or add external file size and archive expansion limits before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/elio-huang-15/skills/word-track-changes)
- [Publisher Profile](https://clawhub.ai/user/elio-huang-15)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces DOCX files with native Word revision markup when invoked through the included Python API or CLI scripts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
