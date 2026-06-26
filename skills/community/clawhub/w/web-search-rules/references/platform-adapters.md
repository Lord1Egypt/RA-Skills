# Platform Adapters

Use this file before operating any knowledge-base platform.

## Common adapter contract

Every adapter must declare:

- `name`: adapter id.
- `method`: API, connector, filesystem, browser, or custom.
- `cloud_upload`: true when content leaves the local machine.
- `capabilities`: allowed operations from `read`, `write`, `list`, `archive`, `delete`, `migrate`, `upload`.
- `auth`: none, manual-login, connector, oauth, api-key-env, or user-provided.
- `confirmation`: highest confirmation level required by this adapter.

Unlisted capabilities are denied.

## Adapter matrix

| Adapter | Storage | Method | Cloud upload | Default status | Notes |
| --- | --- | --- | --- | --- | --- |
| `ima` | Cloud | IMA connector/skill | Yes | Enabled after user selection | Confirm upload batches. |
| `tencent-docs` | Cloud | Tencent Docs connector/skill | Yes | Enabled after user selection | Use document version history when available. |
| `feishu-wiki` | Cloud | Feishu/Lark wiki/doc/drive tools | Yes | Enabled after user selection | Resolve docs and wiki nodes explicitly. |
| `dingtalk-docs` | Cloud | DingTalk document API or browser flow | Yes | Enabled after user selection | Prefer API/connector over browser automation. |
| `obsidian` | Local | Filesystem or Local REST API | No by default | Recommended for privacy | Restrict to approved vault path. |
| `notebooklm` | Cloud | Browser automation or Google Drive import | Yes | Disabled until explicitly selected | High risk; no automated login. |
| `custom` | Unknown | User-provided | Depends | Disabled until declared | Only declared capabilities may run. |

## Standard operations

- Create stores: create `search-url-library` and `unorganized-search-content` or platform equivalents.
- Read rules: load whitelist, blacklist, and uncategorized records.
- Stage content: write normalized metadata, summary, and untrusted content section.
- Archive content: move or copy confirmed staged items to the target knowledge base.
- Delete staged content: dry-run first, then second confirmation.
- Migrate platform: export source, validate counts, import destination, and leave source unchanged unless separately confirmed.

## Feishu Wiki

Use Feishu/Lark tools for wiki, docs, drive, and base operations. Store rules in a Docx document, Markdown file, or Base table depending on the user's workspace preference. Before writing, show the target wiki space, node, and document title. Do not infer a space from a similarly named document.

Recommended structure:

- Wiki node: `Search URL Library`
- Child document or table: `Whitelist`, `Blacklist`, `Uncategorized`
- Wiki node: `Unorganized Search Content`
- Date folders or documents for staged content

## DingTalk Docs

Use DingTalk document APIs/connectors when available. If only browser automation is available, treat the adapter like `browser_automation` and ask before each session. Confirm the workspace, folder, and document title before writes.

Recommended structure:

- Folder/document: `Search URL Library`
- Documents: `Whitelist`, `Blacklist`, `Uncategorized`
- Folder/document: `Unorganized Search Content`
- Date-based staged documents

## Custom adapters

Ask the user for a capability declaration before use:

```json
{
  "name": "custom-platform",
  "method": "api",
  "cloud_upload": true,
  "capabilities": ["read", "write", "archive"],
  "auth": "user-provided"
}
```

If a capability is not declared, do not perform it.
