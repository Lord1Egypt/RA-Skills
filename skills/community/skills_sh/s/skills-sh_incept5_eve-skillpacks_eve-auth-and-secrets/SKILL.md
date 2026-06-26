---
name: eve-auth-and-secrets
description: Authenticate with Eve, manage project secrets, and add SSO login to Eve-deployed apps.
---

# Eve Auth and Secrets

Use this workflow to log in to Eve and manage secrets for your app.

## When to Use

- Setting up a new project profile
- Authentication failures
- Adding or rotating secrets
- Secret interpolation errors during deploys
- Setting up identity providers or org invites
- Adding SSO login to an Eve-deployed app
- Setting up access groups and scoped data-plane authorization
- Configuring group-aware RLS for environment databases

## Authentication

```bash
eve auth login
eve auth login --ttl 30                # custom token TTL (1-90 days)
eve auth status
```

### Challenge-Response Flow

Eve uses challenge-response authentication. The default provider is `github_ssh`:

1. Client sends SSH public key fingerprint
2. Server returns a challenge (random bytes)
3. Client signs the challenge with the private key
4. Server verifies the signature and issues a JWT

### Token Types

| Type | Issued Via | Use Case |
|------|-----------|----------|
| User Token | `eve auth login` | Interactive CLI sessions |
| Job Token | Worker auto-issued | Agent execution within jobs |
| Minted Token | `eve auth mint` | Bot/service accounts |

JWT payloads include `sub` (user ID), `org_id`, `scope`, and `exp`. Verify tokens via the JWKS endpoint: `GET /auth/jwks`.

Role and org membership changes take effect immediately -- the server resolves permissions from live DB memberships, not stale JWT claims. When a request includes a `project_id` but no `org_id`, the permission guard derives the org context from the project's owning org.

### Permissions

Check what the current token can do:

```bash
eve auth permissions
```

Register additional identities for multi-provider access:

```bash
curl -X POST "$EVE_API_URL/auth/identities" -H "Authorization: Bearer $TOKEN" \
  -d '{"provider": "nostr", "external_id": "<pubkey>"}'
```

## Identity Providers

Eve supports pluggable identity providers. The auth guard tries Bearer JWT first, then provider-specific request auth.

| Provider | Auth Method | Use Case |
|----------|------------|----------|
| `github_ssh` | SSH challenge-response | Default CLI login |
| `nostr` | NIP-98 request auth + challenge-response | Nostr-native users |

### Nostr Authentication

Two paths:
- **Challenge-response**: Like SSH but signs with Nostr key. Use `eve auth login --provider nostr`.
- **NIP-98 request auth**: Every API request signed with a Kind 27235 event. Stateless, no stored token.

## Org Invites

Invite external users via the CLI or API:

```bash
# Invite with SSH key registration (registers key so the user can log in immediately)
eve admin invite --email user@example.com --ssh-key ~/.ssh/id_ed25519.pub --org org_xxx

# Invite with GitHub identity
eve admin invite --email user@example.com --github ghuser --org org_xxx

# Invite with web-based auth (Supabase)
eve admin invite --email user@example.com --web --org org_xxx

# API: invite targeting a Nostr pubkey
curl -X POST "$EVE_API_URL/auth/invites" -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"org_id": "org_xxx", "role": "member", "provider_hint": "nostr", "identity_hint": "<pubkey>"}'
```

If no auth method is specified (`--github`, `--ssh-key`, or `--web`), the CLI warns that the user will not be able to log in. The user can self-register later via `eve auth request-access --org "Org Name" --ssh-key ~/.ssh/id_ed25519.pub --wait`.

When the identity authenticates, Eve auto-provisions their account and org membership.

For app-driven onboarding, use the org-scoped invite API instead of the legacy admin invite flow:

```bash
# Create an org-scoped Supabase invite with a return URL for the app
curl -X POST "$EVE_API_URL/orgs/org_xxx/invites" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "role": "member",
    "redirect_to": "https://app.example.com/invite/complete",
    "app_context": { "project_id": "proj_123" }
  }'

# Search existing org members for an assignee picker
curl "$EVE_API_URL/orgs/org_xxx/members/search?q=ali" \
  -H "Authorization: Bearer $USER_TOKEN"
```

