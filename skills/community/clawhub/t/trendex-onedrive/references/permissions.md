# OAuth Scopes & Permissions

Microsoft Graph distinguishes two permission models:

| Type | Used by | Token issued for |
|------|---------|------------------|
| **Delegated** | Apps acting on behalf of a signed-in user | A specific user (`/me`, `/users/{me-id}`) |
| **Application** | Apps acting as themselves (daemons, services) | The application — must call `/users/{user-id}` not `/me` |

The setup script in this skill uses **delegated** permissions with the OAuth2 authorization code flow.

## Scopes used by this skill

| Scope | Type | Purpose |
|-------|------|---------|
| `https://graph.microsoft.com/Files.ReadWrite.All` | Delegated | Read & write all files the signed-in user can access |
| `https://graph.microsoft.com/Sites.ReadWrite.All` | Delegated | SharePoint & OneDrive for Business document libraries |
| `https://graph.microsoft.com/User.Read` | Delegated | Sign in & read basic profile |
| `offline_access` | Delegated | Issue refresh tokens (no `https://...` prefix) |

> `offline_access` is a special OpenID Connect scope. It must be requested at sign-in but is **not** added on the Azure app registration's "API permissions" page.

## All file-related delegated scopes

| Scope | What it grants | When to use |
|-------|----------------|-------------|
| `Files.Read` | Read user's own files | Read-only personal apps |
| `Files.ReadWrite` | Read/write user's own files | Write to personal drive only |
| `Files.Read.All` | Read any file the user can access (incl. shared) | Read-only across shared/business |
| `Files.ReadWrite.All` | Read/write any file the user can access | Full control (this skill's default) |
| `Files.Read.Selected` | App can only access files the user picked via picker | Sandboxed integrations |
| `Files.ReadWrite.Selected` | Same, but writable | Sandboxed integrations |
| `Files.ReadWrite.AppFolder` | Read/write within the app's dedicated folder | Apps using `special/approot` |

For SharePoint / business doc libraries:

| Scope | Purpose |
|-------|---------|
| `Sites.Read.All` | Read items in all SharePoint sites the user can access |
| `Sites.ReadWrite.All` | Read/write items in all sites |
| `Sites.Manage.All` | Create/edit lists & list items |
| `Sites.FullControl.All` | Full control (admin-only consent) |
| `Sites.Selected` | Restrict app to specific sites granted by admin |

## Application (daemon) scopes

For service-to-service automation (no signed-in user), use the client-credentials flow with these:

| Scope | Notes |
|-------|-------|
| `Files.Read.All` | Application — read across the tenant |
| `Files.ReadWrite.All` | Application — read/write across the tenant |
| `Sites.Selected` | Restricted to sites granted by an admin |

App-only tokens **cannot** call `/me/...`. You must address by user/site/drive ID:

```
GET /users/{user-upn-or-id}/drive/root/children
GET /sites/{site-id}/drive/root/children
```

To get a token using client credentials:

```bash
curl -s -X POST "https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "client_secret=$CLIENT_SECRET" \
  --data-urlencode "scope=https://graph.microsoft.com/.default" \
  --data-urlencode "grant_type=client_credentials"
```

Note the special scope `https://graph.microsoft.com/.default` — it requests all permissions an admin has already consented to. No refresh token is issued; just get a new one when needed (also valid ~60 minutes).

Then put it into the skill:

```bash
./scripts/onedrive-token.sh set "$TOKEN"
export ONEDRIVE_DRIVE_PREFIX="/users/jane@contoso.com/drive"
./scripts/onedrive-files.sh list
```

## Consent

**Personal Microsoft accounts** can self-consent to any delegated scope.

**Work / school (Microsoft 365)** accounts:

- Some scopes (e.g. `User.Read`, `Files.Read`) can be user-consented.
- Most `*.All` and all `Sites.*.All` scopes typically require **admin consent**.
- Admins grant tenant-wide consent at:
  - Azure Portal → Microsoft Entra ID → App registrations → {your app} → API permissions → **Grant admin consent for {tenant}**.
- Or via the URL:

  ```
  https://login.microsoftonline.com/{tenant}/adminconsent
    ?client_id={CLIENT_ID}
    &redirect_uri=http://localhost
  ```

## Choosing the right tenant string

The auth/token URLs use `/{tenant}/` segment:

| Value | Audience |
|-------|----------|
| `common` | Any Microsoft account (personal + work/school, any tenant) — default |
| `consumers` | Personal Microsoft accounts only |
| `organizations` | Work/school accounts in any tenant |
| `{tenant-id}` or `{domain}` | Specific tenant only |

The setup script defaults to `common`. Override with `ONEDRIVE_TENANT=...` when running it.

## Minimum scopes per operation

| You want to | Minimum delegated scope |
|-------------|--------------------------|
| List your own files | `Files.Read` |
| Upload/download your own files | `Files.ReadWrite` |
| Access files shared with you | `Files.Read.All` |
| Modify files shared with you | `Files.ReadWrite.All` |
| Read SharePoint sites | `Sites.Read.All` |
| Write to SharePoint sites | `Sites.ReadWrite.All` |
| Stay signed in (refresh tokens) | `offline_access` |
| Show user profile | `User.Read` |

This skill requests `Files.ReadWrite.All Sites.ReadWrite.All User.Read offline_access` as a sane default. Trim down if you have a strict least-privilege requirement.
