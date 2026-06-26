---
name: eve-troubleshooting
description: Troubleshoot common Eve deploy and job failures using CLI-first diagnostics.
---

# Eve Troubleshooting

Use CLI-first diagnostics. Do not assume cluster access.

## Quick Triage Checklist

```bash
eve system health
eve auth status
eve job list --phase active
```

## Common Issues and Fixes

### Auth Fails or "Not authenticated"

```bash
eve auth logout
eve auth login
eve auth status
```

If SSH key is missing, register it with the admin or follow the CLI prompt to fetch from GitHub.

### Secret Missing / Interpolation Error

```bash
eve secrets list --project proj_xxx
eve secrets set MISSING_KEY "value" --project proj_xxx
```

Verify `.eve/dev-secrets.yaml` exists for local interpolation.

### Deploy Job Failed

```bash
eve job follow <job-id>
eve job diagnose <job-id>
eve job result <job-id>
eve env diagnose <project> <env>     # structured DeployFailure + cluster snapshot
```

Check for registry auth errors, missing secrets, or healthcheck failures.

`eve env diagnose` surfaces a typed `last_deploy_failure` (kind, service, pod, namespace, message) plus the live K8s state. Read the failure `kind` first — the CLI no longer collapses real causes into a bare `HTTP request failed`. Compare the diagnose `manifest_hash` against the latest sync to spot applied-release drift.

### Sentinel Slack Alerts

Slack pings from the platform sentinel point at a degraded env. Don't act on the alert text alone — pull the project/env out of it and re-confirm with `eve env diagnose <project> <env>`. If the env reads healthy, the alert was a transient that has self-healed; if not, follow the standard deploy-failure triage above.

### Missing Magic-Link or Invite Email

Pre-flight checks usually catch SES misconfig, but if a recipient swears the mail never landed:

```bash
eve admin email bounces list --recipient user@example.com --limit 20
eve admin email bounces list --event-type Bounce
eve admin email bounces list --event-type Complaint
```

The `email_delivery_events` table is the source of truth — `Bounce` / `Complaint` / `Reject` rows explain silent SES drops. No row at all means the send never happened; re-check `x-eve.branding` reply-to/support emails and the project's `x-eve.auth` policy.

### Magic-Link "Already Used" on First Click

Mail-security scanners (Defender SafeLinks, Mimecast, Proofpoint, Barracuda, IronPort) prefetch URLs and burn single-use OTPs. The platform now wraps every action link behind an SSO interstitial that requires an explicit click, so prefetches no longer consume the token. If a user still hits "already used":

- The wrap has expired (1h TTL) — have them request a fresh magic link.
- They genuinely clicked twice — the second click hits a consumed wrap.
- Telemetry: rows with `get_count > 1` in `magic_link_wraps` are expected for protected mailboxes; only `consumed_at` matters.

### Magic-Link or Invite Lands on the Generic SSO Page

The redirect allowlist rejected the app's custom-domain origin, so SSO fell back to the cluster landing page. Confirm the project's `x-eve.auth.allowed_redirect_origins` (or its registered `custom_domains` rows) include the app origin — origin only, `scheme://host[:port]`, https unless local. Then re-sync:

```bash
eve project sync
eve project auth-context <project_id>     # shows the resolved allowlist
```

Paths, queries, fragments, and userinfo are rejected at sync time, so a stray `https://app.example.com/callback` in the manifest will surface there.

### `/session` 401 on a Custom-Domain App

Browsers strip `SameSite=Lax` cookies on cross-site requests, so a custom-domain app hitting `sso.<cluster>` will see no `eve_sso_rt` and a 401. The SSO broker now sets `SameSite=None; Secure` when `EVE_SSO_SECURE_COOKIES=true`. Verify in the broker logs:

```
[eve-sso] Secure cookies: true (SameSite=none)
```

In the browser devtools, the `eve_sso_rt` cookie on `.<EVE_DEFAULT_DOMAIN>` must show `SameSite=None; Secure; HttpOnly`. If it shows `Lax`, the broker is running in local-http mode — set `EVE_SSO_SECURE_COOKIES=true` and redeploy. Local k3d on `*.lvh.me` keeps `Lax` deliberately (same parent site).

### Domain-Signup Manifest Rejected After Upgrade

The v1 shape (`domains: [string]` plus a block-level `target_org`) is no longer accepted as of 2026-05-12 — manifest sync rejects on first sight. Migrate to v2:

```yaml
x-eve:
  auth:
    org_access:
      domain_signup:
        enabled: true
        domains:
          - { domain: acme.com, target_org: org_acme, role: member }
          - { domain: partner.example, target_org: org_partner }
```

