# Integrations Reference

## Use When
- You need to register OAuth app credentials for a provider (Google Drive, Slack).
- You need to connect a Google Drive account, Slack workspace, or GitHub repo to an Eve org.
- You need to resolve external provider identities to Eve users.
- You need to manage membership requests from unresolved external users.
- You need to browse or search files in connected cloud storage (Google Drive).
- You need to understand how chat file uploads (e.g., Slack) are materialized into agent workspaces.
- You need to let an Eve-deployed app declare which customer orgs can use it, expose in-app admin invites, or land invite/magic-link redirects on a custom domain.

## Load Next
- `references/gateways.md` for chat gateway routing and thread key mechanics.
- `references/agents-teams.md` for agent slug resolution and chat dispatch modes.
- `references/secrets-auth.md` for webhook secrets, app branding, magic-link wraps, and redirect allowlist derivation.
- `references/manifest.md` for `x-eve.branding`, `x-eve.auth`, `org_access`, and `allowed_redirect_origins` manifest fields.
- `references/auth-sdk.md` for `eveAppUserAuth`, `useEveAppAccess`, and the `inviteMember` SDK surface.

## Ask If Missing
- Confirm the target org ID and whether the integration already exists.
- Confirm the provider type (google-drive, slack, or github) and available OAuth app credentials.
- Confirm whether OAuth app credentials have been registered (`eve integrations config <provider>`).
- Confirm whether identity resolution is needed or if users are already bound.

External provider integrations (Slack, Google Drive, GitHub), OAuth app configuration, cloud storage mounts, and identity resolution for Eve orgs.

## Overview

Integrations connect external providers to Eve events and chat routing. Each integration is **org-scoped** — one row per provider account (e.g., one Slack workspace per org).

Key tables:

| Table | Purpose |
|-------|---------|
| `oauth_app_configs` | Per-org OAuth application credentials (client_id, client_secret) |
| `integrations` | Maps provider accounts to orgs (holds OAuth tokens) |
| `cloud_fs_mounts` | Cloud storage mounts linking a provider folder to an org/project |
| `external_identities` | Maps provider user IDs to Eve users |
| `membership_requests` | Tracks pending/approved/denied access requests |

## OAuth App Configuration (BYOA)

Each org registers its own OAuth application credentials — the **Bring Your Own App** (BYOA) pattern. No cluster-level OAuth secrets exist; every org configures its own GCP project or Slack app.

### Why BYOA

- **Isolation**: One org's leaked credentials cannot compromise another.
- **Branding**: Org employees see their own company name on consent screens.
- **Enterprise**: Google Workspace and Slack Enterprise Grid admins can trust and manage the app internally.
- **Rate limits**: Per-org API quotas.

### Setup Flow

1. **Get setup instructions** — provider-specific callback URLs and required scopes:

```bash
eve integrations setup-info google-drive --org <org_id>
eve integrations setup-info slack --org <org_id>
```

2. **Create the OAuth app** in the provider's console (GCP, api.slack.com), using the callback URL from step 1.

3. **Register credentials** in Eve:

```bash
# Google Drive
eve integrations configure google-drive \
  --org <org_id> \
  --client-id "xxx.apps.googleusercontent.com" \
  --client-secret "GOCSPX-xxx" \
  --label "Acme Corp Google Drive"

# Slack (includes signing secret)
eve integrations configure slack \
  --org <org_id> \
  --client-id "12345.67890" \
  --client-secret "abc123" \
  --signing-secret "def456" \
  --label "Acme Corp Slack Bot"
```

4. **Verify config**:

```bash
eve integrations config google-drive --org <org_id>   # secrets redacted
```

5. **Initiate OAuth connection**:

```bash
eve integrations connect google-drive --org <org_id>
```

### Provider Name Normalization

CLI accepts both `google-drive` and `google_drive`. Internally the provider name is normalized to underscore form (`google_drive`, `slack`).

### Manage Config

```bash
eve integrations config <provider> --org <org_id>       # View (secrets redacted)
eve integrations unconfigure <provider> --org <org_id>   # Remove config
```

Removing a config prevents new OAuth flows. Existing integration tokens continue to work until they expire or refresh fails.

### Relationship Between Tables

```
oauth_app_configs              integrations
(one per org per provider)     (one per connected account)
  client_id, client_secret  →    tokens_json (access_token, refresh_token)
  config_json (signing_secret)   settings_json, status
```

One OAuth app config can back multiple integrations (e.g., connecting multiple Google accounts to the same org).

