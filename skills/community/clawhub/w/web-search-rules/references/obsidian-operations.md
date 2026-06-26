# Obsidian Operations

Obsidian is the preferred local adapter for privacy-sensitive use.

## Capabilities

Filesystem method:

```json
{
  "name": "obsidian",
  "method": "filesystem",
  "cloud_upload": false,
  "capabilities": ["read", "write", "list", "archive", "delete", "migrate"],
  "auth": "none",
  "confirmation": "write"
}
```

Local REST API method:

```json
{
  "name": "obsidian",
  "method": "rest-api",
  "cloud_upload": false,
  "capabilities": ["read", "write", "list", "archive", "delete", "migrate"],
  "auth": "api-key-env",
  "confirmation": "write"
}
```

## Path rules

- Require a user-confirmed vault path.
- Resolve paths before writing.
- Deny writes outside the vault.
- Deny filenames with path separators, `..`, Windows reserved names, or unsupported characters.
- Prefer Markdown files and UTF-8 encoding.

## Structure

```text
<Vault>/search-url-library/whitelist/
<Vault>/search-url-library/blacklist/
<Vault>/search-url-library/uncategorized/
<Vault>/unorganized-search-content/YYYY-MM-DD/
```

## API key rule

Do not store Obsidian Local REST API keys in `config.json`. Read them from the host credential manager or environment when the user has configured that method.

## Delete and cleanup

Never remove staged files automatically after archiving. Present a dry-run list and ask for second confirmation.
