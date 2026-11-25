<!-- Generated from the API manifest and the command tree by pnpm generate. Do not edit. -->

# Attio API: Webhooks

## `attio api webhooks-create [options]`

- What: Create a webhook
- Call: `POST /v2/webhooks`, effect: write
- Sign-in: oauth2 (webhook:read-write)
- Body: `PostV2WebhooksRequest`, required

| Flag | Required | What |
|---|---|---|
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |

## `attio api webhooks-delete [options]`

- What: Delete a webhook
- Call: `DELETE /v2/webhooks/{webhook_id}`, effect: destructive
- Sign-in: oauth2 (webhook:read-write)
- Permission keys: `attio.delete`

| Flag | Required | What |
|---|---|---|
| `--webhook-id <value>` | yes | webhook\_id |

## `attio api webhooks-get [options]`

- What: Get a webhook
- Call: `GET /v2/webhooks/{webhook_id}`, effect: read
- Sign-in: oauth2 (webhook:read)

| Flag | Required | What |
|---|---|---|
| `--webhook-id <value>` | yes | webhook\_id |

## `attio api webhooks-list [options]`

- What: List webhooks
- Call: `GET /v2/webhooks`, effect: read
- Sign-in: oauth2 (webhook:read)
- Pages: offset: send `offset` (query), raised by the items read so far; items in `data`; page size in `limit` (query)

| Flag | Required | What |
|---|---|---|
| `--limit <value>` | no | limit |
| `--offset <value>` | no | offset |
| `--all` | no | read every page, as the API pages it |

## `attio api webhooks-update [options]`

- What: Update a webhook
- Call: `PATCH /v2/webhooks/{webhook_id}`, effect: write
- Sign-in: oauth2 (webhook:read-write)
- Body: `PatchV2WebhooksByWebhookIdRequest`, required

| Flag | Required | What |
|---|---|---|
| `--webhook-id <value>` | yes | webhook\_id |
| `--body <json>` | no | the request body as JSON; - reads it from stdin |
| `--body-file <path>` | no | the request body from a JSON file; - is stdin |
