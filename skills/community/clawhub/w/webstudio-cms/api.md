# Webstudio API Surface

This documents the programmatic surface of self-hosted Webstudio: what can be reached, how the
authorization layers differ, and what the underlying data model permits. Deployment facts are
verified against the live community stack; authenticated alternatives are verified against the
running Builder revision's source and Webstudio's versioned CLI/MCP documentation.

## Access layers (verified against a live self-hosted instance)

| Layer | What it is | How to reach it |
|-------|-----------|-----------------|
| **Official CLI/MCP** | Project-scoped native Webstudio API | Build-access share link; preferred for agents |
| **Direct SQL** | Postgres 15 | Authorized host/maintenance role (advanced fallback) |
| **PostgREST** | REST API over the public schema | `http://postgrest:3000/<table>` (internal only) |
| **Builder** | The Webstudio app (UI + tRPC) | `http://localhost:3000` (this is the Remix app, NOT postgrest) |
| **Publisher** | Build API + site proxy | `:4000` build API / `:4001` -> `:80` sites |
| **MinIO** | S3-compatible asset storage | `:9000` (S3 API), `:9001` (console) |

> Gotcha (verified): on the host, `:3000` is the Remix **builder app**, not postgrest.
> PostgREST is reachable only from inside the compose network (e.g. from the app
> container) at `http://postgrest:3000`.

## PostgREST capability and security boundary

The community self-host compose deliberately grants the `anon` database role full table and
sequence access; state-changing functions are also executable through the resulting role/public
privileges. The Builder uses that surface through an internal-only PostgREST service;
in the default compose profile its `POSTGREST_API_KEY` is empty. Removing those grants without first
configuring an authenticated Builder role breaks normal Webstudio database operations.

This preserves the entire PostgREST surface, including CRUD and these RPCs:
`swap_asset_file`, `delete_stale_asset_file_metadata`, `restore_development_build`,
`replace_asset_file_metadata`, `clone_project`, `create_production_build`,
`delete_asset_file_metadata_if_matches`, `database_cleanup`.

Choose one explicit profile:

- **Compatibility:** retain the community grants, keep PostgREST un-published on a private Docker
  network, and treat host/Docker access as deployment-admin authorization. Internal anonymous calls
  remain possible but are never a public or project-scoped admin API.
- **Hardened:** configure the Builder's supported `POSTGREST_API_KEY` JWT, grant its database role
  the same required capabilities, validate the Builder, then revoke `anon`. See
  `postgrest-auth.md` for the migration order and acceptance checks.

`postgrest-auth.md` includes the bounded operating rules for the default profile and the staged,
rollbackable path for attempting the authenticated profile. The default is live-validated; the
hardened profile is source-validated until it passes a deployment-specific disposable-stack test.

For normal agent work, use official Webstudio CLI/MCP with a project-scoped Build-access share
link. A Webstudio `AuthorizationToken` authorizes Builder operations; it is not automatically a
PostgREST JWT and must not be presented as one.

## Database tables (public schema)

- `Build` - the site build (JSON-encoded text namespaces; see `database.md`)
- `Project` - `{id, title, domain, userId, isDeleted, workspaceId, tags, ...}`
- `Asset`, `AssetFileMetadata`, `AssetFolder` - asset metadata (bytes in MinIO)
- `Domain`, `ProjectDomain` - custom domains + DNS records
- `AuthorizationToken` - `{token, projectId, name, relation, canClone, canCopy, canPublish, canUseApi}`
- `User`, `Workspace`, `WorkspaceMember` - auth / multi-tenancy
- `File` - upload records `{name, format, size, meta, status(UploadStatus)}`
- `Notification`, `TransactionLog`, `ClientReferences`, `Product` - peripheral

See `database.md` for the Build schema in full and the load/commit pattern.

## Environment and configuration

Non-secret behavior commonly includes asset limits, publisher URLs, image references, plan
selection, and feature flags. Pin image references by digest for production deployments.

Authentication, database, PostgREST, object-storage, publisher, OAuth, and DNS-provider settings
include secret values. Keep those values in the deployment's approved secret manager. Never read
or print them during discovery, copy them into instructions, or commit them. Document only the
names required by the deployment. See `security.md` before using any credential.

## Authentication

- **Builder UI:** "Login with Secret" using `AUTH_SECRET`, or OAuth if configured.
- **Official CLI/MCP:** a project-scoped Build-access share link. Treat the link as a credential.
- **PostgREST:** either internal `anon` compatibility mode or a JWT role through
  `POSTGREST_API_KEY`; see `postgrest-auth.md`.
- **Publisher:** the community publisher's inbound `/publish` and `/unpublish` routes do not check
  `TRPC_SERVER_API_TOKEN`. That token authenticates publisher callbacks to the Builder. Keep the
  control port internal or isolate `app` and `publisher` on a dedicated control network.
- **AuthorizationToken:** per-project tokens with scoped permissions
  (`canClone`, `canCopy`, `canPublish`, `canUseApi`). Use least-privilege.

For browser automation, prefer an existing authenticated session or a dedicated automation
identity. If the deployment requires `AUTH_SECRET`, obtain explicit approval and use an approved
ephemeral secret injection. Never discover it from `.env`. See `verification.md`.

## Working against the build (not the UI)

Prefer official CLI/MCP or authenticated Builder APIs. The official CLI can inspect and edit the
native project model, publish/unpublish, manage domains, inspect permissions, and run verification.
Direct SQL is an advanced fallback for authorized self-hosted maintenance. Its safe workflow is:

1. Load the draft build columns (see `database.md`).
2. Mutate instances/styles/props/pages.
3. Write the exact row through a transaction-protected, exact-version update; preserve every
   namespace and advance `version`, `lastTransactionId`, and `updatedAt`.
4. Publish through an authenticated or network-isolated admin boundary after approval.
5. Verify on the canvas / live site (see `verification.md`).

## tRPC endpoints (verified)

The builder app exposes tRPC (the UI calls these). **Auth is required** - verified
that `/api/trpc/health` returns `403 Forbidden` without a session, and the editor
URL (`p-<id>.localhost:3000/`) also returns `403` unauthenticated. So you must be
logged in to call tRPC.

In practice you rarely need to call tRPC directly. Use authenticated Builder, CLI, or scoped API
paths first; use the safe direct-database fallback only when needed. If you need a tRPC call,
run it inside the browser page after login so the auth cookies and CSRF token are
attached (see `verification.md`).
