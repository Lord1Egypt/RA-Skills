# Troubleshooting (Symptom-First)

## Use When
- A job, deploy, build, or auth operation is failing and you need a diagnosis path.
- You have an error message or symptom and need the fix, not the architecture.
- You need the quick triage sequence before diving into specific docs.

## Load Next
- `references/deploy-debug.md` for architecture-level debugging (K8s, workers, ingress, custom domains, Sentinel, managed-DB TLS).
- `references/secrets-auth.md` for auth, SSO, mailer/SES suppression, magic-link wrap interstitial, redirect allowlist, and domain-signup details.
- `references/integrations.md` for SES feedback webhook and SNS signature verification specifics.
- `references/manifest.md` for `x-eve.auth` schema (allowed_redirect_origins, org_access, domain_signup v2).
- `references/builds-releases.md` for build-specific failure analysis.
- `references/database-ops.md` for managed-DB connection and migration details.

## Ask If Missing
- Confirm the exact error message or symptom.
- Confirm the environment (staging, local docker, k3d) and `EVE_API_URL`.
- Confirm whether the issue is with a job, deploy, build, or system-level operation.

## Quick Triage (Start Here)

Run these three commands first. They cover 80% of issues.

```bash
eve system health --json                  # 1. Is the platform up?
eve job diagnose <id>                     # 2. What went wrong with this job?
./bin/eh status                           # 3. What's the local environment state?
```

If `system health` fails, the platform is down -- check `eve system logs api`.
If `job diagnose` returns useful output, follow its recommendations.
If `./bin/eh status` shows services stopped, restart with `./bin/eh start <mode>`.

## Auth + Identity Issues

| Symptom | Cause | Fix |
|---|---|---|
| `401 Unauthorized` on every request | No token or expired token | `eve auth login --email <email>` |
| `403 Forbidden` | Missing permission for action | `eve auth permissions` to check catalog; `eve access explain --org <id> --user <id> --permission <perm>` |
| "OAuth token has expired" | Claude auth stale | `./bin/eh auth extract --save` then redeploy |
| Bootstrap fails | Bootstrap window closed or token wrong | Check `eve auth bootstrap --status`; use recovery mode or set `EVE_BOOTSTRAP_TOKEN` |
| Service principal token rejected | Token revoked or scopes insufficient | `eve auth list-service-accounts --org <id>`; recreate if needed |
| `eve auth creds` shows expired | Local AI tool creds stale | Re-auth with the tool (`claude setup-token`, codex login); then `eve auth sync` |

### Mailer / Magic-Link / Invite Delivery

| Symptom | Cause | Fix |
|---|---|---|
| User reports no magic-link or invite email; API logs `Generated GoTrue ... link` and SSO UI says "If your email has access…"; no error | Address sits on SES account-level suppression list — SMTP returns 250 OK but SES silently drops | `eve admin email bounces list --recipient <addr>` to inspect persisted feedback rows; grep API logs for `mailer.suppressed` / `mail.suppressed_drop`; runbook: `docs/runbooks/ses-suppression.md`. Pre-flight check + bounce webhook shipped (feats `0514e0bc`, `438ac902`). |
| Magic-link reported "already used" before the user ever clicked | Mail-security scanner (Defender SafeLinks, Mimecast, Proofpoint, Barracuda, IronPort) prefetched the GoTrue OTP link | Expected — magic-link wrap interstitial requires the user to click "Confirm sign-in" before the GoTrue URL is revealed. Have them re-request. Wrap rows live in `magic_link_wraps` (migration 00098); `get_count > 1` is normal for protected mailboxes. Fix: `b5ef3ea4`. |
| Bounce/complaint webhook calls return 4xx; no rows appear in `email_delivery_events` | SNS posts notifications as `text/plain` (raw JSON string), not `application/json`; older controller couldn't parse | Upgrade past `614fed2b` (`fix(webhooks): parse SNS text/plain body in ses-feedback controller`). On a fork, ensure the `/webhooks/ses-feedback` controller parses text/plain bodies. |
| App invite to a permanently-bounced address: admin sees silent success | Pre-`438ac902` mailer didn't differentiate suppressed addresses from delivered ones | After fix: invite paths re-throw `EmailSuppressedError` so admins see the failure; only the magic-link path swallows it for account-enumeration defense. |

### SSO / Custom-Domain App Auth

