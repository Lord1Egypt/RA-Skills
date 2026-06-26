# CLI Command Reference

## Use When
- You need exact Eve CLI commands, options, and output behavior.
- You need to establish CLI context for org/project/environment or auth state.
- You need cross-resource workflows (jobs, pipelines, manifests, docs, secrets) from one interface.

## Load Next
- `references/overview.md` for platform orientation and environment setup.
- `references/jobs.md`, `references/pipelines-workflows.md`, or `references/manifest.md` for task-specific flags.
- `references/secrets-auth.md` for auth/scope-sensitive workflows.

## Ask If Missing
- Confirm whether the user is on staging, docker, or local k3d and the correct `EVE_API_URL`.
- Confirm target org/project IDs or slugs before crafting commands.
- Confirm any required auth mode (`eve auth login`, bootstrap, or service principal) for the action.

Complete reference for the Eve Horizon CLI (`eve`). Every command supports `--json` for machine-readable output unless noted otherwise.

**Version:** `eve --version` (or `eve -v`, `eve version`) prints the CLI version and, when the API is reachable, the platform version and git SHA. Use `--json` for structured output.

**Data envelope:** All list endpoints return `{ "data": [...] }` in JSON mode. The CLI handles both wrapped and unwrapped responses transparently, so agents should always expect the `data` wrapper when parsing `--json` output from list commands.

## Environment Setup

Default to **staging** for user guidance. Use local/docker only when explicitly asked.

```bash
export EVE_API_URL=https://api.eve.example.com   # staging (default)
export EVE_API_URL=http://localhost:4801          # local/docker (opt-in)
export EVE_API_URL=http://api.eve.lvh.me          # k8s ingress (local k3d stack)
```

Use `./bin/eh status` to discover the correct URL for the current instance. For local development, `eve local up` provisions a full k3d stack and prints the correct API URL.

## Profile

Profiles are **repo-local** configuration bundles. They store API URL, default org/project, harness preference, and auth identity.

```bash
eve profile list                                        # List all profiles
eve profile show [name]                                 # Show profile details (default: active)
eve profile use <name> [--clear]                        # Switch active profile
eve profile create <name> --api-url <url>               # Create a new profile
  [--org <id>] [--project <id>] [--harness <name>]
  [--default-email <email>] [--default-ssh-key <path>]
  [--supabase-url <url>] [--supabase-anon-key <key>]
eve profile set [name] --org <id>                       # Update profile fields
  [--project <id>] [--api-url <url>] [--harness <name>]
  [--default-email <email>] [--default-ssh-key <path>]
eve profile remove <name>                               # Delete a profile
```

Notes:
- Profiles persist to `.eve/profiles.json` in the repo root.
- `--clear` on `use` resets all fields to defaults.
- Set `--org` and `--project` to avoid passing them on every command.

## Auth (First Experience)

`eve auth login` now auto-discovers SSH keys from `~/.ssh/` when no `--ssh-key` is provided. It scans for private keys with matching `.pub` files and tries them in preference order (ed25519 > ecdsa > rsa). On success it prints which key was used. This eliminates the most common new-user friction point -- not knowing which flag to pass. Explicit `--ssh-key`, `EVE_AUTH_SSH_KEY`, or profile `default_ssh_key` still take priority when set.

See `references/cli-auth.md` for full auth command reference.

## Task Modules

Load the module that matches the current question before opening full command blocks:

- `references/cli-auth.md` -- login, bootstrap, service accounts, roles, bindings, policy-as-code.
- `references/cli-org-project.md` -- init, org/project lifecycle, docs, FS sync, FS sharing, resource resolver.
- `references/cli-jobs.md` -- job create/list/show/join/follow, attachments, and batch workflows.
- `references/cli-pipelines.md` -- builds, releases, pipelines, and workflow commands.
- `references/cli-deploy-debug.md` -- environment deploy/recover/rollback, local k3d stack, and CLI-first debugging.

For any topic, open only the matching module to keep load minimal.

## FS Sharing

Share files from the org filesystem via time-limited tokens, or publish path prefixes for unauthenticated public access.

```bash
# Share a file (returns a URL with an embedded token)
eve fs share <path> --org org_xxx
  [--expires 7d] [--label "release notes"]

# List active shares
eve fs shares --org org_xxx

# Revoke a share token
eve fs revoke <token> --org org_xxx

# Publish a path prefix for public (unauthenticated) access
eve fs publish <path-prefix> --org org_xxx [--label "docs"]

# List public paths
eve fs public-paths --org org_xxx
```

Notes:
- `share` creates a short-lived token-based URL for a single file. Default expiry is server-controlled; override with `--expires` (e.g. `7d`, `24h`).
- `publish` makes an entire path prefix publicly accessible without tokens. Use for assets, docs, or anything meant to be world-readable.
- Both commands support `--json` for structured output.

## Cloud FS (Google Drive Mounts)

Mount external cloud storage (e.g. Google Drive) into the org filesystem. Requires an integration connection (see `eve integrations connect google-drive`).

```bash
eve cloud-fs list --org org_xxx [--project <id>]        # List all mounts
eve cloud-fs mount --org org_xxx                        # Create a mount
  --provider <name> --folder-id <id>
  [--project <id>] [--label <text>]
  [--integration <id>]                                  # Auto-detected if omitted
  [--mode read_only|write_only|read_write]              # Default: read_write
  [--auto-index true|false]                             # Auto-index to org docs (default: true)
eve cloud-fs show <mount_id> --org org_xxx              # Mount details
eve cloud-fs update <mount_id> --org org_xxx            # Update mount settings
  [--label <text>] [--mode <mode>] [--auto-index <bool>]
eve cloud-fs unmount <mount_id> --org org_xxx           # Remove a mount (aliases: remove, delete)
eve cloud-fs ls [<path>] --org org_xxx                  # Browse files (alias: browse)
  [--mount <mount_id>]                                  # Default path: /
  [--page-token <token>] [--page-size <n>]
  [--order-by name|name_desc|modified|modified_desc]
  [--all]                                               # Auto-page, capped by EVE_CLOUD_FS_MAX_AUTO_PAGES
  [--recursive|-r]                                      # Bounded server traversal, no page token/all
eve cloud-fs search <query> --org org_xxx               # Search across mounts
  [--mount <mount_id>] [--mime-type <type>]
  [--page-token <token>] [--page-size <n>]
  [--order-by name|name_desc|modified|modified_desc]
  [--all]
```

Notes:
- Browse/search return one provider page by default. If `next_page_token` is present, pass it with `--page-token` or use `--all`.
- `--all --json` merges pages and returns `complete`, `page_count`, and `next_page_token` when the auto-page cap stops iteration.
- Search `--mime-type` is sent to the provider as a MIME filter.
- Recursive browse rejects `--page-token` and `--all`; JSON may include `truncated: true` when server guardrails stop traversal.

## Endpoints (Private Networking)

