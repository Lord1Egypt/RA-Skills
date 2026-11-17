## Description:

Upload PDFs and manage items in a Zotero Web Library. Supports both personal and group libraries. Use when a user wants to add papers/PDFs to Zotero, organize collections, or manage their Zotero library through the API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenhaox](https://clawhub.ai/user/chenhaox)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent configure Zotero access, inspect collections, create item metadata, and optionally attach PDFs to personal or group Zotero libraries after explicit approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Zotero API keys can grant broad library, notes, write, or group write access and may be exposed through command history or plaintext config.

Mitigation: Use ZOTERO_API_KEY or a restricted secret file, create the least-privilege Zotero key that supports the task, avoid broad group write permissions unless required, and review config.json permissions if it contains a key.

Risk: Resolving username-based personal libraries can place the Zotero API key in a Zotero API URL.

Mitigation: Prefer least-privilege keys and environment or secret-file loading, and account for the possibility that the key may appear in server access logs during personal-library lookup.

Risk: Write actions can create collections, create item metadata, or upload PDF attachments to a Zotero library.

Mitigation: Run read-only parse, list, and choose steps first; require explicit approval flags for create actions; and disable PDF upload in config unless attachment uploads are intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenhaox/skills/zotero-pdf-upload)
- [Approval Flow](references/approval-flow.md)
- [Configuration Example](references/config.example.json)
- [Item Metadata Example](references/item.example.json)
- [Zotero API key settings](https://www.zotero.org/settings/keys)
- [Zotero Web Library](https://www.zotero.org)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and machine-readable JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform Zotero API calls that create collections, create item metadata, or upload PDF attachments only when the documented approval flags and configuration allow those actions.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