| Symptom | Cause | Fix |
|---|---|---|
| User signs in via SSO but the app session isn't recognized; `/session` returns 401; session cookies not sent on the cross-site exchange | App lives on a custom domain different from `EVE_SSO_URL`; cookies need `SameSite=None; Secure` to traverse third-party context | Upgrade past `b3d25503` (`fix(sso): SameSite=None on session cookies for custom-domain apps`). Verify `EVE_SSO_SECURE_COOKIES=true`; confirm container log shows `[eve-sso] Secure cookies: true (SameSite=none)`. In browser devtools, check `eve_sso_rt` / `eve_sso` cookies show `SameSite=None; Secure`. Local k3d on `*.lvh.me` keeps `SameSite=Lax` (same-site). |
| `ACME Portal`-style invite or magic link strands user on SSO landing; "Continue to Sign In" goes to `/login` (dead end for already-signed-in user) | App's off-cluster origin isn't on the redirect allowlist; SSO rewrote `redirect_to` to `${EVE_SSO_URL}/?eve_org_id=...` | Declare the app origin under manifest `x-eve.auth.allowed_redirect_origins` (origin-only, `https` except `localhost`/`*.lvh.me`). Project's own eligible custom domains auto-include. Verify with `eve project auth-context <project_id>` — resolved `allowed_redirect_origins` should list the app host. Fix: `4fa8a1aa`. |
| App that previously had domain-signup working on `release-v0.1.281+` now fails manifest sync | v2 breaking change: `x-eve.auth.org_access.domain_signup.domains` is now a list of `{ domain, target_org, role }` objects; v1 list-of-strings + block-level `target_org` is rejected | Migrate manifest to v2 shape (one `target_org` per rule, declared in precedence order). Existing memberships are not retroactively removed. See `docs/system/auth.md#domain-based-signup`. Breaking change: `e402cee4`. |

### Job Token Resource Scope

| Symptom | Cause | Fix |
|---|---|---|
| A job that previously worked now hits 403 on Cloud FS / org filesystem / org docs / envdb access | Scoped job-token enforcement: `ScopedAccessService` now checks the token's `scope` claim (paths, mounts, schemas/tables), not just permission names | `eve job show <id> --json` and inspect `token_scope`; confirm the workflow step or parent declared the right scope; cross-check against the access binding's `scope_json`. Tokens with no `scope` keep legacy permission-name-only behavior. Shipped: `906424e9`; migration `00096_jobs_token_scope.sql`. |

## Secret Resolution Issues

| Symptom | Cause | Fix |
|---|---|---|
| Job fails during clone | `GITHUB_TOKEN` missing or wrong scope | `eve secrets show GITHUB_TOKEN --project <id>`; re-set with `eve secrets set` |
| "secret resolution failed" | `EVE_INTERNAL_API_KEY` missing | Set on both API and worker; restart |
| Empty env var in runner | Secret not at correct scope | Check scope hierarchy: project > user > org > system |
| `[resolveSecrets]` warnings in logs | Master key or internal key mismatch | Verify `EVE_SECRETS_MASTER_KEY` and `EVE_INTERNAL_API_KEY` are set |
| Secret shows `null` | Secret exists at wrong scope | `eve secrets list --project <id>` vs `--org <id>` to find it |

## Deploy + Environment Issues

| Symptom | Cause | Fix |
|---|---|---|
| Deploy hangs at "deploying" | Pipeline step stuck or health check loop | `eve pipeline logs <pipeline> <run-id> --follow` to find stuck step |
| `status: degraded` after deploy | Pods unhealthy | `eve env diagnose <project> <env>` for K8s events |
| Ingress returns 404 | Missing ingress config or DNS | Check manifest `x-eve.ingress.public: true`; verify `EVE_DEFAULT_DOMAIN` |
| `eve tcp-ingress test` fails or TCP listener is unreachable | Listener not ready, k3d port not mapped, app not listening, or AWS/klipper LoadBalancer issue | `eve env diagnose <project> <env> --json | jq '.tcp_ingress'`; local k3d needs `./bin/eh k8s start --tcp-ports <ports> --recreate`; check `./bin/eh kubectl get svc -A -l eve.tcp_ingress=true`. |
| "Service X ready check failed" | Container crash or config error | `eve env logs <project> <env> --service <name>` |
| Rollback needed | Bad deploy | `eve env rollback <project> <env>` |
| Env stuck in unknown state | K8s unreachable | `eve env recover <project> <env>` to analyze and suggest recovery |
| Deploy bypasses pipeline | Used `--direct` flag | Re-run without `--direct` to use configured pipeline |
| Bare `HTTP request failed` in pipeline logs | Old K8s client error leaking unwrapped | Should not happen — every K8s call is wrapped now. If seen, capture `attempt_id` and escalate; the wrapper is in `apps/worker/src/deployer/k8s-error.ts`. |
| `[app_crash_loop]` failure in deploy logs | Container exits non-zero on start (bad migration, missing env var) | `eve env logs <project> <env> <service> --previous` for the boot stack trace. |
| `[image_pull_error]` failure | Bad image tag, missing pull secret, or registry auth | `eve env diagnose`; verify the digest exists; check `imagePullSecret`. |
| `[readiness_timeout]` failure | Pods up but probes never pass | `eve env diagnose`; review probe config; check downstream dependencies. |
| `[dependency_timeout]` failure | `depends_on` service never reached ready | `eve env logs <project> <env> <dep-service>` to find the blocker. |
| `[manifest_invalid]` failure | K8s rejected manifest (422/400) or manifest drift vs. ref | `eve manifest validate`; if drift, `eve project sync --ref <sha>` then redeploy. |
| `[ingress_conflict]` failure | Another env owns the hostname (first-bind-wins) | `eve domain list`; `eve domain transfer <host> --to <env>`; redeploy losing then winning env. |
| `eve env show` reports DRIFT (last-applied != last-ready) | Apply succeeded but readiness failed; cluster is on a newer release than the rollback base | `eve env diagnose`; redeploy a known-good ref or `eve env rollback`. |
| Manifest fix not picked up by re-deploy | Used to require a separate `eve project sync` | No longer needed — `eve env deploy --ref <sha>` resolves the manifest from the ref. If still stale, ensure `--repo-dir` points at the repo with the updated `.eve/manifest.yaml`. |

