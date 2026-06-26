## Description: <br>
Manage Zotero reference libraries via the Web API, including search, item creation from DOI/ISBN/PMID, metadata updates, deletion or trashing, bibliography export, citation cross-referencing, missing DOI lookup, and open-access PDF fetching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Terwox](https://clawhub.ai/user/Terwox) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, students, and agents use this skill to manage personal or group Zotero libraries from a CLI-backed workflow. It supports library search, importing identifiers, updating metadata and tags, exporting bibliographies, checking PDF coverage, and fetching open-access PDFs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and change a Zotero personal or group library when provided an API key. <br>
Mitigation: Use a least-privilege Zotero API key and confirm whether the configured credentials target a personal or group library before running write operations. <br>
Risk: Bulk, delete, update, PDF fetch, export, and override options can modify Zotero data or write local files. <br>
Mitigation: Use scoping and preview controls such as --limit, --collection, --dry-run, and default recoverable trash behavior before using --yes, --permanent, --force, --upload, --download-dir, or --output. <br>


## Reference(s): <br>
- [ClawHub Zotero Skill](https://clawhub.ai/Terwox/zotero) <br>
- [Zotero API Key Settings](https://www.zotero.org/settings/keys/new) <br>
- [Zotero Web API Endpoint](https://api.zotero.org) <br>
- [Zotero Skill Troubleshooting](references/troubleshooting.md) <br>
- [Zotero Status](https://status.zotero.org) <br>
- [Crossref](https://www.crossref.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plain text CLI output, optional JSON for supported commands, and bibliography files such as BibTeX, RIS, or CSL-JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Zotero API credentials; write-capable commands may change Zotero library data, and selected export or PDF workflows may write local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
