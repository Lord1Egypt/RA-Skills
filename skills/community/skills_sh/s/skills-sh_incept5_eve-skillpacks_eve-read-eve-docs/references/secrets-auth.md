# Secrets + Auth Reference

## Use When
- You need to manage secret scope, interpolation, and environment overrides.
- You need to configure auth, identities, roles, or policy behavior.
- You need to onboard service principals or troubleshoot permission failures.

## Load Next
- `references/cli.md` for secret and auth command workflows.
- `references/manifest.md` for manifest `x-eve.requires` and interpolation.
- `references/skills-system.md` when auth affects installed capabilities.

## Ask If Missing
- Confirm scope needed (project, org, user, or system) before setting values.
- Confirm whether values come from `.eve/dev-secrets.yaml`, API sources, or CI inputs.
- Confirm required roles/access groups when permission checks are failing.

## Secrets

### Scope Hierarchy

Secrets resolve in priority order: **project > user > org > system**. Values are encrypted at rest and never returned in plaintext. The `show` endpoint returns a masked value (first/last characters only).

API paths: `/system/secrets`, `/users/:id/secrets`, `/orgs/:id/secrets`, `/projects/:id/secrets`.

### CLI

```bash
eve secrets list --project proj_xxx
eve secrets set KEY value --project proj_xxx
eve secrets show KEY --project proj_xxx

eve secrets ensure --project proj_xxx --keys GITHUB_WEBHOOK_SECRET
eve secrets export --project proj_xxx --keys GITHUB_WEBHOOK_SECRET
```

`ensure` auto-generates allowlisted secrets (e.g., `GITHUB_WEBHOOK_SECRET`). `export` returns the plaintext value for external configuration -- treat it as sensitive.

### Import Secrets from File

Batch-import secrets from a `KEY=VALUE` env file:

```bash
eve secrets import --org org_xxx --file ./secrets.env
eve secrets import --project proj_xxx --file .env
```

Supported scopes: `--project`, `--org`, `--user`, `--system` (admin only). Lines starting with `#` and blank lines are ignored. Values are read verbatim after `=` (quotes are not stripped). Each key is upserted as `env_var`.

### Manifest Validation

Declare required secrets in `eve.yaml`:

```yaml
x-eve:
  requires:
    secrets: [GITHUB_TOKEN, REGISTRY_TOKEN]
```

Validate with:
```bash
eve project sync --validate-secrets
eve project sync --strict
eve secrets validate --project proj_xxx
```

Validation reports missing secrets with scope-aware remediation hints.

### Interpolation

Reference secrets in manifest environment blocks:

```yaml
environment:
  DATABASE_URL: postgres://user:${secret.DB_PASSWORD}@db:5432/app
  API_KEY: ${secret.EXTERNAL_API_KEY}
```

Job `env_overrides` support the same `${secret.KEY}` placeholders for agent
steps, workflow script/shorthand `run` steps, and pipeline `action: { type: run
}` steps. Values are resolved in memory immediately before the harness or bash
process starts; persisted job rows and `eve job show` continue to expose only
the raw placeholder text.

If an override references a missing secret, the step fails before execution with
`missing_secret_override` and the execution log includes the unresolved key
names. Reserved runtime keys such as `PATH`, `HOME`, and `EVE_*` are rejected by
schema validation and stripped defensively at execution time for legacy rows.

### Local Dev Secrets

Create `.eve/dev-secrets.yaml` (gitignored) for local overrides:

```yaml
secrets:
  default:
    DB_PASSWORD: dev_password
  staging:
    DB_PASSWORD: staging_password
```

API secrets overlaid by local dev-secrets. Local takes precedence. For k8s production, set secrets via the API.

### Host Env Files

Two host-level files for local development (never committed):

- **`.env`** (repo root) -- Local secrets and internal tokens.
- **`system-secrets.env.local`** -- System-level defaults, bootstrapped on API startup. Restart API to pick up changes.

### Required System Vars

| Variable | Where | Purpose |
|----------|-------|---------|
| `EVE_SECRETS_MASTER_KEY` | API | Encryption key for secrets at rest |
| `EVE_INTERNAL_API_KEY` | Worker + API | Internal token for resolve endpoint |

### Worker Injection

- Resolved secrets are injected as **environment variables** for the worker and deployer (allowlisted).
- File and `ssh_key` secrets are written outside the repo workspace and are not available to agent processes.
- The worker does **not** write `.eve/secrets.env` into the workspace and does **not** set `EVE_SECRETS_FILE`.

### Git Auth Injection

- **HTTPS clone**: `github_token` secrets are injected into the clone URL for private repo access.
- **SSH clone**: `ssh_key` secrets are written to a temp key and wired via `GIT_SSH_COMMAND`.
- Missing auth surfaces explicit errors with remediation hints (`eve secrets set`).

### Fail-Fast on Resolution Failure

The worker fails fast on secret resolution failure instead of silently substituting
empty strings. Provider credentials are resolved at the platform layer, not cached
in the worker. If `EVE_INTERNAL_API_KEY` is missing or incorrect, the attempt fails
immediately with a descriptive error.

### Troubleshooting Secret Resolution

If a job fails during clone or secret resolution:

1. Confirm the secret exists: `eve secrets show <KEY> --project <id>`
2. Ensure `EVE_INTERNAL_API_KEY` and `EVE_SECRETS_MASTER_KEY` are set for API/worker
3. Check orchestrator/worker logs for `[resolveSecrets]` warnings
4. Re-run with corrected secret scope (project > org > system)

### Incident Response

If you suspect a secret leak:

1. **Contain** -- Rotate the affected secret at the source. Update via `eve secrets set` or `eve secrets import`.
2. **Invalidate** -- Restart affected services to flush cached credentials. If a token was printed to logs, assume compromise.
3. **Audit** -- Review job and pipeline logs for leakage patterns. Check correlation IDs.
4. **Recover** -- Re-run failed jobs after rotation.
5. **Document** -- Record what leaked, where, and why. Add guardrails if due to missing redaction.

---

## Auth

Eve uses **RS256 JWT** tokens with pluggable identity providers (SSH, Nostr). Supabase (HS256) mode is optional when `SUPABASE_JWT_SECRET` is set.

### Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `EVE_AUTH_ENABLED` | No | Enable auth (default `true`) |
| `EVE_AUTH_PRIVATE_KEY` | Yes | RSA private key (PEM string or file path) |
| `EVE_BOOTSTRAP_TOKEN` | Prod | One-time token for initial admin creation |
| `EVE_AUTH_PUBLIC_KEY` | No | Derived from private if omitted |
| `EVE_AUTH_CHALLENGE_TTL_SECONDS` | No | Challenge validity (default `300`) |
| `EVE_AUTH_TOKEN_TTL_DAYS` | No | User token TTL in days (default `1`, max `90`) |
| `EVE_AUTH_KEY_ID` | No | Key identifier in JWKS (default `key-1`) |
| `EVE_SIGNUP_ALLOWED_EMAIL_DOMAINS` | No | Comma-separated allowlist for SSO self-signup (`/auth/signup` and `/auth/magiclink`). Unset = all domains allowed. |

Generate keys:
```bash
openssl genrsa -out eve-auth.key 2048
openssl rsa -in eve-auth.key -pubout -out eve-auth.pub
export EVE_AUTH_PRIVATE_KEY="$(cat eve-auth.key)"
```

### Bootstrap

Create the first admin user. Three security modes:

| Mode | Trigger | Token Required |
|------|---------|----------------|
| **auto-open** | Fresh deploy, no users | No (10-min window) |
| **recovery** | Trigger file on host (`/tmp/eve-bootstrap-enable`) | No |
| **secure** | `EVE_BOOTSTRAP_TOKEN` set | Yes |

```bash
eve auth bootstrap --email admin@example.com --token $EVE_BOOTSTRAP_TOKEN
eve auth bootstrap --status
```

Production requires `EVE_BOOTSTRAP_TOKEN`. Use your real email -- it becomes your login identity.
In local/non-production environments, `eve auth bootstrap` attempts the API recovery path even when bootstrap is marked completed, and can return an existing admin token when recovery mode is allowed.

### Challenge-Response Login

Users authenticate by signing a challenge with a registered identity. The server selects the appropriate verifier based on identity type.

**CLI (recommended):**
```bash
eve auth login --email you@example.com
eve auth login --email you@example.com --ttl 30
```

The CLI requests a challenge, signs the nonce with your SSH key, submits the signature, and stores the token in `~/.eve/credentials.json`.

**SSH manual flow (curl):**
```bash
# 1. Request challenge
curl -X POST "$EVE_API_URL/auth/challenge" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com"}'
# Response: { "challenge_id": "...", "nonce": "...", "expires_at": "..." }

# 2. Sign the nonce (namespace must be "eve-auth")
echo -n "$NONCE" | ssh-keygen -Y sign -f ~/.ssh/id_ed25519 -n eve-auth

# 3. Verify signature
curl -X POST "$EVE_API_URL/auth/verify" \
  -H "Content-Type: application/json" \
  -d '{"challenge_id": "...", "signature": "-----BEGIN SSH SIGNATURE-----\n..."}'
# Response: { "access_token": "...", "user_id": "...", "expires_at": ... }
```

**Nostr manual flow (curl):**
```bash
# 1. Request challenge (note: provider + pubkey, not email)
curl -X POST "$EVE_API_URL/auth/challenge" \
  -H "Content-Type: application/json" \
  -d '{"provider": "nostr", "pubkey": "<64-char-hex-pubkey>"}'

# 2. Sign a kind-22242 event with ["challenge", "<nonce>"] tag (client-side)

# 3. Submit signed event
curl -X POST "$EVE_API_URL/auth/verify" \
  -H "Content-Type: application/json" \
  -d '{"challenge_id": "...", "signature": "<kind-22242-event-json>"}'

# With invite code (for unregistered pubkeys):
curl -X POST "$EVE_API_URL/auth/verify" \
  -d '{"challenge_id": "...", "signature": "...", "invite_code": "abc123..."}'
```

### Self-Service Access Requests

Users can submit access requests without an invite:

```bash
eve auth request-access --org "My Company" --email you@example.com
eve auth request-access --org "My Company" --ssh-key ~/.ssh/id_ed25519.pub
eve auth request-access --status <request_id>
```

Admins review requests via:

```bash
eve admin access-requests list
eve admin access-requests approve <request_id>
eve admin access-requests reject <request_id> --reason "..."
```

List responses use the canonical `{ "data": [...] }` envelope. `eve auth list-service-accounts` output also uses the data envelope.

Approval semantics:
- Approval is transactional (no partial org/user leftovers on failure).
- Duplicate fingerprints reuse the existing identity owner instead of failing.
- Re-approving an already-approved request is idempotent.
- Legacy partial orgs with matching slug+name are reused during approval.

### Access Groups + Scoped Bindings

First-class access groups provide fine-grained data-plane authorization. Groups contain users and service principals, and bindings can carry scoped access constraints for org filesystem paths, org document paths, and environment DB schemas/tables.

#### Groups CLI

```bash
eve access groups create --org org_xxx --slug eng-team --name "Engineering Team" \
  [--description "Backend engineering group"]
eve access groups list --org org_xxx
eve access groups show eng-team --org org_xxx
eve access groups update eng-team --org org_xxx --name "Platform Engineering"
eve access groups delete eng-team --org org_xxx

# Group membership
eve access groups members list eng-team --org org_xxx
eve access groups members add eng-team --org org_xxx --user user_abc
eve access groups members add eng-team --org org_xxx --service-principal sp_xxx
eve access groups members remove eng-team --org org_xxx --user user_abc
```

#### Scoped Bindings

Bindings can carry `--scope-json` to restrict data-plane access:

```bash
eve access bind --org org_xxx --group grp_xxx --role data-reader \
  --scope-json '{"orgfs":{"allow_prefixes":["/shared/","/reports/"]}}'

eve access bind --org org_xxx --user user_abc --role db-analyst \
  --scope-json '{"envdb":{"schemas":["public"],"tables":["analytics_*"]}}'
```

