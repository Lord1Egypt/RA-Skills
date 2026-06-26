# IMA Operations

IMA is a cloud knowledge-base adapter. Treat all full-content writes as cloud uploads.

## Capabilities

Recommended declaration:

```json
{
  "name": "ima",
  "method": "connector",
  "cloud_upload": true,
  "capabilities": ["read", "write", "list", "archive", "delete", "migrate", "upload"],
  "auth": "connector",
  "confirmation": "cloud_upload"
}
```

## Structure

- Knowledge base: `Search URL Library`
  - `Whitelist`
  - `Blacklist`
  - `Uncategorized`
- Knowledge base: `Unorganized Search Content`
  - Date-based staged documents

## Required confirmations

- Confirm before creating or updating knowledge bases.
- Confirm each upload batch and show item count.
- Use dry-run plus second confirmation before deletion or migration.

## Failure handling

If upload fails, keep local staging metadata and report which items remain unsaved. Do not add whitelist rules for items that were not successfully staged or archived unless the user explicitly confirms the rule update separately.