Register private endpoints backed by Tailscale for connecting external services to the Eve cluster.

```bash
eve endpoint add --org org_xxx                          # Register a private endpoint
  --name <name> --tailscale-hostname <fqdn> --port <port>
  [--health-path <path>]                                # Set to "none" to disable
eve endpoint list --org org_xxx                         # List endpoints
eve endpoint show <name> --org org_xxx [--verbose]      # Show details (--verbose runs health check)
eve endpoint remove <name> --org org_xxx                # Remove an endpoint
eve endpoint health <name> --org org_xxx                # Run a health check
eve endpoint diagnose <name> --org org_xxx              # Run diagnostics
```

Notes:
- Endpoints create in-cluster K8s services that proxy to Tailscale hostnames, making private infrastructure reachable from Eve jobs.
- After registering, use the returned `cluster_url` in secrets: `eve secrets set LLM_BASE_URL "${cluster_url}/v1" --scope org`.

## Domains (Custom Ingress Domains)

Bring your own domain for Eve-deployed apps. Domains can be declared under `services.<svc>.x-eve.ingress.domains` or under `environments.<env>.overrides.services.<svc>.x-eve.ingress.domains` and are registered during `eve project sync`. Use `eve domain register` for imperative reservations. DNS must point to the platform ingress before activation.

```bash
eve domain list [--env <name>] [--project <id>] [--json]                # List custom domains (filterable by env)
eve domain register <hostname> --project <id> --service <svc> [--env <env>] [--json]  # Register/reuse a domain row
eve domain verify <hostname> [--project <id>]                           # Verify DNS resolution and update status
eve domain status <hostname> [--project <id>]                           # Show domain detail (including owning env)
eve domain transfer <hostname> --to <env> [--project <id>] [--json]     # Move ownership to another env in the same project
eve domain unbind <hostname> [--project <id>] [--json]                  # Clear env binding; next deploy claims it
eve domain remove <hostname> [--project <id>] [--json]                  # Remove the custom domain entirely
```

Notes:
- Domains are auto-registered during `eve project sync` from top-level service ingress domains and env override ingress domains. A hostname declared in exactly one env override is also bound to that env during sync.
- `eve domain register <host> --project <id> --service <svc> --env <env>` creates or reuses a manual row. Manual rows survive later `eve project sync` calls even when the hostname is not in the manifest.
- `eve domain status <host> --json` returns stable `owner_env`, `dns_state`, `cert_state`, and `last_verified_at` fields.
- Each domain gets its own K8s Ingress with cert-manager TLS via HTTP-01 challenge.
- `eve domain verify` performs real DNS resolution server-side — it checks A/CNAME records against platform ingress and transitions status from `pending_dns` to `dns_verified` if DNS is correct. After verification, redeploy to activate.
- Platform subdomains (e.g., `foo.eve.example.com`) are rejected — use `ingress.alias` instead.
- Max 10 custom domains per project (configurable via `EVE_MAX_CUSTOM_DOMAINS_PER_PROJECT`).
- Hostname is globally unique — first project to claim wins.
- **Env-scoped, first-bind-wins**: within a project, a hostname is owned by the first env to deploy with it. Other envs that reference the same hostname log `owned by environment "<A>"` and skip rendering the ingress. Use `eve domain transfer <host> --to <env>` + redeploys to move ownership, or `eve domain unbind <host>` to clear and let the next deploy claim it. `eve domain list` shows `HOSTNAME | SERVICE | ENV | STATUS | VERIFIED` so you can see who owns what.

## Ingest (Document Ingestion)

Upload documents for processing. The CLI handles the three-step flow (create record, upload to presigned URL, confirm).

```bash
eve ingest <file> --project proj_xxx                    # Ingest a file (shorthand)
  [--title <title>] [--description <desc>]
  [--instructions <text>]                               # Processing instructions
  [--tags <a,b>] [--mime-type <type>]
  [--source-channel <channel>]                          # Default: cli
eve ingest create <file> --project proj_xxx             # Same as above (explicit)
eve ingest list --project proj_xxx                      # List ingest records
  [--status <status>] [--limit <n>] [--offset <n>]
eve ingest show <ingest_id> --project proj_xxx          # Show ingest details
```

Notes:
- Mime type is auto-detected from file extension. Supports text, documents, images, audio, and video.
- On success, returns `ingest_id`, `event_id`, and `job_id` for tracking the processing pipeline.

## Secrets

Secrets support four scopes: `--project`, `--org`, `--user`, `--system`. Project scope is the default.

```bash
eve secrets list --project proj_xxx
eve secrets show <key> --project proj_xxx               # Show secret metadata
eve secrets set <key> <value> --project proj_xxx
eve secrets delete <key> --project proj_xxx
eve secrets import --org org_xxx --file ./secrets.env    # Bulk import from .env file
eve secrets validate --project proj_xxx                 # Check manifest-required secrets
  [--keys KEY1,KEY2]
eve secrets ensure --project proj_xxx --keys KEY1,KEY2  # Ensure keys exist
eve secrets export --project proj_xxx --keys KEY1       # Export values
```

## Agents, Teams + Chat

See `references/agents-teams.md` for full agent and team configuration details.

```bash
# View effective config (pack resolution pipeline)
eve agents config [--repo-dir <path>] [--no-harnesses] [--json]

# JSON includes policy plus resolved agents, teams, and chat_routes arrays.
# Missing implicit teams/chat files in agents-only projects report [].

# Agent runtime status
eve agents runtime-status --org org_xxx [--json]

# Sync config (deprecated — use `eve project sync` instead)
eve agents sync --project proj_xxx --local --allow-dirty
```

## Teams

```bash
eve teams list [--json]
```

## Threads

```bash
# Org-scoped thread management
eve thread create --org org_xxx --key <key>             # Create org thread
eve thread list --org org_xxx [--scope <scope>]         # List org threads
  [--key-prefix <prefix>]
eve thread show <thread-id> --org org_xxx               # Show thread details

eve thread messages <thread-id>                         # List messages
  [--since 5m] [--limit 20] [--json]
eve thread post <thread-id>                             # Post a message
  --body '{"kind":"update","body":"text"}'
  [--actor-type user] [--actor-id <id>] [--job-id <id>]
eve thread follow <thread-id>                           # Tail messages (polls every 3s)

# Structured conversation events (normalized timeline)
eve thread events <thread-id>                           # List events
  [--after <cursor>] [--kind <kind>] [--job <id>]
  [--attempt <id>] [--workflow-step <name>] [--source <name>]
  [--limit 100] [--jsonl] [--follow]
eve thread emit-event <thread-id>                       # Emit an app-defined event
  --kind <kind> [--source app] [--text <text>]
  [--payload '{"key":"value"}']
  [--job <id>] [--attempt <id>] [--agent <slug>]
  [--workflow-step <name>] [--run <id>]

# Distillation (summarize thread into memory or docs)
eve thread distill <thread-id> --org org_xxx
  [--to <doc-path>]                                     # Write distillation to org docs path
  [--agent <slug>] [--category <name>] [--key <key>]    # Write to agent memory
  [--prompt "custom distillation prompt"]
  [--auto --threshold <n> --interval <duration>]        # Auto-distill on message threshold
```

