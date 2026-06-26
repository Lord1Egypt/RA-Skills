# Feishu Wiki and DingTalk Docs Operations

Use this file when the selected platform is `feishu-wiki` or `dingtalk-docs`.

## Feishu Wiki

Recommended declaration:

```json
{
  "name": "feishu-wiki",
  "method": "connector",
  "cloud_upload": true,
  "capabilities": ["read", "write", "list", "archive", "delete", "migrate", "upload"],
  "auth": "connector",
  "confirmation": "cloud_upload"
}
```

Workflow:

1. Resolve the target wiki space explicitly.
2. Resolve or create `Search URL Library` and `Unorganized Search Content` nodes after confirmation.
3. Store rules as Docs, Markdown files, or Base records according to the user's existing workspace pattern.
4. Stage content in date-based child documents.
5. Use dry-run plus second confirmation before deleting nodes or migrating between spaces.

Safety notes:

- Do not infer a wiki space from a partial name if multiple matches exist.
- Show the target space, parent node, document title, and item count before writing.
- Treat all writes as cloud uploads.

## DingTalk Docs

Recommended declaration:

```json
{
  "name": "dingtalk-docs",
  "method": "connector-or-api",
  "cloud_upload": true,
  "capabilities": ["read", "write", "list", "archive", "delete", "migrate", "upload"],
  "auth": "connector",
  "confirmation": "cloud_upload"
}
```

Workflow:

1. Resolve the DingTalk workspace and folder.
2. Resolve or create `Search URL Library` and `Unorganized Search Content` after confirmation.
3. Store rules in separate documents or tables named `Whitelist`, `Blacklist`, and `Uncategorized`.
4. Stage content in date-based documents.
5. Prefer API or connector operations. Use browser automation only if no safer integration is available.

Safety notes:

- Confirm workspace, folder, and document title before each write batch.
- Treat all writes as cloud uploads.
- Browser-only flows require the `browser_automation` confirmation level.
