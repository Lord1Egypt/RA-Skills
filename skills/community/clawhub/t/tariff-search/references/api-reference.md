# API Reference – TurtleClassify

## Endpoint
- **URL:** `POST {base_url}/api/turtle/classify`
- **Default base_url:** `https://www.accio.com`

## Request Payload (TurtleClassifyDTO)
| Field | Required | Type | Description |
|-------|----------|------|-------------|
| `source` | optional (defaults to `alibaba`) | string | Product source identifier |
| `originCountryCode` | ✅ | string | ISO‑3166‑1 alpha‑2 code of the origin country (e.g. `CN`) |
| `destinationCountryCode` | ✅ | string | ISO‑3166‑1 alpha‑2 code of the destination country (e.g. `US`) |
| `productName` | ✅ | string | Name or title of the product |
| `digit` | optional | integer (8 or 10) | Desired HS‑code digit length |
| `productId` | optional | integer | Unique product identifier |
| `productSource` | optional | string | Source of product data |
| `productCategoryId` | optional | integer | Category identifier |
| `productCategoryName` | optional | string | Category name |
| `productProperties` | optional | object | Key‑value map of product attributes (e.g. `{"brand":"Apple","model":"iPhone"}`) |
| `productKeywords` | optional | array of strings | Search keywords |
| `channel` | optional | string | Channel name (e.g. `web`) |

## Response Structure
```json
{ 
  "success": true,
  "msgCode": "200",
  "msgInfo": "ok",
  "data": "{\"success\":true,\"code\":\"200\",\"message\":\"success\",\"data\":{\"hscodeStr\":\"85171200\",\"hscodeDesc\":\"...\",\"tariffRate\":\"0\",\"extendInfo\":\"\"}}"
}
```
- The `data` field may be a JSON **string** or an already‑parsed **object**. After parsing, the inner `data` contains the classification result.

### Classification Result (inner `data`)
| Field | Type | Description |
|-------|------|-------------|
| `hscodeStr` | string | HS code (e.g. `85171200`) |
| `hscodeDesc` | string | English description of the HS code |
| `tariffRate` | string | Tariff rate percentage (may be string, convert to number) |
| `extendInfo` | string | Additional info (often empty) |
| `tariffFormula` | string (optional) | Human‑readable formula of tariff components |
| `tariffCalculateType` | string (optional) | Calculation method, e.g. `ByAmount` |
| `originCountryCode` | string | Echoed from request |
| `destinationCountryCode` | string | Echoed from request |
| `productName` | string | Echoed from request |
| `calculationDetails` | object | Full raw API response captured for debugging |

## Error Codes
- `200` – Success
- `20001` – Parameter validation failed
- `-1` – System error

## Notes
- Maximum **100** products per request (library truncates excess).
- Concurrency limit: ≤10 QPS; library spreads requests with random delays.
- Use title‑case column names (`HS Code`, `Tariff Rate (%)`, …) when exporting to CSV/DataFrames.
