# CLI: Org + Project Setup

## Use When
- You need to bootstrap an org or project and synchronize a manifest.
- You need repo-scoped document workflows or filesystem sync setup.
- You need to resolve resource URIs against org documents or workspace attachments.

## Load Next
- `references/manifest.md` for schema and manifest composition.
- `references/overview.md` for platform identifiers and architecture.
- `references/cli-pipelines.md` for pipeline/workflow run prerequisites.

## Ask If Missing
- Confirm org slug, project slug, and whether org/project already exists.
- Confirm repository URL, branch, and whether bootstrap should create initial environments.
- Confirm whether doc sync requires pull-only or two-way behavior.

## Init

```bash
eve init [directory] [--template <url>] [--branch <branch>] [--skip-skills]
```

Initialize an Eve project. Clones from template if provided, strips `.git`, runs `eve skills install` from `skills.txt` unless `--skip-skills` is set.

## Org

```bash
eve org list [--include-deleted] [--name <filter>]
eve org ensure "my-org" --slug myorg                    # Create or return existing
eve org get <org_id>                                    # Show org details
eve org update <org_id>                                 # Modify org
  [--name "New Name"] [--deleted true/false]
  [--default-agent mission-control]
  [--billing-config '{"..."}']
eve org delete <org_id> [--hard] [--force]               # Delete org (cascades through projects)
eve org spend <org_id>                                  # View org spend
  [--since 2026-01-01] [--until 2026-02-01] [--currency usd]

# Membership
eve org members --org org_xxx                           # List members
eve org members add user@example.com --role admin --org org_xxx
eve org members remove user_abc --org org_xxx
```

**URL impact:** The org `--slug` directly forms deployment URLs and K8s namespaces:
- URL: `{service}.{orgSlug}-{projectSlug}-{env}.{domain}`
- Namespace: `eve-{orgSlug}-{projectSlug}-{env}`
- `${ORG_SLUG}` is available for interpolation in manifest values (see `references/manifest.md`)

Slugs are immutable after creation. Choose short, meaningful values.

Notes on `org delete`:
- Default: soft-delete (sets `deleted_at`, recoverable with `update --deleted=false`).
- `--hard`: cascades hard-delete through all projects + environments (irreversible, requires admin).
- `--force`: continue on partial failures (e.g., K8s unreachable).

## Project

```bash
eve project list [--all] [--include-deleted] [--name <filter>]
eve project ensure --name "My Project" --slug myproj \
  [--repo-url https://github.com/org/repo] [--branch main]  # --repo is an alias for --repo-url
  [--org org_xxx] [--force]
eve project get <project_id>
eve project update <project_id>
  [--name "New Name"] [--repo-url <url>] [--branch <branch>]
  [--deleted true/false]
eve project show <project_id>                           # Alias for get
eve project delete <project_id> [--hard] [--force]      # Delete project (cascades to envs/jobs/builds)
eve project sync [--dir <path>]                         # Sync manifest to API
  [--validate-secrets] [--strict] [--project <id>]
eve project spend <project_id>                          # View project spend
  [--since 2026-01-01] [--until 2026-02-01]
  [--currency usd] [--limit 100]

# Membership
eve project members --project proj_xxx
eve project members add user@example.com --role admin --project proj_xxx
eve project members remove user_abc --project proj_xxx

# Bootstrap (create project + environments in one call)
eve project bootstrap --name my-app --repo-url https://github.com/org/repo \
  --environments staging,production [--branch main] [--slug <slug>] \
  [--template <name>] [--packs pack1,pack2]

# Status (cross-profile deployment overview)
eve project status [--profile <name>] [--env <name>] [--json]

# Auth context (resolved SSO redirect allowlist + domain_signup for a project)
eve project auth-context <project_id> [--json]
```

`eve project auth-context` prints the resolved app auth context: login method,
self_signup/invite_requires_password flags, org access mode, the allowed
redirect-origin allowlist (manifest ∪ project custom domains ∪ cross-org custom
domains), and — for callers with project-admin rights — the `domain_signup`
rule list (one line per rule, `<domain> -> <target_org> (<role>)`, in
declaration order — first-match wins at sign-in time). The CLI tries the
authenticated admin reveal first (`GET /auth/app-context/admin`) and falls
back to the public `GET /auth/app-context`; non-admins see `Domain signup:
enabled (details hidden)` instead of the rule list.

