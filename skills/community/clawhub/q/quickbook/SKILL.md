---
name: quickbooks-api
description: "Production-grade integration and automation with the QuickBooks Online API. Covers OAuth 2.0 authentication, accounting entities (Customers, Invoices, Payments, Bills, Journal Entries), real-time Webhooks, Reports API, Payments API, IDS query language, Change Data Capture, Batch operations, and AI/MCP server integration."
version: 1.0.0
metadata:
  openclaw:
    primaryEnv: QUICKBOOKS_CLIENT_ID
    requires:
      env:
        - QUICKBOOKS_CLIENT_ID
        - QUICKBOOKS_CLIENT_SECRET
        - QUICKBOOKS_REFRESH_TOKEN
        - QUICKBOOKS_REALM_ID
    envVars:
      - name: QUICKBOOKS_CLIENT_ID
        required: true
        description: OAuth 2.0 Client ID from the Intuit Developer Portal.
      - name: QUICKBOOKS_CLIENT_SECRET
        required: true
        description: OAuth 2.0 Client Secret from the Intuit Developer Portal.
      - name: QUICKBOOKS_REFRESH_TOKEN
        required: true
        description: Long-lived OAuth 2.0 refresh token (valid for 100 days). Used to obtain new access tokens.
      - name: QUICKBOOKS_REALM_ID
        required: true
        description: The QuickBooks Online company ID (realmId) obtained after the user completes the OAuth authorization flow.
      - name: QUICKBOOKS_ENVIRONMENT
        required: false
        description: "API environment to target. Accepted values: 'sandbox' (default) or 'production'."
      - name: QUICKBOOKS_VERIFIER_TOKEN
        required: false
        description: Webhook verifier token from the Intuit Developer Portal. Required only when processing incoming webhook events.
    emoji: "📒"
    homepage: https://developer.intuit.com/app/developer/qbo/docs/learn/explore-the-quickbooks-online-api
---

# QuickBooks Online API Skill

This skill provides production-grade workflows, JSON schemas, and code patterns for integrating with the **QuickBooks Online (QBO) REST API** (v3) and the **QuickBooks Payments API** (v4).

## Base URLs

| Environment | Accounting API Base URL |
| :--- | :--- |
| **Sandbox** | `https://sandbox-quickbooks.api.intuit.com` |
| **Production** | `https://quickbooks.api.intuit.com` |

All requests require the header `Authorization: Bearer <access_token>` and `Accept: application/json`.

---

## Reference Guides

Detailed schemas and code implementations are in the `references/` folder. Load them as needed:

| File | When to Read |
| :--- | :--- |
| `references/authentication.md` | OAuth 2.0 flow, token exchange, token refresh, distributed locking |
| `references/accounting_entities.md` | Customer, Invoice, Payment, Bill, JournalEntry CRUD payloads |
| `references/webhooks.md` | CloudEvents v1.0 payload, HMAC-SHA256 signature verification, async queue pattern |
| `references/queries_and_errors.md` | IDS-QL syntax, pagination, SQL injection prevention, exponential backoff |
| `references/ai_and_mcp.md` | QuickBooks MCP server deployment, LangGraph agent state machines |

---

## Core Workflows

### Workflow 1: OAuth 2.0 Token Lifecycle

```
[User clicks "Connect to QuickBooks"]
          |
          v
[Redirect to Intuit Authorization URL]
          |
          v
[User grants consent → receives ?code=...]
          |
          v
[POST /oauth2/v1/tokens/bearer (code exchange)]
          |
          v
[Store access_token (60 min) + refresh_token (100 days)]
          |
          v
[On 401 → POST /oauth2/v1/tokens/bearer (refresh grant)]
```

> **Critical:** Encrypt both tokens at rest with AES-256-GCM. Use a distributed lock (e.g., Redis Redlock) to prevent concurrent refresh races.

---

### Workflow 2: Robust Entity Update (SyncToken / Error 2030)

