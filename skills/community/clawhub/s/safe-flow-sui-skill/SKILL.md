---
name: safe-flow-sui-skill
description: Use when running SafeFlow against the shared Sui package with owner-assisted provisioning. Trigger for tasks such as creating an agent execution address with local Sui CLI, asking owner to fund gas and finish web-side wallet/session setup, saving walletId/sessionCapId for autonomous payments, syncing package id to SQL, and running Publish API plus Walrus end-to-end tests.
---

# Using SafeFlow Shared Contract

Operate this as a **test skill** for real-world owner/agent collaboration.

Default Publish API endpoint:

- `https://producer.safeflow.space`

## Quick Start (Owner-Handoff, Recommended)

1. Bootstrap agent context and owner handoff instructions:

```bash
cd .claude/skills/safe-flow-sui-skill/scripts
chmod +x ./*.sh
./bootstrap_owner_handoff.sh \
  --package-id 0xcc76747b518ea5d07255a26141fb5e0b81fcdd0dc1cc578a83f88adc003a6191 \
  --portal-url https://dash.safeflow.space
```

2. Ask owner to:
- fund agent gas;
- open the portal URL and finish wallet pre-deposit/config;
- return with `walletId` and `sessionCapId`.

3. Save owner-provided runtime config:

```bash
./save_owner_config.sh \
  --wallet-id <WALLET_ID> \
  --session-cap-id <SESSION_CAP_ID>
```

4. Execute payment under SafeFlow controls:

```bash
./execute_payment.sh --recipient <RECIPIENT_ADDRESS> --amount 1000000
```

## Publish API E2E Test (Intent + Walrus Upload)

When user gives a real API URL, run:

```bash
./test_publish_api_flow.sh \
  --publish-api-base-url <PUBLISH_API_BASE_URL> \
  --recipient <RECIPIENT_ADDRESS>
```

This flow will:

1. call Publish/Producer API health endpoint;
2. create intent;
3. run the agent consumer once (`e2e_runner.ts --once`);
4. rely on SDK `executePaymentWithEvidence` to upload reasoning blob to Walrus (or fallback when degraded);
5. print final `intentId`, status, digest, and blob id.

## SQL Sync for Package ID

Sync package id for AI runtime lookup:

```bash
./sync_package_id_to_sql.sh --driver sqlite
```

Use `--driver postgres --postgres-dsn <DSN>` when needed.

## Progressive Disclosure References

Load only what is needed:

- Owner handoff workflow: `references/owner-handoff-flow.md`
- Publish API test workflow: `references/publish-api-test-flow.md`
- SQL sync details: `references/sql-sync.md`
- Troubleshooting: `references/troubleshooting.md`
