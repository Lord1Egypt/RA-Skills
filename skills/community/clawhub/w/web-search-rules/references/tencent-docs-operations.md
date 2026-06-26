# Tencent Docs Operations

Tencent Docs is a cloud collaborative document adapter. Treat rule files and staged content as cloud data.

## Capabilities

Recommended declaration:

```json
{
  "name": "tencent-docs",
  "method": "connector",
  "cloud_upload": true,
  "capabilities": ["read", "write", "list", "archive", "delete", "migrate", "upload"],
  "auth": "connector",
  "confirmation": "cloud_upload"
}
```

## Structure

- Folder or document group: `Search URL Library`
  - `Whitelist`
  - `Blacklist`
  - `Uncategorized`
- Folder or document group: `Unorganized Search Content`
  - Date-based documents

## Operations

- Read rules from the three rule documents.
- Append confirmed rules instead of overwriting whole documents when possible.
- Stage content in date-based documents with original URL and normalized URL.
- Use version history or duplicate backup before destructive changes when available.

## Required confirmations

- Confirm target workspace and folder before writes.
- Confirm cloud upload batches.
- Use dry-run plus second confirmation for delete, cleanup, or migration.
