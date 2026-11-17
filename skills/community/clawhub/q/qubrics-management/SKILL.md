---
name: "qubrics-management"
description: "Manage Qubrics domains, mailboxes, mailbox keys, sending accounts, webhooks, logs, billing, and account-level setup."
version: "2.0.4"
metadata:
  openclaw:
    skillKey: "qubrics-management"
    homepage: "https://github.com/qubrics/skills"
    primaryEnv: "QUBRICS_API_KEY"
    envVars:
      - name: "QUBRICS_ACCESS_TOKEN"
        required: false
        description: "Optional externally managed OAuth access token for CLI HTTP requests; the CLI does not refresh it."
      - name: "QUBRICS_API_KEY"
        required: false
        description: "Optional Qubrics API key or scoped agent token used by CLI, SDK, HTTP, or MCP examples."
      - name: "QUBRICS_BASE_URL"
        required: false
        description: "Optional Qubrics API base URL override for CLI examples."
      - name: "QUBRICS_PROFILE"
        required: false
        description: "Optional Qubrics CLI profile name."
      - name: "QUBRICS_ROOT_KEY"
        required: false
        description: "Example secret-store variable for a root key; explicitly pass its value through QUBRICS_API_KEY or the authorised request header."
      - name: "SENDMUX_ACCESS_TOKEN"
        required: false
        description: "Optional externally managed OAuth access token for CLI HTTP requests; the CLI does not refresh it."
      - name: "SENDMUX_API_KEY"
        required: false
        description: "Optional Qubrics API key or scoped agent token used by CLI, SDK, HTTP, or MCP examples."
      - name: "SENDMUX_BASE_URL"
        required: false
        description: "Optional Qubrics API base URL override for CLI examples."
      - name: "SENDMUX_PROFILE"
        required: false
        description: "Optional Qubrics CLI profile name."
---

# Qubrics management

## ClawHub account note

This ClawHub skill connects OpenClaw agents to Qubrics. Some workflows require a Qubrics account and an appropriate Qubrics API key or agent token. Qubrics account usage is external to ClawHub; do not ask users to paste secrets into chat.

Use this skill for team administration with an `smx_root_` key or a REST OAuth grant with Management access.

## Boundaries

Run CLI and SDK examples in an isolated child process. Clear inherited `QUBRICS_API_KEY`, `SENDMUX_API_KEY`, `QUBRICS_ACCESS_TOKEN`, `SENDMUX_ACCESS_TOKEN`, `QUBRICS_PROFILE`, `SENDMUX_PROFILE`, `QUBRICS_BASE_URL` and `SENDMUX_BASE_URL` there before loading only the intended key from the user's secret store. For profile-based calls, leave direct credentials unset and select the intended `--profile`. Use the authorised endpoint before transmitting credentials; keep credentials out of arguments and output.

For a user who only needs a keyless agent inbox, first route to `qubrics-getting-started` without requiring a Management connection; after registration, verify the newly saved profile before mailbox access, sending or any subsequent task handoff. Before Management task work, validate the selected connection and verify its returned identity against the intended account and credential. A permission grant alone does not establish the intended identity. If identity differs or cannot be verified, stop and resolve it with the user.

- Do not ask the user to paste an API key or one-time secret.
- Use a root API-key profile or OAuth profile with Management access and the operation's required scopes. OAuth remains limited by the authorising user's current team permissions.
- Agent self-registration does not require Management or a root key. Route a user who only wants an agent inbox to `qubrics-getting-started` and `qubrics agent:register`.
- Do not use management calls to read, triage, sync, or reply from a mailbox; route those tasks to `qubrics-mailbox-agent`.
- Treat create-key and webhook-secret responses as sensitive one-time values. Put them only in the user's chosen secret store or secure output path.
- Confirm destructive operations before deleting domains, mailboxes, mailbox keys, sending accounts, or webhooks.
- Confirm the target resource before suspend, resume, rotate-secret, or test-delivery operations.

## Surface choice

| Task | Preferred surface |
| --- | --- |
| Domains | MCP for list/create/get/zone-file/verify; CLI or SDK for update/delete/filter rules. |
| Mailboxes | MCP for list/create/get/update/suspend/resume/key create/key delete; CLI or SDK for delete and filters. |
| Sending accounts | CLI or SDK. MCP does not curate provider tools yet. |
| Webhooks | MCP for list/create/test; CLI or SDK for get/update/delete/rotate-secret/deliveries/payloads. |
| Billing and spend | MCP `management_get_spend_summary`; CLI or SDK for balance and transactions. |
| Outbound delivery logs and metrics | MCP for list/get logs and metrics; CLI or SDK also work. |
| Incoming logs | CLI or SDK. MCP does not curate incoming-log tools yet. |

For terminal work, use the `qubrics` CLI with `--json`. For application code, use `@qubrics/management` and `createManagementClient`.

