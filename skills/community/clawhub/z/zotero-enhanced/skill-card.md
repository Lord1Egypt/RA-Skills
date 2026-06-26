## Description: <br>
Manages the Zotero library with support for adding PDF documents with Crossref or arXiv metadata, searching items, reading attached files, and managing notes across Zotero cloud storage and WebDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoxh](https://clawhub.ai/user/guoxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to search Zotero libraries, read attached PDFs, add PDF documents with fetched metadata, and create, update, read, or delete Zotero notes through shell scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, upload, edit, and delete Zotero library content using user credentials. <br>
Mitigation: Install only if you trust the publisher, use a least-privilege Zotero API key, and rotate or revoke credentials when the workflow is no longer needed. <br>
Risk: Optional WebDAV storage sends files and credentials to a user-configured endpoint. <br>
Mitigation: Use HTTPS WebDAV endpoints you control and avoid confidential PDFs unless the remote services are approved for that data. <br>
Risk: Note deletion can remove library content without an interactive prompt when --no-confirm is used. <br>
Mitigation: Keep delete confirmations enabled by default, use backup or dry-run options where available, and allow --no-confirm only after approving the exact note being deleted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guoxh/zotero-enhanced) <br>
- [Zotero](https://www.zotero.org) <br>
- [Zotero API](https://api.zotero.org/) <br>
- [Crossref API](https://api.crossref.org/) <br>
- [arXiv API](https://export.arxiv.org/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands; scripts return formatted text, JSON, or plain text depending on the operation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zotero API credentials and optional WebDAV credentials; several mutating operations provide dry-run, confirmation, backup, or conflict-checking behavior.] <br>

## Skill Version(s): <br>
1.3.7 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