Notes:
- `distill` summarizes a thread's messages into a condensed form. Output can be routed to an org doc path (`--to`) or to agent memory (`--agent` + `--category` + `--key`).
- `--auto` enables automatic re-distillation when message count exceeds `--threshold` since last distillation, checked on `--interval`.

## KV (Agent Key-Value Store)

Namespaced key-value storage scoped to an agent within an org. Values can be any JSON type.

```bash
eve kv set --org org_xxx --agent <slug> --key <key> --value <json-or-string>
  [--namespace <ns>] [--ttl <seconds>]                  # Optional namespace (default: "default") and TTL
eve kv get --org org_xxx --agent <slug> --key <key>
  [--namespace <ns>]
eve kv list --org org_xxx --agent <slug>                # List keys in namespace
  [--namespace <ns>] [--limit <n>]
eve kv mget --org org_xxx --agent <slug> --keys a,b,c   # Batch get multiple keys
  [--namespace <ns>]
eve kv delete --org org_xxx --agent <slug> --key <key>
  [--namespace <ns>]
```

Notes:
- Namespace defaults to `"default"` when omitted.
- `--value` is parsed as JSON if valid, otherwise stored as a string.
- `--ttl` sets a time-to-live in seconds; expired keys are not returned.

## Memory (Agent Memory)

Structured long-term memory for agents. Entries are organized by agent, category, and key, with support for lifecycle metadata, tagging, confidence scores, and cross-agent search.

```bash
eve memory set --org org_xxx (--agent <slug>|--shared)
  --category <category> --key <key>
  (--file <path>|--stdin|--content <text>)              # Content source
  [--tags "architecture,decision"]                      # Comma-separated tags
  [--confidence 0.9]                                    # Confidence score (0-1)
  [--supersedes <memory-id>]                            # Supersede a previous entry
  [--lifecycle-status active|archived|draft]
  [--review-in 30d] [--expires-in 90d]                  # Lifecycle scheduling

eve memory get --org org_xxx (--agent <slug>|--shared)
  --key <key> [--category <category>]

eve memory list --org org_xxx (--agent <slug>|--shared)
  [--category <category>] [--tags a,b] [--limit <n>]

eve memory delete --org org_xxx (--agent <slug>|--shared)
  --category <category> --key <key>

eve memory search --org org_xxx --query <text>           # Cross-agent memory search
  [--agent <slug>] [--limit <n>]
```

Notes:
- `--shared` stores memory in the org-wide shared namespace (agent slug `shared`).
- `--supersedes` links the new entry to a previous one, forming a revision chain.
- `search` queries across all agents in the org unless `--agent` scopes it to one.
- Lifecycle fields (`--review-in`, `--expires-in`) work identically to org docs.

## Search (Unified Cross-Source Search)

Federated search across all org data sources: memory, docs, threads, attachments, and events.

```bash
eve search --org org_xxx --query <text>
  [--sources memory,docs,threads,attachments,events]    # Comma-separated source filter
  [--agent <slug>]                                      # Scope to agent's data
  [--limit <n>]
```

Notes:
- When `--sources` is omitted, all sources are searched.
- Results are ranked by relevance and grouped by source type.

## Packs (AgentPacks)

```bash
eve packs status [--repo-dir <path>]                    # Show lockfile status + drift
eve packs resolve [--dry-run] [--repo-dir <path>]       # Preview pack resolution
```

## Skills

```bash
eve skills install [source] [--skip-installed]          # Install skill packs
```

**Resolution order** (without a source argument):
1. **Pack-based** -- if `.eve/manifest.yaml` defines `x-eve.packs`, skills are installed from those packs. Requires a matching `.eve/packs.lock.yaml` (run `eve agents sync` to generate it). Per-pack `install_agents` overrides are supported; the global default comes from `x-eve.install_agents`.
2. **skills.txt** -- falls back to reading `skills.txt` and installing all entries.

- With source: installs directly from URL, GitHub repo, or local path and persists to `skills.txt`.
- Supports: `https://github.com/org/repo`, `org/repo` (GitHub shorthand), `./local/path`.
- Glob patterns in `skills.txt` (e.g. `../**`) automatically exclude `private-skills/` directories unless the path explicitly targets them (e.g. `../private-skills/my-skill`).
- Local directory paths in `skills.txt` (e.g. `./my-skills`) are expanded at parse time into individual skill subdirectories, so `./path` behaves identically to `./path/*`. This ensures correct `--skip-installed` checks and consistent enumeration.
- Installs for all supported agents: claude-code, codex, gemini-cli, pi.

## Harnesses

```bash
eve harness list [--capabilities] [--org <id>] [--project <id>]
eve harness get <name> [--org <id>] [--project <id>]
eve harness validate --project <id> [--profile-file profile.json|--workflow <name>] [--env-override KEY=VALUE] [--json]
```

Notes:
- `--capabilities` shows model support, reasoning levels, streaming, and tool use.
- `harness get` shows variants, auth status, and capability matrix.
- `harness validate` dry-runs an inline `harness_profile_override`, standalone `env_overrides`, or a workflow step env composition against project secrets and harness auth without creating a job or invoking a model. Use repeated `--env-override KEY=VALUE`; `${secret.KEY}` placeholders report resolved/missing scope without exposing values.

## Database (Environment DBs)

All `db` subcommands accept either `--env <name>` (API-proxied) or `--url <postgres-url>` (direct connection). When `--url` is used, the CLI connects directly to the database without going through the Eve API. The `EVE_DB_URL` env var (or `.env` file) is used as a fallback for `sql` and `migrate`.

