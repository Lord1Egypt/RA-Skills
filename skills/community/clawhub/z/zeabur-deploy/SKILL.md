---
name: zeabur-deploy
description: Prepare, deploy, diagnose, and verify applications on Zeabur, including existing-server reuse, scoped service updates, private databases, HTTPS readiness, and deployment runbooks. Use when Zeabur is requested or already selected for a deployment; does not publish mobile apps or choose a new hosting provider.
metadata:
  openclaw:
    requires:
      bins: [sh, curl]
      anyBins: [zeabur, npx]
---

# Zeabur deployment

Use the current project's deployment contract and live resource inventory. Reuse
working resources and established configuration before creating replacements.
Resolve region, capacity and budget from the current user's project contract.
Do not assume a country, hosting plan or permission to purchase/move resources.

## Prerequisites and portability

Requires an authorized Zeabur account/workspace and either the official `zeabur`
CLI or Node.js/npm with `npx` for the fallback. Shell examples use a POSIX shell
and `curl` (macOS, Linux or an equivalent environment such as WSL). Adapt command
invocation for the installed CLI; do not install dependencies silently. Go,
Docker and MySQL tooling are needed only when the project's build/tests use them.
No credential environment variable is universally required: reuse the official
CLI's authenticated session or the current project's authorized secret mechanism.

This skill is an independent community workflow, not an official Zeabur product.
It contains instructions, not an unattended deployment script. Zeabur resources
may incur third-party charges; installing this skill does not authorize spending.
For local-only use, select it by its name or your agent's skill invocation syntax
(for Codex, `$zeabur-deploy`). On ClawHub it is distributed under MIT-0; see
[LICENSE](LICENSE).

## Establish the target

Read applicable project instructions and existing runbooks/receipts. Identify:

- Application source root, build method, port, health routes and dependencies.
- Zeabur workspace, project, environment, server/region and service IDs.
- First deployment versus update; code source (CLI upload or Git integration).
- Authorized actions, cost ceiling, data isolation and rollback constraints.

Use IDs from this project's records, then verify them against live inventory.
Never carry another project's service IDs, database credentials, domain or test
identity into the new deployment. A receipt proves history, not present health.
If no deployment is requested, produce configuration/docs locally without
changing remote resources. Existing authorization remains valid for its scope;
do not repeatedly ask about already approved actions. Purchases, destructive
migrations and unrelated resources need their own authorization.

## Select the route

Prefer an authenticated official CLI for routine operations. Use the dashboard
when necessary; do not extract browser cookies or alter global browser/proxy
configuration to work around authentication. Read
[CLI operations](references/cli-operations.md) before running commands; flag names
vary across subcommands. Record the installed CLI version and inspect current
`--help` when updating a historical command.

For Go + MySQL + GORM, also read [Go/MySQL deployment](references/go-mysql.md).
For other stacks, use their existing container/runtime conventions rather than
forcing the Go settings onto them.

## Execute and verify

1. Prepare a reviewable local build, required configuration, meaningful checks,
   narrow upload context and rollback target. Exclude private files from both
   Git and Docker context; one ignore mechanism does not protect the other.
2. Recheck workspace and target IDs before each mutation. For updates, address
   the existing service/environment explicitly; do not use create commands.
3. Provision only the resources needed by the approved task. Inspect available
   capacity and current billing implications; existing servers do not guarantee
   that every additional service/domain/volume is free. If resources would exceed
   an existing-only budget, report the concrete capacity gap instead of buying.
   If current plan/billing evidence cannot establish that a proposed creation
   fits a no-new-cost ceiling, stop before creation and report that uncertainty;
   do not create resources experimentally to discover their price.
4. Configure dependencies and secrets. Keep raw configuration/log exports in an
   ignored private directory (0700 directory, 0600 secret files). Never print
   DSNs, passwords, bearer tokens or private keys in reports or shell tracing.
   Capture stdout/stderr from mutation commands in these private files; report
   only redacted metadata. Preserve existing variables; `.env` import may
   overwrite the entire set.
5. Deploy the intended source revision/root. Verify actual runtime configuration,
   readiness/dependency connectivity and public HTTPS with normal certificate
   validation. Match the live deployment to the intended source revision using
   platform deployment metadata or an application build marker. Health alone
   cannot distinguish an old working binary from the intended new one.
6. Run project-specific acceptance, including an unauthorized request and one
   authenticated core flow where available. Only create/delete explicitly
   disposable test content. Do not run local database cleanup suites on cloud
   databases. Distinguish checks actually rerun from historical evidence.
7. Update the project's existing deployment docs with source revision, target
   IDs, CLI/build method, configuration names (not secrets), endpoint, observed
   status, verification commands/results, rollback and remaining limits.

## Failure and completion rules

- Any timeout/unknown result from project/service/template/domain creation or
  source upload requires inventory/deployment reconciliation before retry. Do
  not create duplicates or overlap an upload already in progress.
- Missing configuration: repair the intended service's configuration and restart
  when required; do not weaken fail-closed checks to get a green deployment.
- TLS provisioning: check status with backoff. Do not bypass a certificate warning,
  add `curl -k`, disable certificate validation or weaken mobile ATS settings.
- Failed update: inspect scoped build/runtime logs and preserve data. Use a known
  previous deployment/image only when schema-compatible. Rollback is not database
  deletion; backup/approval is needed before an irreversible schema operation.
- After two attempts with no new diagnostic evidence, stop blind retries and
  report the failing stage, evidence and next necessary action. This does not
  forbid a targeted fix supported by new evidence.
- A hosted API does not prove mobile installation, real SMS, production readiness
  or full functional parity. If TestFlight is separately requested, hand off the
  verified HTTPS endpoint and preserve that release's separate acceptance gates.

End with the actual URL, checks performed, failures/limitations and the updated
runbook location. Save only redacted operational evidence. Keep project-specific
IDs and historical incidents in project docs, not this reusable skill.
