## Description:

Manage Zotero reference libraries via the Web API, including searching and listing items, adding citations by DOI/ISBN/PMID, updating metadata and tags, exporting bibliographies, cross-referencing citations, finding missing DOIs, and fetching open-access PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terwox](https://clawhub.ai/user/terwox)

### License/Terms of Use:


## Use Case:

Developers, researchers, and agents use this skill to manage Zotero personal or group libraries through the Zotero Web API, including search, citation import, metadata updates, bibliography export, PDF checks, and open-access PDF retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Zotero API key that can expose or modify a user's Zotero library depending on key permissions.

Mitigation: Prefer a read-only Zotero API key unless add, update, delete, or upload features are needed; use --dry-run, --limit, and --collection before batch operations.

Risk: The PDF-fetching feature can download from unvalidated third-party URLs.

Mitigation: Avoid fetch-pdfs on networks where the agent can reach sensitive internal services until URL validation and download-size limits are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terwox/skills/zotero)
- [Zotero API endpoint](https://api.zotero.org)
- [Zotero API key settings](https://www.zotero.org/settings/keys/new)
- [Zotero status](https://status.zotero.org)
- [CrossRef](https://www.crossref.org)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with command examples; CLI output may be text or JSON; exports may be BibTeX, RIS, CSL-JSON, or downloaded PDF files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZOTERO_API_KEY and either ZOTERO_USER_ID or ZOTERO_GROUP_ID; some write and upload features require Zotero API key permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