```bash
eve db schema --env <name> [--project <id>]             # Show DB schema
eve db schema --url <postgres-url>                      # Show schema via direct connection
eve db rls --env <name>                                 # Show RLS policies + group context diagnostics
eve db rls init --with-groups [--out <path>] [--force]  # Scaffold group-aware RLS helper SQL
eve db sql --env <name> --sql "SELECT 1"                # Run query (read-only default)
  [--params '["arg1"]']                                 # Parameterized query
  [--write]                                             # Enable mutations
  [--file ./query.sql]                                  # Run SQL from file
eve db sql --url <postgres-url> --sql "SELECT 1"        # Direct SQL execution
eve db migrate --env <name> [--path db/migrations]      # Apply pending migrations
eve db migrate --url <postgres-url> [--path db/migrations]  # Direct migration apply
eve db migrations --env <name>                          # List applied migrations
eve db new <description> [--path db/migrations]         # Create migration file
eve db reset --env <name> --force [--no-migrate]        # Drop and recreate schema, re-apply migrations
  [--danger-reset-production] [--path db/migrations]
  [--skip-snapshot]                                     # Skip auto-snapshot before reset
eve db reset --url <postgres-url> --force               # Direct schema reset
eve db wipe --env <name> --force                        # Reset schema without re-applying migrations
eve db status --env <name>                              # Managed DB status
eve db extensions list --env <name>                     # List installed DB extensions
eve db rotate-credentials --env <name>                  # Rotate managed DB credentials
eve db scale --env <name> --class db.p1|db.p2|db.p3     # Scale managed DB class
eve db destroy --env <name> --force [--skip-snapshot]   # Destroy managed DB

# Snapshots and restore
eve db snapshot --env <name> [--retention <duration>]   # Create a DB snapshot
eve db snapshot show <snapshot_id> --env <name>         # Show snapshot details
eve db snapshot delete <snapshot_id> --env <name> --force  # Delete a snapshot
eve db snapshot download <snapshot_id> --env <name> --output <path>  # Get download URL
eve db snapshots --env <name>                           # List snapshots
  [--status <status>] [--limit <n>]
eve db restore --env <name> --snapshot <id> --force     # Restore from snapshot
  [--source-env <name>] [--source-project <id>]        # Cross-env/project restore
  [--skip-safety-snapshot]                              # Skip pre-restore safety snapshot
eve db backup-status --env <name>                       # Show backup schedule and status
```

Notes:
- `rls` now includes group context diagnostics: shows the resolved principal, org, project, env, group IDs, and permissions for the current session. Useful for debugging why policies are not matching.
- `rls init --with-groups` scaffolds `app.current_user_id()`, `app.current_group_ids()`, and `app.has_group()` SQL functions to `db/rls/helpers.sql` (or `--out <path>`). Apply the output SQL to your target environment DB, then reference these helpers in RLS policies.
- Migration files: `YYYYMMDDHHmmss_description.sql` in `db/migrations/` by default.
- `reset` drops all schemas (except `pg_catalog`, `information_schema`) and re-applies migrations. Use `--no-migrate` (or `wipe`) to skip migration re-apply.
- `--danger-reset-production` is required when resetting production environments via the API.
- `--url` mode uses the `@eve/migrate` library for direct `migrate`, `migrations`, `reset`, and `wipe` operations.
- `snapshot` creates a point-in-time backup. `restore` overwrites the target DB from a snapshot (creates a safety snapshot first unless `--skip-safety-snapshot`).
- Cross-environment restore is supported via `--source-env` and `--source-project`.
- `backup-status` shows the automated backup schedule, retention policy, and snapshot-on-delete/reset settings.

## Manifest

```bash
eve manifest validate [--path <path>]                   # Validate manifest
  [--validate-secrets] [--strict] [--latest]
  [--project <id>] [--dir <path>]
```

See `references/manifest.md` for manifest schema and configuration.

## App Links

Inspect cross-project app links. App links are declared in `x-eve.app_links`
and reconciled by `eve project sync`.

```bash
eve app-links list [project] [--project <id>] [--json]
eve app-links plan --project <id> [--file .eve/manifest.yaml] [--env <env>] [--json]
eve app-links explain --consumer <id> (--alias <name> | --producer <id> --api <name>) [--json]
```

Notes:
- `list` shows producer exports, consumer subscriptions, and grants to the target project.
- `plan` dry-runs the consumer side of a manifest against active producer grants and reports missing scopes, event feeds, or revoked grants.
- `explain` is the fastest diagnostic for a local subscription alias. It reports `OK`, `MISSING`, `REVOKED`, or `INVALID`.

## API (Proxy)

Call project API sources (OpenAPI, PostgREST, Supabase GraphQL) through Eve's auth layer.

```bash
eve api list [project] [--env <name>]                   # List API sources
eve api show <name> [project] [--env <name>]            # Show API source details
eve api spec <name> [project] [--env <name>]            # Show cached API spec
eve api refresh <name> [project] [--env <name>]         # Refresh cached spec
eve api examples <name> [project] [--env <name>]        # Generate curl examples from spec

eve api call <name> <method> <path>                     # Call API with Eve auth
  [--json <payload|@file>] [--data <payload|@file>]     # JSON request body
  [--graphql <query|@file>]                             # GraphQL query
  [--variables '{"k":"v"}']                             # GraphQL variables
  [--jq <expr>]                                         # Filter response with jq
  [--print-curl]                                        # Print curl command instead
  [--token <override>]                                  # Custom auth token
  [--project <id>] [--env <name>]
```

eve api generate [--out <dir>]                          # Export OpenAPI spec
eve api diff [--exit-code] [--out <dir>]                # Diff generated vs committed spec
```

Notes:
- `call` resolves the base URL from the API source, applies Eve auth, and proxies the request.
- `--json` and `--data` are aliases (`-d` shorthand also works); use only one body flag.
- `--json`/`--data` and `--graphql` accept inline JSON/text or `@file` paths.
- `--env` falls back to `$EVE_ENV_NAME` when omitted.
- `call` rewrites service DNS/ingress base URLs to match runtime context (local shell vs in-cluster job).
- `--jq` requires `jq` installed locally.
- Auth precedence: `--token` > `$EVE_JOB_TOKEN` > profile token.
- `generate` exports the current OpenAPI spec. `diff` compares against committed spec.

## Chat + Integrations (Slack, Google Drive, Nostr)

```bash
# Integration listing and testing
eve integrations list --org org_xxx
eve integrations test <integration_id> --org org_xxx
eve integrations update <integration_id> --org org_xxx       # Update integration settings
  --setting key=value                                        # e.g. admin_channel_id=C12345

# OAuth app configuration (BYOA — Bring Your Own App)
eve integrations setup-info <provider> --org org_xxx         # Show callback URLs, scopes, and setup instructions
eve integrations configure <provider> --org org_xxx          # Register OAuth app credentials
  --client-id "..." --client-secret "..."
  [--signing-secret "..."] [--app-id "..."]                  # Slack-specific
  [--label <text>]
eve integrations config <provider> --org org_xxx             # View OAuth app config (secrets redacted)
eve integrations unconfigure <provider> --org org_xxx        # Remove OAuth app config
eve integrations connect <provider> --org org_xxx            # Initiate OAuth flow (prints authorize URL)

# Slack-specific
eve integrations slack connect --org org_xxx --team-id T123
  --token xoxb-test [--tokens-json '{}'] [--status]
eve integrations slack install-url --org org_xxx [--ttl 24h] # Generate shareable Slack install link

# Project-scoped outbound notifications
eve notifications send --project proj_xxx
  --channel eve-horizon-notifications
  --message "Workflow complete"
  [--integration-id int_xxx] [--thread <ts>] [--json]

# Default agent slug (org-wide fallback)
eve org update org_xxx --default-agent mission-control

