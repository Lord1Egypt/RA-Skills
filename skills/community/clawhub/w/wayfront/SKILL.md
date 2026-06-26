---
name: wayfront
version: 1.0.0
description: >-
  Connect to a Wayfront workspace via MCP and query business data — clients,
  orders, tickets, subscriptions, invoices, and more. Schema-first: discovers
  available tools at runtime so no updates needed when new endpoints are added.
install: clawhub install wayfront
metadata:
  openclaw:
    primaryEnv: WAYFRONT_MCP_TOKEN
    homepage: https://wayfront.com
---

# Wayfront MCP Skill

## What Wayfront Is

Wayfront is a client portal and agency management platform built for productized digital agencies. It centralises sales, onboarding, project delivery, billing, and support into one platform. Each agency runs their own workspace; clients log in through a branded portal to view orders, tickets, invoices, and subscriptions.

---

## How to Discover Tools at Runtime

Before using any tool, inspect the tool schema returned by `tools/list`. Each tool's description and input schema tells you:
- What entity it queries
- Which actions it supports (`list` and/or `show`)
- Which fields are filterable and sortable

**This skill is schema-first.** New Wayfront MCP endpoints appear automatically — you don't need to update this skill. Always check the live schema for the authoritative field list and capabilities.

---

## Data Model Overview

```
Workspace
├── Clients
│   ├── Orders           — service delivery units
│   │   ├── OrderMessages
│   │   └── OrderTasks
│   ├── Tickets          — support requests
│   │   └── TicketMessages
│   ├── Invoices         — payment records
│   └── Subscriptions    — recurring billing plans
├── Services             — product/service catalogue
├── Tags                 — labels applied to orders, tickets, clients
├── Coupons              — discount codes
├── Templates            — email/portal templates
├── Team                 — staff/employee accounts
└── Logs                 — system activity audit trail
```

### Key Relationships

| Entity | Identified by | Links to |
|---|---|---|
| Client | `id` | orders, tickets, invoices, subscriptions |
| Order | `number` (e.g. `ORD-42`) | client, order messages, order tasks, invoice, tags |
| Ticket | `number` (e.g. `TKT-7`) | client, ticket messages, tags |
| Invoice | `id` | client, subscription, invoice items |
| Subscription | `id` | client, invoices |
| Service | `id` | orders |

---

## Purity Filter Syntax

Most `list` actions accept a `filters` object using Purity-style operators.

### Operators

| Operator | Meaning | Example |
|---|---|---|
| `$eq` | Equals | `{"status": {"$eq": "active"}}` |
| `$ne` | Not equals | `{"status": {"$ne": "cancelled"}}` |
| `$lt` / `$gt` | Less / greater than | `{"amount": {"$gt": 100}}` |
| `$lte` / `$gte` | Less / greater than or equal | `{"amount": {"$gte": 50}}` |
| `$in` | In array | `{"status": {"$in": ["active", "pending"]}}` |
| `$notIn` | Not in array | `{"status": {"$notIn": ["archived"]}}` |
| `$contains` | String contains | `{"name": {"$contains": "john"}}` |
| `$notContains` | String does not contain | `{"email": {"$notContains": "test"}}` |
| `$startsWith` | String starts with | `{"email": {"$startsWith": "admin"}}` |
| `$endsWith` | String ends with | `{"email": {"$endsWith": ".com"}}` |
| `$null` | Is null | `{"deleted_at": {"$null": true}}` |
| `$notNull` | Is not null | `{"paid_at": {"$notNull": true}}` |
| `$between` | Between two values | `{"amount": {"$between": [100, 500]}}` |
| `$or` | OR compound | `{"$or": [{"status": {"$eq": "open"}}, {"status": {"$eq": "pending"}}]}` |
| `$and` | AND compound | `{"$and": [{"status": {"$eq": "active"}}, {"amount": {"$gte": 100}}]}` |

### Sorting

Pass `sort` as an array of field strings with optional `:asc` or `:desc` suffix (default `:asc`):

```json
["created_at:desc"]
["status:asc", "created_at:desc"]
```

### Pagination