Use a user token with `orgs:invite` to create or list these invites and `orgs:members:read` for member lookup. Invite emails should land on GoTrue's `/verify` path, not the OAuth callback directly. If the invite is auto-applied during the SSO exchange, Eve returns `invite_redirect_to` so the SSO callback can land the user back in the target app even when the email provider strips nested redirect params. Current invite onboarding establishes the SSO session first, then sends the user through `/set-password` before redirecting to the app.

### App-Branded Invite Emails

Projects opt into app-branded invites with `x-eve.branding` in the manifest. The subject, body, and `From:` display name all carry the app's identity — other apps fall back to "Eve Horizon" defaults.

```yaml
x-eve:
  branding:
    app_name: "ACME Portal"
    app_logo_url: "https://app.example.com/assets/logo.svg"   # https-only
    primary_color: "#1f6feb"
    email_from_name: "ACME Portal"
    reply_to_email: "support@example.com"
    support_email: "support@example.com"
    support_url: "https://example.com/help"
```

Run `eve project sync` after editing. Invites sent with `eve org invite <email> --org <org_id> --project <project_id>` use the project branding. The sender address remains the platform default in Phase 1; only the display name varies. The same branding template is shared with magic-link login emails — only the copy ("Accept invite" vs "Sign in") differs.

## Token Minting (Admin)

Mint tokens for bot/service users without SSH login:

```bash
# Mint token for a bot user (creates user + membership if needed)
eve auth mint --email app-bot@example.com --org org_xxx

# With custom TTL (1-90 days, default: server configured)
eve auth mint --email app-bot@example.com --org org_xxx --ttl 90

# Scope to project with admin role
eve auth mint --email app-bot@example.com --project proj_xxx --role admin
```

Print the current access token (useful for scripts):

```bash
eve auth token
```

## Self-Service Access Requests

Users without an invite can request access:

```bash
eve auth request-access --org "My Company" --email you@example.com
eve auth request-access --org "My Company" --ssh-key ~/.ssh/id_ed25519.pub
eve auth request-access --status <request_id>
```

Admins approve or reject via:

```bash
eve admin access-requests list
eve admin access-requests approve <request_id>
eve admin access-requests reject <request_id> --reason "..."
```

List responses use the canonical `{ "data": [...] }` envelope.

Approval is atomic (single DB transaction) and idempotent -- re-approving a completed request returns the existing record. If the fingerprint is already registered, Eve reuses that identity owner. If a legacy partial org matches the requested slug and name, Eve reuses it during approval. Failed attempts never leave partial state.

## Credential Check

Verify local AI tool credentials:

```bash
eve auth creds                # Show Claude + Codex cred status
eve auth creds --claude       # Only Claude
eve auth creds --codex        # Only Codex
```

Output includes token type (`setup-token` or `oauth`), preview, and expiry. Use this to confirm token health before syncing.

## OAuth Token Sync

Sync local Claude/Codex OAuth tokens into Eve secrets so agents can use them. Scope precedence: project > org > user.

```bash
eve auth sync                       # Sync to user-level (default)
eve auth sync --org org_xxx         # Sync to org-level (shared across org projects)
eve auth sync --project proj_xxx    # Sync to project-level (scoped to one project)
eve auth sync --dry-run             # Preview without syncing
```

This sets `CLAUDE_CODE_OAUTH_TOKEN` / `CLAUDE_OAUTH_REFRESH_TOKEN` (Claude) and `CODEX_AUTH_JSON_B64` (Codex/Code) at the requested scope.

### Claude Token Types

| Token Prefix | Type | Lifetime | Recommendation |
|---|---|---|---|
| `sk-ant-oat01-*` | `setup-token` (long-lived) | Long-lived | Preferred for jobs and automation |
| Other `sk-ant-*` | `oauth` (short-lived) | ~15 hours | Use for interactive dev; regenerate with `claude setup-token` |

`eve auth sync` warns when syncing a short-lived OAuth token. Run `eve auth creds` to inspect token type before syncing.

### Automatic Codex/Code Token Write-Back