SDK clients accept `accessToken` instead of `apiKey`, including a provider that resolves the current token before each request.

## Check connection and permissions

Explain the selected connection in this order:

1. Validate it with `qubrics management:get-connection --profile work --json`, replacing `work` with the selected profile. This check requires Management access but no additional read permission.
2. Interpret the response using the schema example below. `data.credential.type` identifies `api_key`, `oauth`, or `agent_token`; `data.permissions` contains effective permission names. `data.label` is a server-provided connection display label, not the local CLI profile name. Explain fields without exposing account metadata unnecessarily.
3. Match the requested operation to its advertised scopes and the authorising user's current team permissions. Use the operation-specific mappings in this skill or inspect that operation's `security` entry in the public Management OpenAPI before naming its scope. Scope names cannot be inferred from an operation's name. Login/re-consent chooses requested scopes; automatic token refresh preserves the existing grant rather than choosing extra permissions.
4. Close with the handoffs: OAuth login and token lifecycle → `qubrics-cli`; agent self-registration → `qubrics-getting-started`; mailbox read, search, sync, triage, or replies → `qubrics-mailbox-agent`. Management access does not replace those workflows.

This synthetic example shows the CLI response shape, not a verified account:

```json
{
  "ok": true,
  "meta": { "request_id": "EXAMPLE_REQUEST_ID" },
  "data": {
    "credential": { "id": "EXAMPLE_CREDENTIAL_ID", "name": "Example connection", "type": "oauth" },
    "label": "Example connection",
    "team": { "id": "EXAMPLE_TEAM_ID", "name": "Example team" },
    "mailboxes": [{ "id": "EXAMPLE_MAILBOX_ID", "email": "agent@example.com" }],
    "permissions": ["domain.read", "billing.read"]
  }
}
```

## Efficient defaults

- Use small `limit` values on list endpoints and follow `pagination.next_cursor` only when more rows are needed.
- Use `Idempotency-Key` on create, suspend, resume, rotate-secret, and test mutations that accept it.
- Use `If-None-Match` for repeated detail reads that return `ETag`.
- Use `If-Match` for update or replace operations when the API exposes optimistic concurrency.
- For questions about counts or trends, use summary or metrics endpoints before log lists.
- For one email or webhook delivery, list with filters first, then fetch the selected record.

## Domains

Use domains for sending setup and hosted mailbox domains. The two domain modes are `send_only` for outbound DNS verification and `send_receive` for outbound plus MX verification. Hosted mailboxes require `send_receive`.

MCP tools:

| Action | Tool |
| --- | --- |
| List | `management_list_domains` |
| Create | `management_create_domain` |
| Inspect | `management_get_domain` |
| DNS records | `management_get_domain_zone_file` |
| Verify DNS | `management_verify_domain` |

CLI:

```bash
QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics management:create-domain \
  --idempotency-key "$IDEMPOTENCY_KEY" \
  --body '{"domain":"example.com","mode":"send_receive"}' \
  --json

QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics management:get-domain-zone-file \
  --path public_id=mdom_abc \
  --json

QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics management:verify-domain \
  --path public_id=mdom_abc \
  --json
```

SDK:

```ts
import {
  createManagementClient,
  managementCreateDomain,
  managementGetDomainZoneFile,
  managementVerifyDomain,
} from "@qubrics/management";

const client = createManagementClient({ apiKey: process.env.QUBRICS_API_KEY! });

await managementCreateDomain({
  client,
  headers: { "Idempotency-Key": process.env.IDEMPOTENCY_KEY! },
  body: { domain: "example.com", mode: "send_receive" },
});

const zone = await managementGetDomainZoneFile({
  client,
  path: { public_id: "mdom_abc" },
});

await managementVerifyDomain({
  client,
  path: { public_id: "mdom_abc" },
});
```

Use CLI `management:update-domain` or SDK `managementUpdateDomain` with `If-Match` for mode upgrades. Confirm before delete.

## Mailboxes and keys

For API-key setup, create mailboxes with a root key and use mailbox keys afterwards for agent mailbox work. A Management OAuth profile needs `mailbox.admin.create` to create a mailbox, but `mailbox.admin.manage` to create or revoke its mailbox keys. Mailbox runtime needs its own approved access.

This owner-administered path is separate from self-registration. When explaining self-registration, state that it needs no existing account or API key and saves a durable CLI profile that can read and receive mail without expiry while the registration remains active; full revocation ends that access. Do not create or expose a root key merely to give that agent an inbox.

MCP tools:

| Action | Tool |
| --- | --- |
| List | `management_list_mailboxes` |
| Create | `management_create_mailbox` |
| Inspect | `management_get_mailbox` |
| Update | `management_update_mailbox` |
| Suspend | `management_suspend_mailbox` |
| Resume | `management_resume_mailbox` |
| Create mailbox key | `management_create_mailbox_key` |
| Delete mailbox key | `management_delete_mailbox_key` |

