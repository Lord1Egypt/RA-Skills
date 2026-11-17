# Webstudio Database & Stack

The deployment is a Docker Compose stack. Everything (elements, styles, pages,
assets) is ultimately stored in Postgres; the build is a JSON `Build` row that the
builder edits in the UI and that we edit directly via SQL. This file documents the
standard self-hosted Webstudio stack.

## Services

| Service | Port | Role |
|---------|------|------|
| `app` | :3000 | Builder UI |
| `db` | (internal) | Postgres 15 |
| `postgrest` | (internal :3000) | REST API over Postgres |
| `minio` | :9000/:9001 | S3-compatible asset storage |
| `publisher` | :4000 build / :4001 -> :80 site proxy | Build API + serves published sites |
| `migrate`, `db-setup`, `minio-init` | one-shot | Schema/perms/bucket init |

```bash
docker compose ps          # health check
docker compose logs -f app # builder logs
docker compose logs publisher | tail   # publish confirmations
```

## Accessing the database

For project editing, use official Webstudio CLI/MCP first. It applies native transactions,
validation, versioning, and project authorization.

For deployment maintenance, use a deployment-specific restricted role. Keep its credential in the
approved secret manager and inject it without placing the value in command arguments or output.

If your deployment renamed services or the DB, adjust the `docker compose exec`
service name / `-d` db name to match. The DB user is typically `postgres`.

The community stack's Builder may depend on `anon`. Do not revoke it until the authenticated
`POSTGREST_API_KEY` migration in `postgrest-auth.md` passes. Internal anonymous PostgREST and direct
host SQL are deployment-wide admin surfaces, not project-scoped credentials.

Direct SQL is an advanced maintenance fallback. Use a restricted maintenance role rather than
the `postgres` superuser for routine edits. Keep the database private to the deployment network.

## Build table schema (the core)

The `Build` table holds the entire site as JSON text columns. Columns:

- `id`, `projectId`, `createdAt`, `updatedAt`, `version`
- `pages` - page tree `{homePageId, rootFolderId, pages:[{id,name,rootInstanceId,path,meta}], folders}`
- `instances` - the element tree
- `styleSources` - `{type:'local'|'token', id, name?}`
- `styles` - `{breakpointId, styleSourceId, property, value}`
- `styleSourceSelections` - `{instanceId, values:['<iid>:ws:style']}` (binds styles to element)
- `props` - element props `{id:'<iid>:<name>', instanceId, name, type, value}`
- `breakpoints` - `{id, label, maxWidth?}`
- `dataSources`, `resources`, `marketplaceProduct`, `projectSettings` - advanced, usually `[]`/defaults
- `deployment` - NULL = draft; set = published build
- `publishStatus` - `PENDING` | `PUBLISHED` | `FAILED`
- `isCleaned`

A project can have several historical or concurrent rows. Resolve the target project first, then
select one exact draft within that project. Confirm the build ID and project ID before proceeding.

## Other tables

- `Project` - `{id, title, domain, userId, isDeleted, workspaceId, ...}`
- `Asset` - `{id, projectId, name, filename, folderId}` (metadata; bytes live in MinIO)
- `AssetFileMetadata` - `{projectId, assetId, revision, document(jsonb)}`
- `Domain` / `ProjectDomain` - custom domains and DNS records (`txtRecord`, `cname`)
- `AuthorizationToken` - `{token, projectId, name, relation, canClone, canCopy, canPublish, canUseApi}`
- `User`, `Workspace`, `WorkspaceMember` - auth/multi-tenancy
- `File` - `{name, format, size, status(UploadStatus), meta}` (uploads)

## Loading and committing a build safely

Direct database edits can corrupt the authoritative site state. Before a write, get explicit
approval, back up the exact row, and record its project ID, build ID, and concurrency value such
as `updatedAt` or `version`.

Do not construct SQL by interpolating JSON, write site data to a predictable `/tmp` path, or update
every draft. Use a PostgreSQL client that actually exists in the deployment and supports bound
parameters. Inspect the running schema first: current community builds store Webstudio namespaces
as `text`, not `jsonb`.

The required transaction contract is:

1. Begin a transaction and select one row by both build ID and project ID with
   `deployment is null` and `for update`.
2. Require its `version` to equal the version captured with the backup.
3. Load and preserve all current namespaces: `pages`, `instances`, `styles`, `styleSources`,
   `styleSourceSelections`, `props`, `breakpoints`, `dataSources`, `resources`,
   `marketplaceProduct`, and `projectSettings`.
4. Validate the mutated Webstudio structures. Prefer the official CLI/MCP schemas rather than
   hand-rolled JSON checks.
5. Update only that row with bound values. Set `version` to the prior version plus one, set a new
   unique `lastTransactionId`, and set `updatedAt` to the current time. Webstudio's native patch
   path performs all three; omitting them can desynchronize the editor.
6. Keep the original `projectId`, draft status, and untouched namespaces unchanged.
7. Require exactly one returned row. Roll back on zero or multiple rows, validation failure, or a
   version mismatch.
8. Re-read the row, compare the intended namespaces, and keep the mode-0600 backup until canvas
   and live-site verification pass.

The actual host may use `docker compose exec db psql` as a break-glass transport because Docker
access is already deployment-admin authority. That does not justify using `postgres` routinely or
embedding arbitrary site JSON in shell/SQL strings.

After commit, re-read the same build ID and verify only the intended values changed. Keep the
backup until canvas and published-site verification pass.

## Finding things by structure (not hardcoded ids)

Instance ids are random and change between builds. Locate elements by walking the
tree, not by remembered ids:

```js
const byId = {}; for (const i of inst) byId[i.id] = i
const page = pages.pages.find(p => p.name === 'Home')
const root = byId[page.rootInstanceId]
function walk(id, fn) {
  const i = byId[id]; if (!i) return
  fn(i)
  for (const c of i.children||[]) if (c.type==='id') walk(c.value, fn)
}
```

Match on tag + structure (e.g. a `div` whose children are all `a` = a card grid),
not on remembered ids.