Scope structure supports three resource types:
- `orgfs`: `allow_prefixes`, `read_only_prefixes` for org filesystem paths
- `orgdocs`: `allow_prefixes`, `read_only_prefixes` for org document paths
- `envdb`: `schemas`, `tables` for environment database access

Built-in roles (`owner` / `admin` / `member`) are granted a **wildcard envdb scope** automatically. Their `envdb:read` / `envdb:write` permissions resolve to access on any schema/table they have permission on, without needing an explicit `envdb` scope block on the membership. Custom roles bound via `eve access bind` still need an explicit scope to access envdb resources.

> Scope narrows; permission grants. A workflow that declares `scope.orgfs.allow_prefixes` (or `scope.orgdocs.*`, `scope.cloud_fs.*`) still needs the **step agent** to declare the matching `orgfs:read` / `orgfs:write` etc. in `access.permissions`. `DEFAULT_AGENT_PERMISSIONS` does not include orgfs / orgdocs / cloud_fs. See `references/agents-teams.md` § Agent Permissions and `references/pipelines-workflows.md` § Workflow Token Scope.

#### Executor default permission sets

When a `script:` or `action: { type: run }` step does not declare `permissions:`,
the executor falls back to a built-in default. Authors widen with an explicit
list on the step.

| Execution type | Default | Includes |
| --- | --- | --- |
| `agent` | `DEFAULT_AGENT_PERMISSIONS` | `jobs:*` (read/write/harness_override), `projects:read`, `threads:*`, `envdb:read`, `secrets:read`, `builds:read`, `pipelines:read` |
| `script` | `DEFAULT_SCRIPT_JOB_PERMISSIONS` | broad platform-ops baseline: `jobs:read+write`, `projects:read`, `envs:read+write`, `envdb:read+write`, `releases:read`, `builds:read`, `pipelines:read`, `secrets:read` |
| `action: { type: run }` | `DEFAULT_ACTION_RUN_JOB_PERMISSIONS` | least-privilege: `jobs:read+write`, `projects:read`, `envs:read` only — **no** `secrets:read`. Authors opt in to wider access. |

All three are defined in `packages/shared/src/permissions.ts`. The
`assertActorCanGrantPermissions` guard rejects any declared permission
the invoking actor does not themselves hold.

#### Resource-Specific Access Checks

Check access against specific resources:

```bash
eve access can --org org_xxx --user user_abc --permission orgfs:read \
  --resource-type orgfs --resource /reports/q4.md --action read

eve access can --org org_xxx --group grp_xxx --permission envdb:read \
  --resource-type envdb --resource public.analytics --action read
```

`explain` also shows scope match details:

```bash
eve access explain --org org_xxx --user user_abc --permission orgfs:write
```

#### Memberships Introspection

Inspect the full effective access for any principal:

```bash
eve access memberships --org org_xxx --user user_abc
eve access memberships --org org_xxx --service-principal sp_xxx
```

Returns: base roles, group memberships, direct bindings, effective bindings (with role expansion and group resolution), effective permissions, and effective scopes for orgfs/orgdocs/envdb.

#### Policy-as-Code (Groups + Scoped Bindings)

The `.eve/access.yaml` format now supports groups and scoped bindings:

```yaml
access:
  groups:
    eng-team:
      name: Engineering Team
      description: Backend engineering group
      members:
        - type: user
          id: user_abc
        - type: service_principal
          id: sp_xxx
    data-team:
      name: Data Analytics Team
      members:
        - type: user
          id: user_def

  roles:
    data-reader:
      scope: org
      permissions: [orgfs:read, orgdocs:read, envdb:read]

  bindings:
    - roles: [data-reader]
      subject:
        type: group
        id: data-team
      scope:
        orgfs:
          allow_prefixes: ["/shared/", "/reports/"]
        envdb:
          schemas: [public]
```

`validate`, `plan`, and `sync` now handle groups, group members, and scoped bindings. The plan output includes group creates/updates/prunes, member adds/removes, and binding scope replacements.

### Credential Check

Inspect local AI tool credential availability:

```bash
eve auth creds                # Show Claude + Codex cred status
eve auth creds --claude       # Only Claude
eve auth creds --codex        # Only Codex
```

Verify managed Claude auth after syncing:

```bash
eve auth verify --harness claude --project proj_xxx --json
```

This creates a short managed Claude job and returns `ok`, selected key/scope,
token class, Claude Code `apiKeySource`, and whether the model replied
`EVE_AUTH_OK`.

### OAuth Token Sync

Sync local OAuth tokens into Eve secrets:

```bash
eve auth sync                 # Sync to user-level (default)
eve auth sync --org org_xxx   # Sync to org-level
eve auth sync --project proj_xxx  # Sync to project-level
eve auth sync --dry-run       # Preview without syncing
```

This sets `CLAUDE_CODE_OAUTH_TOKEN` (Claude) and `CODEX_AUTH_JSON_B64` (Codex/Code) at the requested scope.

Claude runtime selection uses scope specificity first (`project > org > user >
system`). Within the same scope, `ANTHROPIC_API_KEY` wins over
`CLAUDE_CODE_OAUTH_TOKEN`; across scopes, a more-specific setup-token beats a
broader API key. Setup-tokens are materialized to attempt-scoped
`CLAUDE_CONFIG_DIR` under `EVE_JOB_USER_HOME`, and conflicting Claude auth env
vars are scrubbed after `env_overrides`.

#### Token Types and Lifetimes

| Token prefix | Type | Lifetime | Recommendation |
|---|---|---|---|
| `sk-ant-oat01-*` | `setup-token` (long-lived) | Long-lived | Preferred for jobs and automation |
| Other `sk-ant-*` | `oauth` (short-lived) | ~15h | Use for interactive dev; regenerate with `claude setup-token` |

`eve auth sync` warns when syncing a short-lived OAuth token. Use `eve auth creds` to inspect token type before syncing:

```bash
eve auth creds                # Shows token type (setup-token vs oauth) and Codex expiry
```

#### Automatic Codex/Code Token Write-Back