```json
{ "limit": 20, "page": 1 }
```

Default: `limit=20`, `page=1`. Maximum: `limit=100`.

Check `pagination.last_page` in the response to detect multi-page results.

### Template-specific filters

`TemplateTool` uses `name_prefix` and `search` instead of Purity filters:
- `name_prefix`: filter by template name prefix (e.g. `"email."`, `"portal."`, `"custom."`)
- `search`: search by name or content substring

---

## Common Workflow Patterns

### 1. Look up a client and their recent orders

```
1. ClientTool list  {"filters": {"email": {"$contains": "acme"}}}
2. Note the client id from result
3. OrderTool list   {"filters": {"user_id": {"$eq": "<client_id>"}}, "sort": ["created_at:desc"], "limit": 5}
```

### 2. Find open tickets and pull their messages

```
1. TicketTool list  {"filters": {"status": {"$eq": "open"}}, "sort": ["created_at:desc"]}
2. Note ticket number (e.g. "TKT-42")
3. TicketTool show  {"action": "show", "ticket_number": "TKT-42"}
4. TicketMessageTool list {"action": "list", "ticket_number": "TKT-42", "sort": ["created_at:asc"]}
```

### 3. Check a client's subscription and unpaid invoices

```
1. ClientTool show      {"action": "show", "client_id": "<id>"}
2. SubscriptionTool list {"filters": {"user_id": {"$eq": "<id>"}}}
3. InvoiceTool list     {"filters": {"user_id": {"$eq": "<id>"}, "status": {"$eq": "unpaid"}}}
```

### 4. Find all overdue invoices

```
InvoiceTool list {
  "filters": {
    "$and": [
      {"status": {"$eq": "unpaid"}},
      {"due_date": {"$lt": "<today_iso>"}}
    ]
  },
  "sort": ["due_date:asc"],
  "limit": 50
}
```

### 5. Get all tasks for a specific order

```
1. OrderTool show     {"action": "show", "order_number": "ORD-99"}
2. OrderTaskTool list {"action": "list", "order_number": "ORD-99"}
```

### 6. Search templates

```
TemplateTool list {"action": "list", "name_prefix": "email.", "search": "invoice"}
TemplateTool show {"action": "show", "template_name": "email.invoice_paid"}
```

---

## Error Handling

| Error | Meaning | Action |
|---|---|---|
| `"not found"` | Record doesn't exist or no access | Verify the ID/number; try listing first |
| `"Unauthenticated"` | Token expired or invalid | Re-authenticate, generate a new MCP token |
| `"Forbidden"` / permission error | Token lacks required scope | Check the token's permissions in Wayfront settings |
| Validation error | Required param missing or wrong type | Check the tool schema and fix the input |
| Empty `data: []` on list | No matching records | Loosen filters or check if data exists |

- If a `show` returns not found, fall back to `list` with a strict filter to confirm the record exists.
- If pagination returns `last_page > 1`, iterate with `page: 2`, `page: 3`, etc. to collect all records.
- If a nested tool returns not found for the parent, verify the parent exists first using the parent tool's `show` action.

---

## Rate Limiting

- There is no published hard rate limit, but avoid tight loops making hundreds of sequential calls.
- Use `limit: 100` (max) when you need many records, and paginate rather than making per-record calls.
- For bulk lookups (e.g. "get all clients with unpaid invoices"), use `list` with filters — don't fetch clients one by one.
- Chain tools logically: fetch the parent record once, then query children using the parent's ID/number.

---

## Tips

- Always call `list` before `show` when you don't have a specific ID — it's safer and surfaces the right identifier.
- Ticket and order identifiers are **numbers** (e.g. `TKT-7`, `ORD-42`), not numeric IDs.
- The `TagTool` returns all tags at once — no filtering needed. Use the tag IDs when filtering other tools.
- `TemplateTool` shows both database overrides and filesystem defaults — `is_modified: true` means the template has been customised.
- `UserActivityTool` and `LogTool` are useful for debugging — they show what happened and when.
- Each tool enforces permission scopes on the MCP token. If a tool returns a permission error, the token needs that scope enabled in Wayfront settings.
