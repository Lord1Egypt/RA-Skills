# CLI: Auth + Access

## Use When
- You need to establish identity (`eve auth login`, bootstrap, bootstrap status).
- You need to create and audit service accounts, groups, roles, and binding policy.
- You need token and OAuth credential refresh/sync workflows.

## Load Next
- `references/secrets-auth.md` for scope-based secrets and auth policy context.
- `references/overview.md` for role and tenant context.
- `references/cli-org-project.md` when auth commands follow org/project creation flows.

## Ask If Missing
- Confirm whether the user is on staging, local docker, or k3d.
- Confirm whether actions are user-driven (`auth login`) or machine-driven (`service-account`, `migrate`).
- Confirm if policy checks need org/project/group scope.

## Profile

Profiles are repo-local configuration bundles. They store API URL, default org/project, harness preference, and auth identity.

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

## Auth

```bash
# Login / logout
eve auth login --email you@example.com                  # SSH-key login (default)
  [--ttl 30]                                            # Token TTL in days (1-90)
  [--ssh-key ~/.ssh/id_ed25519]                         # Explicit key path
  [--password]                                          # Supabase password login
  [--supabase-url <url>]                                # Custom Supabase endpoint
eve auth logout                                         # Clear local credentials

# Identity
eve auth status                                         # Show current auth state
eve auth whoami                                         # Alias for status
eve auth permissions                                    # List effective permissions
eve auth token                                          # Print current access token (raw)

# Bootstrap (first-time platform setup)
eve auth bootstrap --email you@example.com --token $EVE_BOOTSTRAP_TOKEN
  [--ssh-key <path>] [--display-name "Name"]
eve auth bootstrap --status                             # Check bootstrap eligibility

# Self-service onboarding
eve auth request-access --org "My Company" --email you@example.com
  [--ssh-key <path>] [--nostr-pubkey <hex>]
  [--wait]                                              # Poll until approved
eve auth request-access --status <request_id>           # Check request status

# Admin token minting
eve auth mint --email user@example.com --ttl 7          # Mint token for another user
  [--org <id>] [--project <id>] [--role admin]

# AI tool credential check
eve auth creds                                          # Show Claude + Codex creds
eve auth creds --claude                                 # Only check Claude
eve auth creds --codex                                  # Only check Codex
eve auth creds --json                                   # Machine-readable
# creds now shows Claude token type: "setup-token (long-lived)" vs "oauth (short-lived, ~15h)"
# For Codex, picks the freshest token across ~/.codex/auth.json and ~/.code/auth.json

# Managed Claude auth probe
eve auth verify --harness claude --project proj_xxx --json
# Creates a short managed Claude job, checks claude_auth_selected, apiKeySource != none,
# and model reply EVE_AUTH_OK. JSON includes key, scope, token class, and apiKeySource.

# OAuth token sync to Eve
eve auth sync                                           # Sync to user-level (default)
eve auth sync --org org_xxx                             # Sync to org-level
eve auth sync --project proj_xxx                        # Sync to project-level
eve auth sync --dry-run                                 # Preview without syncing
eve auth sync --claude                                  # Only sync Claude tokens
eve auth sync --codex                                   # Only sync Codex tokens
# sync warns if Claude token is short-lived OAuth (not sk-ant-oat01- prefix).
# Fix: run `claude setup-token` then re-run `eve auth sync`.

# Service accounts (machine identity)
eve auth create-service-account --name "pm-backend" --org org_xxx \
  --scopes "jobs:create,jobs:read,projects:read"
eve auth list-service-accounts --org org_xxx
eve auth revoke-service-account --name pm-backend --org org_xxx
```

Notes:
- SSH is the default CLI login method. CLI auto-fetches SSH keys from GitHub when none are registered.
- Nostr auth uses NIP-98 request headers or kind-22242 challenge-response.
- `auth token` outputs the raw Bearer token for scripting and curl.
- `auth status` now resolves the displayed role from the active profile's org membership and lists all org memberships with `(active)` marker.
- `auth mint` is admin-only; creates tokens scoped to specific orgs/projects/roles.
- Service accounts create machine identities with scoped tokens for app backends.
- On local/non-production stacks, `auth bootstrap` attempts server-side recovery even after bootstrap is marked complete.
- `request-access --wait` tip: include `--wait` to auto-poll and log in on approval instead of manually polling with `--status`.

## Access (Roles, Bindings, Policy-as-Code)

```bash
# Permission queries (require org admin)
eve access can --org org_xxx --user user_abc --permission chat:write
  [--group <slug>] [--resource-type <type>]             # Scope check to group/resource
  [--resource <id>] [--action <action>]
eve access can --org org_xxx --service-principal sp_xxx --permission jobs:read
eve access explain --org org_xxx --user user_abc --permission jobs:admin
  [--project proj_xxx]                                  # Trace permission origin

# Custom roles (additive overlays on base membership roles)
eve access roles create pm_manager --org org_xxx --scope org \
  --permissions jobs:read,jobs:write,threads:read,chat:write
eve access roles list --org org_xxx
eve access roles show pm_manager --org org_xxx
eve access roles update pm_manager --org org_xxx --add-permissions events:read
eve access roles delete pm_manager --org org_xxx

# Role bindings
eve access bind --org org_xxx --user user_abc --role pm_manager
  [--project proj_xxx] [--group <slug>]                 # --project required (no profile fallback)
  [--scope-json '{"orgfs":"/eng/*","envdb":"schema:app"}']  # Restrict access paths
eve access bindings list --org org_xxx [--project proj_xxx]
eve access unbind --org org_xxx --user user_abc --role pm_manager
  [--project proj_xxx]

# Access groups (fine-grained data-plane authorization)
eve access groups create "Engineering" --org org_xxx [--slug eng-team]
  [--description "..."]                                      # Name as positional arg or --name
eve access groups list --org org_xxx
eve access groups show <slug-or-id> --org org_xxx
eve access groups update <slug-or-id> --org org_xxx [--name] [--slug] [--description]
eve access groups delete <slug-or-id> --org org_xxx

# Group membership
eve access groups members list <slug-or-id> --org org_xxx
eve access groups members add <slug-or-id> --org org_xxx --user <id>
eve access groups members add <slug-or-id> --org org_xxx --service-principal <id>
eve access groups members remove <slug-or-id> --org org_xxx --user <id>

# Memberships introspection (effective access for a principal)
eve access memberships --org org_xxx --user <id>
eve access memberships --org org_xxx --service-principal <id>

# Policy-as-code (declarative .eve/access.yaml)
eve access validate --file .eve/access.yaml             # Validate syntax
eve access plan --file .eve/access.yaml --org org_xxx   # Preview changes
  [--json]
eve access sync --file .eve/access.yaml --org org_xxx   # Apply changes
  [--yes] [--prune]                                     # --prune removes undeclared
```

Notes:
- `can`/`explain` work for users, service principals, and groups.
- Custom roles are additive -- they layer permissions on top of base membership roles.
- `--prune` removes roles/bindings present in API but absent from the YAML file.
- Groups are first-class authorization primitives for data-plane segmentation. Bindings can carry `--scope-json` to restrict orgfs/orgdocs/envdb access paths.
- `bind --project` must be passed explicitly when creating project-scoped bindings; the CLI no longer falls back to the profile's default project to avoid silently mis-scoping bindings.
- Policy sync validates that bindings with data-plane permissions (orgfs/orgdocs/envdb) include matching scope constraints. Bindings without required scopes fail validation.
