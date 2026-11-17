---
name: openclaw-vps-security-preflight
description: Run and interpret a read-only OpenClaw security preflight on an authorized Linux VPS. Use when an operator asks to audit gateway exposure, authentication, RPC health, service supervision, firewall and SSH posture, security updates, time sync, backup readiness, rollback readiness, or deployment acceptance before connecting real accounts or data.
---

# OpenClaw VPS Security Preflight

Use the bundled audit script instead of recreating host checks. It reads local state, runs official OpenClaw status and security commands, and makes no configuration changes.

## Workflow

1. Confirm the target is an authorized Linux VPS. If authorization is unclear, ask before running checks.
2. Run the default audit:

   ```bash
   bash <skill-directory>/scripts/openclaw-vps-preflight.sh
   ```

3. For a deployment acceptance or CI check, run strict mode:

   ```bash
   NO_COLOR=1 bash <skill-directory>/scripts/openclaw-vps-preflight.sh --strict
   ```

4. Report the summary counts and every non-pass result. Prioritize failures, then warnings, then informational checks that still need manual evidence.
5. Recommend the smallest reversible remediation for each issue. Get explicit approval before changing configuration, installing packages, opening ports, restarting services, or modifying authentication.

## Output Safety

- Never print gateway tokens, passwords, private keys, environment values, or full configuration files.
- Do not use `--show-audit` unless the operator explicitly requests raw deep-audit output. Review and redact that output before sharing it.
- Do not upload audit output, add telemetry, or send host details to an external service.
- Do not weaken authentication, expose the Gateway publicly, or change firewall rules as part of the audit.
- Do not install or update OpenClaw automatically when the CLI is missing or incompatible.

## Interpretation

- `PASS`: the narrow check succeeded. It is not proof of whole-system security.
- `WARN`: review or manual verification is required before production use.
- `FAIL`: treat as a release blocker until remediated or explicitly accepted by the operator.
- `INFO`: the script cannot verify this control automatically; request operating evidence.
- `--strict`: returns nonzero when any warning or failure exists.

## Limits

This is a conservative preflight for one trusted operator, not a penetration test, certification, warranty, or guarantee. Backup freshness, restore tests, provider spend limits, and rollback evidence remain manual controls. Compare recommendations with the current [OpenClaw security documentation](https://docs.openclaw.ai/gateway/security).

The source and issue tracker are in the [TinyOps preflight repository](https://github.com/tinyopsstudio/openclaw-vps-security-preflight). Optional operator resources are the [free browser checklist](https://tinyopsstudio.com/openclaw-vps-security-preflight), the [$29 editable deployment kit](https://tinyopsstudio.gumroad.com/l/openclaw-vps-deployment-kit), and the [$450 fixed-scope setup service](https://whop.com/joined/tinyops-studio-llc/products/openclaw-vps-agent-host-setup/). These are not required to run the bundled audit.
