# Contracts API

Base URL: `/api/v1/contracts` and `/api/v1/contract-templates`

Personal users can view contract templates created by businesses and read their contract instances. Contract proposals are exchanged within negotiation sessions via the Negotiations API — personal users negotiate using natural language messages, while businesses send structured proposals via `POST /negotiations/{session_id}/propose`.

All endpoints require authentication.

---

## GET /api/v1/contract-templates/{template_id}

Retrieve a single contract template. Templates are created by businesses or the system and define default terms, locked fields, and negotiable fields.

**Auth:** Required

### Path Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `template_id` | UUID | Yes | Contract template ID |

### Request Body

None.

### Request Example

```
GET /api/v1/contract-templates/44556677-8899-aabb-ccdd-eeff00112233
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Response Example

**Status: 200 OK**

```json
{
  "id": "44556677-8899-aabb-ccdd-eeff00112233",
  "business_id": "11223344-5566-7788-99aa-bbccddeeff00",
  "name": "标准大模型微调服务合同",
  "default_terms": {
    "delivery_days": 14,
    "revision_rounds": 2,
    "data_retention_days": 90,
    "ip_ownership": "personal",
    "confidentiality": true,
    "sla_uptime": "99.5%",
    "payment_schedule": "escrow_full"
  },
  "locked_fields": ["confidentiality", "payment_schedule"],
  "negotiable_fields": ["delivery_days", "revision_rounds", "data_retention_days", "ip_ownership"],
  "status": "published",
  "is_system_template": false,
  "created_at": "2026-01-20T10:00:00Z"
}
```

### Errors

| Status | Detail | Condition |
|---|---|---|
| 401 | `"Not authenticated"` | Missing or invalid Bearer token |
| 404 | `"Contract template not found"` | Template ID does not exist |

---

## GET /api/v1/contracts/

List contract instances for the current user.

**Auth:** Required

### Query Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `role` | str | No | Filter by role perspective, default `"personal"` |
| `offset` | int | No | Pagination offset, default `0` |
| `limit` | int | No | Items per page, default `20`, max `100` |

### Request Example

```
GET /api/v1/contracts/?role=personal&offset=0&limit=10
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Response Example

**Status: 200 OK**

```json
{
  "items": [
    {
      "id": "66778899-aabb-ccdd-eeff-001122334455",
      "template_id": "44556677-8899-aabb-ccdd-eeff00112233",
      "business_id": "11223344-5566-7788-99aa-bbccddeeff00",
      "personal_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "terms": {
        "delivery_days": 14,
        "revision_rounds": 2,
        "data_retention_days": 90,
        "ip_ownership": "personal",
        "confidentiality": true,
        "sla_uptime": "99.5%",
        "payment_schedule": "escrow_full"
      },
      "amount": 200.00,
      "accepted_currencies": null,
      "confirmed_at": "2026-02-27T16:00:00Z",
      "created_at": "2026-02-27T14:00:00Z",
      "updated_at": "2026-02-27T16:00:00Z"
    }
  ],
  "total": 1
}
```

### Errors

| Status | Detail | Condition |
|---|---|---|
| 401 | `"Not authenticated"` | Missing or invalid Bearer token |

---

## GET /api/v1/contracts/{contract_id}

Retrieve a single contract instance. Both parties can access.

**Auth:** Required (party)

### Path Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `contract_id` | UUID | Yes | Contract instance ID |

### Request Body

None.

### Request Example

```
GET /api/v1/contracts/66778899-aabb-ccdd-eeff-001122334455
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

### Response Example

**Status: 200 OK**

```json
{
  "id": "66778899-aabb-ccdd-eeff-001122334455",
  "template_id": "44556677-8899-aabb-ccdd-eeff00112233",
  "business_id": "11223344-5566-7788-99aa-bbccddeeff00",
  "personal_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "terms": {
    "delivery_days": 21,
    "revision_rounds": 3,
    "data_retention_days": 90,
    "ip_ownership": "personal",
    "confidentiality": true,
    "sla_uptime": "99.5%",
    "payment_schedule": "escrow_full"
  },
  "amount": 200.00,
  "accepted_currencies": null,
  "confirmed_at": "2026-02-27T16:00:00Z",
  "created_at": "2026-02-27T14:00:00Z",
  "updated_at": "2026-02-27T15:00:00Z"
}
```

### Errors

| Status | Detail | Condition |
|---|---|---|
| 401 | `"Not authenticated"` | Missing or invalid Bearer token |
| 403 | `"Not authorized to access this contract"` | User is not personal or business |
| 404 | `"Contract not found"` | Contract ID does not exist |
