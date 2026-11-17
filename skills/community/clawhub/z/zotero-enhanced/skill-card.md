## Description:

Zotero library management with PDF metadata auto-fetch (Crossref/arXiv), item search, file read, and note management. Supports cloud and WebDAV storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoxh](https://clawhub.ai/user/guoxh)

### License/Terms of Use:

MIT

## Use Case:

Researchers, students, and developers use this skill to search Zotero libraries, add PDFs with academic metadata, read stored documents, and manage Zotero notes from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Zotero API credentials and may modify a user's remote library.

Mitigation: Use a Zotero API key with the minimum scopes needed and review dry-run output before write operations.

Risk: Note deletion can be irreversible, especially when --no-confirm is used.

Mitigation: Prefer confirmation prompts, use --dry-run before deletion, and enable --backup when preserving note content is required.

Risk: Optional WebDAV storage requires sending credentials to a user-configured storage endpoint.

Mitigation: Use only WebDAV servers the user controls and trusts; the artifact documents https:// enforcement for WebDAV URLs.

## Reference(s):

- [Zotero](https://www.zotero.org)
- [Zotero API](https://api.zotero.org/)
- [Crossref API](https://api.crossref.org/)
- [arXiv API](https://export.arxiv.org/api/)
- [ClawHub skill page](https://clawhub.ai/guoxh/skills/zotero-enhanced)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal text with inline bash commands and JSON API responses where scripts expose raw item data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Zotero API credentials, optional WebDAV credentials, and local command-line dependencies including curl, jq, pdftotext, zip, unzip, and md5sum or md5.]

## Skill Version(s):

1.3.14 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
