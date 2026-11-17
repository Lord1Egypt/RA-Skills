# 企查查中转站 API 参考

企查查中转站通过统一鉴权入口提供企查查 MCP 与 Chat API，将 6 类、185 项企业数据能力中转给 OpenClaw 和其他 MCP 客户端。

生产环境地址：`https://zqcc.mkstone.club`

## Credentials

zqcc exposes two credential types:

| Credential | Format | Use |
| --- | --- | --- |
| AppKey | `zqcc_...` | MCP endpoint and Chat API |
| Login JWT | JWT string returned by phone login | Personal console HTTP APIs |

This skill requires only the AppKey. Never send the login JWT to MCP and never use the AppKey as a website login token.

## Register and Get an AppKey

Recommended path:

1. Open <https://zqcc.mkstone.club>.
2. Enter a mainland China mobile number.
3. Complete the image captcha and request an SMS code.
4. Submit the SMS code through “登录 / 自动注册”. New numbers are registered automatically.
5. Copy the AppKey from the user console.

The first login response may show the complete AppKey directly. Later, the console loads the active AppKey from `GET /api/me/api-keys`. Rotating the AppKey disables all previously active keys immediately.

## MCP Endpoint

```text
POST /mcp/stream
Authorization: Bearer <ZQCC_APP_KEY>
Content-Type: application/json
```

The endpoint implements stateless JSON-RPC requests. It is commonly configured as Streamable HTTP, but callers should not depend on SSE output or server-side MCP sessions.

### Initialize

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": { "name": "example", "version": "1.0.0" }
  }
}
```

### List Tools

```json
{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}
```

Use this response as the authority for current tool names, descriptions, and input schemas.

### Call a Tool

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "get_company_registration_info",
    "arguments": {
      "searchKey": "深圳市腾讯计算机系统有限公司"
    }
  }
}
```

Typical response envelope:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      { "type": "text", "text": "..." }
    ]
  }
}
```

The router recognizes `company`, `risk`, `ipr`, `operation`, `executive`, and `history` tool families. Names returned by `tools/list` should be used exactly. Compatibility aliases such as `company.get_contact_info` may work, but are not preferred.

## Chat API

```text
POST /api/v1/chat
Authorization: Bearer <ZQCC_APP_KEY>
Content-Type: application/json
```

Request:

```json
{
  "sessionId": "customer-001",
  "message": "查询这家企业的工商信息、司法风险和经营动态"
}
```

Response:

```json
{
  "sessionId": "customer-001",
  "answer": "..."
}
```

Both fields are required and `sessionId` has a maximum length of 120 characters. The server retains a bounded recent history by AppKey and session ID.

## MCP Client Configuration

```json
{
  "mcpServers": {
    "zqcc": {
      "url": "https://zqcc.mkstone.club/mcp/stream",
      "headers": {
        "Authorization": "Bearer <ZQCC_APP_KEY>"
      }
    }
  }
}
```

Recommended timeout: 300 seconds for request and response handling.

## Billing

- Successful business tool calls consume credits according to the tool price.
- Tools without an explicit price currently use a fallback charge.
- `tools/list` and other non-business discovery calls are not user-visible billable calls.
- A successful Chat API answer costs chat credits; successful tool calls performed during the chat are billed separately.
- Prices are service-side policy and may change. Check the zqcc console for the authoritative balance and call ledger.

## HTTP Errors

| Status | Meaning | Action |
| --- | --- | --- |
| 400 | Invalid JSON, arguments, or unroutable tool | Fix the request; refresh `tools/list` |
| 401 | Missing or invalid AppKey | Check `ZQCC_APP_KEY`; do not retry repeatedly |
| 402 | Insufficient zqcc credits | Recharge through the zqcc console |
| 502 | Upstream request failure | Retry once with backoff if the operation is safe |
| 503 | No available upstream key or all upstream quotas exhausted | Retry later |

Some MCP-level failures are returned with HTTP 200 inside a JSON-RPC `error` or `result.isError` response. Inspect both the HTTP status and JSON body.

## Public User Console APIs

These endpoints exist for the website console and require the login JWT, not the AppKey:

- `GET /api/me`
- `GET /api/me/api-keys`
- `POST /api/me/api-keys/rotate`
- `GET /api/me/logs`
- `POST /api/me/redeem-codes/redeem`
- `GET|POST /api/me/wechat-bots`

The skill does not automate login, SMS verification, key rotation, recharge, WeChat bot creation, or administrator operations. Those actions should remain explicit user-controlled workflows.
