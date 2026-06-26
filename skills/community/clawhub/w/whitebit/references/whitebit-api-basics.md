# WhiteBIT API Basics

Use this as a fast reference for request shape and failure handling.

## Core Transport Rules
- Base URL pattern: `https://whitebit.com/api/v4/{endpoint}`
- Public endpoints: `GET` with query parameters.
- Private endpoints: `POST` with JSON body.
- Responses are JSON; timestamps are Unix time.

## Private Authentication Essentials
Private requests require HMAC-SHA512 signing.

Required headers:
- `Content-type: application/json`
- `X-TXC-APIKEY`: public API key
- `X-TXC-PAYLOAD`: base64-encoded request body
- `X-TXC-SIGNATURE`: HMAC-SHA512 signature (hex)

For many private calls, request body includes:
- `request`: endpoint path (for example `/api/v4/main-account/balance`)
- `nonce`: unique identifier

## Rate Limits
- Public REST endpoints: `2000 requests / 10 sec`
- Private REST endpoints: varies by endpoint (check endpoint docs via MCP search)

## Error Formats
Public error shape:

```json
{
  "success": false,
  "message": "ERROR MESSAGE",
  "params": []
}
```

Private error shape:

```json
{
  "code": 0,
  "message": "MESSAGE",
  "errors": {
    "PARAM1": ["MESSAGE"],
    "PARAM2": ["MESSAGE"]
  }
}
```

## Endpoint Groups To Query Via MCP
- `Market Data`
- `Spot Trading`
- `Account & Wallet`

Use WhiteBIT docs MCP search before every new endpoint/action to avoid stale assumptions.