After each harness invocation, the worker checks if the Codex/Code CLI refreshed `auth.json` during the session. If the token changed, it is automatically written back to the originating secret scope (user/org/project) so the next job starts with a fresh token. This is transparent and non-fatal -- a write-back failure logs a warning but does not affect the job result.

For Codex/Code credentials, the sync picks the freshest token across `~/.codex/auth.json` and `~/.code/auth.json` by comparing `tokens.expires_at`.

## Access Groups + Scoped Access

Groups are first-class authorization primitives that segment data-plane access (org filesystem, org docs, environment databases). Create groups, add members, and bind roles with scoped constraints:

```bash
# Create a group
eve access groups create --org org_xxx --slug eng-team --name "Engineering"

# Add members
eve access groups members add eng-team --org org_xxx --user user_abc
eve access groups members add eng-team --org org_xxx --service-principal sp_xxx

# Bind a role with scoped access
eve access bind --org org_xxx --group grp_xxx --role data-reader \
  --scope-json '{"orgfs":{"allow_prefixes":["/shared/"]},"envdb":{"schemas":["public"]}}'

# Check effective access
eve access memberships --org org_xxx --user user_abc
```

### Scope Types

| Resource | Scope Fields | Example |
|----------|-------------|---------|
| Org Filesystem | `orgfs.allow_prefixes`, `orgfs.read_only_prefixes` | `"/shared/"`, `"/reports/"` |
| Org Documents | `orgdocs.allow_prefixes`, `orgdocs.read_only_prefixes` | `"/pm/features/"` |
| Environment DB | `envdb.schemas`, `envdb.tables` | `"public"`, `"analytics_*"` |

### Group-Aware RLS

Scaffold RLS helper functions for group-based row-level security in environment databases:

```bash
eve db rls init --with-groups
```

This creates SQL helpers (`app.current_user_id()`, `app.current_group_ids()`, `app.has_group()`) that read session context set by Eve's runtime. Use them in RLS policies:

```sql
CREATE POLICY notes_group_read ON notes FOR SELECT
  USING (group_id = ANY(app.current_group_ids()));
```

### Membership Introspection

Inspect a principal's full effective access -- base org/project roles, group memberships, resolved bindings, and merged scopes:

```bash
eve access memberships --org org_xxx --user user_abc
eve access memberships --org org_xxx --service-principal sp_xxx
```

The response includes `effective_scopes` (merged across all bindings), `effective_permissions`, and each binding's `matched_via` (direct or group).

### Resource-Specific Access Checks

Check and explain access against a specific data-plane resource:

```bash
eve access can orgfs:read /shared/reports --org org_xxx
eve access explain orgfs:write /shared/reports --org org_xxx --user user_abc
```

The response includes `scope_required`, `scope_matched`, and per-grant `scope_reason` explaining why a binding did or did not match the requested resource path.

### Policy-as-Code (v2)

Declare groups, roles, and scoped bindings in `.eve/access.yaml`. Use `version: 2`:

```yaml
version: 2
access:
  groups:
    eng-team:
      name: Engineering Team
      description: Scoped access for engineering collaborators
      members:
        - type: user
          id: user_abc
  roles:
    app_editor:
      scope: org
      permissions:
        - orgdocs:read
        - orgdocs:write
        - orgfs:read
        - envdb:read
  bindings:
    - subject: { type: group, id: eng-team }
      roles: [app_editor]
      scope:
        orgdocs: { allow_prefixes: ["/groups/app/**"] }
        orgfs: { allow_prefixes: ["/groups/app/**"] }
        envdb: { schemas: ["app"] }
```

Validate, plan, and sync:

```bash
eve access validate --file .eve/access.yaml
eve access plan --file .eve/access.yaml --org org_xxx
eve access sync --file .eve/access.yaml --org org_xxx
```

Sync is declarative: it creates, updates, and prunes groups, members, roles, and bindings to match the YAML. Invalid scope configurations fail fast before any mutations are applied. Binding subjects can be `user`, `service_principal`, or `group`.

## Key Rotation

Rotate the JWT signing key:

1. Set `EVE_AUTH_JWT_SECRET_NEW` alongside the existing secret
2. Server starts signing with the new key but accepts both during the grace period
3. After grace period (`EVE_AUTH_KEY_ROTATION_GRACE_HOURS`), remove the old secret
4. Emergency rotation: set only the new key (immediately invalidates all existing tokens)

