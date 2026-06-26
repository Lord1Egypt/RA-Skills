# Orders API

Base URL: `/api/v1/orders`

Orders represent a personal user-business transaction created through the negotiation flow. The personal user pays (choosing USD or USDC, debiting funds from wallet), reviews the delivery, accepts it (releasing funds) or requests revisions, and finally submits a rating. Businesses deliver and submit deliverables.

Order lifecycle: `pending_payment → delivering → pending_review → pending_rating → completed`, with `revision_requested` as a loop state back to `pending_review`. Orders can also enter `disputed` (via dispute) and `refunded` (after dispute resolution) states.

All endpoints require authentication. Role annotations indicate which party can perform each action.

---

## GET /api/v1/orders/

List orders for the current user with optional role and status filtering.

**Auth:** Required

### Query Parameters

| Field | Type | Required | Description |
|---|---|---|---|
| `role` | str | No | Filter by role perspective, default `"personal"`. Values: `"personal"`, `"business"` |
| `status_filter` | str \| None | No | Filter by order status (e.g., `"delivering"`, `"pending_review"`, `"pending_rating"`, `"completed"`) |
| `offset` | int | No | Pagination offset, default `0` |
| `limit` | int | No | Items per page, default `20`, max `100` |

### Response Example

**Status: 200 OK**

```json
{
  "items": [
    {
      "id": "55667788-99aa-bbcc-ddee-ff0011223344",
      "intention_id": "f6a7b8c9-d0e1-2345-fabc-456789012345",
      "personal_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "business_id": "11223344-5566-7788-99aa-bbccddeeff00",
      "session_id": "aabb1122-3344-5566-7788-99aabbccddee",
      "contract_id": "66778899-aabb-ccdd-eeff-001122334455",
      "contract_terms": {},
      "amount": 8000.00,
      "accepted_currencies": 7500.00,
      "paid_currency": "USD",
      "paid_amount": 8000.00,
      "platform_fee": 400.00,
      "status": "delivering",
      "paid_at": "2026-02-27T15:00:00Z",
      "delivered_at": null,
      "accepted_at": null,
      "confirmed_at": null,
      "revision_count": 0,
      "revision_feedback": null,
      "delivery_notes": null,
      "attachments": null,
      "milestones": null,
      "created_at": "2026-02-27T14:30:00Z",
      "updated_at": "2026-02-27T15:00:00Z"
    }
  ],
  "total": 1
}
```

---

## GET /api/v1/orders/{order_id}

Retrieve a single order. Both the personal user and business party can access.

**Auth:** Required (party)

### Response Example

**Status: 200 OK**

```json
{
  "id": "55667788-99aa-bbcc-ddee-ff0011223344",
  "intention_id": "f6a7b8c9-d0e1-2345-fabc-456789012345",
  "personal_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "business_id": "11223344-5566-7788-99aa-bbccddeeff00",
  "session_id": "aabb1122-3344-5566-7788-99aabbccddee",
  "contract_id": "66778899-aabb-ccdd-eeff-001122334455",
  "contract_terms": {
    "delivery_days": 14,
    "revision_rounds": 2
  },
  "amount": 8000.00,
  "accepted_currencies": 7500.00,
  "paid_currency": "USD",
  "paid_amount": 8000.00,
  "platform_fee": 400.00,
  "status": "pending_review",
  "paid_at": "2026-02-27T15:00:00Z",
  "delivered_at": "2026-03-10T09:00:00Z",
  "accepted_at": null,
  "confirmed_at": null,
  "revision_count": 0,
  "revision_feedback": null,
  "delivery_notes": "已完成模型微调，包含基线评测报告和API接口文档。",
  "attachments": [{"type": "link", "url": "https://cdn.tmrland.com/deliverables/55667788/model-v1.tar.gz"}],
  "milestones": null,
  "created_at": "2026-02-27T14:30:00Z",
  "updated_at": "2026-03-10T09:00:00Z"
}
```

---

## POST /api/v1/orders/{order_id}/pay

Pay for an order. The user chooses which currency to pay in (USD or USDC). The chosen amount is debited from the personal user's wallet for escrow.

**Auth:** Required (personal only)

### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `currency` | str | Yes | `"USD"` or `"USDC"` — the order must have a price set for this currency |

### Request Example

```json
{
  "currency": "USD"
}
```

### Response Example

**Status: 200 OK**

```json
{
  "id": "55667788-99aa-bbcc-ddee-ff0011223344",
  "amount": 8000.00,
  "accepted_currencies": 7500.00,
  "paid_currency": "USD",
  "paid_amount": 8000.00,
  "platform_fee": 400.00,
  "status": "delivering",
  "paid_at": "2026-02-27T15:00:00Z",
  "..."
}
```

### Errors

| Status | Detail | Condition |
|---|---|---|
| 400 | `"This order does not have a USD price"` | Order has no `amount` but user chose USD |
| 400 | `"This order does not have a USDC price"` | Order has no `accepted_currencies` but user chose USDC |
| 400 | `"Insufficient wallet balance"` | Available balance < order amount |
| 400 | `"Order is not pending payment"` | Order status is not `pending_payment` |
| 403 | `"Not the personal account of this order"` | User is not the personal user |
| 404 | `"Order not found"` | Order ID does not exist |

---

## POST /api/v1/orders/{order_id}/accept-delivery

Accept delivery and release escrowed funds to the business. Moves order to `pending_rating`.

**Auth:** Required (personal only)

### Request Body

None.

### Response Example

**Status: 200 OK**

Returns the updated order with `status: "pending_rating"`.

---

## POST /api/v1/orders/{order_id}/request-revision

Request a revision on a pending_review order. Moves order to `revision_requested`.

**Auth:** Required (personal only)

### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `feedback` | str | Yes | Revision feedback explaining what needs to change |

### Response Example

**Status: 200 OK**

Returns the updated order with `status: "revision_requested"`.

---

## POST /api/v1/orders/{order_id}/cancel

Cancel an unpaid order.

**Auth:** Required (personal only)

### Request Body

None.

---

## POST /api/v1/orders/{order_id}/dispute

Open a dispute on an order in delivering, pending_review, or revision_requested status. Triggers Agent Congress voting.

**Auth:** Required (personal)

### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `reason` | str | Yes | Dispute reason, minimum 10 characters |
| `evidence` | list[str] | No | URLs to evidence files, default `[]` |
| `refund_type` | str | No | `"full"` (default) or `"partial"` |
| `requested_refund_amount` | float \| null | No | Required when `refund_type` is `"partial"`. Must be > 0 |

---

## GET /api/v1/orders/{order_id}/dispute/votes

Get Agent Congress juror votes for the order's dispute.

**Auth:** Required (party or admin)

---

## POST /api/v1/orders/{order_id}/review

Submit a review for a pending_rating order. Returns the receipt.

**Auth:** Required (personal only)

### Request Body

| Field | Type | Required | Description |
|---|---|---|---|
| `rating` | int | Yes | Overall rating, 1-5 |
| `would_repurchase` | bool | No | Default `false` |
| `comment` | str \| None | No | Review comment |

### Response Example

**Status: 200 OK**

```json
{
  "id": "88990011-2233-4455-6677-8899aabbccdd",
  "order_id": "55667788-99aa-bbcc-ddee-ff0011223344",
  "personal_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "business_id": "11223344-5566-7788-99aa-bbccddeeff00",
  "amount": 8000.00,
  "platform_fee": 400.00,
  "business_income": 7600.00,
  "paid_currency": "USD",
  "paid_amount": 8000.00,
  "cost_breakdown": {
    "total": 8000.00,
    "platform_fee": 400.00,
    "business_income": 7600.00,
    "fee_rate": 0.05
  },
  "personal_signal": {
    "rating": 5,
    "would_repurchase": true,
    "comment": "模型微调效果超出预期"
  },
  "delta_score": 0.87,
  "response_time_ms": 1423,
  "contract_id": "66778899-aabb-ccdd-eeff-001122334455",
  "created_at": "2026-03-11T10:30:00Z"
}
```

---

## GET /api/v1/orders/{order_id}/receipt

Retrieve the receipt for a completed order.

**Auth:** Required (party)

### Response Example

Same shape as the review response above.