# Chat simulation (gateway-routed, default)
eve chat simulate --team-id T123 --text "hello"
  [--channel-id C123] [--user-id U123]
  [--provider slack] [--thread-id <id>]
  [--external-email user@example.com]
  [--event-type <type>] [--dedupe-key <key>]
  [--metadata '{}'] [--json]

# Chat simulation (legacy project-scoped path)
eve chat simulate --project proj_xxx
  --team-id T123 --text "hello"
  [--channel-id C123] [--user-id U123]
  [--provider slack] [--thread-key <key>] [--metadata '{}']
```

Notes:
- `chat simulate` defaults to the gateway path (`/gateway/providers/simulate`) which routes by agent slug. Omit `--project` to use this path.
- Pass `--project` to force the legacy per-project simulate path. The CLI warns when this fallback is used.
- `--thread-id` replaces `--thread-key` on the gateway path (both are accepted for backward compat).
- `--external-email` can also be passed inside `--metadata` as `external_email` for backward compat.
- `integrations update` patches individual settings on an existing integration (e.g. changing `admin_channel_id`).
- `integrations slack install-url` generates a time-limited install link for sharing with workspace admins. Use `--ttl` to control expiry (default: server-controlled).
- `notifications send` posts a one-way Slack notification through the org integration without exposing raw Slack tokens. It requires `notifications:send` on the project/job token.
- Supported providers: `google-drive`, `slack`. The BYOA flow is: `setup-info` (get URLs/scopes) -> `configure` (register credentials) -> `connect` (initiate OAuth).

Slack commands (run inside Slack):

```text
@eve <agent-slug> <command>
@eve agents list
@eve agents listen <agent-slug>
@eve agents unlisten <agent-slug>
@eve agents listening
```

Nostr relay subscriptions provide a non-webhook transport. See `references/gateways.md`.

## GitHub Integration

One-command webhook setup for connecting a project's GitHub repo to Eve event triggers.

```bash
# Set up webhook (auto-creates via gh CLI if available, otherwise prints instructions)
eve github setup [--project proj_xxx]
  [--regenerate]                                       # Regenerate webhook secret
  [--json]

# Check webhook status
eve github status [--project proj_xxx] [--json]

# Fire a synthetic github.push test event
eve github test [--project proj_xxx] [--json]
```

Notes:
- `setup` ensures `GITHUB_WEBHOOK_SECRET` exists in project secrets and returns the webhook URL + secret.
- If the `gh` CLI is installed and authenticated, `setup` auto-creates or updates the webhook on the repo. Otherwise it prints the URL, secret, and manual instructions (including a ready-to-paste `gh api` command).
- `--regenerate` deletes the existing secret and creates a new one (useful for rotation).
- `test` creates a synthetic `github.push` event on the project's default branch. Use it to verify pipeline triggers fire correctly.
- Webhook URL format: `${EVE_PUBLIC_API_URL}/integrations/github/events/${project_id}`.
- Required permissions: `secrets:write` (setup), `secrets:read` (status), `events:write` (test).

## Identity

Link external provider identities (e.g. Slack user) to the current Eve user.

```bash
eve identity link <provider> --org org_xxx                   # Generate a link token for a provider
```

Notes:
- Supported providers: `slack`.
- Returns a token with instructions for completing the identity link (e.g. sending a DM to the Eve bot in Slack).
- Org scope is required; falls back to profile default.

## Events (Triggers)

```bash
eve event list --project proj_xxx
  [--type github.push] [--source github] [--status <s>]
eve event show <event-id>
eve event emit --type manual.test --source manual
  [--env staging] [--ref-sha <sha>] [--ref-branch main]
  [--actor-type user] [--actor-id <id>]
  [--dedupe-key <key>]
  --payload '{"k":"v"}'
```

See `references/events.md` for the complete event type catalog and trigger syntax.

## Traces (OTEL Trace Query)

Agent-queryable surface over the OTEL trace store. No AWS console access required.

```bash
eve traces query --project proj_xxx --request-id req_01h... [--json]
eve traces query --project proj_xxx --trace-id <trace-id> [--json]
eve traces query --project proj_xxx --service <name> --since 5m --error
eve traces query --project proj_xxx --service <name> --route "POST /api/items" --since 1h --p99
  [--limit <n>] [--no-cache]
```

Notes:
- Provide at least one of `--request-id`, `--trace-id`, `--since`, `--route`, or `--error`.
- Returns structured spans (service, duration, error/fault/throttle flags) plus a
  summary `{ trace_count, span_count, p99_ms }`.
- Backed by the platform trace store; the response includes `backend` and
  `backend_available` so agents can detect when traces are unavailable.
- For request-id-based diagnostics that combine logs, events, deploy metadata,
  and traces in one shot, prefer `eve env diagnose <project> <env> --request <id> --json`.

## Supervision

```bash
eve supervise [<job-id>] [--timeout 60] [--since <cursor>] [--json]
```

Monitors job tree and team coordination. Returns events, children, inbox, and cursor for long-polling.

## Migrate

```bash
eve migrate skills-to-packs                             # Convert skills.txt to x-eve.packs YAML
```

Reads `skills.txt` and generates the equivalent `x-eve.packs` manifest fragment for migration from legacy skills to the AgentPacks system.

## Providers

```bash
eve providers list [--json]                             # List registered providers
eve providers discover <provider> [--json]              # Discover models for a provider
```

Notes:
- Providers are first-class entities with auth config, harness mapping, and model discovery.
- `discover` fetches live model lists from the provider's API (cached with TTL).

## Analytics

```bash
eve analytics summary --org org_xxx [--window 7d]       # Org-wide summary
eve analytics jobs --org org_xxx [--window 7d]           # Job counters (created/completed/failed/active)
eve analytics pipelines --org org_xxx [--window 7d]      # Pipeline success rates and durations
eve analytics env-health --org org_xxx                   # Environment health snapshot (total/healthy/degraded/unknown)
eve analytics cost-by-agent --org org_xxx [--window 7d]  # Cost breakdown per agent (attempts, tokens, USD)
```

Notes:
- All analytics endpoints return aggregate counters, not per-item listings. Use `--json` for machine-readable output.
- `--window` accepts relative durations like `7d`, `24h`, `30d`.
- `cost-by-agent` shows per-agent cost, attempt count, and input/output token totals.

## Webhooks

```bash
eve webhooks create --org org_xxx --url <url> --events <evt1,evt2> --secret <secret>
  [--filter '{"key":"val"}'] [--project <id>]
eve webhooks list --org org_xxx
eve webhooks show <webhook_id> --org org_xxx
eve webhooks deliveries <webhook_id> --org org_xxx [--limit 50]
eve webhooks test <webhook_id> --org org_xxx
eve webhooks delete <webhook_id> --org org_xxx
eve webhooks enable <webhook_id> --org org_xxx
eve webhooks replay <webhook_id> --org org_xxx
  [--from-event <event_id>] [--to <iso-time>] [--max-events <n>] [--dry-run]
