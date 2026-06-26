# NotebookLM Operations

NotebookLM is a high-risk cloud adapter because content is uploaded to Google services and operations often require browser automation.

## Capabilities

Browser method:

```json
{
  "name": "notebooklm",
  "method": "browser-automation",
  "cloud_upload": true,
  "capabilities": ["read", "archive", "upload"],
  "auth": "manual-login",
  "confirmation": "browser_automation"
}
```

Google Drive import method:

```json
{
  "name": "notebooklm",
  "method": "google-drive-import",
  "cloud_upload": true,
  "capabilities": ["archive", "upload"],
  "auth": "oauth",
  "confirmation": "cloud_upload"
}
```

## Hard rules

- NotebookLM is disabled until the user explicitly selects it.
- Do not automate Google login.
- Do not store Google passwords, cookies, credentials, refresh tokens, or browser sessions in skill config.
- Prefer a separate browser profile.
- Warn before each upload batch that content will be sent to Google.
- Use minimal OAuth scopes for Drive import, such as `drive.file`, when the host implementation supports OAuth.

## Suggested flow

1. Confirm NotebookLM as the selected platform.
2. Show cloud upload warning and item count.
3. Ask the user to log in manually if browser automation is used.
4. Upload only user-confirmed items.
5. Append audit records with item count and confirmation id.
6. Keep local staging until the user confirms cleanup separately.