## App SSO Integration

Add Eve SSO login to any Eve-deployed app using two shared packages: `@eve-horizon/auth` (backend) and `@eve-horizon/auth-react` (frontend). The platform auto-injects `EVE_SSO_URL`, `EVE_ORG_ID`, `EVE_PROJECT_ID`, and `EVE_API_URL` into deployed services.

### Magic-Link Login Opt-In (Passwordless Apps)

Apps can opt into passwordless browser login with `x-eve.auth.login_method: magic_link`. The SSO login page is branded for the project and shows email magic-link login instead of username/password.

```yaml
x-eve:
  auth:
    login_method: magic_link              # or password_or_magic_link, password
    self_signup: false                    # unknown emails get generic success, no email
    invite_requires_password: false       # invite callback skips /set-password
```

Magic-link emails are sent by Eve API through `POST /auth/magic-link` (not GoTrue directly) so the platform can enforce project policy, share the `x-eve.branding` template with invite emails, and avoid account enumeration. Projects without `x-eve.auth` keep legacy SSO behavior. Create new users with `eve org invite <email> --org <org_id> --project <project_id>`.

### Magic-Link Confirmation Interstitial (Security)

Eve-rendered magic-link and invite emails embed a wrap URL (`https://sso/m/mlw_<id>`), not the raw GoTrue verify URL. Email-security scanners (Defender SafeLinks, Mimecast, Proofpoint, Barracuda) follow every URL in mail and would otherwise consume single-use OTPs before the human clicks. The wrap renders a branded "Confirm sign-in / Accept invite" page; only the POST from the button reveals the GoTrue URL and 302-redirects. Treat this as a platform guarantee — no app-side work required.

### Domain-Based Signup (Path C Auto-Attach)

Pre-approve email domains so anyone with a matching address can sign in via magic link without a per-user invite. On first successful login the platform attaches them as `member` of the rule's `target_org`. One project can route different domains to different orgs.

```yaml
x-eve:
  auth:
    login_method: magic_link
    invite_requires_password: false
    org_access:
      mode: allowlist
      allowed_orgs: [org_Acme, org_Partner, org_Retailer]
      domain_signup:
        enabled: true
        domains:
          - { domain: example.com,  target_org: org_Acme, role: member }
          - { domain: partner.example,    target_org: org_Partner }
          - { domain: retailer.example, target_org: org_Retailer }
```

Rules are walked in declaration order — first match wins, so declare more-specific patterns first. Each rule's `target_org` must appear in `allowed_orgs`. Declaring free-email providers (`free-mail.example`) is allowed but produces a manifest coherence warning. Explicit pending invites take priority over domain signup (Path B beats Path C). Removing a rule stops new signups but does not retroactively remove existing memberships — drop those with `eve org members remove`.

Audit via the event spine: `auth.domain_signup.invite_created` and `auth.domain_signup.member_attached` carry `org_id`, `matched_rule`, and `matched_domain`.

### App Org Access and Admin Invites

Apps default to project-owner-org access. Use `mode: allowlist` to declare which customer orgs may use the app, and enable in-app admin invites that send branded magic-link onboarding:

```yaml
x-eve:
  auth:
    org_access:
      mode: allowlist
      allowed_orgs: [org_customer123, customer-slug]
      invite:
        enabled: true
        admin_roles: [admin, owner]
        invited_role: member          # fixed; app invites cannot create admins
```

Endpoints: `GET /auth/app-access` returns the user's allowed orgs (plus which ones they can invite into); `POST /auth/app-invites` lets an org admin/owner invite a regular member with the project-branded email. For cross-org apps, use `eveAppUserAuth()` on the backend instead of `eveUserAuth()` — it consults `/auth/app-access` and selects the org from `X-Eve-Org-Id`, `?eve_org_id=`, or first allowed.

### Project-Scoped Redirect Allowlist (Custom-Domain Apps)

The SSO broker only accepts redirect targets under the cluster domain by default. Apps deployed on their own domain must declare their origins:

```yaml
x-eve:
  auth:
    allowed_redirect_origins:
      - https://app.example.com
      - https://www.example.com
```