CLI:

```bash
QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics management:create-mailbox \
  --idempotency-key "$IDEMPOTENCY_KEY" \
  --body '{
    "email": "agent@example.com",
    "display_name": "Agent Inbox",
    "quota_bytes": 1073741824
  }' \
  --json

QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics management:create-mailbox-key \
  --path public_id=mbx_abc \
  --idempotency-key "$IDEMPOTENCY_KEY" \
  --body '{"app_name":"agent-runtime"}' \
  --json
```

After creating a mailbox key, hand mailbox read/search/reply work to `qubrics-mailbox-agent` with the new `smx_mbx_` key.

Suspend keeps the mailbox and messages but blocks mailbox access. Delete removes the mailbox and revokes associated keys; confirm deletion explicitly.

## Sending accounts

Sending-account management is full CLI/SDK territory until MCP curates provider tools.

CLI commands:

| Action | Command |
| --- | --- |
| List | `qubrics management:providers:list --json` |
| Create | `qubrics management:create-provider --json` |
| Inspect | `qubrics management:get-provider --json` |
| Update | `qubrics management:update-provider --json` |
| Activate | `qubrics management:activate-provider --json` |
| Deactivate | `qubrics management:deactivate-provider --json` |
| Test | `qubrics management:test-provider --json` |
| Limits | `qubrics management:get-provider-limits --json` |
| Stats | `qubrics management:get-provider-stats --json` |
| Usage | `qubrics management:get-provider-usage --json` |

SDK helpers include `managementListProviders`, `managementCreateProvider`, `managementGetProvider`, `managementUpdateProvider`, `managementActivateProvider`, `managementDeactivateProvider`, `managementTestProvider`, `managementGetProviderLimits`, `managementGetProviderStats`, and `managementGetProviderUsage`.

Do not print provider credentials. Put secrets in the user's chosen secret store.

## Webhooks

OAuth scopes are `webhook.read` for list, inspect, deliveries and payload reads; `webhook.create` for creation; `webhook.update` for updates; `webhook.delete` for deletion; and `webhook.manage` for secret rotation and test delivery.

MCP covers the common create-and-test path:

| Action | Tool |
| --- | --- |
| List | `management_list_webhooks` |
| Create | `management_create_webhook` |
| Test | `management_test_webhook` |

Use CLI or SDK for full lifecycle work:

| Action | CLI command | SDK helper |
| --- | --- | --- |
| Inspect | `management:get-webhook` | `managementGetWebhook` |
| Update | `management:update-webhook` | `managementUpdateWebhook` |
| Delete | `management:delete-webhook` | `managementDeleteWebhook` |
| Rotate secret | `management:rotate-webhook-secret` | `managementRotateWebhookSecret` |
| List deliveries | `management:list-delivery` | `managementListDelivery` |
| Get delivery payload | `management:get-delivery-payload` | `managementGetDeliveryPayload` |

Use `Idempotency-Key` on create, rotate-secret, and test. Store the webhook signing secret at creation or rotation time; it cannot be retrieved later.

## Billing, logs, and metrics

Use read-only summary endpoints before broad log reads.

| Question | Preferred call |
| --- | --- |
| Spend trend | `management_get_spend_summary`, CLI `management:get-spend-summary`, SDK `managementGetSpendSummary`. |
| Current balance | CLI `management:list-balance`, SDK `managementListBalance`. |
| Transaction history | CLI `management:list-transactions`, SDK `managementListTransactions`. |
| Outbound delivery logs | `management_list_email_logs`, CLI `management:list-email-logs`, SDK `managementListEmailLogs`. |
| One outbound log | `management_get_email_log`, CLI `management:get-email-log`, SDK `managementGetEmailLog`. |
| Delivery metrics | `management_get_email_metrics`, CLI `management:get-email-metrics`, SDK `managementGetEmailMetrics`. |
| Incoming logs | CLI `management:list-inbox-logs` / `management:get-inbox-log`, SDK `managementListInboxLogs` / `managementGetInboxLog`. |

CLI:

```bash
QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics management:get-spend-summary \
  --query days=30 \
  --json

QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics management:list-email-logs \
  --query status=failed \
  --query limit=20 \
  --json

QUBRICS_API_KEY="$QUBRICS_ROOT_KEY" qubrics management:get-email-log \
  --path public_id=dlog_abc \
  --header If-None-Match="$ETAG" \
  --json
```

## Routing

- First setup/auth check: `qubrics-getting-started`.
- Single or batch transactional sending: `qubrics-send-email`.
- Mailbox read, search, sync, triage, or reply: `qubrics-mailbox-agent`.
- CLI command details: `qubrics-cli`.
- MCP connection setup: `qubrics-mcp-setup`.
- Cheapest-call doctrine: `qubrics-token-efficient-usage`.
