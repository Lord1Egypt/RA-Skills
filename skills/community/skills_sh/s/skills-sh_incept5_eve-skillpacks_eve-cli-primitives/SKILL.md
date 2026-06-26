---
name: eve-cli-primitives
description: Core Eve CLI primitives and capabilities for app developers. Use as the quick reference for commands and flows.
---

# Eve CLI Primitives

Use this skill as the command map for Eve. Keep examples short and concrete.

## Profiles (API Target + Defaults)

```bash
# Create and use a profile
eve profile create staging --api-url https://api.eve.example.com
eve profile use staging

# Set defaults to avoid repeating flags
eve profile set --default-email you@example.com --default-ssh-key ~/.ssh/id_ed25519
eve profile set --org org_xxx --project proj_xxx

# Inspect current profile
eve profile show
```

## Authentication

```bash
eve auth login
eve auth status
eve auth logout
eve auth permissions

# Sync local OAuth tokens for agent harnesses (optional)
eve auth sync

# Nostr challenge (API-level, no CLI command yet)
# POST /auth/challenge {"provider": "nostr", "pubkey": "<hex>"}
```

## Orgs and Projects

```bash
eve org list
eve org ensure my-org --slug myorg

eve project list
eve project ensure --name "My App" --slug my-app --repo-url git@github.com:me/my-app.git --branch main

# Membership management
eve org members --org org_xxx
eve org members add user@example.com --role admin --org org_xxx
eve org members remove user_abc --org org_xxx

eve project members --project proj_xxx
eve project members add user@example.com --role admin --project proj_xxx
eve project members remove user_abc --project proj_xxx
```

**URL impact:** The org `--slug` and project `--slug` directly form your deployment URLs and K8s namespaces:
- URL: `{service}.{orgSlug}-{projectSlug}-{env}.{domain}` (e.g., `api.myorg-my-app-staging.eve.example.com`)
- Namespace: `eve-{orgSlug}-{projectSlug}-{env}` (e.g., `eve-myorg-my-app-staging`)

Choose slugs carefully — they are immutable after creation.

## Environments and Deploys

```bash
# Create a persistent environment
eve env create staging --project proj_xxx --type persistent

# Inspect environments
eve env list --project proj_xxx
eve env show staging --project proj_xxx

# Deploy an environment (requires --ref with 40-char SHA or a ref resolved against --repo-dir)
eve env deploy staging --ref main --repo-dir .

# When environment has a pipeline configured, the above triggers the pipeline.
# Use --direct to bypass pipeline and deploy directly:
eve env deploy staging --ref main --repo-dir . --direct

# Pass inputs to pipeline:
eve env deploy staging --ref main --repo-dir . --inputs '{"key":"value"}'

# Diagnostics
eve env diagnose proj_xxx staging
eve env diagnose proj_xxx staging --request <req_id>     # request-level integrated diagnose
eve env logs proj_xxx staging <service>
eve env logs proj_xxx staging <service> --follow         # stream logs
eve env logs proj_xxx staging <service> --filter route=/api/x --filter status=500
eve env delete proj_xxx staging
```

`--filter k=v` is repeatable; common keys: `route`, `status`, `level`, `request_id`. Use `--grep` for free-text matching, `--since`/`--tail` to bound the window.

## Jobs (Create + Observe)

```bash
eve job create --description "Review auth flow"
eve job list --phase active
eve job show <job-id>
eve job follow <job-id>
eve job diagnose <job-id>
eve job result <job-id>

# Per-job harness + env overrides (Eden-style per-request brain selection)
eve job create --description "..." \
  --harness-override-file ./profile.json \
  --env-override OPENAI_API_KEY='${secret.OPENAI_KEY}' \
  --env-override MODEL_ENDPOINT=https://qwen.local
```

`--harness-override-file` takes a JSON object `{harness, model?, reasoning_effort?, variant?, temperature?}`. `--env-override KEY=VALUE` is repeatable, validates UPPER_SNAKE_CASE keys, and supports `${secret.KEY}` interpolation resolved at spawn time.

## Coordination (Supervise + Threads)

```bash
eve supervise <job-id> --timeout 60
eve thread messages <thread-id> --since 10m
eve thread post <thread-id> --body '{"kind":"directive","body":"focus on auth"}'
eve thread follow <thread-id>
```

## Agents + Chat

```bash
# Sync agent/team/chat configuration from repo
eve agents sync --project proj_xxx --ref main --repo-dir .
# Inspect resolved agent config (from latest sync)
eve agents config --project proj_xxx --json
# Simulate chat routing without Slack
eve chat simulate --project proj_xxx --team-id T123 --channel-id C456 --user-id U789 --text "hello"

# Set org default agent slug (fallback when no slug matches)
eve org update org_xxx --default-agent mission-control
```

