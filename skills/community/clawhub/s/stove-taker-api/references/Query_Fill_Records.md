# Query Fill Records [â](#query-fill-records)

## Endpoint Information [â](#endpoint-information)

**Endpoint**: `GET /api/v1/orders/filled`

**Description**: Flexible query of order fill records, supports multiple filtering conditions, pagination, and sorting

**Authentication**: API Key credential authentication

## Query Parameters [â](#query-parameters)

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| order_id | uuid | No | Order ID |
| order_hash | string | No | Order hash |
| taker | string | No | Taker address |
| tx_hash | string | No | Transaction hash |
| fill_quantity_min | string | No | Minimum fill quantity |
| fill_quantity_max | string | No | Maximum fill quantity |
| fill_amount_min | string | No | Minimum fill amount |
| fill_amount_max | string | No | Maximum fill amount |
| fee_amount_min | string | No | Minimum fee amount |
| fee_amount_max | string | No | Maximum fee amount |
| incentive_amount_min | string | No | Minimum incentive amount |
| incentive_amount_max | string | No | Maximum incentive amount |
| block_number_min | long | No | Minimum block number |
| block_number_max | long | No | Maximum block number |
| status | enum | No | Fill status (see OrderStatus) |
| created_after | string | No | Created after |
| created_before | string | No | Created before |
| sort_by | string | No | Sort field |
| sort_order | string | No | Sort direction |
| page | int | No | Page number |
| page_size | int | No | Page size |

## Response Parameters [â](#response-parameters)

| Field | Type | Description |
| --- | --- | --- |
| total | int | Total records |
| page | int | Current page |
| page_size | int | Page size |
| total_pages | int | Total pages |
| fills | object array | Fill record list |
| fills[].id | uuid | Fill record unique identifier |
| fills[].order_id | uuid | Order ID |
| fills[].order_hash | string | Order hash |
| fills[].taker | string | Taker address |
| fills[].fill_quantity | string | Fill quantity |
| fills[].fill_amount | string | Fill amount |
| fills[].fee_amount | string | Fee amount |
| fills[].incentive_amount | string | Incentive amount |
| fills[].tx_hash | string | Transaction hash |
| fills[].block_number | long | Block number |
| fills[].status | enum | Fill status (see OrderStatus) |
| fills[].created_at | string | Creation time |

## Request Example [â](#request-example)

```bash
curl -X GET "/api/v1/orders/filled?page=1&page_size=20" \
     -H "X-API-Key: YOUR_API_KEY" \
     -H "Content-Type: application/json"
```

## Response Example [â](#response-example)

```json
{
    "code": 0,
    "data": {
        "total": 100,
        "page": 1,
        "page_size": 20,
        "total_pages": 5,
        "fills": [
            {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "order_id": "660e8400-e29b-41d4-a716-446655440001",
                "order_hash": "0x1234567890abcdef...",
                "taker": "0xabcdef1234567890...",
                "fill_quantity": "50",
                "fill_amount": "7512500000000000000000",
                "fee_amount": "75125000000000000000",
                "incentive_amount": "500000000000000000",
                "tx_hash": "0xfedcba0987654321...",
                "block_number": 12345678,
                "status": "partially_filled",
                "created_at": "2025-01-17T03:10:00Z"
            }
        ]
    }
}
```

## Enum Types [â](#enum-types)

### OrderStatus - Order Status [â](#orderstatus-order-status)

| Enum | Description |
| --- | --- |
| partially_filled | Partially filled |
| filled | Fully filled |

## Notes [â](#notes)

- Fill records are sorted by creation time in descending order
- Can query by multiple condition combinations
- Supports filtering by amount range, quantity range, etc.
