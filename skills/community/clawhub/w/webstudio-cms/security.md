# Webstudio Security Boundaries

Use this file before any authenticated, state-changing, or production operation.

## Authorization and scope

- Work only on a Webstudio deployment the operator owns or is authorized to administer.
- Confirm the deployment, project ID, and intended action before reading or changing state.
- Treat investigation and planning as read-only. Database writes, asset deletion, domain changes,
  user or token changes, and publishing require explicit user approval.
- Never turn an internal-only endpoint into a public endpoint to make automation easier.

## Credentials

`AUTH_SECRET`, OAuth client secrets, database credentials, PostgREST JWT secrets, object-storage
keys, publisher tokens, and DNS-provider tokens are sensitive credentials.

- Do not search for or read a deployment's `.env` file merely because it exists.
- Do not request secret values in chat or place them in prompts, shell arguments, source files,
  screenshots, logs, or command output.
- Prefer an already-authenticated browser session, a dedicated low-privilege automation identity,
  or a project-scoped token.
- If `AUTH_SECRET` is the only supported login method, obtain explicit approval for that login and
  receive the value through the operator's approved secret manager or ephemeral environment
  injection. The automation may read the injected process variable but must never reveal it.
- Remove the injected value when the operation ends. Rotate any credential that may have leaked.

Secret names may be documented because operators need to configure deployments. Secret values
must remain in a secret manager or deployment mechanism with restrictive access.

## Network exposure

- Publish only the Builder and intended site-serving ports. Keep Postgres, PostgREST, and the
  publisher control port private.
- MinIO's S3 API may be exposed only when clients require it; keep its admin console private,
  replace default credentials, and use TLS at the boundary.
- A Docker `internal` network is preferred for database/control traffic. Do not attach unrelated
  workloads to the trusted application network.
- Treat Docker daemon access as root-equivalent deployment administration.

## PostgREST and database access

The community self-host stack depends on broad `anon` privileges unless the Builder is configured
with `POSTGREST_API_KEY`. Do not revoke those grants in isolation: that removes Webstudio
functionality. Choose one documented profile from `postgrest-auth.md`.

- In compatibility mode, keep PostgREST private and treat Docker/host access as deployment-admin
  access. Never expose the service or present internal anonymous calls as a public admin API.
- In hardened mode, move the Builder to a dedicated JWT database role, validate every required
  Builder operation, update `db-setup`, and only then revoke `anon`.
- For project-scoped automation, prefer official CLI/MCP with a Build-access share link. Database
  role grants are not project-scoped unless the database enforces that scope.
- For the advanced direct-database fallback, use a restricted maintenance role, bound parameters,
  one exact project/build target, a transaction, optimistic concurrency, a backup, and an exact
  affected-row check. Do not connect as the `postgres` superuser for routine edits.

The exact role and grants depend on the deployment schema. Inspect current grants before changing
them, preserve required application access, and test the Builder after hardening.

## Publishing and destructive actions

- Publishing is an external production change. Show the operator the project, draft build, domain,
  and build mode, then obtain explicit confirmation immediately before starting it.
- Prefer the authenticated Builder or official CLI/MCP with a scoped token. The community
  publisher's control API has no inbound credential check. Preserve it behind a dedicated private
  app-to-publisher network; never publish its control port. Direct internal calls are break-glass
  deployment administration and require the same explicit approval as a database write.
- Back up the exact draft before publishing. Confirm the returned build ID and final status.
- Deletion, restore, database cleanup, token creation, and DNS changes require separate approval.

## Supply-chain controls

- Pin CLI packages to a reviewed version, for example `webstudio@<approved-version>`.
- Pin container images by immutable digest in production.
- Review version changes before updating. Do not use `latest` in an unattended admin workflow.
- Record the approved versions with the deployment so later runs reuse them.

## Reporting

Report which authenticated boundary was used, which project/build changed, whether a backup was
created, and the verification result. Never include credential values or full authorization tokens.
