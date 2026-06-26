---
name: eve-deploy-debugging
description: Deploy and debug Eve-compatible apps via the CLI, with a focus on staging environments.
---

# Eve Deploy and Debug

Use these steps to deploy and diagnose app issues quickly.

## Environment Setup

- Get the staging API URL from your admin.
- Create and use a profile:

```bash
eve profile create staging --api-url https://api.eve.example.com
eve profile use staging
```

## Infrastructure Change Policy

Never run `kubectl apply`, `helm install`, or any direct Kubernetes resource creation against shared infrastructure. All infrastructure changes go through Terraform. Use the Eve CLI (`eve env`, `eve env deploy`) to manage application deployments — the platform handles the underlying k8s resources.

## Deploy Flow (Staging)

```bash
# Create env if needed
eve env create staging --project proj_xxx --type persistent

# Deploy (requires --ref with 40-char SHA or a ref resolved against --repo-dir)
eve env deploy staging --ref main --repo-dir .

# When environment has a pipeline configured, the above triggers the pipeline.
# Use --direct to bypass pipeline and deploy directly:
eve env deploy staging --ref main --repo-dir . --direct

# Pass inputs to pipeline:
eve env deploy staging --ref main --repo-dir . --inputs '{"key":"value"}'
```

### Deploy Polling Flow

When `eve env deploy` is called:

1. **Direct deploy** (no pipeline): Returns `deployment_status` directly. Poll health endpoint until `ready === true`.
2. **Pipeline deploy**: Returns `pipeline_run_id`. Poll `GET /pipelines/{name}/runs/{id}` until all steps complete, then check health.

Deploy is complete when: `ready === true` AND `active_pipeline_run === null`.

## Observe the Deploy

```bash
eve job list --phase active
eve job follow <job-id>              # Real-time SSE streaming
eve job watch <job-id>               # Poll-based status updates
eve job diagnose <job-id>            # Full diagnostic
eve job result <job-id>              # Final result
eve job runner-logs <job-id>         # Raw worker logs
```

### Real-Time Debugging (3-Terminal Approach)

```bash
# Terminal 1: Pipeline/job progress
eve job follow <job-id>

# Terminal 2: Environment health
eve env diagnose <project> <env>

# Terminal 3: System-level logs
eve system logs
```

## Debugging Workflows

### Job Won't Start

1. Check dependencies: `eve job dep list <job-id>`
2. Check if blocked: `eve job show <job-id>` → look at `blocked_by`
3. Verify environment readiness: `eve env show <project> <env>`
4. Check orchestrator: `eve system orchestrator status`

### Job Failed

1. Get the error: `eve job diagnose <job-id>`
2. Check logs: `eve job follow <job-id>` or `eve job runner-logs <job-id>`
3. If build failure: `eve build diagnose <build-id>`
4. If secret failure: `eve secrets list --project <project_id>`

### Job Stuck Active

1. Check if waiting for input: `eve job show <job-id>` → `effective_phase`
2. Check thread messages: `eve thread messages <thread-id>`
3. Check runner pod: `eve system pods`

### System Issues

1. API health: `eve system health`
2. Orchestrator: `eve system orchestrator status`
3. Recent events: `eve system events`

### Deploy Failed (Structured Diagnosis)

When a deploy fails, prefer structured output over raw HTTP errors:

```bash
eve env diagnose <project> <env>
```

`eve env diagnose` surfaces a typed `last_deploy_failure` (kind, service, pod, namespace, message), the live K8s state, and `manifest_hash` of the deployed release versus the latest sync — use this to spot applied-release drift before re-running. The CLI no longer hides failures behind a bare `HTTP request failed`.

### Custom Domains

Custom hostnames are declared in the manifest under `x-eve.ingress.domains` and bound on first deploy. To operate them:

```bash
eve domain list --env <env>          # what is bound where
eve domain verify <hostname>         # DNS check + cert state + next steps
eve domain status <hostname>         # which env owns it today
eve domain transfer <hostname> --to <env>   # move ownership across envs in same project
eve domain unbind <hostname>         # release so the next deploy claims it
```