After each harness invocation, the worker checks if the Codex/Code CLI refreshed `auth.json` during the session. If the token changed, it is automatically written back to the originating secret scope (user/org/project) so the next job starts with a fresh token. This is transparent and non-fatal -- a write-back failure logs a warning but does not affect the job result.

#### Internal Secret Update Endpoint

The platform exposes `PATCH /internal/secrets/:scope_type/:scope_id/:key` for worker-to-API token write-back:
- Requires `x-eve-internal-token` header (same `EVE_INTERNAL_API_KEY` used by secret resolution)
- **Update-only** -- returns 404 if the secret does not already exist (no create semantics)
- Accepts `{ "value": "..." }` body

### Token Types

**User Tokens** -- Issued on successful login. Used for API access.
```json
{ "sub": "user_abc123", "email": "user@example.com", "type": "user", "iat": 1706000000, "exp": 1706086400 }
```

**Job Tokens** -- Scoped tokens issued to running jobs with limited permissions.

**App-Link Tokens** -- Short-lived RS256 JWTs minted for a consumer app-link
subscription to call a producer API. They carry `type: app_link`,
`subscription_id`, `consumer_project_id`, `producer_project_id`,
`consumer_principal`, `consumer_env`, `producer_env`, `api_name`, and requested
scopes. Verification re-reads the active subscription and grant, so producer
revocation is effective before token expiry. The token audience is
`project:<producer_project_id>`.

Internal mint endpoint:

```
POST /internal/auth/mint-app-link-token
```

Only platform workers/deployers call it with `x-eve-internal-token`; app code
receives the minted value through `EVE_APP_LINK_<ALIAS>_TOKEN`.
```json
{ "user_id": "user_abc123", "org_id": "org_xyz789", "permissions": ["job:read", "job:write"], "type": "job", "iat": 1706000000, "exp": 1706086400 }
```

**Service Principal Tokens** -- RS256 JWT with `sub: sp:{principal_id}`, `type: service_principal`, explicit `scopes` array. No implicit role expansion.

### Permissions

Eve uses a unified permission model. Job tokens carry a limited `permissions` list scoped to the project/job. Custom roles are additive only.

```bash
eve auth permissions          # Full permission catalog
eve auth whoami               # Current user + effective permissions
```

API: `GET /auth/permissions` (catalog), `GET /auth/me` (current user).

Permission resolution: `effective = expand(base_role) UNION all(bound_custom_role_permissions)`.

### Identity Management

Identities can be SSH public keys, Nostr pubkeys, or other provider-specific credentials. Each is linked to a user account.

Register additional identities:
```bash
curl -X POST "$EVE_API_URL/auth/identities" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"public_key": "ssh-ed25519 AAAA... user@laptop", "label": "laptop"}'
```

Admins can register keys for other users by including `"email": "user@example.com"` in the body.

### JWKS Endpoint

Public keys for token verification:
```bash
curl "$EVE_API_URL/.well-known/jwks.json"
# Returns: { "keys": [{ "kty": "RSA", "kid": "key-1", "use": "sig", "alg": "RS256", ... }] }
```

During key rotation, both old and new keys appear in JWKS.

### Key Rotation

**Standard rotation (with grace period):**
```bash
# 1. Generate new key pair
openssl genrsa -out eve-auth-new.key 2048
openssl rsa -in eve-auth-new.key -pubout -out eve-auth-new.pub

# 2. Configure grace period
export EVE_AUTH_PRIVATE_KEY="$(cat eve-auth-new.key)"
export EVE_AUTH_PUBLIC_KEY="$(cat eve-auth-new.pub)"
export EVE_AUTH_PUBLIC_KEY_OLD="$(cat eve-auth-old.pub)"
export EVE_AUTH_KEY_ID="key-2"
export EVE_AUTH_KEY_ID_OLD="key-1"

# 3. Restart API. New tokens use key-2; old tokens still verify via key-1.
# 4. After old tokens expire (default 24h), remove OLD vars and restart.
```

**Emergency rotation (key compromise):**
```bash
export EVE_AUTH_PRIVATE_KEY="$(cat eve-auth-new.key)"
export EVE_AUTH_KEY_ID="key-emergency-$(date +%s)"
unset EVE_AUTH_PUBLIC_KEY_OLD   # Do not honor old tokens
# Restart. All existing tokens are immediately invalidated.
```

---

## Identity Providers

Eve uses a pluggable identity provider framework. Providers register at startup and the auth guard evaluates them in a two-stage chain: **Bearer JWT first**, then provider-specific request auth.

### Provider Interface

Every provider implements:

```typescript
interface IdentityProvider {
  readonly name: string;
  createChallenge(params): Promise<ChallengeData>;
  verifyChallenge(challenge, proof, identities): Promise<VerifiedIdentity | null>;
  fingerprint(publicKey: string): Promise<string>;
  // Optional: per-request auth (no login required)
  extractFromRequest?(req): ExtractedCredential | null;
  verifyRequestCredential?(credential): Promise<VerifiedIdentity | null>;
}
```

`fingerprint` computes a deterministic dedup key to prevent duplicate registrations. `VerifiedIdentity` with `identity: null` triggers invite-gated provisioning.

### Auth Chain

```
Request --> @Public route? --> allow
        --> Stage 1: Bearer JWT (RS256/HS256) --> success: allow
        --> Stage 2: Provider request auth (registry iterates all providers) --> success: allow
        --> 401 Unauthorized
```

Stage 2 catches all errors and logs warnings. A broken provider does not cause a 500.

### SSH Provider (`github_ssh`)

- **Challenge**: Random 32-byte `base64url` nonce.
- **Verify**: Runs `ssh-keygen -Y verify` as subprocess. Iterates all registered SSH identities for the user until one matches.
- **Fingerprint**: `ssh-keygen -lf`, returns MD5 fingerprint (e.g., `MD5:ab:cd:...`).
- **Request-level auth**: Not supported. SSH requires the challenge/response flow.

### Nostr Provider (`nostr`)

Two authentication paths:

**Challenge/Verify (login)**: Client signs a kind-22242 event containing a `["challenge", "<nonce>"]` tag. Server verifies event ID + Schnorr signature (BIP-340), checks the challenge tag, matches pubkey to registered identities. Unregistered pubkeys trigger invite-gated provisioning.

