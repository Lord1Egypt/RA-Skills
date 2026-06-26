# Sushiro China — wechat-mini-program API reference

Base: `https://crm-cn-prd.sushiro.com.cn/wechat/api/2.0`

All endpoints are `GET`. Three public endpoints were verified accessible with the shared mini-program Bearer token. Other paths (`menu`, `ticket`, `groupQueues`, `getStoreByArea`, `config`, …) return 404 with the shared token.

## Required headers

```
Authorization: Bearer 4OI44O844Kv44Oz5qSc6Ki855So77yad2VjaGF05YWx6YCa4
Referer:       https://servicewechat.com/wx7ac31ef6c073a7ed/159/page-frame.html
User-Agent:    Mozilla/5.0 ...   (any browser-like UA)
Accept:        */*
```

- The Bearer token is a **shared wechat-mini-program credential**, not user-bound. No login required.
- The `Referer` is mandatory — without it the gateway returns 403.
- TLS fingerprint matters. `python-requests`/`httpx` get blocked by upstream CDN; curl works. Node native https works.

## Endpoint 1: list stores

```
GET /stores?latitude=<lat>&longitude=<lng>&numresults=<n>
```

- All three query params are required. `latitude=1&longitude=1` is safe to use when you don't need geo-sorting (returns all stores in arbitrary order).
- Pass real coords to sort by distance from that point (`distance` field is populated).
- `numresults=10000` returns the full set (current total: ~111 stores).

Response shape is occasionally wrapped — sometimes a raw `[...]` array, sometimes `{"<key>": [...]}`. The `sushiro` script handles both.

Each element (selected fields):

```json
{
  "id": 1012,
  "name": "南山天利名城店",
  "nameKana": "深圳",
  "address": "广东省深圳市南山区海德三道195号天利名城购物中心304",
  "area": "深圳南山区",
  "latitude": 22.518675,
  "longitude": 113.935388,
  "distance": "-1",
  "storeStatus": "OPEN",
  "netTicketStatus": "ONLINE",
  "wait": 0,
  "waitTimeCounter": -1,
  "waitTimeCap": 180,
  "tablesCapacity": 6,
  "countersCapacity": 1,
  "reservationStatus": "...",
  "openDate": "2026-01-01"
}
```

## Endpoint 2: single store detail

```
GET /getStoreById?storeId=<id>
```

Returns one store object with the same shape as above, plus extra fields:
`groupQueues`, `groupQueuesCount`, `maxCustomersMobileTable`, `cancellationMobileMinutes`, etc.

## Endpoint 3: areas list

```
GET /areas
```

Returns a flat JSON array of strings — every `area` value used by stores (e.g. `"深圳南山区"`, `"北京海淀区"`). Useful for building a picker.

## Field semantics

| Field | Type | Meaning |
|---|---|---|
| `id` | int | Store id (3-4 digits) |
| `storeStatus` | string | `OPEN` \| `CLOSED` \| `PRE_OPEN` |
| `netTicketStatus` | string | `ONLINE` accepts remote queue tickets; `OFFLINE` walk-in only |
| `wait` | int | **Groups currently in queue**, not minutes |
| `waitTimeCounter` | int | -1 when not exposed; otherwise estimated min for counter seats |
| `waitTimeCap` | int | Upper bound estimate in minutes (typically 180) |
| `nameKana` | string | City name (legacy field name from JP schema, contains 中文) |
| `area` | string | Neighborhood, formatted `<city><district>` |
| `tablesCapacity` | int | Table seats |
| `countersCapacity` | int | Counter seats |

## Failure modes

- **401 / 403** — token rotated, or `Referer` header missing.
- **404** — endpoint path doesn't exist (most random paths under `/wechat/api/2.0/` 404 with a Spring Boot–style error body).
- **5xx** — CDN/origin issue; retry after backoff.
- **Empty array** — usually means the geo-filter is bogus or `numresults=0`.

## Useful jq snippets

```bash
# Top 10 busiest stores nationwide
sushiro stores --json | jq 'sort_by(-(.wait // 0)) | .[:10]'

# All cities with their total queue
sushiro stores --json | jq 'group_by(.nameKana) | map({city: .[0].nameKana, wait: map(.wait // 0) | add}) | sort_by(-.wait)'

# Stores that became OPEN in last 30 days (using openDate)
sushiro stores --json | jq --arg d "$(date -v-30d +%Y-%m-%d)" 'map(select(.openDate >= $d))'
```