Ownership is **env-scoped with first-bind-wins**: the first env to deploy with a hostname owns it, and other envs referencing the same hostname log `owned by environment "<A>"` and skip rendering. Use `transfer` + redeploy (or scope per-env via `environments.<env>.overrides`) to move it.

### Platform Sentinel Alerts

The platform runs a continuous environment sentinel that posts Slack alerts when envs degrade. Treat a sentinel ping as a starting point: pull the project/env from the alert, then run `eve env diagnose <project> <env>` to confirm the current state before reacting — alerts can lag a self-heal.

The daily Sentinel summary may include a monthly cost section. Use
`eve system env-cost --all` for the full breakdown; it reads stored
environment cost snapshots and labels stale or unavailable estimates. Do not
query OpenCost directly from the Slack-summary path.

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Token expired | `eve auth login` |
| `git clone failed` | Missing credentials | Set `github_token` or `ssh_key` secret |
| `service not provisioned` | Environment not created | `eve env create <env>` |
| `image pull backoff` | Registry auth failed | If using BYO/custom registry, verify `REGISTRY_USERNAME` + `REGISTRY_PASSWORD`; for managed apps use `registry: "eve"` |
| `healthcheck timeout` | App not starting | Check app logs, verify ports in manifest |

## Build Failures

If a deploy pipeline fails at the build step:

```bash
eve build list --project <project_id>
eve build diagnose <build_id>
eve build logs <build_id>
eve secrets list --project <project_id>     # Required for BYO/custom registry: REGISTRY_USERNAME, REGISTRY_PASSWORD
```

Common build failures:
- **Registry auth**: For BYO/custom registry, verify `REGISTRY_USERNAME` and `REGISTRY_PASSWORD` secrets
- **Dockerfile not found**: Check `build.context` path in manifest
- **Multi-stage build failure**: BuildKit handles these correctly; Kaniko may have issues
- **Workspace errors**: Build context not available — check `eve build diagnose`

## Worker Image Registry

Eve publishes worker images to the configured private registry with these variants:

| Variant | Contents |
|---------|----------|
| `base` | Node.js, git, standard CLI tools |
| `python` | Base + Python runtime |
| `rust` | Base + Rust toolchain |
| `java` | Base + JDK |
| `kotlin` | Base + Kotlin compiler |
| `full` | All runtimes combined |

**Version pinning**: Use semver tags (e.g., `v1.2.3`) in production. Use SHA tags or `:latest` in development.

## Platform Environment Variables

Eve automatically injects these into every deployed service container:

| Variable | Purpose |
|----------|---------|
| `EVE_API_URL` | Internal cluster URL for server-to-server calls |
| `EVE_PUBLIC_API_URL` | Public ingress URL for browser-facing apps (when configured) |
| `EVE_SSO_URL` | SSO broker URL for user authentication (when configured) |
| `EVE_PROJECT_ID` | Current project ID |
| `EVE_ORG_ID` | Current organization ID |
| `EVE_ENV_NAME` | Current environment name |

Use `EVE_API_URL` for backend calls. Use `EVE_PUBLIC_API_URL` for browser/client-side code. Services can override any of these by defining them explicitly in their manifest `environment` section.

## Access URLs

- URL pattern: `{service}.{orgSlug}-{projectSlug}-{env}.{domain}`
- Local dev default domain: `lvh.me`
- Ask the admin for the correct domain (staging vs production).

## Environment-Specific Debugging

| Environment | How to Debug |
|-------------|--------------|
| **Local (k3d)** | Direct service access via ingress, `eve system logs` |
| **Docker Compose** | `docker compose logs <service>`, dev-only (no production use) |
| **Kubernetes** | Ingress-based access, `kubectl -n eve logs` as last resort |

## Private Endpoints (Tailscale)