eve webhooks replay-status <webhook_id> <replay_id> --org org_xxx
```

Notes:
- Webhook subscriptions support HMAC signature verification and retry logic.
- Filters scope events to specific patterns. Project-scoped webhooks are optional.

## User

Inspect user details and memberships.

```bash
eve user show [user_id|me] [--json]                    # Show user profile, org + project memberships
```

Notes:
- Defaults to `me` (the authenticated user) when no user ID is given.
- Output includes email, display name, admin status, org memberships (slug + role), and project memberships (`org_slug/project_slug` + role).

## Admin

Administrative commands (require elevated permissions).

```bash
# List all platform users (shows email, org + project memberships, roles)
eve admin users [--json]

# User invitation
eve admin invite --email user@example.com
  [--github <username>] [--ssh-key <path>]              # Auth methods (at least one recommended)
  [--role <role>] [--org <org_id>]
  [--web] [--redirect-to <url>]                         # --web sends Supabase invite email

# Access request management
eve admin access-requests list
eve admin access-requests approve <request_id>
eve admin access-requests reject <request_id> --reason "..."

# Billing
eve admin balance show <org_id>                         # Current balance
eve admin balance credit <org_id> --amount 100.00       # Add credit
  [--currency usd] [--description "reason"]
eve admin balance transactions <org_id>                 # Transaction history
  [--limit 50] [--offset 0]

eve admin usage list --org org_xxx                      # Usage records
  [--since 2026-01-01] [--until 2026-02-01] [--limit 100]
eve admin usage summary --org org_xxx                   # Aggregated usage summary
  [--since 2026-01-01] [--until 2026-02-01]

# Pricing
eve admin pricing seed-defaults                         # Seed default rate cards

# Receipts
eve admin receipts recompute                            # Recompute cost receipts
  [--since 2026-01-01] [--project proj_xxx]
  [--dry-run] [--force]

# Ingress aliases (custom domain aliases for services)
eve admin ingress-aliases list                          # List all aliases
  [--alias <alias>] [--project <id>] [--environment <id>]
  [--limit <n>] [--offset <n>]
eve admin ingress-aliases reclaim <alias> --reason "..."  # Reclaim an alias

# Email delivery events (SES bounces, complaints, deliveries, rejects)
eve admin email bounces list                            # Recent delivery events
  [--recipient <addr>]                                  # Filter by recipient
  [--event-type Bounce|Complaint|Delivery|Reject]
  [--limit <n>] [--json]
```

Notes:
- `users` lists every registered user with their email, display name, admin status, memberships, and roles. One row per user-membership pair (org or project). Columns: Email, Name, Admin, Scope (`org`/`project`), Target (org slug or `org_slug/project_slug`), Role, Created. Useful for auditing access.
- `invite --ssh-key` registers an SSH public key file (e.g. `~/.ssh/id_ed25519.pub`) as an auth identity. If no auth method is given (`--github`, `--ssh-key`, or `--web`), the CLI warns that the user won't be able to log in.
- Users can self-register via `eve auth request-access --org "Org Name" --ssh-key ~/.ssh/id_ed25519.pub --wait`.
- Access-request approval is retry-safe (`approve` returns the existing approved record on repeat calls).
- Duplicate identity fingerprints are attached to the existing identity owner.
- `ingress-aliases reclaim` forcibly releases an alias from its current project/environment. Requires a `--reason`.
- `email bounces list` reads the `email_delivery_events` table populated by the SES SNS webhook. Use it to investigate magic-link / invite delivery failures — see `references/observability.md` for the table schema and mailer pre-flight behavior.

## System (Internal)

```bash
eve system status                                       # Platform status overview
eve system health [--json]                              # Health check (reports Degraded on DB failure)
eve system config                                       # Show system configuration
eve system settings                                     # List all settings
eve system settings get <key>                           # Get setting value
eve system settings set <key> <value>                   # Set setting value
eve system env-health [--status <healthy|degraded|critical>] [--limit 100] [--json]
                                                     # Cross-org environment health report (system_admin)
eve system env-cost [--all] [--month YYYY-MM] [--source opencost] [--json]
                                                     # Cross-org MTD environment cost estimates

eve system orchestrator status                          # Orchestrator state
eve system orchestrator set-concurrency <n>             # Set job concurrency

eve system jobs [--org <id>] [--project <id>]           # Active jobs overview
  [--phase <p>] [--limit 50]
eve system envs [--org <id>] [--project <id>]           # Environment overview
eve system logs <service> [--tail 50]                   # Service logs
eve system pods                                         # K8s pod status
eve system events [--limit 50]                          # Recent platform events
```

Notes:
- `eve system env-health` is the platform-wide sentinel view. It returns the latest health check row per environment, including issue details, degraded tick counters, and any circuit-breaker actions.
- `eve system env-cost` reads `GET /admin/cost/environments` and returns month-to-date environment allocation snapshots. Default table output shows the top 20 environments; `--all` shows every environment; `--json` emits the raw API payload with `total_usd`, `shared_usd`, `observed_at`, `stale`, and `stale_after_hours`.
- Environment cost uses precomputed snapshots from the opt-in orchestrator OpenCost collector. The command never queries OpenCost directly. Freshness labels are explicit: `fresh estimate`, `stale estimate`, or `unavailable`.
- `eve analytics env-health --org <org_id>` remains the org-scoped aggregate view. Use `eve system env-health` when you need cross-org detail as a `system_admin`.
- Sentinel configuration is stored in system settings:
  - `sentinel.enabled`
  - `sentinel.slack.integration_id`
  - `sentinel.slack.channel_id`
- The inbound Slack responder also requires the gateway deployment env var `EVE_SENTINEL_CHANNEL_ID` to match `sentinel.slack.channel_id`.

## Local Stack (k3d)

Provision and manage a full Eve platform stack locally using k3d (k3s-in-Docker). Requires Docker Desktop. The CLI auto-installs `k3d` and `kubectl` into `~/.eve/bin/` if not already present.

Supported platforms: macOS and Linux (amd64 and arm64).

```bash
# Bring up the local stack (creates cluster, pulls images, migrates DB, starts all services)
eve local up
  [--version <x.y.z>]                                  # Platform version (default: latest)
  [--skip-deploy]                                      # Start cluster only, skip image deploy
  [--skip-health]                                      # Don't wait for API health check
  [--timeout <seconds>]                                # Rollout timeout (default: 300)
  [--verbose]                                          # Show kubectl/docker output
  [--json]                                             # Machine-readable output

# Stop the local cluster (preserves state)
eve local down
  [--destroy]                                          # Delete cluster and all data
  [--force]                                            # Skip confirmation prompt

# Full status dashboard
eve local status
  [--watch]                                            # Auto-refresh every 5s
  [--json]

# Health check (exits non-zero if unhealthy)
eve local health [--json]