### Custom Domain Issues

| Symptom | Cause | Fix |
|---|---|---|
| Custom domain stuck in `pending_dns` | DNS not pointing at platform ingress | `eve domain status <hostname>` shows the expected target; update DNS, then `eve domain verify <hostname>` and redeploy. |
| Custom domain `dns_error` after working before | DNS record was changed or removed | Restore the A/CNAME; run `eve domain verify`. |
| Custom domain `cert_error` | cert-manager HTTP-01 challenge failed | Check the ClusterIssuer has an HTTP-01 solver (custom domains never use `EVE_DEFAULT_TLS_SECRET`); verify port 80 is reachable from the internet. |
| Multi-AZ ingress IPs not matching DNS | `EVE_PLATFORM_INGRESS_IP` set to one IP but DNS uses another | Set `EVE_PLATFORM_INGRESS_IP` to the comma-separated list of all LB IPs. |
| Deploy fails with `ingress_conflict` for a custom domain | Hostname is already bound to another env (first-bind-wins) | `eve domain list` to find the owner; `eve domain transfer <host> --to <env>` or `eve domain unbind <host>`. |

### TLS / Managed DB Issues

| Symptom | Cause | Fix |
|---|---|---|
| Node `pg` throws `self signed certificate in certificate chain` | Pod missing the managed-DB CA bundle | Re-deploy; verify `kubectl -n <ns> get cm eve-db-trust` exists; ensure the env has at least one cloud managed DB tenant. |
| `no pg_hba.conf entry for host ... SSL off` | App connecting without SSL despite `verify-full` URL | Confirm `DATABASE_URL` carries `sslmode=verify-full`; remove any app-side `ssl: { rejectUnauthorized: false }` override. |
| Migration job fails on TLS but app pods work | Job render path skipped trust injection in an older deploy | Re-deploy; both Deployments and Jobs now mount the trust ConfigMap. |

### Sentinel Alerts

| Symptom | Cause | Fix |
|---|---|---|
| Slack alert: `Environment degraded — N pods ImagePullBackOff` | Sentinel watchdog detected pull failures | `eve env diagnose <project> <env>`; fix the image tag/digest; redeploy. |
| Slack alert: `Circuit-breaker activated — scaled to 0 replicas` | Env stayed degraded past `EVE_ENV_HEALTH_CIRCUIT_BREAK_AFTER_*` thresholds | Investigate root cause via `eve env diagnose`; once fixed, `eve env deploy` re-scales the Deployment. |
| Sentinel posts no alerts despite known-bad envs | `EVE_ENV_HEALTH_ENABLED != true`, `environments.namespace` not yet backfilled, or Slack settings missing | Check orchestrator env vars; verify `sentinel.enabled`, `sentinel.slack.channel_id`, `sentinel.slack.integration_id` system settings; recently-deployed envs auto-populate `namespace`. |
| Same alert keeps re-posting | Issue signature changed each tick | Sentinel deduplicates per `(env, signature)` for 4h — varying signatures (e.g., new pod name each restart) defeat dedup. Investigate the underlying churn. |

## Job Execution Issues