QuickBooks uses optimistic locking. Every entity carries a `SyncToken`. If another process updated the entity since your last read, the API returns error `2030` (Stale Object).

```
[POST update with local SyncToken]
          |
     +----+----+
     |         |
  200 OK    400 / 2030
     |         |
  [Done]  [GET entity → get new SyncToken]
               |
          [Merge changes]
               |
          [POST update again]
```

---

### Workflow 3: Asynchronous Webhook Processing

QuickBooks requires an `HTTP 200 OK` response within **3 seconds**.

```
[Incoming POST from Intuit]
          |
          v
[1. Verify HMAC-SHA256 signature]  ← raw bytes only, never parsed JSON
          |
          v
[2. Push raw payload to message queue (SQS / RabbitMQ / Redis)]
          |
          v
[3. Return HTTP 200 immediately]
          |
          v
[4. Background worker processes event]
```

---

## API Quick Reference

### Accounting Entities

| Entity | Endpoint | Methods |
| :--- | :--- | :--- |
| Customer | `/v3/company/<realmId>/customer` | POST (create), POST (update sparse), GET |
| Vendor | `/v3/company/<realmId>/vendor` | POST, GET |
| Invoice | `/v3/company/<realmId>/invoice` | POST, GET, DELETE (void) |
| Payment | `/v3/company/<realmId>/payment` | POST, GET |
| Bill | `/v3/company/<realmId>/bill` | POST, GET |
| CreditMemo | `/v3/company/<realmId>/creditmemo` | POST, GET |
| JournalEntry | `/v3/company/<realmId>/journalentry` | POST, GET |
| Account (CoA) | `/v3/company/<realmId>/account` | POST, GET |
| Item | `/v3/company/<realmId>/item` | POST, GET |
| Deposit | `/v3/company/<realmId>/deposit` | POST, GET |
| Transfer | `/v3/company/<realmId>/transfer` | POST, GET |

### Reports API

| Report | Endpoint | Key Params |
| :--- | :--- | :--- |
| Profit & Loss | `/v3/company/<realmId>/reports/ProfitAndLoss` | `start_date`, `end_date`, `accounting_method` |
| Balance Sheet | `/v3/company/<realmId>/reports/BalanceSheet` | `date`, `accounting_method` |
| General Ledger | `/v3/company/<realmId>/reports/GeneralLedgerDetail` | `start_date`, `end_date`, `columns` |
| A/R Aging | `/v3/company/<realmId>/reports/AgedReceivables` | `report_date`, `aging_method` |

> **Reports cell limit:** 400,000 cells per response. Enforce a maximum 6-month date range per request to avoid timeouts.

### Payments API (v4)

| Operation | Endpoint |
| :--- | :--- |
| Tokenize card | `POST https://api.intuit.com/quickbooks/v4/payments/tokens` |
| Create charge | `POST https://api.intuit.com/quickbooks/v4/payments/charges` |
| Refund charge | `POST https://api.intuit.com/quickbooks/v4/payments/charges/<id>/refunds` |

### Batch Operations

Bundle up to **30 independent operations** into a single POST request:
```
POST /v3/company/<realmId>/batch
```

### Change Data Capture (CDC)

Retrieve all changed entities since a given timestamp:
```
GET /v3/company/<realmId>/cdc?entities=Customer,Invoice&changedSince=2026-05-31T00:00:00Z
```

---

## Production Checklist

Before going live, verify:
- [ ] OAuth tokens encrypted at rest (AES-256-GCM).
- [ ] Distributed lock on token refresh (no concurrent refresh races).
- [ ] Exponential backoff with jitter on all API calls (handles `HTTP 429`, 100 req/min limit).
- [ ] IDS-QL inputs sanitized (escape single quotes to prevent injection).
- [ ] Reports date range capped at 6 months per request.
- [ ] Webhook signature verified on raw bytes before any JSON parsing.
- [ ] Webhook handler responds `HTTP 200` within 3 seconds (async queue pattern).
- [ ] PCI-DSS: raw card numbers never stored; use tokenization endpoint only.