Entries are origin-only (`scheme://host[:port]`); paths/queries/fragments are rejected at manifest-validate time. The final allowlist returned by `GET /auth/app-context` is the union of: (1) explicit manifest entries, (2) the project's own eligible custom domains (`custom_domains` rows with `environment_id` and status `dns_verified`/`cert_provisioning`/`active`), and (3) cross-org custom domains owned by projects in `allowed_orgs`. Inspect with `eve project auth-context <project_id>`.

This replaces the hard-coded `EVE_DEFAULT_DOMAIN` allowlist for non-cluster origins. The broker uses the list for both `redirect_to` validation in `/callback` and CORS on `/session` and `/logout`. The `@eve-horizon/auth-react` provider auto-passes `project_id` on session/logout calls so cross-site cookies are scoped correctly.

### SameSite=None on Custom Domains (Platform Guarantee)

When SSO is deployed with `EVE_SSO_SECURE_COOKIES=true`, the broker emits `eve_sso_rt` and `eve_sso` cookies with `Secure; SameSite=None`. This is required for the React provider's cross-site `fetch('/session', { credentials: 'include' })` probe to carry cookies when the app is on a custom domain. Local k3d (`http://*.lvh.me`) stays on `SameSite=Lax`. Apps no longer need to configure this themselves.

### Restrict Self-Signup to Approved Email Domains

The SSO service gates `/auth/signup` and `/auth/magiclink` by email domain when the env var `EVE_SIGNUP_ALLOWED_EMAIL_DOMAINS` is set (comma-separated). Unset means all domains are allowed (default). The signup tab on the SSO login page displays a domain hint when restrictions are active.

```bash
# On the SSO deployment, set:
EVE_SIGNUP_ALLOWED_EMAIL_DOMAINS=acme.com,partner.io
```

Rejected requests return HTTP 422 with `error: email_domain_not_allowed`. Use this to keep public SSO endpoints invite-only-by-domain without disabling self-signup entirely. Existing accounts and admin invites are unaffected.

### Backend (`@eve-horizon/auth`)

Install: `npm install @eve-horizon/auth`

Use the unified middleware by default for new apps:

| Export | Behavior |
|--------|----------|
| `eveAuth()` | Non-blocking middleware. Verifies user or agent tokens and attaches normalized identity at `req.eveIdentity`. |
| `eveIdentityGuard()` | Returns 401 if `req.eveIdentity` is not set. Place on protected routes. |
| `eveAuthConfig()` | Handler returning `{ sso_url, eve_api_url, ... }` from auto-injected env vars. Frontend fetches this to discover SSO. |
| `eveAuthMe()` | `/auth/me` handler for the React SDK and custom clients. |

Keep the legacy split middleware only for apps that explicitly want user-only or agent-only handling:

| Export | Behavior |
|--------|----------|
| `eveUserAuth()` | User-only non-blocking middleware. Attaches `req.eveUser: { id, email, orgId, role }`. |
| `eveAuthGuard()` | Returns 401 if `req.eveUser` is not set. |
| `eveAuthMiddleware()` | Blocking middleware for agent/job tokens. Attaches `req.agent` with full `EveTokenClaims`. Returns 401 on failure. |
| `verifyEveToken(token)` | JWKS-based local verification (15-min cache). Returns `EveTokenClaims`. |
| `verifyEveTokenRemote(token)` | HTTP verification via `/auth/token/verify`. Always current. |

**Express setup** (~3 lines):

```typescript
import { eveAuth, eveIdentityGuard, eveAuthConfig, eveAuthMe } from '@eve-horizon/auth';

app.use(eveAuth());
app.get('/auth/config', eveAuthConfig());
app.get('/auth/me', eveAuthMe());               // Full response for React SDK
app.use('/api', eveIdentityGuard());
```

`req.eveIdentity` normalizes both token types:

- User token: `id`, `email`, `orgId`, `role`, `permissions`, `isAgent: false`
- Agent/job token: `jobId`, `agentSlug`, stable `email` as `{agent_slug}@eve.agent`, `permissions`, `isAgent: true`

