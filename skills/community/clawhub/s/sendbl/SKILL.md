---
name: sendbl
description: Create sendbl file-exchange links — request files from someone, send a file, check link status, list files in a link, or delete a link. Use when the user wants to share a file or collect files from a counterparty over a link.
homepage: https://sendbl.com
metadata:
  openclaw:
    primaryEnv: SENDBL_API_KEY
    requires:
      env: [SENDBL_API_KEY]
    emoji: "📎"
---

# sendbl

Create and manage [sendbl](https://sendbl.com) file-exchange links from the assistant. sendbl is a file-transfer API for LLM agents: links to **collect** files from someone, or to **send** a file to someone, with quotas and expiry.

## Setup (one-time)

1. Sign in at <https://sendbl.com/account> with Google.
2. Open <https://sendbl.com/account/tokens> and create a **personal access token**. Treat this token as a password: store it only in your environment, revoke it from the same page if it is ever exposed, and rotate it periodically.
3. Set the env var:

   ```sh
   export SENDBL_API_KEY="sk_pat_..."
   ```

The skill will not work without `SENDBL_API_KEY`.

## API base URL

All endpoints below are relative to:

```
https://api.sendbl.com/v1
```

All API key calls send the key as the `x-api-key` header.

## Capabilities

### 1. Request files from someone

When the user wants someone else to upload files **to** them.

```sh
curl -sS -X POST "https://api.sendbl.com/v1/requestFiles" \
  -H "x-api-key: $SENDBL_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "expires_in_hours": 72,
    "max_files": 10,
    "purpose": "<short reason>",
    "message": "<optional note shown to uploader>"
  }'
```

Returns `upload_url` (share with the counterparty), `download_url` (for retrieval), `owner_token` (keep — required for delete and list-files), and `upload_link_id`.

After calling, **tell the user to save `owner_token` and `upload_link_id`** — they cannot be recovered later.

### 2. Send a file to someone

When the user wants to share a single file. This is the convenience wrapper.

```sh
curl -sS -X POST "https://api.sendbl.com/v1/sendFile" \
  -H "x-api-key: $SENDBL_API_KEY" \
  -H "content-type: application/json" \
  -d '{
    "recipient_name": "<name or email>",
    "filename": "<file.ext>",
    "purpose": "<short reason>",
    "message": "<optional note>"
  }'
```

Returns `presigned_upload_url` (PUT the actual bytes there), `download_url` (share with recipient — null until upload completes), `owner_token`, and `file_id`.

**The skill itself does not upload bytes.** Instruct the user to PUT the file:

```sh
curl -X PUT --data-binary @<local-file> "<presigned_upload_url>"
```

### 3. Check link status (no auth)

```sh
curl -sS "https://api.sendbl.com/v1/uploadLinkStatus?upload_link_id=<id>"
```

Returns status (`open` / `closed` / `expired`), `expires_at`, `file_count`. Use when the user pastes a link and wants to know if it's still valid.

### 4. List files in a link

Requires the `owner_token` from step 1 (or 2).

```sh
curl -sS "https://api.sendbl.com/v1/uploadedFiles?token=<owner_token>&limit=50"
```

Returns the array of files with `file_id` and `filename`. To get a download URL for one of them:

```sh
curl -sS "https://api.sendbl.com/v1/fileDownloadLink?token=<owner_token>&file_id=<file_id>"
```

### 5. Delete a link

Requires the `owner_token`. Removes the link **and all uploaded files**.

```sh
curl -sS -X DELETE "https://api.sendbl.com/v1/uploadLink?token=<owner_token>"
```

Confirm with the user before calling — this is irreversible.

## Errors

- `401 unauthorized` — missing or invalid `x-api-key` / `owner_token`. If the skill worked previously and now returns 401, the token has likely been revoked — instruct the user to issue a new one at <https://sendbl.com/account/tokens>.
- `403 forbidden` — token role mismatch (e.g., uploader token used for owner action).
- `429 quota_exceeded` — API key has hit the monthly link limit. Surface this verbatim; do not retry.
- `404 link_not_found` — link expired or was deleted.

## Conventions

- Never POST file bytes to the sendbl API. Bytes always go to the presigned S3 URL via PUT.
- Always remind the user to save `owner_token` and `upload_link_id` after creating a link — they're not retrievable later.
- Treat `download_url` and `upload_url` as different audiences: upload URL goes to the sender, download URL goes to the recipient.
- Default `expires_in_hours` to 72 unless the user specifies otherwise.
