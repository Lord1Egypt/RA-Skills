# MCP Server 零依赖实现 (v17.0)

## 背景

star-search v17.0 要做标准 **Model Context Protocol (MCP)** server, 让 LLM agent (Claude Desktop / Cursor / Cline / Hermes) 能直接调用 `web_search` 当作 tool。

官方 Anthropic 出了 `mcp` Python SDK (`pip install mcp`)。**项目历史约束: 不引新依赖**。

**解法**: 用 stdlib + 已装的 aiohttp **手搓** MCP 协议 (JSON-RPC 2.0 + SSE), 零新依赖。

## MCP 协议要点

**协议版本**: `2025-06-18` (2026年6月当前)

**两种 transport**:
1. **stdio** — 本地 LLM agent (Claude Desktop), 一行一个 JSON
2. **HTTP/SSE** — 远程 LLM agent, server 推送 endpoint URL

**3 个核心 JSON-RPC 方法**:
- `initialize` — 握手, 返回 `protocolVersion` + `capabilities` + `serverInfo`
- `tools/list` — 列出 4 个 tools (inputSchema 用 JSON Schema)
- `tools/call` — 调用 tool, 返回 `{content: [{type: "text", text: "..."}]}`

**2 个 notification** (无 id 不响应):
- `notifications/initialized` — initialize 完成后客户端发
- `notifications/cancelled` — 取消正在执行的请求

## stdio transport (本地)

```python
import sys, json, asyncio

async def run_stdio():
    stdin, stdout = sys.stdin, sys.stdout
    while True:
        # 一行一个 JSON (Content-Length 模式更标准, 但 line-delimited 简单 Claude Desktop 也支持)
        line = await asyncio.get_event_loop().run_in_executor(None, stdin.readline)
        if not line: break
        line = line.strip()
        if not line: continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            stdout.write(json.dumps({
                "jsonrpc": "2.0", "id": None,
                "error": {"code": -32700, "message": f"Parse error: {e}"}
            }) + "\n")
            stdout.flush()
            continue

        resp = await handle_request(req)  # 业务逻辑
        if resp is not None:
            stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            stdout.flush()
```

**关键**: `notification` (没 `id` 字段) 处理后**返回 None**, 不写 stdout。

## HTTP/SSE transport (远程) — 难点

**MCP HTTP 协议**:
1. 客户端 `GET /sse` — 建立 SSE 长连接
2. server **立即推送** `event: endpoint\ndata: <完整 URL>`
3. 客户端 `POST /messages?session_id=<从 endpoint URL 拿>` — 发 JSON-RPC 请求
4. server 把响应**通过对应 session 的 SSE 通道推回**

```python
from aiohttp import web
import asyncio

sse_clients = {}  # session_id -> asyncio.Queue

async def sse_handler(request):
    session_id = str(id(request))  # 用 id(request) 当 session_id
    resp = web.StreamResponse(
        status=200,
        headers={
            "Content-Type": "text/event-stream",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )
    await resp.prepare(request)

    # 立即推 endpoint
    endpoint_url = f"http://{request.host}/messages?session_id={session_id}"
    await resp.write(f"event: endpoint\ndata: {endpoint_url}\n\n".encode())

    sse_clients[session_id] = asyncio.Queue()
    try:
        while True:
            msg = await sse_clients[session_id].get()
            await resp.write(f"data: {json.dumps(msg, ensure_ascii=False)}\n\n".encode())
    except (asyncio.CancelledError, ConnectionResetError):
        pass
    finally:
        sse_clients.pop(session_id, None)
    return resp

async def messages_handler(request):
    session_id = request.query.get("session_id")
    if not session_id or session_id not in sse_clients:
        return web.Response(status=400, text="Invalid session_id")

    try:
        req = await request.json()
    except Exception as e:
        return web.Response(status=400, text=f"Invalid JSON: {e}")

    resp = await handle_request(req)
    if resp is not None:
        await sse_clients[session_id].put(resp)
    return web.Response(status=202, text="Accepted")
```

## 客户端测试脚本 — session_id 坑

**坑**: 不要把 `session_id` 写死! 客户端必须**先解析 server 推的 endpoint URL** 拿 session_id:

```python
import aiohttp
from urllib.parse import urlparse

async with aiohttp.ClientSession() as s:
    async with s.get("https://search.token-star.cn/mcp/sse") as r:
        await r.content.readline()  # event: endpoint
        line = await r.content.readline()  # data: <URL>
        endpoint_full = line.decode().replace("data: ", "").strip()
        parsed = urlparse(endpoint_full)
        messages_url = f"{URL_BASE}{parsed.path}?{parsed.query}"
        # 写死 session_id → POST 400 Invalid session_id
```

## nginx 反代 SSE (生产环境) — 关键 3 行

```nginx
location /mcp/ {
    proxy_pass http://127.0.0.1:8765/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;

    # SSE 关键 3 行
    proxy_buffering off;             # 关 nginx 缓冲, 立即推
    proxy_read_timeout 86400s;       # 长连接
    proxy_set_header Connection '';  # 移除 hop-by-hop header
}
```

**不加 `proxy_buffering off`, SSE 会被 nginx 缓冲, client 永远收不到 server 推的 endpoint!**

## Pitfalls (踩过的坑)

1. **写死 session_id → 客户端 POST 报 "Invalid session_id"** — 必须从 server 推的 endpoint URL 解析
2. **忘加 `proxy_buffering off` → SSE 不推送** — 客户端永远等不到 endpoint event
3. **notification 当 request 处理 → stdout 写一行 JSON 给 client 报错** — 严格判断 `if req_id is None and "id" not in req: return None`
4. **`mcp` Python SDK 装不上** → 零依赖手搓是 fallback, 同样能跑完整协议
5. **HTTPS 端点的 SSE `data:` URL 是 `http://`** — server 内推的是内网 URL, client 要把 `http://` 替换成 `https://`

## 4 个 MCP Tools 设计 (v17.0)

| Tool | inputSchema | 引擎 |
|---|---|---|
| `web_search` | `{query, num_results?, force_refresh?}` | 默认 deep + 财经 query 自动 finance |
| `web_search_news` | `{query, num_results?}` | tech_news (csdn/cnblogs + 5 RSS) |
| `web_search_finance` | `{query, num_results?}` | 7 财经引擎 |
| `get_engines` | `{}` | 16 引擎清单 (LLM 决策用) |

**v17.2 升级**: `web_search` 加 `answer: bool` 参数, 触发 LLM 总结模式。

## Claude Desktop 接入配置

`~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "star-search": {
      "command": "python3",
      "args": ["/Users/lizhe/.hermes/skills/research/star-search/mcp_server.py"],
      "env": {
        "STAR_SEARCH_API": "http://127.0.0.1:5000/v1/search"
      }
    }
  }
}
```

**远程 (无需本地 Python)**: 任何 HTTP MCP client 连 `https://search.token-star.cn/mcp/sse`。

## 为什么不引 mcp SDK

| 维度 | mcp SDK | 零依赖自实现 |
|---|---|---|
| 安装 | `pip install mcp` (用户拒绝) | 0 步 |
| 体积 | ~2MB | ~14KB |
| 协议覆盖 | 全 | 全 (JSON-RPC 2.0 + SSE) |
| Claude Desktop 兼容 | 100% | 100% (只要协议对) |

**结论**: 项目小 + 协议简单 + 用户对依赖敏感 → 零依赖自实现最稳。