## Packs (AgentPacks)

```bash
eve packs status
eve packs resolve --dry-run
eve migrate skills-to-packs
```

Slack gateway commands (run inside Slack):

```text
@eve <agent-slug> <command>
@eve agents list
@eve agents listen <agent-slug>
@eve agents unlisten <agent-slug>
@eve agents listening
```

Nostr commands (via DM to platform pubkey):

```text
/agent-slug command text
agent-slug: command text
```

## Secrets

```bash
eve secrets list --project proj_xxx
eve secrets set API_KEY "value" --project proj_xxx
eve secrets delete API_KEY --project proj_xxx
eve secrets show API_KEY --project proj_xxx
eve secrets ensure --project proj_xxx --keys API_KEY
eve secrets export --project proj_xxx --keys API_KEY
```

## System Admin (if authorized)

```bash
eve system status
eve system jobs
eve system envs
eve system env-health --json
eve system env-cost --all
eve system logs api --tail 50
eve system pods
eve system events
```

`eve system env-cost` returns month-to-date environment allocation snapshots
from the admin API. It is a snapshot view, not a live OpenCost query; stale or
unavailable estimates are labelled in the output.

## Workflows

```bash
eve workflow list
eve workflow run qa-review --input '{"task":"audit"}'
eve workflow invoke qa-review --input '{"task":"audit"}'
eve workflow run qa-review --input '{...}' --env-override MODEL=opus-4.5
eve workflow logs job_abc123
```

`--env-override KEY=VALUE` is repeatable on `run` and `invoke`; values flow through to each step's job as `env_overrides`.

## Integrations (Slack, Nostr, GitHub)

```bash
eve integrations list --org org_xxx
eve integrations slack connect --org org_xxx --team-id T123 --token xoxb-test
eve integrations test <integration_id> --org org_xxx

# Nostr integration (via API)
# POST /integrations {"provider": "nostr", "account_id": "<platform-pubkey>", ...}
```

## Pipelines and Workflows

```bash
eve pipeline list
eve pipeline show <project> <name>
eve pipeline run <name> --ref <sha> --env <env> --repo-dir ./my-app

eve workflow list
eve workflow show <project> <name>
eve workflow run <project> <name> --input '{"k":"v"}' [--env-override KEY=VALUE]
eve workflow invoke <project> <name> --input '{"k":"v"}' [--env-override KEY=VALUE] [--no-wait]
eve workflow logs <job-id>
```

## Builds

Builds are first-class primitives that track image construction from input (spec) to execution (run) to output (artifacts).

```bash
# List builds for a project
eve build list [--project <id>]

# Create a build spec
eve build create --project <id> --ref <sha> --manifest-hash <hash>

# Show build spec details
eve build show <build_id>

# Start a build run
eve build run <build_id>

# List runs for a build
eve build runs <build_id>

# View build logs
eve build logs <build_id> [--run <run_id>]

# List produced image artifacts (digests)
eve build artifacts <build_id>

# Full diagnostic dump (spec + runs + artifacts + logs)
eve build diagnose <build_id>

# Cancel an active build
eve build cancel <build_id>
```

Builds happen automatically during pipeline `build` steps. Use `eve build diagnose` to debug build failures.

## Traces (OTEL)

Agent-queryable trace store. Pair with `eve env diagnose --request <id>` and `eve env logs --filter request_id=<id>` for end-to-end request triage.

```bash
eve traces query --request-id <id>                    # spans for a single request
eve traces query --trace-id <id>                      # spans for a known trace
eve traces query --service api --since 15m --error    # recent errors in a service
eve traces query --route /api/projects --p99          # p99 latency for a route
eve traces query --request-id <id> --json             # machine-readable
```

One of `--request-id`, `--trace-id`, `--since`, `--route`, or `--error` is required. `--no-cache` bypasses the trace cache.

## Custom Domains

```bash
eve domain list [--env <name>] [--project <id>]
eve domain verify <hostname>             # check DNS and show activation status
eve domain status <hostname>             # show domain status and owning env
eve domain transfer <hostname> --to <env>  # move ownership between envs
eve domain unbind <hostname>             # clear binding so next deploy claims it
eve domain remove <hostname>             # delete the domain entirely
```

## System Health

```bash
eve system health
```

## Harnesses (Optional)

```bash
eve harness list
eve harness list --capabilities
eve harness get mclaude
eve agents config --json
```

## Notes

- Use `--project` if no default project is set in the profile.
- Integrations are org-scoped; use `--org` for integrations commands.
- Prefer `eve job ...` (singular) for job commands.
