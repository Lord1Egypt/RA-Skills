# 直连协议参考（MCP Streamable HTTP）

`scripts/xianmu_mcp.py` 已封装下述全部细节；本文件供无 Python 环境时用 curl 兜底，或排查问题时理解原理。

## 端点与鉴权

- 端点：`https://www.wwzu.com/mcp`（可用环境变量 `XIANMU_MCP_URL` 覆盖，勿随意改动）
- 认证：每个请求带 `Authorization: Bearer xm-你的Key`
- 传输：MCP Streamable HTTP（JSON-RPC 2.0 over HTTP POST；响应可能为普通 JSON 或 SSE 流）

## 调用三步（curl 示例）

```bash
KEY="xm-你的Key"; URL="https://www.wwzu.com/mcp"

# 1) initialize 握手 —— 从响应头记录 mcp-session-id
curl -sS -D /tmp/xm_headers -o /tmp/xm_body "$URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $KEY" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"curl-client","version":"1.0"}}}'
SID=$(grep -i '^mcp-session-id:' /tmp/xm_headers | tr -d '\r' | awk '{print $2}')

# 2) notifications/initialized —— 返回 202，无响应体
curl -sS -o /dev/null -w "%{http_code}\n" "$URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $KEY" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'

# 3) tools/call —— 记得带会话头；响应可能是 SSE（data: 行）或 JSON
curl -sS "$URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "Authorization: Bearer $KEY" \
  -H "Mcp-Session-Id: $SID" \
  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_site_overview","arguments":{}}}'
```

`tools/list` 同理（`params: {}`）。工具结果在 `result.content[].text`（JSON 字符串），
`result.isError=true` 表示工具业务错误。

## 响应解析要点

- 普通响应 `Content-Type: application/json`：整个 body 就是一个 JSON-RPC 响应对象。
- SSE 响应 `Content-Type: text/event-stream`：逐行找 `data:` 前缀，每行 `data:` 后是一个
  JSON-RPC 对象，取含 `result`/`error` 且 `id` 匹配的那个。
- `notifications/initialized` 是通知（无 id），服务端回 202 且无 body，不要当错误。

## 会话与重试

- 会话标识在 `mcp-session-id` 响应头，后续每个请求都要回传。
- 会话过期表现为 HTTP 404（Session not found）：丢弃会话、从第 1 步重新握手再试。
  `xianmu_mcp.py` 已内置"404 自动重握手一次"。

## 错误语义

| HTTP | 含义 | 客户端动作 |
|---|---|---|
| 401 | API Key 无效/已撤销/过期 | 到 wwzu.com/mcp-keys.php 重建；更新 `XIANMU_API_KEY` |
| 429 | 4 个免费查询工具今日额度用尽（普通 100 次/Key、VIP 300 次） | 调 `reset_daily_quota` 扣积分重置，或次日自动恢复 |
| 404 | URL 不对（未指到 /mcp）或会话失效 | 核对 URL；重新 initialize |
| 2xx + `result.isError=true` | 工具业务错误（参数互斥、积分不足等） | 读 `content[].text` 里的原因与引导 |

积分不足、无效套餐等**业务错误不通过 HTTP 状态码表达**，都在 2xx 响应的 `isError` 文本里。

## 脚本环境变量与退出码

| 变量 | 说明 |
|---|---|
| `XIANMU_API_KEY` | 必填。脚本会尝试从脚本目录/当前目录的 `.env` 补读（真实环境变量优先） |
| `XIANMU_MCP_URL` | 默认 `https://www.wwzu.com/mcp` |

退出码：`0` 成功；`1` 传输/协议/配置错误（stderr 已翻译 401/429 为人话）；`2` 工具业务错误。

## 排错

- **SSL 证书错误**（企业代理/自建 CA）：修好系统证书链是正解；临时绕过有中间人风险，不建议。
- **超时**：脚本单请求超时 90 秒；`chat_with_character`（LLM 生成）可能接近上限，属正常。
- **频次**：脚本每次调用独立握手（无长连接），频繁调用请优先使用已配置 MCP 的客户端以省额度
  ——额度只对 4 个内容查询工具计数，计费层与角色对话不受影响。