**NIP-98 Request Auth**: Per-request auth via `Authorization: Nostr <base64>` header. Client creates a kind-27235 event with URL, method, and body hash tags. Server validates:
1. Event ID + Schnorr signature
2. `kind === 27235`
3. URL tag matches canonical request URL
4. Method tag matches request method
5. For non-GET: `payload` tag equals `sha256(body)`
6. Timestamp within +/-60s of server time
7. Replay protection via `auth_request_replays` table (120s TTL)

### Invite-Gated Provisioning

When an unregistered identity authenticates, the system attempts to provision via org invites.

**Create an invite (admin):**
```bash
curl -X POST "$EVE_API_URL/auth/invites" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"org_id": "org_xxx", "provider_hint": "nostr", "identity_hint": "<pubkey>", "role": "member", "expires_in_hours": 72}'
```

**Provisioning flow:**
1. Unregistered identity authenticates (challenge/verify or NIP-98)
2. Provider returns `VerifiedIdentity` with `identity: null`
3. Invite lookup: explicit `invite_code` takes priority, then `identity_hint` matching
4. Atomic provisioning: create user (synthetic email), create identity row, create org membership with invite role, mark invite used

**List invites:**
```bash
curl "$EVE_API_URL/auth/invites/org_xxx" -H "Authorization: Bearer $ADMIN_TOKEN"
```

### Org-Scoped Email Invites

Use the org-scoped invite API when an Eve-compatible app needs to invite a user by email, optionally send an email immediately, and preserve an app return URL through SSO onboarding.

**Permissions:**
- `orgs:invite` -- create and list org-scoped invites
- `orgs:members:read` -- list org members and search by email/display-name prefix

**Create an org-scoped invite:**
```bash
curl -X POST "$EVE_API_URL/orgs/org_xxx/invites" \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "role": "member",
    "redirect_to": "https://app.example.com/invite/complete",
    "project_id": "proj_123"
  }'
```

`project_id` is optional. When present, it must belong to the org being invited into and resolves project branding for the email subject, body, and `From:` display name. It is also copied into `app_context.project_id` for auditability.

**CLI:**
```bash
eve org invite user@example.com \
  --org org_xxx \
  --project proj_123 \
  --redirect-to https://app.example.com/invite/complete
```

Projects define invite email branding in `.eve/manifest.yaml`:

```yaml
x-eve:
  branding:
    app_name: "ACME Portal"
    app_logo_url: "https://sandbox.acme.example/assets/logo.svg"
    primary_color: "#1f6feb"
    email_from_name: "ACME Portal"
    reply_to_email: "support@acme.example"
    support_email: "support@acme.example"
    support_url: "https://acme.example/help"
```

Run `eve project sync` after changing the manifest. If an invite omits `project_id` or the project has no branding, Eve Horizon defaults are used. Phase 1 keeps the sender address on the platform default; only the display name is app-branded.

**List org-scoped invites:**
```bash
curl "$EVE_API_URL/orgs/org_xxx/invites" -H "Authorization: Bearer $USER_TOKEN"
```

**Member picker lookup:**
```bash
curl "$EVE_API_URL/orgs/org_xxx/members/search?q=ali" \
  -H "Authorization: Bearer $USER_TOKEN"
```

`redirect_to` is stored on the invite record. Invite emails flow through a GoTrue `generate_link` action link and then GoTrue's `/verify` endpoint, which returns to the SSO root with tokens in the hash fragment. If the invite is auto-applied during Supabase token exchange, Eve returns `invite_redirect_to` from `/auth/exchange`, and the SSO callback uses it as a fallback destination when nested redirect params are stripped from the email link. For default invite accepts, the SSO broker establishes the session, routes the user through `/set-password`, then redirects to the final app URL.

If the originating project sets `x-eve.auth.invite_requires_password: false`, SSO skips `/set-password` and redirects to the final app URL after the session is established.

### App-Scoped Magic-Link Login

Projects can opt into passwordless app login:

```yaml
x-eve:
  auth:
    login_method: magic_link
    self_signup: false
    invite_requires_password: false
```

SSO fetches `GET /auth/app-context?project_id=<project_id>` to render the project-branded login page. The app-scoped magic-link form calls `POST /auth/magic-link`; Eve verifies the project policy and recipient eligibility before generating a GoTrue magic-link action URL and sending the email through the shared branded mailer. `login_method: password_or_magic_link` keeps password login visible while still routing the secondary magic-link request through Eve API. Projects without `x-eve.auth` keep the legacy SSO magic-link path.

Magic-link emails use the same `x-eve.branding` values as invite emails. `self_signup: false` returns generic success for unknown emails but does not call GoTrue and does not send email.

### Magic-Link Confirmation Interstitial

All Eve-rendered magic-link and invite emails go out with a wrapped URL (`https://sso/m/mlw_<26 base32>`) instead of the raw GoTrue verify URL. The OTP is only revealed when a human clicks "Sign in" / "Accept invite" on the SSO-rendered interstitial, so corporate scanners (Defender SafeLinks, Mimecast, Proofpoint, Barracuda, Cisco IronPort) that GET every URL in incoming mail no longer burn the single-use token.

- `AuthService.wrapActionLink` stores the GoTrue URL in `magic_link_wraps` (migration `00094_project_auth_config.sql` + `00098_magic_link_wraps.sql`; 1h TTL, 24h retention) and returns the wrap URL.
- `HEAD/GET /m/:wrap` is fully idempotent — every scanner prefetch increments `get_count` for telemetry; only `POST /m/:wrap` (the button submit) atomically consumes the wrap and 302's to GoTrue's verify endpoint.
- Wrap tokens are validated against the `mlw_<26 base32>` typeid regex before any DB lookup. The interstitial honours the project-aware redirect allowlist and sets `Cache-Control: no-store` + `Referrer-Policy: no-referrer`.
- A consumed wrap emits `auth.action_link.wrap_redeemed` on the event spine with `{ org_id, email_hash, kind, get_count, latency_ms }` for monitoring scanner activity.

App developers do not need to change anything; this is platform-side.

### Domain-Based Signup (Email Allowlist Without Invites)

