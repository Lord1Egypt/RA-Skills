## Description: <br>
Upload PDFs and manage items in a Zotero Web Library. Supports both personal and group libraries. Use when a user wants to add papers/PDFs to Zotero, organize collections, or manage their Zotero library through the API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenhaox](https://clawhub.ai/user/chenhaox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to a Zotero personal or group library so it can inspect collections, create item metadata, and optionally upload PDF attachments with explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Zotero API keys can grant library and write access, and setup can store the key locally in plaintext. <br>
Mitigation: Prefer ZOTERO_API_KEY or a protected secret file, use a least-privilege Zotero key, and avoid inline config storage. <br>
Risk: Write operations can create collections, create items, or upload PDFs to a Zotero library. <br>
Mitigation: Run read-only inspection first and require explicit approval flags before collection, item, or PDF upload changes. <br>
Risk: Personal-library ID lookup sends the API key in the Zotero keys endpoint URL, which may appear in server logs. <br>
Mitigation: Prefer explicit library IDs where practical and use least-privilege credentials as described by the skill guidance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenhaox/zotero-pdf-upload) <br>
- [Approval Flow](references/approval-flow.md) <br>
- [Config Example](references/config.example.json) <br>
- [Item Example](references/item.example.json) <br>
- [Zotero](https://www.zotero.org) <br>
- [Zotero API Key Settings](https://www.zotero.org/settings/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration/status outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the Zotero Web API to read or modify library collections, item metadata, and PDF attachments after explicit approval.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
