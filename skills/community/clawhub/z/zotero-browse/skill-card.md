## Description:

Zotero Browse lets an agent search a local Zotero library, summarize library contents, and extract text from stored PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyononthemoon](https://clawhub.ai/user/lyononthemoon)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, students, and knowledge workers with a local Zotero library use this skill to search bibliographic records, inspect recent library contents, and extract stored PDF text for summarization or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect local Zotero records and stored PDF text.

Mitigation: Install and use it only when the agent is intended to access that local Zotero library and document content.

Risk: The optional export path can save extracted PDF text to disk.

Mitigation: Use --output only when a saved text file is needed and review the destination path before running it.

Risk: PDF contents may include untrusted or misleading text.

Mitigation: Treat extracted PDF text as material to summarize or analyze, not as instructions for the agent to follow.

## Reference(s):

- [Zotero SQLite Database Schema](references/schema.md)
- [ClawHub skill page](https://clawhub.ai/lyononthemoon/skills/zotero-browse)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with Python command examples and text output from local Zotero and PDF scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 with sqlite3 and PyMuPDF; output may include local bibliographic metadata, PDF metadata, extracted PDF text, and optional text files when export is requested.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