# Destroy and recreate from scratch
eve local reset
  [--force]                                            # Skip confirmation prompt

# Stream service logs
eve local logs [<service>]                             # Omit service for all logs
  [--follow] [-f]                                      # Tail logs
  [--tail <n>]                                         # Lines to show (default: 50)
  [--since <duration>]                                 # e.g. 5m, 1h

# Multi-project app-link mesh on the local k3d stack
eve local mesh init <name> [--org <org_id>] [--env local] [--profile <profile>] [--force]
eve local mesh add <project-slug> --path <checkout> [--role producer|consumer] [--workspace <name>]
eve local mesh use <name>
eve local mesh list [--json]
eve local mesh show [--workspace <name>] [--json]
eve local mesh up [--workspace <name|path>] [--only <project>] [--skip-pre-check] [--skip-cli-build] [--json]
eve local mesh redeploy <project> [--workspace <name>] [--skip-cli-build]
eve local mesh status [--workspace <name>] [--json]
eve local mesh diagnose [--workspace <name>] [--project <slug>] [--probe] [--json]
eve local mesh logs <project>/<component> [--workspace <name>] [--follow] [--tail <n>] [--since <duration>]
eve local mesh down [--workspace <name>] [--delete-projects]

# Build/import a producer app-link CLI image directly
eve project image build-cli [project-slug|project-id] [--repo-dir <path>] [--dockerfile <path>] [--tag <image>] [--import-to-k3d] [--json]
```

**Services:** api, orchestrator, worker, gateway, agent-runtime, auth, mailpit, sso, postgres.

**Local URLs** (available after `eve local up`):
- API: `http://api.eve.lvh.me`
- Auth: `http://auth.eve.lvh.me`
- Mail: `http://mail.eve.lvh.me`
- SSO: `http://sso.eve.lvh.me`

**Typical workflow:**
```bash
eve local up                                           # First run: ~5min (image pulls)
export EVE_API_URL=http://api.eve.lvh.me
eve org ensure "my-org" --slug my-org                  # Bootstrap an org
eve local status --watch                               # Monitor services
eve local logs api --follow                            # Debug API issues
eve local down                                         # Stop (state preserved)
eve local up                                           # Restart (fast, no re-pull)
eve local reset --force                                # Nuclear option: destroy + recreate
```

Notes:
- `up` is idempotent: re-running starts a stopped cluster or skips if already running.
- `down` without `--destroy` preserves cluster state; `up` resumes quickly.
- `eve local mesh` requires a running local API and refuses non-local API URLs.
- Mesh workspace project names are Eve project slugs (4-8 alphanumeric chars)
  and must match `x-eve.app_links.*.project` references.
- Every project in a mesh should declare the same environment name, normally
  `environments.local`.
- When a producer export uses an image-mode `x-eve.cli`, `mesh up` builds
  `Dockerfile.cli`, imports `local/<producer>-cli:<sha>` into k3d, and syncs
  that image into the grant for local job CLI injection.
- `reset` is equivalent to `down --destroy` followed by `up`.
- Version resolution queries the configured registry for the latest common platform tag.
  - Set `ECR_REGISTRY=<registry>` to override the registry host.
  - Set `ECR_NAMESPACE=<namespace>` to override the image namespace (defaults to `eve-horizon`).
- **ECR auto-auth:** `up` automatically authenticates Docker to ECR Public before pulling platform images. If the AWS CLI is installed and configured, it runs `aws ecr-public get-login-password` to obtain a token and logs Docker in. This avoids ECR Public's anonymous rate limits (1 pull/s, 10 pulls/min per IP). If the AWS CLI is not available, pulls proceed without auth but may fail under rate limits -- the error message includes a manual login command.
- Image pull retries now handle `403 Forbidden` and `429 Too Many Requests` responses, and HTTP fetches (e.g. registry tag listing) retry with exponential backoff on 429.
- The cluster binds ports 80/443 on localhost via k3d's load balancer.
- Public raw TCP ingress tests need explicit k3d port mappings. Contributors
  can recreate the local cluster with `./bin/eh k8s start --tcp-ports 33400,33500 --recreate`.
- Kube context is set to `k3d-eve-local` automatically.

## Job Execution Runtime

Platform behaviors that affect how jobs and harnesses execute. These are not CLI commands but are important context for understanding job output.

**Type auto-resolve:** If a pipeline step declares `type: run` with a `service` reference but no `command`, the platform auto-resolves it to `type: job` and logs a warning. This catches a common manifest mistake. Update your manifest to use `type: job` directly to silence the warning.

**Secret forwarding:** All resolved project secrets (project, org, and user scope) are now forwarded to the harness process environment. This means secrets like `GITHUB_TOKEN`, custom API keys, and other credentials set via `eve secrets set` are available to the agent without additional configuration. Worker-internal variables (`DATABASE_URL`, etc.) remain excluded by the sanitization allowlist.

**Worker image tooling:** The worker image now includes `gh` (GitHub CLI) and `jq`. When `GITHUB_TOKEN` or `GH_TOKEN` is set in project secrets, `gh` authenticates automatically inside jobs.

**Log normalization:** The platform stream API now includes a pre-computed `text` field on every log event, providing human-readable output without harness-specific parsing. Both `eve job logs` and `eve job follow` use a shared normalization layer (`normalizeLogLine` from `@eve/shared`) that handles Codex, Claude, and other harness event formats uniformly.

Budget-configured jobs emit `budget.summary` rows on completion and
`budget.exceeded` rows when enforcement terminates an attempt. Use
`eve job logs <id> --json` or `eve job diagnose <id> --json` to inspect
`total_tokens`, `weighted_tokens`, `cache_read_tokens`,
`cache_read_token_weight`, and `cache_read_tokens_excluded`.

**Codex harness improvements:**
- Streaming logs render cleanly: tool use shows the tool name with a truncated input preview, status messages are prefixed with `>`, and result text is extracted properly.
- Final result text and token usage are extracted from Codex job logs for display in `eve job show` and `eve job result`.

## Debugging (CLI-first)

See `references/deploy-debug.md` for the debugging ladder and system health workflows.

Quick reference:
- `eve job diagnose <id>` -- primary job debugging entry point
- `eve job follow <id>` -- stream harness logs in real time
- `eve job runner-logs <id>` -- K8s pod logs for startup failures
- `eve env diagnose <project> <env>` -- environment health, K8s events, and ingress diagnostics
- `eve env diagnose <project> <env> --request <id> --json` -- request-level logs, events, deploy metadata, audit rows, and traces
- `eve env logs <project> <env> <service> --follow --filter req_id=<id>` -- stream app-service logs with structured filters
- `eve traces query --project <project> --request-id <id> --json` -- query trace spans without console access
- `eve tcp-ingress test <project> <env> --listener <name>` -- TCP connect probe for public raw TCP listeners
- `eve env recover <project> <env>` -- analyze state and suggest recovery action
- `eve system health` -- platform-wide health check