## Google Drive Integration

### Prerequisites

1. Configure Google OAuth app credentials via `eve integrations configure google-drive` (see BYOA section above).
2. The Google Drive API must be enabled in the org's GCP project.

### OAuth Authorization

After configuring credentials, initiate the Google Drive OAuth flow:

```bash
eve integrations connect google-drive --org <org_id>
```

This prints an authorization URL. Open it in a browser to grant access. The callback creates an integration with a refresh token. Token refresh is automatic — the platform reads the org's `client_id` and `client_secret` from `oauth_app_configs` when refreshing.

API endpoint: `GET /orgs/:org_id/integrations/google-drive/authorize`

### Cloud FS Mounts

Cloud FS mounts link a Google Drive folder to an org (or project). Files in the mounted folder are browsable and searchable via the CLI.

```bash
# Create a mount
eve cloud-fs mount \
  --provider google-drive \
  --folder-id 0ABxxx \
  --label "Shared Drive" \
  --org <org_id> \
  [--project <project_id>] \
  [--mode read_only|write_only|read_write] \
  [--auto-index true|false]

# List mounts
eve cloud-fs list --org <org_id>

# Show mount details
eve cloud-fs show <mount_id> --org <org_id>

# Update mount settings
eve cloud-fs update <mount_id> --label "New Name" --org <org_id>

# Remove a mount
eve cloud-fs unmount <mount_id> --org <org_id>
```

### Browsing and Searching

Browse files at a path within a mount, or search across all mounts:

```bash
# Browse files at a path
eve cloud-fs ls / --mount <mount_id> --org <org_id>
eve cloud-fs ls /reports --mount <mount_id> --org <org_id>
eve cloud-fs ls / --mount <mount_id> --page-size 100 --org <org_id>
eve cloud-fs ls / --mount <mount_id> --page-token <token> --org <org_id>
eve cloud-fs ls / --mount <mount_id> --all --json --org <org_id>
eve cloud-fs ls / --mount <mount_id> --recursive --json --org <org_id>

# Search files
eve cloud-fs search "Q4 report" --org <org_id>
eve cloud-fs search "*.pdf" --mount <mount_id> --mime-type application/pdf --all --org <org_id>
```

Browse/search return one provider page by default and may include
`next_page_token`. Use `--page-token` for manual cursor round trips or `--all`
to auto-page up to `EVE_CLOUD_FS_MAX_AUTO_PAGES` (default 200). JSON `--all`
output includes `complete`, `page_count`, and `next_page_token` when iteration
stops early. `--order-by` accepts `name`, `name_desc`, `modified`, or
`modified_desc`. Search `--mime-type` is passed through to Google Drive as a
MIME filter. Recursive browse is bounded server-side, rejects `--page-token`
and `--all`, and may return `truncated: true`.

### RBAC Permissions

| Permission | Grants |
|------------|--------|
| `cloud_fs:read` | List mounts, browse files, search |
| `cloud_fs:write` | Reserved for write-capable Cloud FS operations |
| `cloud_fs:admin` | Create/update/delete mounts, upload/create folders, and integration management |

### Token Refresh

Token refresh is transparent. When an access token expires, the platform reads the org's OAuth app credentials from `oauth_app_configs` and exchanges the refresh token for a new access token. If refresh fails (e.g., credentials revoked), the integration status is updated accordingly.

## Slack Integration

### Prerequisites

Configure Slack app credentials via BYOA before connecting:

```bash
eve integrations setup-info slack --org <org_id>        # Get callback/webhook URLs
eve integrations configure slack \
  --org <org_id> \
  --client-id "..." \
  --client-secret "..." \
  --signing-secret "..."                                # Required for webhook verification
```

### Connect (OAuth Install Link — Recommended)

Generate a shareable install link. The recipient needs only Slack workspace admin access — no Eve credentials.

```bash
# Generate install link (24h TTL by default)
eve integrations slack install-url --org <org_id>

# Custom TTL
eve integrations slack install-url --org <org_id> --ttl 7d
```

The link redirects to Slack OAuth. On approval, Eve exchanges the code for a bot token and creates the integration automatically. Gateway hot-loads the new integration within ~30 seconds (no restart needed).

