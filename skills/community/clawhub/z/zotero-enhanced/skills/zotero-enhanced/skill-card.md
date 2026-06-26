## Description: <br>
Manages the Zotero library with support for adding PDF documents with Crossref or arXiv metadata, searching items, reading attached files, and managing notes across Zotero cloud storage or WebDAV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoxh](https://clawhub.ai/user/guoxh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to search Zotero libraries, read attached PDFs, add new PDF documents with fetched metadata, and create, update, read, or delete Zotero notes through shell scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Zotero API access and can optionally use WebDAV credentials. <br>
Mitigation: Use only credentials intended for this workflow, keep them in environment variables, and remove or rotate them when no longer needed. <br>
Risk: Legacy add scripts can mutate a Zotero library before failing or uploading through WebDAV. <br>
Mitigation: Prefer scripts/add_to_zotero_universal.sh with --dry-run for PDF additions, and use the older add scripts only after confirming WebDAV variables and intended upload behavior. <br>
Risk: Note and document operations can create, update, or delete library content. <br>
Mitigation: Use dry-run modes where available, keep delete confirmations enabled unless automation requires otherwise, and use backup options before destructive note operations. <br>


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
1.3.6 (source: server release metadata and artifact changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