Each rule must declare its own `target_org`, and each `target_org` must already appear in the project's `allowed_orgs`. Free-email domains (`free-mail.example`, `outlook.com`, ...) emit a coherence warning, not a reject — declaring them is almost always wrong. See `references/manifest.md` and `docs/system/auth.md#domain-based-signup` for the full v2 shape.

### Workflow Step Token "Resource Denied"

Workflow step jobs now carry a `token_scope` claim derived from workflow- and step-level `scope` blocks (intersected with any API-supplied scope). If a step gets `denied` on an org filesystem path, env DB table, or Cloud FS mount, the scope is the suspect:

```bash
eve job show <job-id> --json | jq '.token_scope'
```

Compare the claim against the manifest's workflow/step `scope`. Step scope intersects workflow scope — it can only narrow, never widen. If the step needs a path the workflow forbids, broaden the workflow `scope` (or drop it). Request-supplied `scope` requires the `jobs:harness_override` permission; there is no `--scope-*` CLI flag yet.

### Custom Domain Issues

```bash
eve domain verify <hostname>     # DNS check + cert state + next steps
eve domain status <hostname>     # which env owns it
eve domain list --env <env>      # everything bound to this env
```

Common causes:
- **DNS not resolved**: `verify` will print the expected target and `dns_result.verified: false` — fix the CNAME/A record before re-running deploy.
- **Cert pending**: cert-manager HTTP-01 challenge in flight; re-run `verify` after a minute.
- **First-bind-wins conflict**: another env already claimed the hostname. Use `eve domain transfer <host> --to <env>` and redeploy, or scope the domain per-env via `environments.<env>.overrides`.

### Registry Push Fails with UNAUTHORIZED

If build jobs fail with `UNAUTHORIZED: authentication required` when pushing:

1. Verify secrets are set: `eve secrets list --project proj_xxx`
2. If using a custom BYO registry, verify credentials map to `registry.host`
3. Confirm the imagePull metadata in your manifest is correct
4. Add OCI source label to Dockerfile: `LABEL org.opencontainers.image.source="https://github.com/ORG/REPO"`

Some registries require repository-linked package metadata or workspace-level auth alignment.

### Build Failures

#### Symptoms
- Pipeline fails at build step
- `eve build diagnose` shows run status = `failed`

#### Triage
```bash
eve build list --project <id>          # Find recent builds
eve build diagnose <build_id>          # Full state dump
eve build logs <build_id>              # Raw build output
```

#### Common Causes

**Registry authentication:**
- If using custom registry mode, verify `REGISTRY_USERNAME` and `REGISTRY_PASSWORD` secrets are set (or provider-equivalent registry credentials). With managed registry (`registry: "eve"`), this step is usually not required.
- Ensure credentials can access the configured registry account and namespace
- Check: `eve secrets list --project <id>`

**Dockerfile issues:**
- Service must have `build.context` in manifest pointing to directory with Dockerfile
- Dockerfile path defaults to `<context>/Dockerfile`
- Multi-stage builds work with BuildKit; may fail with Kaniko

**Workspace/clone errors:**
- Build requires workspace at the correct git SHA
- Check `eve build diagnose` for workspace preparation errors

**Image push failures:**
- OCI labels help link packages to repos: add `LABEL org.opencontainers.image.source="https://github.com/OWNER/REPO"` to Dockerfile
- Ensure registry host and auth match manifest `registry.host` when using BYO/custom registry

### Job Stuck or Blocked

```bash
eve job show <job-id>
eve job dep list <job-id>
```

Resolve dependencies or update phase with `eve job update` if appropriate.

Stale-attempt recovery now covers all assignees and graceful agent-runtime shutdown, and agent-runtime pod death no longer strands attempts. If a job still looks stuck after a recent restart, give the recovery loop one cycle before manually intervening — it usually reclaims on its own.

### Chat Route Doesn't Match

Chat route matching is now case-insensitive on the regex side. If a route still fails to fire, the pattern itself is the suspect — not the casing. Re-check the `match` regex in your chat config, then resync the manifest.

### Agent-Runtime Org Discovery

Agent-runtime auto-discovers orgs at startup; you no longer need an `org_default` config entry. If a fresh deploy can't see an org's jobs, check that the org actually has at least one project + agent registered, then check agent-runtime logs — don't go looking for a missing `org_default`.

### App Not Reachable After Deploy

- Confirm deploy job succeeded (`eve job result`).
- Validate ingress host pattern: `{service}.{orgSlug}-{projectSlug}-{env}.{domain}`.
- Ensure service port matches `x-eve.ingress.port`.

## Escalation

If CLI output is insufficient, collect:

- `eve system health`
- `eve job diagnose <job-id>`
- manifest diff (recent changes)

Then hand off to the platform operator.