**Install token mechanics**: The CLI calls `POST /orgs/:org_id/integrations/slack/install-token` (requires `integrations:write`). The API returns a signed URL containing an HMAC token (`eve-slack-install-<base64url(payload)>.<base64url(hmac)>`). The token is single-use (JTI tracked), time-bounded (default 24h, max 7d), and org-scoped. The public endpoint `GET /integrations/slack/install?token=...` validates the token and redirects to Slack OAuth — no Eve auth session required.

### Gateway Hot-Loading

The gateway polls `GET /internal/integrations/active` every 30 seconds. Any integration not yet in the provider registry is initialized automatically. This means a Slack workspace connected via the install link (or manual connect) becomes operational within ~30 seconds without a gateway restart. On shutdown, the sync timer is cleared and all provider instances are gracefully torn down.

### Connect (Manual — Fallback)

```bash
# Connect Slack workspace to org
eve integrations slack connect \
  --org <org_id> \
  --team-id <T-ID> \
  --token xoxb-...

# Full bootstrap with all tokens
eve integrations slack connect \
  --org <org_id> \
  --team-id <T-ID> \
  --tokens-json '{"access_token":"xoxb-...","bot_user_id":"U...","team_id":"T...","app_id":"A..."}'

# Verify
eve integrations list --org <org_id>
eve integrations test <integration_id> --org <org_id>
```

### Routing

- `@eve <agent-slug> <command>` — resolves slug to project/agent (unique per org)
- If first word after `@eve` is not a known slug → routes to org `default_agent_slug`
- Channel messages without mention → dispatched to channel/thread listeners

### Auth

- **Signing secret**: Verifies inbound webhook signatures. Each org's signing secret is stored in `oauth_app_configs.config_json` and set during `eve integrations configure slack --signing-secret "..."`. The gateway reads it from the integration's enriched `settings_json`.
- **Bot token**: `xoxb-...` for outbound messages, stored in integration `tokens_json`

### Non-Chat Slack Notifications

Jobs and workflows that did not originate in Slack can send one-way channel
notifications through Eve:

```bash
eve notifications send \
  --project <project_id_or_slug> \
  --channel eve-horizon-notifications \
  --message "Workflow complete"
```

This calls `POST /projects/:project_id/notifications/send`, requires
`notifications:send`, resolves the org Slack integration server-side, and posts
with the stored bot token. The token is never exposed to the job. Pass
`--integration-id <id>` when an org has multiple active Slack workspaces.

Channel may be a Slack channel ID (`C...`, `G...`, `D...`) or a channel name
with or without `#`. Name lookup uses `channels:read` and `groups:read`; posting
uses `chat:write` and optionally `chat:write.public` for public channels where
the app has not been invited.

### Required Bot Events

| Event | Purpose |
|-------|---------|
| `app_mention` | `@eve` commands |
| `message.channels` | Public channel listeners |
| `message.groups` | Private channel listeners |
| `message.im` | Direct messages |

### Integration Settings

```bash
# Set admin notification channel for membership requests
eve integrations update <integration_id> --org <org_id> \
  --setting admin_channel_id=C-ADMIN-CHANNEL
```

### Chat File Materialization

When a user uploads files in a Slack message (or any chat provider), the gateway automatically downloads and stages them for agents. The pipeline is provider-agnostic downstream — each provider handles its own auth for file downloads.

**Flow**:
1. **Gateway** (async, after webhook ack): Provider calls `resolveFiles()` — downloads files using the bot token, uploads to S3 via API presigned URLs, replaces provider URLs with `eve-storage://` references.
2. **API**: Presigned URL endpoint (`POST /internal/storage/chat-attachments/presign`) keeps S3 credentials centralized. Both gateway (upload) and worker (download) use it.
3. **Worker** (workspace provisioning): Detects `eve-storage://` URLs in `job.metadata.files`, downloads via presigned URLs, stages to `.eve/attachments/`, writes `.eve/attachments/index.json`.
4. **Agent**: Reads `.eve/attachments/index.json` for the file manifest. Files are at `.eve/attachments/{filename}`.

**S3 key format**: `chat-attachments/{org_id}/{provider}:{account_id}/{channel_id}/{message_ts}/{file_id}-{filename}`

Thread replies group under the thread root timestamp so all files in a conversation are co-located.

**Limits**: 50 MB per file, 100 MB total per message, 10 files per message. Files exceeding limits are skipped (original provider URL preserved in metadata as fallback).

**Provider interface**: Each provider implements an optional `resolveFiles(files, context)` method. The `FileResolveContext` provides `getUploadUrl` callback so providers never need direct S3 access. Currently implemented for Slack; other providers (WebChat, GitHub) follow the same pattern.