Connect services on private networks (home lab GPUs, internal APIs, dev machines) to the Eve cluster. The platform creates K8s ExternalName services backed by Tailscale egress proxies.

```bash
# Register a private endpoint
eve endpoint add \
  --name lmstudio \
  --provider tailscale \
  --tailscale-hostname mac-mini.tail12345.ts.net \
  --port 1234 \
  --org org_xxx

# List and inspect
eve endpoint list --org org_xxx
eve endpoint show lmstudio --org org_xxx

# Diagnose connectivity
eve endpoint diagnose lmstudio

# Remove
eve endpoint remove lmstudio --org org_xxx
```

Each endpoint gets a stable in-cluster DNS name: `http://{orgSlug}-{name}.eve-tunnels.svc.cluster.local:{port}`. Wire it into apps/agents via secrets:

```bash
eve secrets set LLM_BASE_URL \
  "http://myorg-lmstudio.eve-tunnels.svc.cluster.local:1234/v1" \
  --scope project
```

Diagnostics check: operator status, K8s service existence, DNS resolution, TCP connectivity, and HTTP health.

## Worker Toolchain-on-Demand

The default worker image is `base` (~800MB with Node.js, git, and all harnesses). Toolchains (Python, Rust, Java, Kotlin, media) are injected on-demand via init containers rather than bundled in a fat image.

**Deployment impact**: If an agent job needs toolchains, the runner pod starts init containers that copy toolchain binaries from small pre-built images. First pull adds ~5-10s; subsequent jobs on the same node use cached images.

**Debugging toolchain issues**:

```bash
# Check if toolchains are declared in agent config
# agents.yaml: toolchains: [python]

# If a toolchain binary is missing at runtime:
# 1. Verify agent config has the toolchain declared
# 2. Check init container logs on the runner pod
# 3. Verify toolchain images are available in the registry
```

To use the full image (all toolchains bundled): set `EVE_WORKER_VARIANT=full` or use `--variant full` locally.

## App Undeploy/Delete Lifecycle

Remove environments and clean up resources:

```bash
# Undeploy services from an environment (stops pods, keeps env record)
eve env undeploy <project> <env>

# Delete the environment entirely (removes env record, managed DB, secrets)
eve env delete <project> <env>
```

When a managed DB is attached, `eve env delete` deprovisions it. Secrets scoped to the environment are cleaned up. The environment's pipeline history remains in the audit log.

For app-level cleanup, remove the project:

```bash
eve project delete <project-id>
```

This cascades: environments, secrets, pipeline history, and build artifacts are removed.

## Workspace Janitor

Production disk management for agent workspaces:

- `EVE_WORKSPACE_MAX_GB` — total workspace budget
- `EVE_WORKSPACE_MIN_FREE_GB` — trigger cleanup threshold
- `EVE_SESSION_TTL_HOURS` — auto-evict stale sessions
- LRU eviction when approaching budget; TTL cleanup for idle sessions
- K8s: per-attempt PVCs deleted on completion

## Managed DB TLS

Managed Postgres now ships a trusted CA chain to apps. **Do not** set `rejectUnauthorized: false` or `ssl: { rejectUnauthorized: false }` in service code — verified TLS is the default. If a client errors on cert verification, check that the service is reading `${managed.<db>.url}` rather than a hand-crafted DSN.

## Stable Egress (Allowlisted Source IPs)

When a vendor requires fixed source IPs, opt the service into platform-managed stable egress in the manifest:

```yaml
services:
  poller:
    x-eve:
      networking:
        egress: stable      # default is 'nat'
```

The deployer schedules the pod on the stable-egress node group with `hostNetwork: true` so traffic exits via that node's IGW path. Only opt in when needed (it bypasses NAT and constrains scheduling). See `eve-manifest-authoring` for the full field shape.

## Related Skills

- Local dev loop: `eve-local-dev-loop`
- Secrets: `eve-auth-and-secrets`
- Manifest changes: `eve-manifest-authoring`