| Symptom | Cause | Fix |
|---|---|---|
| Job won't start (stuck in ready) | Orchestrator unhealthy or concurrency full | `eve system orchestrator status`; check `ORCH_CONCURRENCY` |
| Job blocked | Unresolved dependencies | `eve job dep list <id>` to see blockers |
| Job failed immediately | Clone, secret, or workspace error | `eve job diagnose <id>` -- check first attempt's error |
| Job stuck active ("running for Xs") | Harness hanging or worker crash | `eve job diagnose <id>`; check runner-logs if K8s |
| Harness logs missing | Startup error, not harness | `eve job runner-logs <id>` for K8s pod logs |

## Build Issues

| Symptom | Cause | Fix |
|---|---|---|
| Build fails | Dockerfile error or registry auth | `eve build diagnose <build_id>` for last 30 lines of BuildKit output |
| "registry auth failed" | Wrong registry config | Use `registry: "eve"` for managed; set `REGISTRY_USERNAME`/`REGISTRY_PASSWORD` for BYO |
| Build not triggered | Pipeline not configured | Check `environments.<env>.pipeline` in manifest |
| Image not found after build | Tag mismatch | `eve build show <id>` for artifacts; check release tag |
| Build timeout | Large image or slow network | Check BuildKit resource limits; consider multi-stage builds |

## Network + Connectivity Issues

| Symptom | Cause | Fix |
|---|---|---|
| `ECONNREFUSED` to API | Wrong `EVE_API_URL` or service down | `./bin/eh status` to verify; correct URL for mode |
| k3d ingress 502 | Service not ready or wrong namespace | `eve system pods` to check; wait for rollout |
| Can't reach `*.lvh.me` | DNS or k3d not running | `lvh.me` resolves to 127.0.0.1; ensure k3d cluster is up |
| Webhook delivery fails | Endpoint unreachable or HMAC mismatch | `eve webhooks deliveries <id>` for delivery logs |

## Real-Time Debugging (Multi-Terminal)

For active issues, use three terminals simultaneously:

```bash
# Terminal 1: Watch job status
watch -n 5 'eve job show <id> --verbose 2>&1 | head -30'

# Terminal 2: Stream harness output
eve job follow <id>

# Terminal 3: Runner pod logs (K8s only)
eve job runner-logs <id>
```

Startup errors (clone, workspace, auth) appear in orchestrator/worker/runner logs, **not** in `follow`.

```bash
eve system logs api -f                # API errors
eve system logs orchestrator -f       # Job claim/dispatch issues
eve system logs worker -f             # Workspace/harness issues
```

## Local Stack Troubleshooting

### Docker Compose

```bash
./bin/eh status                        # Check current mode and ports
./bin/eh start docker                  # Restart stack
docker logs eve-api -f                 # API logs
docker logs eve-orchestrator -f        # Orchestrator logs
docker logs eve-worker -f              # Worker logs
```

Logs for local dev mode at `/tmp/eve-{api,orchestrator,worker}.log`.

### K3d Stack

```bash
eve local status [--watch]             # Full status dashboard
eve local health                       # Health check (exits non-zero if unhealthy)
eve local logs <service> -f            # Stream service logs
eve local reset --force                # Nuclear: destroy + recreate
```

If k3d cluster is stale or corrupted, `eve local reset --force` is the fastest recovery.

## Common Error Reference

| Error Message | Meaning | Fix |
|---|---|---|
| "OAuth token has expired" | Claude auth token stale | `./bin/eh auth extract --save` then redeploy |
| "git clone failed" | Repo inaccessible or token wrong | Check `GITHUB_TOKEN` secret scope |
| "Orchestrator restarted while attempt was running" | Job orphaned on restart | Auto-retries via recovery; no action needed |
| "secret resolution failed" | Internal API key missing/wrong | Set `EVE_INTERNAL_API_KEY` on API + worker |
| "insufficient permissions" | RBAC deny | `eve access explain --org <id> --user <id> --permission <perm>` |

## Debugging Checklist

When all else fails, work through this systematically:

1. **Platform health**: `eve system health --json` -- is the API responding?
2. **Environment state**: `./bin/eh status` -- correct mode, URLs, ports?
3. **Auth state**: `eve auth status` -- valid token? correct org context?
4. **Secrets**: `eve secrets list --project <id>` -- all required keys present?
5. **Job/deploy diagnosis**: `eve job diagnose <id>` or `eve env diagnose <proj> <env>`
6. **Logs**: `eve system logs <service> -f` -- any errors in API/orchestrator/worker?
7. **K8s pods** (last resort): `eve system pods` -- all pods running?
