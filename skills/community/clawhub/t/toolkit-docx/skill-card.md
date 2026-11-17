## Description:

DOCX Toolkit helps agents create, read, edit, and analyze Word .docx documents, including formatted document generation, existing document edits, and content extraction or reorganization, while excluding PDF, spreadsheet, and Google Docs workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sougannkyou](https://clawhub.ai/user/sougannkyou)

### License/Terms of Use:

Proprietary

## Use Case:

Developers and document automation agents use this skill to create, inspect, convert, validate, and edit Word .docx files for reports, memos, letters, and similar business documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends a global unpinned npm install for the DOCX generation library, which can change dependency behavior over time.

Mitigation: Use a pinned local dependency before relying on the skill for repeatable or sensitive document workflows.

Risk: DOCX workflows may process sensitive documents and unpack document XML into the workspace.

Mitigation: Run the skill in an isolated workspace and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sougannkyou/skills/toolkit-docx)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JavaScript, XML, and command-line snippets for DOCX creation, inspection, conversion, validation, and repair.]

## Skill Version(s):

0.21.4 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