Pre-approve email domains so anyone with a matching address can sign in via magic link without a per-user invite. Each rule maps one domain pattern to one target org, so a single project can serve multiple customer orgs.

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
          - domain: example.com
            target_org: org_Acme
          - domain: partner.example
            target_org: org_Partner
          - domain: retailer.example
            target_org: org_Retailer
```

**v2 schema (2026-05-12, breaking change).** Each entry under `domains` is now an object with a required `target_org`. The v1 list-of-strings shape and the block-level `target_org`/`role` fields are gone; manifest sync rejects them.

The operator declares the trusted domains; the platform trusts them (no DNS proof). Free-email providers like `free-mail.example` emit a manifest coherence warning per rule but are not blocked.

Eligibility ordering on `POST /auth/magic-link`:

1. Known user with allowed-org or project membership → branded send.
2. Pending *explicit* admin-issued invite → generic success; the invite remains the entry point.
3. Email's domain matches one rule (first-match in declaration order; declare more-specific rules first if precedence matters) → write a one-shot `org_invites` row tagged `app_context.source: domain_signup`, `app_context.org_id: <matched rule.target_org>`, `app_context.matched_rule: <pattern>` and send branded magic link. The SSO callback consumes the invite and upserts membership into the matched rule's `target_org`.
4. Otherwise fall through to legacy `self_signup`, then to generic success.

Repeat magic-link requests within 72 hours reuse the existing invite row for the same email + target org (idempotent). Audit events `auth.domain_signup.invite_created` (includes `org_id`, `email_domain`, `matched_rule`, `email_hash`) and `auth.domain_signup.member_attached` flow through the event spine for subscribed webhooks; PII is reduced to a domain string plus a 12-char SHA-256 prefix of the email.

The public `/auth/app-context` exposes only `auth.org_access.domain_signup_enabled` (bool) — the raw rule list is **never** surfaced unauthenticated. Project admins can fetch `GET /auth/app-context/admin?project_id=...` (or run `eve project auth-context <project_id>`) for the full rule list with per-rule `target_org`.

To revoke access for a rule: remove it from the manifest (stops new signups under that rule) and explicitly drop existing memberships with `eve org members remove --org <org> --user <user>`. Removing the rule does **not** retroactively delete members that already joined.

### Post-Auth Redirect Allowlist (Custom Domains)

By default the SSO broker only accepts `redirect_to` and CORS origins under the
cluster domain (`EVE_DEFAULT_DOMAIN`, e.g. `eve.example.com`). Apps deployed on
their own domain need their origin opted into the allowlist or the SSO drops
the redirect and lands users on the SSO root.

The resolved allowlist is the union of three sources, returned by
`GET /auth/app-context?project_id=<id>` as `auth.allowed_redirect_origins`:

1. Explicit `x-eve.auth.allowed_redirect_origins` in the manifest (origin-only;
   paths/query/fragments rejected at validate time).
2. Eligible custom domains owned by the project — `custom_domains` rows with
   `environment_id IS NOT NULL` and status in (`dns_verified`,
   `cert_provisioning`, `active`).
3. When `auth.org_access.mode: allowlist`, eligible custom domains owned by
   any project in `allowed_orgs` (one hop).

The SSO broker uses this list for redirect validation in `/callback`, `/login`,
and `/`, and for CORS on `/session` and `/logout`. Custom-domain apps using
`@eve-horizon/auth-react` automatically send `project_id` to `/session` and
`/logout` so CORS can resolve the project-scoped allowlist.

Inspect the resolved list:

```bash
eve project auth-context <project_id>
```

A signed-in user landing on `/` or `/login` with a validated `redirect_to` is
immediately 302'd to the target — the login form is bypassed and there is no
intermediate "you can close this tab" landing page.

The SSO refresh-token cookie (`eve_sso_rt`, HttpOnly) and UX-hint cookie
(`eve_sso`) are set on `.<EVE_DEFAULT_DOMAIN>` with `SameSite=None; Secure`
when `EVE_SSO_SECURE_COOKIES=true`, so the `@eve-horizon/auth-react`
`fetch('/session', { credentials: 'include' })` probe carries them on
cross-site requests from custom-domain apps. Local k3d (`http://*.lvh.me`)
falls back to `SameSite=Lax` because the app and SSO share the `.lvh.me`
parent. Logged at boot as `[eve-sso] Secure cookies: true (SameSite=none)`.

### Branded Auth Email Delivery + SES Suppression

All app-branded auth email (org invites, app invites, app-scoped magic-link login, system-admin Supabase invites) goes through a single `MailerService` on the Eve API. When SMTP is pointed at Amazon SES, the mailer adds a pre-send check against the SES account-level suppression list and emits structured log events so silent drops are observable.

| Behavior | Detail |
| --- | --- |
| Pre-send check | Calls `GetSuppressedDestination` when `GOTRUE_SMTP_HOST` is `*.amazonaws.com` (or `EVE_MAILER_CHECK_SUPPRESSION=true`). Suppressed → `EmailSuppressedError`, no SMTP send. |
| Magic-link drop | `sendEligibleMagicLink` swallows `EmailSuppressedError`, returns `{ sent: true }` (enumeration defense), logs `mail.suppressed_drop kind=magic_link to=... reason=... since=...`. |
| Invite drop | All invite paths (org, app, Supabase admin invites) re-throw — admins see the failure. |
| Fail-open | Non-`NotFoundException` AWS errors (broken IRSA, throttling) log `mailer.suppression_check_failed` and proceed with SMTP. |
| Bounce capture | SES → SNS → `POST /webhooks/ses-feedback` (signature-verified, idempotent) → `email_delivery_events` table. |

Env vars on the API (set per environment, not per project):

| Variable | Default | Purpose |
| --- | --- | --- |
| `EVE_MAILER_CHECK_SUPPRESSION` | `auto` | `auto`/`true`/`false`. |
| `EVE_MAILER_SES_REGION` | parsed from `GOTRUE_SMTP_HOST` | Region for SES SDK calls. |
| `EVE_SES_CONFIGURATION_SET` | — | Adds `X-SES-CONFIGURATION-SET` header so SES routes events to SNS. |
| `EVE_SES_FEEDBACK_TOPIC_ARN` | — | Allow-list for the SES feedback webhook. |

