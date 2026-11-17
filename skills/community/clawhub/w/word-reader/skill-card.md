## Description:

Reads Word .docx and .doc files and extracts text, tables, document metadata, and image information in text, JSON, or Markdown formats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xtfnhcyjpgf](https://clawhub.ai/user/xtfnhcyjpgf)

### License/Terms of Use:

MIT

## Use Case:

Developers, employees, and external users can use this skill to inspect Word documents, extract document content, convert results to text, JSON, or Markdown, and process directories of Word files in batch workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can make system-level package changes.

Mitigation: Review the installer before running it, prefer a virtual environment for Python dependencies, avoid --break-system-packages, and use sudo or antiword only when legacy .doc support is required.

Risk: Extracted text, metadata, and batch output files can contain sensitive document contents.

Mitigation: Treat all extracted results as sensitive, limit where output files are written, and review generated text, JSON, or Markdown before sharing.

## Reference(s):

- [python-docx documentation](https://python-docx.readthedocs.io/)
- [ClawHub Word Reader release](https://clawhub.ai/xtfnhcyjpgf/skills/word-reader)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; script output can be text, JSON, or Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write extracted results to a user-specified output file; batch mode returns per-document results.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