Use `agentSlug` or the stable agent email for RLS, audit logs, and app-level routing. Do not key agent identity off `{job_id}@eve.agent`; that older pattern was per-job and unstable.

**NestJS setup**: apply `eveAuth()` globally in `main.ts`, then use a thin guard wrapper:

```typescript
// main.ts
import { eveAuth } from '@eve-horizon/auth';
app.use(eveAuth());

// auth.guard.ts -- thin NestJS adapter
@Injectable()
export class EveGuard implements CanActivate {
  canActivate(ctx: ExecutionContext): boolean {
    const req = ctx.switchToHttp().getRequest();
    if (!req.eveIdentity) throw new UnauthorizedException();
    return true;
  }
}

// auth-config.controller.ts
@Controller()
export class AuthConfigController {
  private handler = eveAuthConfig();

  @Get('auth/config')
  getConfig(@Req() req, @Res() res) { this.handler(req, res); }
}
```

**Verification strategies**: `eveAuth()` and `eveUserAuth()` default to `'local'` (JWKS, cached 15 min). Use `strategy: 'remote'` for immediate membership freshness at ~50ms latency per request.

**Custom role mapping**: If your app needs roles beyond Eve's `owner/admin/member`, bridge after `eveAuth()`:

```typescript
app.use((req, _res, next) => {
  if (req.eveIdentity && !req.eveIdentity.isAgent) {
    req.user = {
      ...req.eveIdentity,
      appRole: req.eveIdentity.role === 'member' ? 'viewer' : 'admin',
    };
  }
  next();
});
```

### Frontend (`@eve-horizon/auth-react`)

Install: `npm install @eve-horizon/auth-react`

| Export | Purpose |
|--------|---------|
| `EveAuthProvider` | Context provider. Bootstraps session: checks sessionStorage, probes SSO `/session`, caches tokens. |
| `useEveAuth()` | Hook: `{ user, loading, error, config, loginWithSso, loginWithToken, logout }` |
| `EveLoginGate` | Renders children when authenticated, login form otherwise. |
| `EveLoginForm` | Built-in SSO + token-paste login UI. |
| `createEveClient(baseUrl?)` | Fetch wrapper with automatic Bearer injection. |

**Simple setup** -- `EveLoginGate` handles the loading/login/authenticated states:

```tsx
import { EveAuthProvider, EveLoginGate } from '@eve-horizon/auth-react';

<EveAuthProvider apiUrl="/api">
  <EveLoginGate>
    <ProtectedApp />
  </EveLoginGate>
</EveAuthProvider>
```

**Custom auth gate** -- use `useEveAuth()` for full control over loading, login, and error states:

```tsx
import { EveAuthProvider, useEveAuth } from '@eve-horizon/auth-react';

function AuthGate() {
  const { user, loading, loginWithToken, loginWithSso, logout } = useEveAuth();
  if (loading) return <Spinner />;
  if (!user) return <LoginPage onSso={loginWithSso} onToken={loginWithToken} />;
  return <App user={user} onLogout={logout} />;
}

export default () => (
  <EveAuthProvider apiUrl="/api">
    <AuthGate />
  </EveAuthProvider>
);
```

**API calls with auth**: Use `createEveClient()` for automatic Bearer token injection:

```typescript
import { createEveClient } from '@eve-horizon/auth-react';
const client = createEveClient('/api');
const res = await client.fetch('/data');
```

### Migration from Custom Auth

The SDK replaces ~700-800 lines of hand-rolled auth with ~50 lines. Delete custom JWKS/token verification, Bearer extraction middleware, SSO URL discovery, session probe logic, token storage helpers, and login form. Keep app-specific role mapping and local password auth.

For the full migration checklist, types reference, token lifecycle, and advanced patterns (SSE auth, token paste mode, token staleness), see [references/app-sso-integration.md](references/app-sso-integration.md).

## Service Tokens for Deployed Services

Every deployed service receives an auto-injected `EVE_SERVICE_TOKEN` (90-day RS256 JWT, `type: service`) for server-to-server calls back into the Eve API. The deployer mints it on each deploy — apps no longer need to manually set this secret.

Tokens default to **read-only** permissions (`projects:read`, `jobs:read`, `threads:read`, `envs:read`, `secrets:read`, `builds:read`, `pipelines:read`, `agents:read`, `events:read`). Apps that need write access declare additional permissions explicitly in the manifest:

```yaml
services:
  api:
    x-eve:
      permissions: [jobs:write, events:write, threads:write]
```

Use this for app -> Eve API calls (creating jobs, emitting events, updating threads). For the full schema and call patterns, see [eve-read-eve-docs/references/secrets-auth.md](../eve-read-eve-docs/references/secrets-auth.md) and [eve-read-eve-docs/references/manifest.md](../eve-read-eve-docs/references/manifest.md).

## BYOK Model (LLM API Keys)

Eve does not proxy inference traffic. All model access is BYOK (Bring Your Own Keys): harnesses and apps bring their own API keys via secrets and call providers directly.

Store LLM provider keys as project secrets:

```bash
eve secrets set ANTHROPIC_API_KEY "sk-ant-xxx" --project proj_xxx
eve secrets set OPENAI_API_KEY "sk-xxx" --project proj_xxx
eve secrets set OPENAI_BASE_URL "https://my-vllm.runpod.ai/v1" --project proj_xxx
```

Harnesses resolve these automatically. For self-hosted models (vLLM, LM Studio via Tailscale), set the base URL and API key as secrets -- Eve provides connectivity via private endpoints (see `eve-deploy-debugging`), not a managed inference layer.

## Per-Org OAuth Credentials (BYOA)

Each org brings its own OAuth app credentials for Google Drive, Slack, and other integrations. No cluster-level shared secrets.

```bash
# View setup instructions (redirect URIs, required scopes)
eve integrations setup-info google-drive
eve integrations setup-info slack

# Register OAuth app credentials
eve integrations configure google-drive \
  --client-id "xxx.apps.googleusercontent.com" \
  --client-secret "GOCSPX-xxx" \
  --label "Acme Corp Google Drive"

eve integrations configure slack \
  --client-id "12345.67890" \
  --client-secret "abc123" \
  --signing-secret "def456" \
  --app-id "A0123ABC" \
  --label "Acme Corp Slack Bot"

# View current config (secrets redacted)
eve integrations config google-drive

# Then connect as before (uses per-org credentials)
eve integrations connect google-drive
eve integrations connect slack
```

Benefits: isolated credentials per org, custom consent screen branding, independent rate limits, no shared-secret blast radius.

## Project Role Resolution

Role and org membership changes take effect immediately -- the server resolves permissions from live DB memberships, not stale JWT claims. When a request includes a `project_id` but no `org_id`, the permission guard derives the org context from the project's owning org.

The Auth SDK (`@eve-horizon/auth`) exposes this via `eveUserAuth()` middleware. Use `strategy: 'remote'` for immediate membership freshness when needed.

## Project Secrets

```bash
# Set a secret
eve secrets set API_KEY "your-api-key" --project proj_xxx

# List keys (no values)
eve secrets list --project proj_xxx

# Delete a secret
eve secrets delete API_KEY --project proj_xxx

# Import from file
eve secrets import .env --project proj_xxx
```

### Secret Interpolation

Reference secrets in `.eve/manifest.yaml` using `${secret.KEY}`:

```yaml
services:
  api:
    environment:
      API_KEY: ${secret.API_KEY}
```

### Manifest Validation

Validate that all required secrets are set before deploying:

```bash
eve manifest validate --validate-secrets    # check secret references
eve manifest validate --strict              # fail on missing secrets
```

### Local Secrets File

For local development, create `.eve/dev-secrets.yaml` (gitignored):

```yaml
secrets:
  default:
    API_KEY: local-dev-key
    DB_PASSWORD: local-password
  staging:
    DB_PASSWORD: staging-password
```

### Worker Injection

At job execution time, resolved secrets are injected as environment variables into the worker container. File-type secrets are written to disk and referenced via `EVE_SECRETS_FILE`. The file is removed after the agent process reads it.

### Git Auth

The worker uses secrets for repository access:
- **HTTPS**: `github_token` secret → `Authorization: Bearer` header
- **SSH**: `ssh_key` secret → written to `~/.ssh/` and used via `GIT_SSH_COMMAND`

## Auth Mail Delivery (SES)

