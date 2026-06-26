# CLI: Deploy + Debugging

## Use When
- You need environment deploy, reset, rollback, or alias/recovery operations.
- You need CLI-first incident response steps for jobs and environments.
- You need local stack lifecycle commands for k3d.

## Load Next
- `references/deploy-debug.md` for system-level platform diagnostics.
- `references/pipelines-workflows.md` when deploy is pipeline-triggered.
- `references/cli-jobs.md` for job-level investigation.

## Ask If Missing
- Confirm whether the deployment is k3d, docker, or cloud production.
- Confirm whether deployment is pipeline-triggered or direct (`--direct`).
- Confirm target environment and release/build artifacts available before changing state.

## Environments (Deployments)

```bash
# Deploy
eve env deploy <env-name> --ref <sha-or-branch>
  [--repo-dir ./my-app]                                 # Resolve ref from local repo
  [--direct]                                            # Bypass pipeline
  [--inputs '{"k":"v"}']
  [--image-tag <tag>]                                   # Use specific image tag
  [--watch] [--timeout 300]                             # Wait for deployment to complete
  [--skip-preflight]                                    # Skip preflight checks
eve env deploy <env-name> --release-tag v1.2.3            # Deploy by release tag (no ref needed)

# Create / manage
eve env create <name> --type persistent|temporary
  [--namespace <ns>] [--db-ref <ref>]
eve env list [project]
eve env show <project> <env>
eve env services <project> <env>                        # List running services
eve env health <project> <env>                          # Health check
eve env diagnose <project> <env> [--events]             # Full diagnostic + K8s events
eve env diagnose <project> <env> --request <id> --json  # Request-level logs/events/deploy/traces

# Logs
eve env logs <project> <env> <service>
  [--since 5m] [--tail 100] [--grep "error"]
  [--follow] [--filter req_id=req_01h...] [--filter level=error]
  [--pod <name>] [--container <name>]
  [--previous] [--all-pods]

# Traces
eve traces query --project <project> --request-id <id> --json
eve traces query --project <project> --service <service> --since 5m --error
eve traces query --project <project> --service <service> --route "POST /api/items" --since 1h --p99

# Recovery
eve env rollback <env> --release <id|tag|previous>      # Roll back to a known release
  [--project <id>] [--skip-preflight]
eve env reset <env> [--release <id|tag|previous>]       # Teardown workloads and redeploy
  [--project <id>] [--force]
  [--danger-reset-production] [--skip-preflight]
eve env recover <project> <env>                         # Analyze state, suggest recovery command

# Lifecycle
eve env suspend <project> <env> --reason "maintenance"  # Pause environment
eve env resume <project> <env>                          # Resume environment
eve env undeploy <env> [--project=<id>] [--force]        # Tear down K8s deployment, keep config
eve env delete <project> <env> [--force]                # Destroy environment
  [--danger-delete-production]                          # Required for production envs
```

Notes:
- If a pipeline is configured, `eve env deploy` triggers that pipeline. Use `--direct` to bypass.
- Deploy accepts either `--ref` (git SHA) or `--release-tag` (named release) -- provide exactly one.
- When `--repo-dir` points to a repo containing `.eve/manifest.yaml`, the manifest is expanded (`workflows.*.$ref` and `agent.prompt_file`) and automatically synced to the API before deploying. If no local manifest is found, the server-side manifest is used as-is.
- **Auto-creation**: `eve env deploy` auto-creates the environment if it is defined in `manifest.environments` but does not yet exist in the database.
- Deploy error messages list environments defined in the manifest if the provided target name is invalid.
- `env show` displays ingress aliases (custom domain mappings) when present.
- `rollback` redeploys a previous release without teardown; `reset` tears down first then redeploys.
- `env undeploy` tears down the K8s namespace but preserves the environment record. Sets `deploy_status` to `undeployed` and clears `current_release_id`. Redeploy later with `eve env deploy`.
- `env suspend/resume` pause and resume without deletion.
- `env logs --follow` streams via SSE — no polling loop required. Combine with
  `--filter k=v` (repeatable, ANDs together) for structured matching on JSON
  log lines; falls back to `--grep` substring on non-JSON output. Pod restarts
  emit divider events; `--all-pods` merges across the deployment.
- `env diagnose --request <req_id>` is the integrator: one call returns logs
  (across services, merged by timestamp), K8s events, the active release at
  request time, optional audit rows (opt-in via manifest `x-eve.audit_log_table`),
  and trace pointers. Use `--window <seconds>` to widen the search (default 60s).
- `eve traces query` reads the OTEL trace store directly so agents can inspect
  spans without AWS console access. Pair with a `request_id` from the logs.

## Debugging (CLI-first)

See `references/deploy-debug.md` for the debugging ladder and health workflows.

Quick reference:
- `eve job diagnose <id>` -- primary job debugging entry point
- `eve job follow <id>` -- stream harness logs in real time
- `eve job runner-logs <id>` -- K8s pod logs for startup failures
- `eve env diagnose <project> <env>` -- environment health, K8s events, and HTTP/TCP ingress diagnostics
- `eve env diagnose <project> <env> --request <id> --json` -- one request across logs, events, deploy metadata, audit rows, and traces
- `eve env logs <project> <env> <service> --follow --filter req_id=<id>` -- live app-service logs with structured filters
- `eve traces query --project <project> --request-id <id> --json` -- trace spans without console access
- `eve tcp-ingress test <project> <env> --listener <name>` -- raw TCP connect probe for `x-eve.tcp_ingress` listeners
- `eve env recover <project> <env>` -- analyze state and suggest recovery action

Ingress checks:
- `eve env diagnose <project> <env> --json | jq '.http_ingress'` -- confirm HTTP hosts, controller flavor, requested/effective timeout, and body-size values.
- `eve env diagnose <project> <env> --json | jq '.tcp_ingress'` -- inspect public raw TCP listeners and provisioning state.

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
```

Contributor helper for public raw TCP ingress tests:

```bash
./bin/eh k8s start --tcp-ports 33400,33500 --recreate
./bin/eh k8s deploy
eve tcp-ingress test <project> <env> --listener a1-gt06
```

Existing k3d clusters must be recreated to add new host port mappings.

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
- `reset` is equivalent to `down --destroy` followed by `up`.
- `eve local up` now supports registry override:
  - `ECR_REGISTRY=<registry>` sets image host (for example, ECR mirror URLs).
  - `ECR_NAMESPACE=<namespace>` sets repository namespace (defaults to `eve-horizon`).
- `eve local up` writes namespace annotation `eve-managed-by=cli`. It will refuse to overwrite stacks currently managed by other tooling (for example, `./bin/eh k8s deploy`) unless reset first.
- The cluster binds ports 80/443 on localhost via k3d's load balancer.
- Kube context is set to `k3d-eve-local` automatically.