Platform admins (system_admin role) can inspect recent delivery events:

```bash
eve admin email bounces list                            # last 50
eve admin email bounces list --recipient user@x.com     # filter
eve admin email bounces list --event-type Bounce --json # for scripts
```

`eve env diagnose <project> <env>` also surfaces the last 20 events for that env's org members under `recent_email_delivery_events`.

Clearing an account-level SES suppression entry is an ops action; the mailer never deletes suppression entries on its own:

```bash
aws sesv2 delete-suppressed-destination --email-address <addr> --region us-west-2
```

### SSO Self-Signup Domain Restriction

Set `EVE_SIGNUP_ALLOWED_EMAIL_DOMAINS` on the SSO service to gate `/auth/signup` and `/auth/magiclink` to a specific allowlist:

```yaml
# k8s/base/sso-deployment.yaml
- name: EVE_SIGNUP_ALLOWED_EMAIL_DOMAINS
  value: "example.com,example.co.uk"
```

- Comma-separated, case-insensitive on the domain part of the email.
- Unset = all domains allowed (default behavior).
- Disallowed signups receive `422 { "error": "email_domain_not_allowed" }`.
- The hosted login page renders a hint on the Sign Up tab listing the allowed domains.
- Invite-based provisioning (org-scoped invites, NIP-98, SSH) is not gated by this setting; only self-signup endpoints are.

---

## App Auth SDKs

For adding Eve SSO login to deployed apps, use the shared auth packages:

- **`@eve-horizon/auth`** -- Backend middleware (Express). **Recommended**: `eveAuth()` (unified, handles both user and agent tokens, attaches `req.eveIdentity` with `isAgent` boolean) + `eveIdentityGuard()`. Also provides `eveUserAuth()` (user-only), `eveAuthGuard()`, `eveAuthConfig()`, `eveAuthMe()`, `eveAuthMiddleware()` (agent-only, blocking), and lower-level `verifyEveToken()`/`verifyEveTokenRemote()`. Agent job tokens include `agent_slug` and stable `email` (`{agent_slug}@eve.agent`) claims for agent identity, and may include an optional `scope` claim for orgfs/orgdocs/envdb/cloud_fs resource narrowing.
- **`@eve-horizon/auth-react`** -- Frontend SDK (React). Provides `<EveAuthProvider>` (with optional `projectId` prop for project role resolution), `useEveAuth()` hook (with `orgs`, `activeOrg`, `switchOrg`), `<EveLoginGate>`, `<EveLoginForm>`, and `createEveClient()` fetch wrapper. Also exposes `getStoredToken()`/`storeToken()`/`clearToken()` for direct `sessionStorage` access.

### Auto-Injected Environment Variables

Apps deployed to Eve receive these env vars automatically from the platform deployer:

| Variable | Description |
|----------|-------------|
| `EVE_API_URL` | Internal API URL (server-to-server) |
| `EVE_PUBLIC_API_URL` | Public-facing API URL (optional) |
| `EVE_SSO_URL` | SSO broker URL |
| `EVE_ORG_ID` | Organization ID |
| `EVE_PROJECT_ID` | Project ID |
| `EVE_ENV_NAME` | Environment name |
| `EVE_SERVICE_TOKEN` | 90-day RS256 JWT (`type: service`) for server-to-server calls back into the Eve API |

