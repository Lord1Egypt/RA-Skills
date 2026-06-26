# WhatsApp Number Checker API

REST API reference for making requests or generating sample code when MCP is not used.

## Base URL

```
https://wa-check-api.whatsabot.com
```

## Authorization

Include this header on every request:

```
x-api-key: YOUR_API_KEY
```

## Rate limit

1000 requests per hour.

---

## Check if number is on WhatsApp

**GET** `/api/wa/check`

Verify whether a phone number is registered on WhatsApp.

### Query parameters

| Parameter | Required | Description                          |
|-----------|----------|--------------------------------------|
| `phone`   | Yes      | E.164 or digits only, e.g. `34605797764` |

### Success response (code: 0)

```json
{
  "code": 0,
  "result": {
    "exist": true
  }
}
```

- `result.exist`: `true` means the number is registered on WhatsApp; `false` means it is not.

### Error codes

| code | message                  | Description              |
|------|--------------------------|--------------------------|
| 1001 | Missing API key          | x-api-key header missing |
| 1002 | Invalid phone parameter  | Invalid phone parameter  |
| 1003 | Invalid API key          | API key is invalid       |
| 1004 | Insufficient credits     | Not enough credits       |
| 1005 | Rate limit exceeded      | Rate limit exceeded      |
| 1006 | Upstream service error   | Upstream service error   |
| 1007 | Failed to deduct credit  | Credit deduction failed  |
| 1000 | Internal error           | Internal error           |

### Examples

**cURL**

```bash
curl --request GET \
  --url "https://wa-check-api.whatsabot.com/api/wa/check?phone=34605797764" \
  --header "x-api-key: YOUR_API_KEY"
```

**Node (fetch)**

```javascript
const res = await fetch('https://wa-check-api.whatsabot.com/api/wa/check?phone=34605797764', {
  headers: { 'x-api-key': process.env.API_KEY }
})
const data = await res.json()
// { code: 0, result: { exist: boolean } }
```

---

## Get available credits

**GET** `/api/user/credits`

Returns the current available credits for the API key. No query parameters; only the auth header is required.

### Success response (code: 0)

```json
{
  "code": 0,
  "result": { "total": 42 }
}
```

### Example

```bash
curl --request GET \
  --url "https://wa-check-api.whatsabot.com/api/user/credits" \
  --header "x-api-key: YOUR_API_KEY"
```
