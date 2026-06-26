# OneDrive Manual Setup Guide

Use this guide if you don't have the Azure CLI (`az`) or want to do everything through the Azure Portal UI.

## Prerequisites

- A Microsoft account (personal `outlook.com`/`hotmail.com`/`live.com` **or** Microsoft 365 work/school).
- Access to [Azure Portal](https://portal.azure.com).
- `jq` and `curl` installed locally.

> Personal accounts can self-consent to any scope. Work/school accounts may require an administrator to grant tenant-wide consent for `*.All` scopes.

## Step 1 — Register an Azure AD application

1. Go to https://portal.azure.com → **Microsoft Entra ID** → **App registrations**.
2. Click **+ New registration**.
3. Fill in:
   - **Name:** `Clawdbot-OneDrive` (or anything you like).
   - **Supported account types:** _"Accounts in any organizational directory and personal Microsoft accounts (Any Microsoft Entra directory — Multitenant — and personal Microsoft accounts)"_.
   - **Redirect URI:** Platform = **Web**, URI = `http://localhost`.
4. Click **Register**.

## Step 2 — Get the client ID and secret

On the app's overview page:

1. Copy **Application (client) ID** → this is your `CLIENT_ID`.
2. (Optional) Copy **Directory (tenant) ID** if you want to lock the app to one tenant.
3. Left menu → **Certificates & secrets** → **+ New client secret**.
4. Description: `onedrive-cli`. Expiration: choose up to 24 months.
5. **Copy the `Value` immediately** — you can't see it again. This is your `CLIENT_SECRET`.

## Step 3 — Configure API permissions

1. Left menu → **API permissions** → **+ Add a permission**.
2. Choose **Microsoft Graph** → **Delegated permissions**.
3. Add these scopes:
   - `Files.ReadWrite.All` — read & write all files the user can access.
   - `Sites.ReadWrite.All` — required for SharePoint / OneDrive for Business document libraries.
   - `User.Read` — needed for sign-in (basic profile).
4. Click **Add permissions**.

`offline_access` is requested at sign-in time and does not need to be added here.

If you are on a work/school tenant where admin consent is required, click **Grant admin consent for {tenant}** (only an admin can do this).

## Step 4 — Save your config

Create the directory and config file locally:

```bash
mkdir -p ~/.onedrive-mcp && chmod 700 ~/.onedrive-mcp

cat > ~/.onedrive-mcp/config.json <<'EOF'
{
  "client_id":     "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET",
  "tenant":        "common",
  "redirect_uri":  "http://localhost",
  "scopes":        "https://graph.microsoft.com/Files.ReadWrite.All https://graph.microsoft.com/Sites.ReadWrite.All https://graph.microsoft.com/User.Read offline_access"
}
EOF

chmod 600 ~/.onedrive-mcp/config.json
```

For a single-tenant business app, replace `"tenant": "common"` with `"tenant": "YOUR_TENANT_ID"`.

## Step 5 — Authorize (get an authorization code)

Build this URL (replace `YOUR_CLIENT_ID`):

```
https://login.microsoftonline.com/common/oauth2/v2.0/authorize
  ?client_id=YOUR_CLIENT_ID
  &response_type=code
  &redirect_uri=http://localhost
  &response_mode=query
  &scope=https://graph.microsoft.com/Files.ReadWrite.All%20https://graph.microsoft.com/Sites.ReadWrite.All%20https://graph.microsoft.com/User.Read%20offline_access
```

(Put it on one line, no spaces. Replace newlines with nothing.)

1. Open the URL in a browser.
2. Sign in with the Microsoft account that owns the OneDrive you want to use.
3. Approve the requested permissions.
4. You'll be redirected to `http://localhost?code=XXXXX...` (the page won't load — that's fine).
5. Copy the value of `code=` (everything between `code=` and either `&` or end of URL).

## Step 6 — Exchange the code for tokens

```bash
CLIENT_ID="..."
CLIENT_SECRET="..."
CODE="the-code-from-step-5"
SCOPES="https://graph.microsoft.com/Files.ReadWrite.All https://graph.microsoft.com/Sites.ReadWrite.All https://graph.microsoft.com/User.Read offline_access"

curl -s -X POST "https://login.microsoftonline.com/common/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET" \
  --data-urlencode "code=$CODE" \
  --data-urlencode "redirect_uri=http://localhost" \
  --data-urlencode "grant_type=authorization_code" \
  --data-urlencode "scope=$SCOPES" \
  | tee ~/.onedrive-mcp/credentials.json | jq

chmod 600 ~/.onedrive-mcp/credentials.json
```

You should see a JSON response with `access_token`, `refresh_token`, `expires_in`, etc.

## Step 7 — Verify

```bash
TOKEN=$(jq -r '.access_token' ~/.onedrive-mcp/credentials.json)
curl -s "https://graph.microsoft.com/v1.0/me/drive" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '{owner: .owner.user.displayName, total: .quota.total, used: .quota.used}'
```

If you see your name and quota numbers, you're set. From here use the scripts:

```bash
./scripts/onedrive-files.sh list
./scripts/onedrive-files.sh quota
./scripts/onedrive-token.sh info
```

## Refreshing tokens

Access tokens expire after ~60 minutes. As long as `refresh_token` is present in `credentials.json`, refresh with:

```bash
./scripts/onedrive-token.sh refresh
```

Or directly:

```bash
RT=$(jq -r '.refresh_token' ~/.onedrive-mcp/credentials.json)
curl -s -X POST "https://login.microsoftonline.com/common/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET" \
  --data-urlencode "refresh_token=$RT" \
  --data-urlencode "grant_type=refresh_token" \
  --data-urlencode "scope=$SCOPES" \
  > ~/.onedrive-mcp/credentials.json
```

A new `refresh_token` is rotated on each call — always overwrite the file.

## Using an existing access token (BYO token)

If you already have a Microsoft Graph access token from somewhere else (Postman, MSAL, another app, service principal, etc.):

```bash
# Option 1 — env var (one-off)
export ONEDRIVE_ACCESS_TOKEN="eyJ0eXAi..."
./scripts/onedrive-files.sh list

# Option 2 — persisted
./scripts/onedrive-token.sh set "eyJ0eXAi..." "optional-refresh-token"
```

The token must have at least `Files.Read` (or `Files.ReadWrite` for writes) and `User.Read` to call the endpoints used here.

## Troubleshooting

**AADSTS50011: Reply URL does not match**
The redirect URI configured on the app must match the `redirect_uri` parameter exactly, including trailing slash. Use `http://localhost` (no trailing slash) consistently.

**AADSTS65001: User or administrator has not consented**
For work/school tenants, an admin must click _Grant admin consent_ on the API permissions page. Alternatively use a personal account.

**AADSTS70011: Invalid scope**
- Scopes must be space-separated, not comma-separated.
- Use the full URI form (`https://graph.microsoft.com/Files.ReadWrite.All`) — short forms only work for some flows.
- `offline_access` is the only scope that does NOT take the Graph URI prefix.

**Token works for `/me/drive` but not `/sites/...`**
You're missing `Sites.Read.All` or `Sites.ReadWrite.All`. Reconsent.

**`invalid_grant: AADSTS70008: refresh token has expired`**
Refresh tokens last 90 days (personal) or until the tenant policy revokes them. Re-run the full authorize flow (Step 5).