`EVE_SERVICE_TOKEN` is auto-minted per service by the deployer on every deploy. Its permissions come from `x-eve.permissions` in the manifest (read-only by default). See [Service Tokens](#service-tokens-deployed-services) below and `references/manifest.md` for the manifest schema.

The backend middleware reads these automatically. The frontend provider discovers auth config via the backend's `/auth/config` endpoint. Use `${SSO_URL}` in manifest `environment:` blocks for interpolation.

### Token Flow

1. `EveAuthProvider` checks `sessionStorage` for a cached token.
2. If none, probes the SSO broker `/session` endpoint (root-domain cookie).
3. If an SSO session exists, gets a fresh RS256 token and caches it.
4. If no SSO session, shows the login form (SSO redirect or token paste).
5. All API requests include `Authorization: Bearer <token>`.

For SSE endpoints, the middleware also accepts `?token=` query parameter.

For development or headless environments, use `eve auth token` to obtain a token for pasting.

**Token staleness**: The `orgs` claim reflects membership at token mint time. With the default 1-day TTL, membership changes can take up to 24h to reflect. Use `strategy: 'remote'` for immediate membership checks.

### Auth-React Org Awareness

`@eve-horizon/auth-react` exposes org membership and switching via the `useEveAuth()` hook:

```typescript
const { orgs, activeOrg, switchOrg } = useEveAuth();
// orgs: EveAuthOrg[]  — all orgs the user belongs to
// activeOrg: EveAuthOrg | null  — currently selected org
// switchOrg(orgId: string): void  — switch active org

type EveAuthOrg = {
  id: string;
  role: 'owner' | 'admin' | 'member';
};
```

- The backend already returns memberships in the token/session; the SDK now exposes them.
- Active org persists in `localStorage` across sessions.
- Backward compatible: `user.orgId` still works for single-org apps.

### Project Role Resolution

The `/auth/me` endpoint accepts an `X-Eve-Project-Id` header. When present, it resolves the user's project membership and returns `project_role` (`'owner' | 'admin' | 'member' | null`).

- **Backend**: Use `eveAuthMe({ projectHeader: 'x-eve-project-id' })` to forward the header and include project role in the response.
- **Frontend**: Pass `projectId` to `<EveAuthProvider>` to send the header automatically. Access via `user.projectRole`.
- **Custom roles**: Map `project_role` to app-specific roles (e.g. `editor/viewer`) in backend middleware.

See `references/auth-sdk.md` for full details.

---

## Harness Credentials (BYOK Model)

Eve does not manage inference endpoints or proxy LLM traffic. Apps and agents bring their own API keys (BYOK) via Eve secrets. Harnesses call upstream providers directly using resolved secrets — no platform-managed models, no managed catalog, no inference proxy.

### Required Secrets by Harness

| Harness | Secret | Optional |
|---------|--------|----------|
| mclaude / claude | `CLAUDE_CODE_OAUTH_TOKEN` setup-token or `ANTHROPIC_API_KEY` | `ANTHROPIC_BASE_URL` (for custom endpoints) |
| zai | `Z_AI_API_KEY` | `Z_AI_BASE_URL` |
| code / codex | `OPENAI_API_KEY` or `CODEX_AUTH_JSON_B64` | `OPENAI_BASE_URL` |
| gemini | `GEMINI_API_KEY` or `GOOGLE_API_KEY` | |
| zai | `Z_AI_API_KEY` | |

For private repos: `GITHUB_TOKEN` (HTTPS) or `ssh_key` (SSH via `GIT_SSH_COMMAND`).

### Self-Hosted Models (RunPod, vLLM, LM Studio, etc.)

Users who run their own models store the endpoint URL and API key as Eve secrets. The harness or app uses standard env vars (`OPENAI_BASE_URL`, `OPENAI_API_KEY`) — Eve is not involved in the lifecycle of the GPU endpoint.

For Tailscale-only endpoints, use private endpoints (platform networking primitive) to make them reachable from cluster pods.

### How It Works

```
Job created with harness=mclaude
  -> Runtime resolves project/org/user/system secrets
  -> Claude selector chooses key/scope/token class and materializes setup-token if needed
  -> Harness adapter injects sanitized env/config into the harness process
  -> Harness calls provider API directly
  -> Eve never touches inference traffic
```

---

## Per-Org OAuth Credentials

Orgs bring their own OAuth app credentials for external providers (Google Drive, Slack) instead of relying on cluster-level defaults. Credentials are stored in the `oauth_app_configs` table (one config per org per provider).

### Setup Flow

1. Admin creates an OAuth app in the provider's console (GCP for Google Drive, api.slack.com for Slack).
2. Admin registers the credentials with Eve:

```bash
eve integrations configure google-drive \
  --client-id "xxx.apps.googleusercontent.com" \
  --client-secret "GOCSPX-xxx" \
  --label "Acme Corp Google Drive"

eve integrations configure slack \
  --client-id "12345.67890" \
  --client-secret "abc123" \
  --signing-secret "def456" \
  --app-id "A0123ABC"
```

3. Initiate the OAuth connection: `eve integrations connect google-drive`

### How It Works

- A single callback URL per provider handles all orgs. Org routing uses the `state` parameter (signed JWT).
- Token refresh uses the org's own `client_id` + `client_secret` from `oauth_app_configs`.
- Slack webhook verification uses the org's own `signing_secret` (resolved via org-scoped webhook URL or `team_id` lookup).
- No cluster-level `EVE_GOOGLE_CLIENT_ID`, `EVE_SLACK_CLIENT_ID`, etc. required.

### CLI

```bash
eve integrations setup-info google-drive   # Shows redirect URI, required scopes
eve integrations config google-drive       # View current config (secrets redacted)
eve integrations unconfigure google-drive  # Remove config
```

### API

```
POST   /orgs/:org_id/integrations/providers/:provider/config   # Upsert credentials
GET    /orgs/:org_id/integrations/providers/:provider/config    # View (redacted)
DELETE /orgs/:org_id/integrations/providers/:provider/config    # Remove
GET    /orgs/:org_id/integrations/providers/:provider/setup-info
```

Permission: `integrations:write` for create/update/delete, `integrations:read` for view.

---

## Service Tokens (Deployed Services)

Every deployed service automatically gets `EVE_SERVICE_TOKEN` injected as a platform env var. This is the canonical way for an app to call the Eve API back from inside its own runtime — no manual secret setup, no `eve auth login` from inside a container.

### Token Shape

- RS256 JWT, `type: service`, `sub: service:<service-name>`
- Claims: `org_id`, `project_id`, `env_name`, `service_name`, `permissions`
- TTL: 90 days, refreshed on every deploy
- Verified by the same JWKS as user/job tokens — `@eve-horizon/auth` middleware accepts it transparently

### Read-Only by Default

Service tokens carry **read-only permissions** unless the manifest explicitly grants more. The platform-side defaults are:

```
projects:read, jobs:read, threads:read, envs:read,
secrets:read, builds:read, pipelines:read, agents:read, events:read
```

Apps that need to write must opt in via `x-eve.permissions` on the service in `.eve/manifest.yaml`:

```yaml
services:
  api:
    x-eve:
      permissions: [jobs:write, events:write, threads:write]
```

Declared permissions are **merged** with the read-only defaults — list only the extra scopes. Redeploy to mint a new token with the updated scopes. See `references/manifest.md` for the full manifest schema.

This is a security-relevant default change: an app that previously assumed write access from the platform-injected token will now get `403 Missing required permission` until it declares the scope it needs.

### Using The Token

```bash
curl -X POST "$EVE_API_URL/projects/$EVE_PROJECT_ID/jobs" \
  -H "Authorization: Bearer $EVE_SERVICE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{ "description": "from app", "env_name": "'"$EVE_ENV_NAME"'" }'
```

`EVE_INTERNAL_API_KEY` must be configured on the platform for token minting to succeed. If minting fails the deployer logs a warning and `EVE_SERVICE_TOKEN` is empty — the deploy still proceeds.

---

## Service Principals + Token Minting

App backends authenticate as services via scoped tokens:

```bash
eve auth create-service-account --name "pm-app-backend" --org org_xxx \
  --scopes "jobs:create,jobs:read,projects:read"
eve auth list-service-accounts --org org_xxx
eve auth revoke-service-account --name pm-app-backend --org org_xxx
```

API: `POST /orgs/:id/service-principals`, `POST .../service-principals/:sp_id/tokens` (mint), `DELETE .../tokens/:tok_id` (revoke).

Admins can also mint tokens without SSH login (useful for bots):

```bash
eve auth mint --email app-bot@example.com --org org_xxx --ttl 90
```

Creates user and membership if needed. TTL capped at server's `EVE_AUTH_TOKEN_TTL_DAYS`.
