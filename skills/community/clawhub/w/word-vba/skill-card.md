## Description:

Automates Microsoft Word through Python VBA/ActiveX to read, write, merge, fill templates, replace text, generate tables of contents, compare, and batch-process DOC/DOCX files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document automation users use this skill to control local Microsoft Word for precise DOC/DOCX reading, creation, formatting, merging, template filling, and batch edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill drives Microsoft Word under the user's local account and can read or change local documents.

Mitigation: Install only when local Word automation is needed, use explicit output paths, and keep backups of important documents.

Risk: Opening untrusted Word files through local automation can expose the user to document-borne risks.

Mitigation: Avoid opening untrusted Word files and scan documents before processing them.

Risk: Batch replacement, merging, template filling, and comparison workflows can produce incorrect or unintended document changes.

Mitigation: Write results to separate output files and review generated documents before distribution or overwrite.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/word-vba)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks; local DOC/DOCX files when the generated helper code is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Windows, Microsoft Word 2010 or later, and pywin32; use explicit output paths and review generated documents before replacing originals.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