**Attachment index schema** (`.eve/attachments/index.json`):
```json
{
  "files": [{
    "id": "F019ABC123",
    "name": "spec.pdf",
    "path": ".eve/attachments/F019ABC123-spec.pdf",
    "mimetype": "application/pdf",
    "size": 245760,
    "source_provider": "slack"
  }]
}
```

## GitHub Integration

```bash
# Set up GitHub integration for a project
eve github setup
```

- Webhook endpoint: `/integrations/github/events/:projectId`
- Auth: `EVE_GITHUB_WEBHOOK_SECRET` + project-scoped secret override
- Events: Push, pull request, and configured GitHub webhook events trigger Eve pipelines and workflows

## App Integrations (org access, in-app admin invites, branded email, redirect allowlist)

Eve-deployed apps integrate with customer orgs through three project-level controls authored in `.eve/manifest.yaml` and synced onto `projects.branding` and `projects.auth_config`. The platform-side mechanics live in `manifest.md`, `auth-sdk.md`, and `secrets-auth.md`; this section is the integration map.

### App org access (multi-tenant SSO)

```yaml
x-eve:
  auth:
    login_method: magic_link
    self_signup: false
    invite_requires_password: false
    org_access:
      mode: allowlist            # default project_org limits app to project owner org
      allowed_orgs: [org_customer123, customer-slug]
      invite:
        enabled: true
        admin_roles: [admin, owner]
        invited_role: member     # fixed to member; app invites cannot mint admins
```

Manifest sync resolves slugs to canonical org IDs. Public `GET /auth/app-context?project_id=...` exposes only summary booleans (`multi_org`, `invite_enabled`, `domain_signup_enabled`); the full allowlist and domain-signup rules require `GET /auth/app-context/admin` or `eve project auth-context <project_id>`.

### In-app admin invites

Org admins/owners in any `allowed_orgs` org can invite regular members directly from the app:

```http
POST /auth/app-invites
Authorization: Bearer <eve-user-token>
{ "project_id": "proj_xxx", "org_id": "org_customer123", "email": "new@example.com", "redirect_to": "https://app.example.com/" }
```

React: `useEveAppAccess().inviteMember({ orgId, email })`. CLI fallback: `eve org invite <email> --org <org_id> --project <project_id> [--redirect-to <url>]`. The invite carries `app_context.{project_id, org_id}`; accepting it provisions an `org_memberships(target_org, user, member)` row, never a project membership. System-created invites from `domain_signup` rules have `created_by = NULL` and `app_context.source = 'domain_signup'` (migration `00097_org_invite_system_created.sql`) so audits can distinguish them from admin-issued invites.

### App-branded invite + magic-link emails

```yaml
x-eve:
  branding:
    app_name: "ACME Portal"
    app_logo_url: "https://sandbox.acme.example/assets/logo.svg"
    primary_color: "#1f6feb"
    email_from_name: "ACME Portal"
    reply_to_email: "support@acme.example"
    support_email: "support@acme.example"
```

`projects.branding` (migration `00093_project_branding.sql`) drives the email subject, body, and `From:` display name for invite and magic-link mail when the invite is created with `--project <project_id>`. The sender address remains the platform default in Phase 1; missing branding falls back to "Eve Horizon" defaults. Header-injection guards reject CR/LF in `app_name`, `email_from_name`, `reply_to_email`; non-HTTPS logos are silently omitted.

### Redirect allowlist (custom-domain apps)

For apps on custom domains, declare which off-cluster origins SSO may redirect to and which origins may call `/session`:

```yaml
x-eve:
  auth:
    allowed_redirect_origins:
      - https://sandbox.acme.example
      - https://app.example.com
```

The resolved list returned by `/auth/app-context` as `auth.allowed_redirect_origins` is the union of: explicit manifest entries; the project's own eligible custom domains (status `dns_verified | cert_provisioning | active`); and — when `org_access.mode: allowlist` — eligible custom domains owned by any project in `allowed_orgs`. This replaces the legacy `EVE_DEFAULT_DOMAIN`-only allowlist, so invite redemption and magic-link callback land on the app's declared path (e.g. `/cameras`) instead of the SSO landing page. Inspect with `eve project auth-context <project_id>`.

## Identity Resolution

When an external user (e.g., Slack) messages `@eve`, the platform resolves their identity through three tiers. The first match short-circuits the rest.

### Tier 1: Email Auto-Match

