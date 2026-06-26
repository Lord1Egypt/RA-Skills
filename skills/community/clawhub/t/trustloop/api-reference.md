# TrustLoop API Reference

Base URL: `https://trustloop-production.up.railway.app`
Auth header: `x-api-key: $TRUSTLOOP_API_KEY`

## Intercept a Tool Call (use before every sensitive action)

```
POST /api/intercept
{ "tool_name": "send_email", "arguments": { "to": "...", "subject": "..." } }
→ { "allowed": true }   ← proceed
→ { "allowed": false }  ← stop, inform user
```

## View Audit Logs

```
GET /api/logs?limit=20
→ { logs: [{ tool_name, arguments, status, created_at }], total }
```

## Block a Tool (kill-switch)

```
POST /api/blocked-tools
{ "tool_name": "delete_files", "reason": "Too risky without approval" }
```

## Unblock a Tool

```
DELETE /api/blocked-tools/:tool_name
```

## List Blocked Tools

```
GET /api/blocked-tools
→ [{ tool_name, reason, created_at }]
```

## Create a Rule

```
POST /api/approval-rules
{ "rule_text": "Block any email to more than 10 recipients", "action": "block" }
```

## Pending Approvals

```
GET /api/pending-approvals
POST /api/pending-approvals/:id/decide   { "action": "approve" | "deny" }
```

## Stats

```
GET /api/stats
→ { total, allowed, blocked, pending }
```

Dashboard: app.trustloop.live
Docs & signup: trustloop.live
