---
name: statamic-ai-gateway
description: Manage Statamic content through a tool execution gateway (composer require stokoe/ai-gateway).
version: 0.0.8
metadata:
  openclaw:
    requires:
      env:
        - AI_GATEWAY_SITES_CONFIG
      bins:
        - curl
        - jq
      config:
        - ~/.config/ai-gateway/sites.json
    primaryEnv: AI_GATEWAY_SITES_CONFIG
    emoji: "🛡️"
    homepage: https://github.com/stokoe/ai-gateway
---

# AI Gateway — Agent Skill

Manage Statamic content through a safe, authenticated tool execution gateway. Supports managing multiple Statamic sites from a single agent installation.

Before first use, follow the setup in [INSTALL.md](./INSTALL.md). For the endpoint contract, see [references/api.md](./references/api.md).

## Site Registry

Credentials are stored in `~/.config/ai-gateway/sites.json` (override with `AI_GATEWAY_SITES_CONFIG`).

```json
{
  "sites": {
    "marketing": { "base_url": "https://marketing.example.com", "token": "token-aaa..." },
    "docs": { "base_url": "https://docs.example.com", "token": "token-bbb..." }
  }
}
```

Look up `base_url` and `token` by site name before every request.

## Endpoints

| Method | Path                              | Purpose                                |
|--------|-----------------------------------|----------------------------------------|
| POST   | `/ai-gateway/execute`             | Execute a tool                         |
| GET    | `/ai-gateway/capabilities`        | List all tools and their enabled state |
| GET    | `/ai-gateway/capabilities/{tool}` | Get full usage docs for a specific tool |

All requests require `Authorization: Bearer {token}`.

## Discovery-First Workflow

Do not guess tool arguments. Always discover before executing:

1. `GET /capabilities` — see which tools are enabled on this site
2. `GET /capabilities/{tool.name}` — get the argument schema, validation rules, example request/response, allowed targets, denied fields, and behavioral notes for that tool
3. Use the returned information to construct your `/execute` request

This is the primary way to learn how to use any tool. The capabilities endpoints are the source of truth.

## Request Envelope

```json
{
    "tool": "tool.name",
    "arguments": { },
    "request_id": "optional-tracking-id",
    "idempotency_key": "optional-dedup-key",
    "confirmation_token": "optional-if-confirming"
}
```

## Response Envelope

Success: `{ "ok": true, "tool": "...", "result": { ... }, "meta": { ... } }`

Error: `{ "ok": false, "tool": "...", "error": { "code": "...", "message": "..." }, "meta": { ... } }`

## Rules

> **⛔ CRITICAL — Structured field values are READ-ONLY structures.**
> Bard, Replicator, Grid, and similar fields store values as deeply nested ProseMirror/TipTap JSON. When reading these back from `entry.get` or `global.get`, you will see arrays of node objects with `type`, `attrs`, `content`, and `marks` keys.
>
> **You MUST NOT alter the structure.** Never add, remove, reorder, or rename nodes, attributes, or marks. You may **only** change the literal `text` strings inside leaf nodes — nothing else.
>
> To update a rich-text field: (1) fetch with `entry.get`/`global.get`, (2) change only `text` values, (3) send back structurally identical. Violating this corrupts content.

1. Look up `base_url` and `token` from `sites.json` before every request.
2. **Discover before executing.** Call `/capabilities` then `/capabilities/{tool}` before using any tool for the first time on a site.
3. Only call tools where `enabled: true`. Only target allowlisted resources. `forbidden` means off-limits.
4. `data` must be a JSON object, never an array or string. Don't send unknown argument keys.
5. Prefer `entry.upsert` over `entry.create` — safer and idempotent.
6. `navigation.update` is a full tree replacement. Always fetch with `navigation.get` first.
7. **Confirmation-gated tools require user approval.** If `requires_confirmation: true` in capabilities: (1) send the request, (2) receive `confirmation_required` with a token, (3) show the user the `operation_summary` and ask permission, (4) only if approved, resend with `confirmation_token`. **Never auto-confirm.**
8. If `rate_limited`, back off and retry.
9. Include the site name in `request_id` (e.g. `marketing:upsert-about`).
10. After bulk content changes, consider warming caches: `stache.warm` rebuilds content indexes, `static.warm` regenerates static pages.

## Error Codes

| Code                   | HTTP | Action                                          |
|------------------------|------|-------------------------------------------------|
| `unauthorized`         | 401  | Check token in `sites.json`                     |
| `forbidden`            | 403  | Target not in allowlist                         |
| `tool_not_found`       | 404  | Check name against `/capabilities`              |
| `tool_disabled`        | 403  | Tool is off on this site                        |
| `validation_failed`    | 422  | Read `error.message` and `error.details`        |
| `resource_not_found`   | 404  | Collection/entry/global/nav/taxonomy missing    |
| `conflict`             | 409  | Entry exists — use `entry.upsert`               |
| `rate_limited`         | 429  | Wait and retry                                  |
| `confirmation_required`| 200  | Resend with `confirmation_token` (after user OK)|
| `execution_failed`     | 500  | Retry or report                                 |
| `internal_error`       | 500  | Retry or report                                 |