### HTTP Ingress Diagnostics

`eve env diagnose` renders an `HTTP Ingress` table and returns `.http_ingress[]`
in JSON when services expose public HTTP ingress. Use it to confirm requested
and effective request timeout/body-size values after changing
`x-eve.ingress.timeout` or `x-eve.ingress.max_body_size`.

```bash
eve env diagnose <project> <env>
eve env diagnose <project> <env> --json | jq '.http_ingress'
```

Each row includes the service, hosts, controller flavor, requested and effective
timeout/body-size values, and the source (`manifest`, `platform_default`,
`unsupported_controller`, or `missing`).

### Public TCP Ingress

For services declaring `x-eve.tcp_ingress`, `eve env diagnose` renders a
`TCP Ingress` table and returns `.tcp_ingress[]` in JSON. Listener states are
`pending`, `provisioning`, or `ready`.

```bash
eve env diagnose <project> <env> --json | jq '.tcp_ingress'
eve tcp-ingress test <project> <env> --listener a1-gt06
eve tcp-ingress test <project> <env> --listener a1-gt06 --timeout 10 --json
```

`eve tcp-ingress test` resolves the listener through env diagnose, opens a TCP
socket from the CLI host, prints `OK` or `FAIL`, and exits non-zero on failure.
It does not speak the app's device protocol.

## Resource Cleanup

```bash
eve build delete <build_id>                  # Delete build + runs/artifacts
eve build prune [--project=] [--keep=10]     # Delete old builds, keep latest N
eve release delete <tag> [--project=]        # Delete release by tag
eve release prune [--project=] [--keep=5]    # Delete old releases, keep latest N
eve agents delete <slug> [--project=]        # Delete agent config + routes
eve agents delete-team <team_id> [--project=] # Delete team
eve thread delete <thread_id>               # Delete thread + messages
eve pipeline delete <name> [--project=]     # Delete pipeline + run history
```

## All Commands Summary

| Category | Key Commands |
|----------|-------------|
| **Profile** | `list`, `show`, `use`, `create`, `set`, `remove` |
| **Auth** | `login`, `logout`, `status`, `token`, `permissions`, `bootstrap`, `mint`, `creds`, `sync`, `request-access`, `create-service-account`, `list-service-accounts`, `revoke-service-account` |
| **Access** | `can`, `explain`, `roles create/list/show/update/delete`, `bind`, `unbind`, `bindings list`, `groups create/list/show/update/delete`, `groups members list/add/remove`, `memberships`, `validate`, `plan`, `sync` |
| **Org** | `list`, `ensure`, `get`, `update`, `delete` (soft/hard), `spend`, `members`, `membership-requests` |
| **Project** | `list`, `ensure`, `get`, `update`, `delete` (soft/hard), `sync`, `spend`, `members`, `bootstrap`, `status` |
| **Docs** | `write`/`create`, `read`, `show`, `list`, `search`, `stale`, `review`, `versions`, `query`, `delete` |
| **Jobs** | `create`, `list`, `ready`, `blocked`, `show`, `current`, `tree`, `diagnose`, `update`, `close`, `cancel`, `dep`, `claim`, `release`, `attempts`, `logs`, `submit`, `approve`, `reject`, `result`, `receipt`, `compare`, `follow`, `wait`, `watch`, `runner-logs`, `attach`, `attachments`, `attachment`, `batch`, `batch-validate` |
| **Ingest** | `create` (or `<file>`), `list`, `show` |
| **Cloud FS** | `list`, `mount`, `unmount`, `show`, `update`, `ls`, `search` |
| **Endpoints** | `add`, `list`, `show`, `remove`, `health`, `diagnose` |
| **TCP Ingress** | `test` |
| **Builds** | `create`, `list`, `show`, `run`, `runs`, `logs`, `artifacts`, `diagnose`, `cancel`, `delete`, `prune` |
| **Releases** | `resolve`, `delete`, `prune` |
| **Pipelines** | `list`, `show`, `run`, `runs`, `show-run`, `approve`, `cancel`, `logs`, `delete` |
| **Workflows** | `list`, `show`, `run`, `invoke`, `retry`, `logs` |
| **Notifications** | `send` |
| **Environments** | `create`, `deploy`, `undeploy`, `list`, `show`, `services`, `health`, `diagnose`, `logs`, `rollback`, `reset`, `recover`, `suspend`, `resume`, `delete` |
| **FS** | `sync` (`init`, `status`, `logs`, `pause`, `resume`, `disconnect`, `mode`, `conflicts`, `resolve`, `doctor`), `share`, `shares`, `revoke`, `publish`, `public-paths` |
| **Secrets** | `list`, `show`, `set`, `delete`, `import`, `validate`, `ensure`, `export` |
| **Agents** | `config`, `runtime-status`, `sync` (deprecated), `delete`, `delete-team` |
| **Teams** | `list` |
| **Threads** | `create`, `list`, `show`, `messages`, `post`, `follow`, `distill`, `delete` |
| **KV** | `set`, `get`, `list`, `mget`, `delete` |
| **Memory** | `set`, `get`, `list`, `delete`, `search` |
| **Search** | `search` (unified cross-source) |
| **Packs** | `status`, `resolve` |
| **Skills** | `install` |
| **Harnesses** | `list`, `get` |
| **Database** | `schema`, `rls`, `rls init`, `sql`, `migrate`, `migrations`, `new`, `reset`, `wipe`, `status`, `rotate-credentials`, `scale`, `destroy`, `snapshot`, `snapshots`, `restore`, `backup-status` |
| **Manifest** | `validate` |
| **App Links** | `list`, `plan`, `explain` |
| **Providers** | `list`, `discover` |
| **Analytics** | `summary`, `jobs`, `pipelines`, `env-health`, `cost-by-agent` |
| **Webhooks** | `create`, `list`, `show`, `delete`, `replay` |
| **API** | `list`, `show`, `spec`, `refresh`, `examples`, `call`, `generate`, `diff` |
| **GitHub** | `setup`, `status`, `test` |
| **Events** | `list`, `show`, `emit` |
| **Traces** | `query` |
| **Chat** | `simulate` |
| **Identity** | `link` |
| **Integrations** | `list`, `configure`, `config`, `unconfigure`, `setup-info`, `connect`, `slack connect`, `slack install-url`, `test`, `update` |
| **Supervision** | `supervise` |
| **Migrate** | `skills-to-packs` |
| **Local Stack** | `up`, `down`, `status`, `health`, `reset`, `logs` |
| **User** | `show` |
| **Admin** | `users`, `invite`, `access-requests`, `balance`, `usage`, `pricing`, `receipts`, `ingress-aliases`, `email bounces` |
| **System** | `status`, `health`, `config`, `settings`, `orchestrator`, `jobs`, `envs`, `env-health`, `env-cost`, `logs`, `pods`, `events` |