All branded auth emails (org/app invites, app-scoped magic-link, system-admin Supabase invites) flow through a single `MailerService`. When SMTP points at SES (`GOTRUE_SMTP_HOST=*.amazonaws.com` or `EVE_MAILER_CHECK_SUPPRESSION=true`), the mailer adds a pre-flight `GetSuppressedDestination` check so account-level suppressions cannot silently look like a successful send.

| Outcome | Behavior |
|---------|----------|
| Address suppressed | Throws `EmailSuppressedError`; no SMTP send |
| Not found | Send proceeds |
| AWS error (IRSA, throttling, network) | Fails open — logs `mailer.suppression_check_failed`, send proceeds |

Caller behavior: `sendEligibleMagicLink` swallows `EmailSuppressedError` and returns generic success (preserves account-enumeration defense), logging `mail.suppressed_drop`. Invite paths re-throw so admins see the error.

When `EVE_SES_CONFIGURATION_SET` is set, SES routes Bounce/Complaint/Delivery/Reject events to SNS, which POSTs to `/webhooks/ses-feedback`. The webhook verifies SNS signature, checks `TopicArn` against `EVE_SES_FEEDBACK_TOPIC_ARN`, and persists one row per affected recipient in `email_delivery_events` (idempotent by `sha256(snsMessageId|eventType|recipient)`).

Inspect events via the admin CLI:

```bash
eve admin email bounces list
eve admin email bounces list --recipient user@example.com
eve admin email bounces list --event-type Bounce --limit 100 --json
```

Read-only from the local table; does not mutate SES. To clear an account-level suppression, see the SES suppression runbook.

Structured log events to grep in API pod logs: `mailer.sent`, `mailer.smtp_failed`, `mailer.suppressed`, `mailer.suppression_check_failed`, `mail.suppressed_drop`, `sns.subscription_confirmed`, `sns.rejected`, `ses.feedback_persisted`.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Not authenticated | Run `eve auth login` |
| Token expired | Re-run `eve auth login` (tokens auto-refresh if within 5 min of expiry) |
| Bootstrap already completed | Use `eve auth login` (existing user) or `eve admin invite` (new users). On non-prod stacks, `eve auth bootstrap` auto-attempts server recovery. For wrong-email recovery: `eve auth bootstrap --email correct@example.com` |
| Secret missing | Confirm with `eve secrets list` and set the key |
| Interpolation error | Verify `${secret.KEY}` spelling; run `eve manifest validate --validate-secrets` |
| Git clone failed | Check `github_token` or `ssh_key` secret is set |
| Service can't reach API | Verify `EVE_API_URL` is injected (check `eve env show`) |
| Scoped access denied | Run `eve access explain <permission> <resource> --org <org>` to see scope match details. Check that the binding's scope constraints include the target path/schema. Built-in roles (owner/admin/member) carry wildcard `envdb` scope, so envdb denial for those roles points at the permission set, not missing scope |
| Wrong role shown | Role is resolved from live DB memberships. Run `eve auth permissions` to see effective role. If multi-org, check `eve auth status` for per-org membership listing |
| Short-lived Claude token in jobs | Run `eve auth creds` to check token type. If `oauth` (not `setup-token`), regenerate with `claude setup-token` then re-sync with `eve auth sync` |
| Codex token expired between jobs | Automatic write-back should refresh it. If not, re-run `eve auth sync`. Check that `~/.codex/auth.json` or `~/.code/auth.json` has a fresh token |
| App SSO not working | Verify `EVE_SSO_URL` is injected (`eve env show`). For local dev, set `EVE_SSO_URL`, `EVE_ORG_ID`, and `EVE_API_URL` manually |
| Stale org membership in app tokens | Default 1-day TTL. Use `strategy: 'remote'` in `eveUserAuth()` for immediate membership checks |

### Incident Response (Secret Leak)

If a secret may be compromised:
1. **Contain**: Rotate the secret immediately via `eve secrets set`
2. **Invalidate**: Redeploy affected environments
3. **Audit**: Check `eve job list` for recent jobs that used the secret
4. **Recover**: Generate new credentials at the source (GitHub, AWS, etc.)
5. **Document**: Record the incident and update rotation procedures