The gateway fetches the provider user's email and checks if an Eve user with that email exists and is an org member. If so, the identity is automatically bound. No user action required.

### Tier 2: Self-Service CLI Link

An existing Eve user can link their external identity:

```bash
eve identity link slack --org <org_id>
```

Generates a one-time token. User sends `@eve link <token>` in Slack. The gateway validates and binds.

### Tier 3: Admin Approval

When neither Tier 1 nor 2 resolves, a **membership request** is created.

Admins handle requests via:
- **CLI**: `eve org membership-requests list --org <org_id>`
- **Slack**: Block Kit Approve/Deny buttons (if `admin_channel_id` configured)

On approval: Eve user created (if needed), org membership added, identity bound, user notified.

### Resolution Decision Table

| Has Eve email? | Is org member? | Result |
|----------------|---------------|--------|
| Yes | Yes | Tier 1: auto-bind |
| Yes | No | Tier 3: membership request |
| No / unknown | -- | Tier 2 (self-link) or Tier 3 |

### Membership Request CLI

```bash
eve org membership-requests list --org <org_id>
eve org membership-requests approve <request_id> --org <org_id>
eve org membership-requests deny <request_id> --org <org_id>
```

## External Identities

External identities map provider user IDs to Eve users. Once bound, subsequent messages skip resolution entirely.

Lifecycle:
1. **Created** when provider user first seen (`eve_user_id` = null)
2. **Bound** when resolution succeeds (`eve_user_id` set)
3. **Unbound** if Eve user deleted (returns to unresolved)

## CLI Quick Reference

| Command | Purpose |
|---------|---------|
| **OAuth App Configuration (BYOA)** | |
| `eve integrations setup-info <provider> --org <org>` | Get callback URLs and setup instructions |
| `eve integrations configure <provider> --org <org> --client-id "..." --client-secret "..."` | Register OAuth app credentials |
| `eve integrations config <provider> --org <org>` | View OAuth app config (secrets redacted) |
| `eve integrations unconfigure <provider> --org <org>` | Remove OAuth app config |
| `eve integrations connect <provider> --org <org>` | Initiate OAuth connection flow |
| **Cloud FS (Google Drive)** | |
| `eve cloud-fs list --org <org>` | List cloud FS mounts |
| `eve cloud-fs mount --provider google-drive --folder-id <id> --org <org>` | Create a mount |
| `eve cloud-fs show <mount_id> --org <org>` | Show mount details |
| `eve cloud-fs update <mount_id> --org <org>` | Update mount settings |
| `eve cloud-fs unmount <mount_id> --org <org>` | Remove a mount |
| `eve cloud-fs ls [path] --mount <mount_id> --org <org>` | Browse files |
| `eve cloud-fs search <query> --org <org>` | Search files across mounts |
| **Slack** | |
| `eve integrations list --org <org>` | List integrations |
| `eve integrations test <id> --org <org>` | Test integration health |
| `eve integrations slack install-url --org <org> [--ttl 7d]` | Generate shareable Slack install link |
| `eve integrations slack connect --org <org> --team-id <id> --token <token>` | Connect Slack (manual fallback) |
| `eve integrations update <id> --org <org> --setting key=value` | Update settings |
| `eve notifications send --project <project> --channel <name-or-id> --message <text>` | Send a project-scoped Slack channel notification |
| **Identity** | |
| `eve identity link slack --org <org>` | Self-service identity link |
| `eve org membership-requests list --org <org>` | List pending requests |
| `eve org membership-requests approve <id> --org <org>` | Approve request |
| `eve org membership-requests deny <id> --org <org>` | Deny request |
| **GitHub** | |
| `eve github setup` | GitHub webhook setup |
| **App integrations (org access, invites, branding)** | |
| `eve org invite <email> --org <org> --project <project> [--role member] [--redirect-to <url>]` | Send app-branded invite scoped to the project's org policy |
| `eve project auth-context <project>` | Show resolved `org_access`, `allowed_redirect_origins`, and admin-only `domain_signup` rules |

## Related Skills

- **Chat gateway details**: `references/gateways.md`
- **Auth, branding, magic-link wraps, redirect allowlist**: `references/secrets-auth.md`
- **Manifest fields (`x-eve.branding`, `x-eve.auth`, `org_access`, `allowed_redirect_origins`)**: `references/manifest.md`
- **App SSO + SDK (`eveAppUserAuth`, `useEveAppAccess`, `inviteMember`)**: `references/auth-sdk.md`
