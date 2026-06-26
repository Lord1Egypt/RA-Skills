# Disputes API

Disputes are resolved by the **Agent Congress** — a panel of 9 AI jurors that independently evaluate evidence and vote. There is no manual negotiation, messaging, or escalation flow. When a dispute is created (via `POST /api/v1/orders/{order_id}/dispute`), it enters `voting` status and the Congress service processes it asynchronously.

All endpoints require authentication.

---

## POST /api/v1/orders/{order_id}/dispute

Create a dispute on an order. Triggers Agent Congress voting.

**Auth:** Required (personal)

### Path Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `order_id` | UUID | Yes | Order ID |

### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `reason` | str | Yes | Dispute reason, minimum 10 characters |
| `evidence` | list[str] | No | URLs to evidence files, default `[]` |
| `refund_type` | str | No | `"full"` (default) or `"partial"` |
| `requested_refund_amount` | float \| null | No | Required when `refund_type` is `"partial"`. Must be > 0 |

### Request Example

```json
{
  "reason": "The delivered model's accuracy is 45%, far below the 70% baseline specified in the contract.",
  "evidence": [
    "https://cdn.tmrland.com/evidence/eval-report-55667788.pdf"
  ],
  "refund_type": "partial",
  "requested_refund_amount": 5000.00
}
```

### Response Example

**Status: 200 OK**

```json
{
  "id": "77889900-aabb-ccdd-eeff-112233445566",
  "order_id": "55667788-99aa-bbcc-ddee-ff0011223344",
  "initiator_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "reason": "The delivered model's accuracy is 45%, far below the 70% baseline specified in the contract.",
  "evidence": ["https://cdn.tmrland.com/evidence/eval-report-55667788.pdf"],
  "contract_snapshot": {"delivery_days": 14, "revision_rounds": 2},
  "refund_type": "partial",
  "requested_refund_amount": 5000.00,
  "status": "voting",
  "resolution": null,
  "resolution_notes": null,
  "refund_amount": null,
  "votes_buyer": 0,
  "votes_seller": 0,
  "avg_confidence": null,
  "resolved_at": null,
  "created_at": "2026-03-12T09:00:00Z",
  "updated_at": "2026-03-12T09:00:00Z"
}
```

### Errors

| Status | Detail | Condition |
|---|---|---|
| 400 | `"Order is not in a disputable status"` | Order not in delivering/pending_review/revision_requested |
| 404 | `"Order not found"` | Order ID does not exist |
| 409 | `"Dispute already exists"` | Order already has a dispute |

---

## GET /api/v1/orders/{order_id}/dispute

Retrieve the dispute associated with an order.

**Auth:** Required (party or admin)

### Response Example

**Status: 200 OK**

Same shape as the dispute creation response. After Congress voting completes, `status` becomes `"resolved"`, and `resolution`, `resolution_notes`, `refund_amount`, `votes_buyer`, `votes_seller`, and `avg_confidence` are populated.

```json
{
  "id": "77889900-aabb-ccdd-eeff-112233445566",
  "order_id": "55667788-99aa-bbcc-ddee-ff0011223344",
  "initiator_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "reason": "The delivered model's accuracy is 45%, far below the 70% baseline specified in the contract.",
  "evidence": ["https://cdn.tmrland.com/evidence/eval-report-55667788.pdf"],
  "contract_snapshot": {"delivery_days": 14, "revision_rounds": 2},
  "refund_type": "partial",
  "requested_refund_amount": 5000.00,
  "status": "resolved",
  "resolution": "partial_refund",
  "resolution_notes": "Majority ruled partial refund due to quality shortfall.",
  "refund_amount": 4000.00,
  "votes_buyer": 6,
  "votes_seller": 3,
  "avg_confidence": 0.82,
  "resolved_at": "2026-03-12T09:05:00Z",
  "created_at": "2026-03-12T09:00:00Z",
  "updated_at": "2026-03-12T09:05:00Z"
}
```

### Errors

| Status | Detail | Condition |
|---|---|---|
| 403 | `"Not authorized"` | User is not a party or admin |
| 404 | `"No dispute found"` | No dispute exists for this order |

---

## GET /api/v1/orders/{order_id}/dispute/votes

Get individual Agent Congress juror votes for the order's dispute.

**Auth:** Required (party or admin)

### Response Example

**Status: 200 OK**

```json
[
  {
    "id": "aa112233-4455-6677-8899-aabbccddeeff",
    "dispute_id": "77889900-aabb-ccdd-eeff-112233445566",
    "juror_index": 1,
    "juror_name": "Contract Analyst",
    "juror_role": "Evaluates whether delivery meets contractual obligations",
    "vote": "buyer",
    "reasoning": "The contract specifies 70% accuracy baseline. The delivered model achieves only 45%, a clear breach of terms.",
    "confidence": 0.95,
    "created_at": "2026-03-12T09:03:00Z"
  },
  {
    "id": "bb223344-5566-7788-99aa-bbccddeeff00",
    "dispute_id": "77889900-aabb-ccdd-eeff-112233445566",
    "juror_index": 2,
    "juror_name": "Technical Reviewer",
    "juror_role": "Assesses technical quality of deliverables",
    "vote": "buyer",
    "reasoning": "Evaluation report confirms accuracy shortfall. The methodology appears sound.",
    "confidence": 0.88,
    "created_at": "2026-03-12T09:03:00Z"
  }
]
```

### Errors

| Status | Detail | Condition |
|---|---|---|
| 403 | `"Not authorized"` | User is not a party or admin |
| 404 | `"No dispute found"` | No dispute exists for this order |

---

## GET /api/v1/disputes/{dispute_id}

Retrieve full dispute details (admin or party). Returns the dispute with Congress vote details.

**Auth:** Required (party or admin)

### Response Example

**Status: 200 OK**

Same fields as `GET /orders/{order_id}/dispute` plus a `votes` array with Congress juror details.

### Errors

| Status | Detail | Condition |
|---|---|---|
| 403 | `"Not a party to this dispute"` | User is not a party or admin |
| 404 | `"Dispute not found"` | Dispute ID does not exist |

---

## Dispute Status Flow

```
voting → resolved
```

- `voting`: Congress AI jurors are evaluating the dispute
- `resolved`: Verdict delivered. Resolution is one of: `full_refund`, `partial_refund`, `seller_wins`

If Congress voting times out (>1 hour), the dispute auto-resolves with `full_refund` as a safety net.

## Order Status After Dispute

- `disputed`: Order moves to this status when a dispute is created
- `refunded`: Order moves to this status when the dispute resolves with a refund (full or partial)
- Order returns to normal flow if `seller_wins`
