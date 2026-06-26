---
name: zoho-mail
description: Read, search, and manage Zoho Mail via the Zoho Mail REST API.
homepage: https://www.zoho.com/mail/help/api/
metadata: {"clawdbot":{"emoji":"📧","requires":{"bins":["jq","curl"],"env":["ZOHO_CLIENT_ID","ZOHO_CLIENT_SECRET","ZOHO_REFRESH_TOKEN"]}}}
---

# Zoho Mail Skill

Read, search, and manage Zoho Mail directly from Clawdbot.

## Setup

1. Go to [Zoho API Console](https://api-console.zoho.com/) and create a **Self Client**
2. Note the **Client ID** and **Client Secret**
3. Generate a grant code with scopes: `ZohoMail.messages.READ,ZohoMail.folders.READ,ZohoMail.accounts.READ`
4. Exchange the grant code for a refresh token:
   ```bash
   curl -s -X POST "https://accounts.zoho.com/oauth/v2/token" \
     -d "code=YOUR_GRANT_CODE" \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET" \
     -d "grant_type=authorization_code" | jq
   ```
5. Set environment variables:
   ```bash
   export ZOHO_CLIENT_ID="your-client-id"
   export ZOHO_CLIENT_SECRET="your-client-secret"
   export ZOHO_REFRESH_TOKEN="your-refresh-token"
   ```

## Authentication

Zoho uses OAuth 2.0. Access tokens expire after 1 hour, so always refresh before making API calls. The refresh token does not expire unless revoked.

### Get an access token
```bash
ZOHO_ACCESS_TOKEN=$(curl -s -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "refresh_token=$ZOHO_REFRESH_TOKEN" \
  -d "client_id=$ZOHO_CLIENT_ID" \
  -d "client_secret=$ZOHO_CLIENT_SECRET" \
  -d "grant_type=refresh_token" | jq -r '.access_token')
```

**Important:** Run this command before every API session or when you get a 401 error. All commands below assume `$ZOHO_ACCESS_TOKEN` is set.

## Usage

All commands use curl with the `Zoho-oauthtoken` authorization header. Note: Zoho uses `Zoho-oauthtoken` prefix, **not** `Bearer`.

### Get account ID
```bash
curl -s "https://mail.zoho.com/api/accounts" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[0] | {accountId, mailboxAddress, firstName, lastName}'
```

Store the account ID for subsequent calls:
```bash
ZOHO_ACCOUNT_ID=$(curl -s "https://mail.zoho.com/api/accounts" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq -r '.data[0].accountId')
```

### List folders
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/folders" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {folderName, folderId, unreadCount, messageCount}'
```

### Get Inbox folder ID
```bash
INBOX_ID=$(curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/folders" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq -r '.data[] | select(.folderName=="Inbox") | .folderId')
```

### List inbox messages
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/messages/view?folderId=$INBOX_ID&limit=10&start=0" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {subject, sender, fromAddress, receivedTime, messageId, status2}'
```

### List messages in a specific folder
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/messages/view?folderId={folderId}&limit=10&start=0" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {subject, sender, receivedTime, messageId}'
```

### Read a specific email
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/messages/{messageId}" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data | {subject, sender, fromAddress, toAddress, ccAddress, receivedTime, content}'
```

### Get email body content only
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/messages/{messageId}/content" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq -r '.data.content'
```

### Search emails
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/messages/search?searchKey={query}&limit=10" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {subject, sender, receivedTime, messageId, summary}'
```

Search syntax supports:
- Simple text: `searchKey=invoice`
- From filter: `searchKey=from:john@example.com`
- Subject filter: `searchKey=subject:quarterly report`
- Date range: `searchKey=after:2024-01-01 before:2024-06-30`
- Combined: `searchKey=from:boss@company.com subject:meeting`

### List email threads
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/threads/view?folderId=$INBOX_ID&limit=10&start=0" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {subject, threadId, messageCount}'
```

### Get thread details (all messages in a thread)
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/threads/{threadId}" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq
```

### List labels/tags
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/tags" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {tagName, tagId, color}'
```

### List attachments on an email
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/folders/{folderId}/messages/{messageId}/attachments" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {attachmentName, attachmentId, fileSize}'
```

### Get account info
```bash
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data | {firstName, lastName, mailboxAddress, usedStorage, planStorage}'
```

## Regional Endpoints

If your Zoho account is not in the US region, replace `mail.zoho.com` and `accounts.zoho.com` with:

| Region    | Mail API                  | Auth                    |
|-----------|---------------------------|-------------------------|
| US        | mail.zoho.com             | accounts.zoho.com       |
| EU        | mail.zoho.eu              | accounts.zoho.eu        |
| India     | mail.zoho.in              | accounts.zoho.in        |
| Australia | mail.zoho.com.au          | accounts.zoho.com.au    |
| Japan     | mail.zoho.jp              | accounts.zoho.jp        |
| Canada    | mail.zohocloud.ca         | accounts.zohocloud.ca   |

## Notes

- Access tokens expire after **1 hour** — refresh before each session
- The refresh token does **not** expire unless revoked
- Rate limit: **30 API requests per minute** per account
- `receivedTime` is in milliseconds since epoch — convert with: `date -d @$((receivedTime/1000))`
- `status2` field: `"0"` = unread, `"1"` = read
- Auth header uses `Zoho-oauthtoken` prefix, **not** `Bearer`
- Keep your Client Secret and Refresh Token secure!

## Examples

```bash
# Full session: refresh token, get account, list inbox
ZOHO_ACCESS_TOKEN=$(curl -s -X POST "https://accounts.zoho.com/oauth/v2/token" \
  -d "refresh_token=$ZOHO_REFRESH_TOKEN" \
  -d "client_id=$ZOHO_CLIENT_ID" \
  -d "client_secret=$ZOHO_CLIENT_SECRET" \
  -d "grant_type=refresh_token" | jq -r '.access_token')

ZOHO_ACCOUNT_ID=$(curl -s "https://mail.zoho.com/api/accounts" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq -r '.data[0].accountId')

INBOX_ID=$(curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/folders" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq -r '.data[] | select(.folderName=="Inbox") | .folderId')

# List latest 5 inbox emails
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/messages/view?folderId=$INBOX_ID&limit=5" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {subject, sender, receivedTime}'

# Search for emails from a specific person
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/messages/search?searchKey=from:monika@example.com&limit=5" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | {subject, sender, summary}'

# Get unread count per folder
curl -s "https://mail.zoho.com/api/accounts/$ZOHO_ACCOUNT_ID/folders" \
  -H "Authorization: Zoho-oauthtoken $ZOHO_ACCESS_TOKEN" | jq '.data[] | select(.unreadCount > 0) | {folderName, unreadCount}'
```