`eve project status` shows a unified deployment overview across all configured profiles. For each profile it reports:

- **Project** -- ID and name
- **Environments** -- name, type (`persistent`/`temporary`), status (`active`/`suspended`)
- **Revision** -- current release git SHA (short), version/tag, and deploy age (e.g. `3h ago`)
- **Services** -- per-component pod readiness (`ready`/`not-ready`/`completed`), with inferred ingress URLs and any custom ingress alias URLs

Flags:
- `--profile <name>` -- restrict output to a single profile (default: all profiles)
- `--env <name>` -- filter to a specific environment within each profile
- `--json` -- machine-readable output with full `{ profiles: [...] }` envelope

The command aggregates data from the project, releases, environments, and pod diagnostics APIs. Suspended environments are listed but skip service queries. Service URLs are inferred from the namespace and cluster domain (e.g. `https://{component}.{orgSlug}-{projectSlug}-{env}.{domain}`).

Notes:
- `project delete` default: soft-delete (sets `deleted_at`, recoverable with `update --deleted=false`). `--hard`: physically removes all data including environments, jobs, builds, and releases (irreversible, requires admin). `--force`: continue on partial failures.
- `project ensure` supports repo-less creation for early bootstrap; omit `--repo-url` to reserve slug/id first, then set repo later with `project ensure --repo-url ...` or `project update --repo-url ...`.
- `repo_url` accepts HTTPS, SSH (`git@host:org/repo.git`), or `file://` (local/dev only).
- `project sync` reads the manifest from `--dir` (or cwd) and pushes it to the API.
- `project auth-context` prints the resolved SSO allowlist (manifest origins ∪ project's own eligible custom domains ∪ cross-org custom domains via `org_access.allowed_orgs`). Use it to verify what redirect targets and CORS origins SSO will accept for an app. See `secrets-auth.md` and `manifest.md` for the full model.

## Docs (Org Documents)

Org docs are versioned, queryable documents stored at canonical paths. Documents support lifecycle metadata: review schedules, expiry, and staleness tracking.

```bash
eve docs write --org org_xxx --path /pm/features/FEAT-123.md --stdin
  [--review-in 30d] [--expires-in 90d]                    # Lifecycle scheduling
  [--lifecycle-status active|archived|draft]               # Lifecycle status
eve docs create ...                                        # Alias for write
eve docs read --org org_xxx --path /pm/features/FEAT-123.md
eve docs read --org org_xxx --path /pm/features/FEAT-123.md --version 3
eve docs show --org org_xxx --path /pm/features/FEAT-123.md --verbose
eve docs versions --org org_xxx --path /pm/features/FEAT-123.md
eve docs query --org org_xxx --path-prefix /pm/features/ \
  --where 'metadata.feature_status in draft,review' --sort updated_at:desc
eve docs search --org org_xxx --query "risk score"
  [--mode text|semantic|hybrid]                            # Search mode (default: text)
eve docs stale --org org_xxx [--overdue-by 7d]             # Find docs past review date
  [--prefix /agents/] [--limit 50]
eve docs review --org org_xxx --path /pm/features/FEAT-123.md \
  --next-review 30d                                        # Mark reviewed, set next review
eve docs delete --org org_xxx --path /pm/features/FEAT-123.md

eve docs patch --org org_xxx --path /wiki/state.yaml \
  --replace "health: green" "health: amber"                  # Search and replace
eve docs patch --org org_xxx --path /wiki/state.yaml \
  --append "## New Section"                                  # Append to end
eve docs patch --org org_xxx --path /wiki/state.yaml \
  --insert-after "signals:" $'\n  - paging active'           # Insert after anchor
eve docs patch --org org_xxx --path /wiki/state.yaml \
  --operations '[{"op":"replace","search":"old","replace":"new"}]'  # JSON ops

eve docs diff --org org_xxx --path /wiki/state.yaml           # Latest vs previous
eve docs diff --org org_xxx --path /wiki/state.yaml --from 1 --to 5  # Specific versions
eve docs diff --org org_xxx --path /wiki/state.yaml --unified  # Unified format

eve docs list --org org_xxx --path /wiki --tree                # Human-readable hierarchy
eve docs list --org org_xxx --path /wiki --tree --json         # Nested JSON tree

eve docs search --org org_xxx --query "error rate" \
  --path /world-model --context 3                             # Path prefix + context lines

eve docs write-dir --org org_xxx --source ./wiki-pages \
  --path-prefix /operating-model                              # Bulk write from directory
eve docs sync --org org_xxx --source ./wiki \
  --path-prefix /operating-model --dry-run --delete           # Safe sync with dry-run
eve docs watch --org org_xxx --path /world-model --since now   # Stream doc change events
```

Notes:
- `--review-in` and `--review-due` are mutually exclusive (relative duration vs ISO timestamp).
- `--expires-in` and `--expires-at` are mutually exclusive.
- `stale` returns documents whose `review_due` has passed. Use `--overdue-by` to filter by staleness threshold.
- `search --mode semantic` uses vector similarity; `hybrid` combines text + semantic.
- `patch` supports three operation types: `replace` (search+replace), `append`, `insert_after`. Mutually exclusive with `--operations` JSON.
- `diff` defaults to latest vs previous version. Use `--from`/`--to` for specific versions.
- `list --tree` renders a hierarchical directory tree instead of flat paths.
- `search --path` filters results to a prefix. `--context N` includes N surrounding lines from each matched document.
- `write-dir` maps local files to doc paths under `--path-prefix`.
- `sync --dry-run` reports changes without mutating. `--delete` removes remote docs not found locally (never default).
- `watch` polls org events for `system.doc.created|updated|deleted`, filtered by `--path` prefix. Outputs NDJSON.

## FS Sync (Org Filesystem)

Org-scoped filesystem sync control plane (device enrollment, links, stream, conflicts).

```bash
eve fs sync init --org org_xxx --local ~/Eve/acme --mode two-way
  [--include "*.md,docs/**"] [--exclude "node_modules/**"]
  [--remote-path /subdir]                                    # Remote root (default: /)
  [--device-name "my-laptop"]                                # Device label (default: hostname)
eve fs sync status --org org_xxx
eve fs sync logs --org org_xxx --follow

eve fs sync pause --org org_xxx [--link <link_id>]
eve fs sync resume --org org_xxx [--link <link_id>]
eve fs sync disconnect --org org_xxx [--link <link_id>]
eve fs sync mode --org org_xxx --set pull-only [--link <link_id>]

eve fs sync conflicts --org org_xxx [--open-only]
eve fs sync resolve --org org_xxx --conflict fscf_xxx --strategy pick-remote
eve fs sync doctor --org org_xxx
```

Notes:
- Sync modes map to API values: `two-way -> two_way`, `push-only -> push_only`, `pull-only -> pull_only`.
- `init` enrolls a device and creates a sync link in one step. Use `--include`/`--exclude` for glob-based filtering.
- `logs --follow` streams SSE events (`fs_event`, `fs_checkpoint`) and resumes with `--after`.
- If `--link` is omitted for lifecycle commands, CLI targets the most recently updated link in the org.

### FS Share Tokens

Create time-limited, revocable share URLs for any org filesystem file. The URL redirects (302) to a presigned MinIO/S3 download URL — no Eve auth required on access.

```bash
# Create a share token (7d TTL by default)
eve fs share /docs/report.md --org org_xxx [--expires 24h] [--label "Q1 report"]
# → Share URL: http://api.../orgs/mto/fs/public/docs/report.md?token=share_xxx

# List active (non-revoked, non-expired) shares
eve fs shares --org org_xxx [--json]

# Revoke a share token
eve fs revoke share_xxx --org org_xxx
```

Expiry formats: `7d`, `24h`, `30m`, `3600s`.

### FS Public Paths

Register path prefixes for permanent, tokenless public access. All files under the prefix are accessible without any authentication.

```bash
# Register a prefix as public
eve fs publish /assets/ --org org_xxx [--label "Static assets"]

# List registered public path prefixes
eve fs public-paths --org org_xxx [--json]

# Remove a public path registration
# (use the API: DELETE /orgs/{org}/fs/public-paths/{id})
```

Public path access URL pattern: `GET /orgs/{slug}/fs/public/{path}` — no token or auth header required.

## Resources (Resolver)

Resource URIs unify org docs and job attachments.

```bash
eve resources resolve org_docs:/pm/features/FEAT-123.md
eve resources resolve org_docs:/pm/features/FEAT-123.md@v4 --json
eve resources ls org_docs:/pm/features/
eve resources cat job_attachments:/myproj-a3f2dd12/plan.md
```
