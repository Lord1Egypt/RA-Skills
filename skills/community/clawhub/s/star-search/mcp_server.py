"""
star-search MCP Server v17.2
零依赖: 用 stdio JSON-RPC 2.0 + aiohttp (SSE for HTTP transport)
MCP 协议: https://modelcontextprotocol.io/specification/2025-06-18

Transports:
- stdio (本地, Claude Desktop / Hermes agent / Cursor / Cline)
- HTTP/SSE (远程, 端口 8765)

Tools:
- web_search: 16 引擎并发搜索
- web_search_news: 新闻模式
- web_search_finance: 财经模式
- get_engines: 列引擎清单
"""

import asyncio
import json
import os
import sys
import argparse
from typing import Any, Optional

import aiohttp

# ============ star-search API ============
STAR_SEARCH_API = os.environ.get(
    "STAR_SEARCH_API",
    "http://127.0.0.1:5000/v1/search"
)

# ============ MCP 协议常量 ============
PROTOCOL_VERSION = "2025-06-18"
SERVER_NAME = "star-search"
SERVER_VERSION = "17.2.0"

# ============ 4 个 Tools 定义 ============
TOOLS_DEF = [
    {
        "name": "web_search",
        "description": (
            "用 star-search (16 引擎: sogou/baidu/360/weixin/bing_cn/csdn/cnblogs/"
            "eastmoney/cls/tencent_cloud/sina_finance/sohu + 5 RSS) 搜索中文/英文/财经。"
            "智能识别 query 自动用最佳引擎。v17.2 支持 answer=true 返回 LLM 总结的"
            "200-400字中文答案 + 来源 (类似 Perplexity AI)。耗时: 普通 0.5-3s, 答案模式 2-4s。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "搜索 query (中文/英文均可). 财经关键词自动识别 (股票/股价/上证/A股/基金/ETF/指数等)"
                },
                "num_results": {
                    "type": "integer",
                    "description": "返回结果数 (1-20, 默认 8)",
                    "default": 8,
                    "minimum": 1,
                    "maximum": 20
                },
                "force_refresh": {
                    "type": "boolean",
                    "description": "是否跳过缓存强制重搜 (默认 false)",
                    "default": False
                },
                "answer": {
                    "type": "boolean",
                    "description": "v17.2: 是否返回 LLM 总结的中文答案 (200-400字 + 来源). 慢 2-4s, 适合需要直接答案的场景",
                    "default": False
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "web_search_news",
        "description": (
            "新闻模式搜索: tech_news 引擎组合 (csdn/cnblogs + 5 RSS: ithome/36kr/sspai/oschina/woshipm)。"
            "适合搜科技/AI/产品/创业新闻。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索 query"},
                "num_results": {"type": "integer", "default": 8, "minimum": 1, "maximum": 20}
            },
            "required": ["query"]
        }
    },
    {
        "name": "web_search_finance",
        "description": (
            "财经专属模式: 7 引擎并发 (eastmoney/cls/sina_finance/sohu/baidu/weixin/bing_cn)。"
            "适合搜股票/股价/A股/基金/ETF/财报/财经新闻。"
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "财经搜索 query"},
                "num_results": {"type": "integer", "default": 8, "minimum": 1, "maximum": 20}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_engines",
        "description": "列出 star-search 全部 16 引擎和 5 种模式, 帮助 LLM 决定用哪个 tool。",
        "inputSchema": {
            "type": "object",
            "properties": {},
            "additionalProperties": False
        }
    },
]


# ============ 调 star-search API ============
async def call_star_search_api(query: str, num_results: int = 8,
                                force_refresh: bool = False,
                                mode: Optional[str] = None,
                                answer: bool = False) -> dict:
    payload = {
        "query": query,
        "top": num_results,
        "force_refresh": force_refresh,
    }
    if mode:
        payload["mode"] = mode
    if answer:
        payload["answer"] = True

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                STAR_SEARCH_API,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status != 200:
                    text = await resp.text()
                    return {"error": f"HTTP {resp.status}: {text[:200]}"}
                return await resp.json()
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}


def format_results(data: dict, with_answer: bool = False) -> str:
    if "error" in data:
        return f"❌ Error: {data['error']}"

    count = data.get("count", 0)
    elapsed = data.get("elapsed_ms", 0)
    results = data.get("results", [])

    # v17.2: 答案模式 (LLM 总结)
    if with_answer and "answer" in data:
        ans = data["answer"]
        if ans.get("answer"):
            lines = [
                f"💡 **AI 答案** ({ans.get('elapsed_ms', 0)}ms, {ans.get('model', '?')}):\n",
                f"{ans['answer']}\n",
                f"---\n",
                f"🔍 **参考来源** ({count} 条, 搜索 {elapsed}ms):\n",
            ]
            for i, r in enumerate(results, 1):
                title = r.get("title", "(无标题)")
                url = r.get("url", "")
                engine = r.get("engine", "?")
                lines.append(f"[{i}] {title}")
                lines.append(f"    {engine} · 🔗 {url}\n")
            return "\n".join(lines)

    # 默认: 蓝链列表
    lines = [f"🔍 找到 {count} 条结果 ({elapsed}ms)\n"]

    for i, r in enumerate(results, 1):
        title = r.get("title", "(无标题)")
        url = r.get("url", "")
        snippet = r.get("snippet", "")
        engine = r.get("engine", "?")
        domain = r.get("domain", "")
        verified = "✓ 跨源" if r.get("verified") else ""

        lines.append(f"[{i}] {title}")
        if snippet:
            lines.append(f"    {snippet[:200]}")
        lines.append(f"    {engine} · {domain} · {verified}")
        lines.append(f"    🔗 {url}\n")

    return "\n".join(lines)


ENGINES_LIST = """🚀 star-search 引擎清单 (16 个, 4 种语言)

**HTTP 引擎 (11)**: sogou · baidu · 360 · weixin · bing_cn · csdn · cnblogs · eastmoney · cls · sina_finance · sohu · tencent_cloud
**RSS 引擎 (5)**: rss_ithome · rss_36kr · rss_sspai · rss_oschina · rss_woshipm

**模式 (5)**:
- deep (默认): CN_ENGINES 中文 7 引擎并发
- tech_news: csdn/cnblogs + 5 RSS
- finance: 7 财经引擎 + 兜底
- global: 语言感知
- dev_rss: 全 RSS + GitHub

**智能识别**: 含财经关键词自动用 finance 模式
**跨源验证**: 同一事实在多源出现标 ✓
"""


# ============ JSON-RPC 2.0 处理 ============
async def handle_request(req: dict) -> Optional[dict]:
    """处理一个 JSON-RPC 2.0 请求, 返回响应 (notification 返回 None)"""
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    # 如果没有 id, 是 notification 不响应
    if req_id is None and "id" not in req:
        # 通知: 静默处理
        if method == "notifications/initialized":
            pass
        return None

    try:
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": {
                        "name": SERVER_NAME,
                        "version": SERVER_VERSION
                    }
                }
            }

        elif method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"tools": TOOLS_DEF}
            }

        elif method == "tools/call":
            name = params.get("name")
            args = params.get("arguments", {})

            if name == "web_search":
                want_answer = args.get("answer", False)
                data = await call_star_search_api(
                    query=args["query"],
                    num_results=args.get("num_results", 8),
                    force_refresh=args.get("force_refresh", False),
                    answer=want_answer
                )
                text = format_results(data, with_answer=want_answer)

            elif name == "web_search_news":
                data = await call_star_search_api(
                    query=args["query"],
                    num_results=args.get("num_results", 8),
                    mode="tech_news"
                )
                text = format_results(data)

            elif name == "web_search_finance":
                data = await call_star_search_api(
                    query=args["query"],
                    num_results=args.get("num_results", 8)
                )
                text = format_results(data)

            elif name == "get_engines":
                text = ENGINES_LIST

            else:
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {"code": -32601, "message": f"Unknown tool: {name}"}
                }

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": text}],
                    "isError": "❌" in text
                }
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method not found: {method}"}
            }

    except Exception as e:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32603, "message": f"{type(e).__name__}: {e}"}
        }


# ============ stdio transport ============
async def run_stdio():
    """stdio transport (本地 LLM agent)"""
    log = lambda *a: print(*a, file=sys.stderr, flush=True)
    log(f"[star-search-mcp] stdio transport, server v{SERVER_VERSION}")
    log(f"[star-search-mcp] API endpoint: {STAR_SEARCH_API}")

    # stdio 通信: 每次读一行 JSON (Content-Length header 模式更标准, 但 line-delimited JSON 简单)
    # 用 line-delimited (一行一个 JSON) - Claude Desktop 支持两种
    stdin, stdout = sys.stdin, sys.stdout
    stdin_buf = b""

    while True:
        # 读一行
        line = await asyncio.get_event_loop().run_in_executor(None, stdin.readline)
        if not line:
            break
        line = line.strip()
        if not line:
            continue

        try:
            req = json.loads(line)
        except json.JSONDecodeError as e:
            err_resp = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"Parse error: {e}"}
            }
            stdout.write(json.dumps(err_resp, ensure_ascii=False) + "\n")
            stdout.flush()
            continue

        resp = await handle_request(req)
        if resp is not None:
            stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            stdout.flush()


# ============ HTTP/SSE transport ============
async def run_http(port: int = 8765):
    """HTTP/SSE transport (远程 LLM agent, SSE 推送响应)"""
    from aiohttp import web

    # SSE 会话: 每个 client 一个 queue
    sse_clients = {}  # session_id -> asyncio.Queue

    async def sse_handler(request: web.Request) -> web.StreamResponse:
        """GET /sse - 建立 SSE 连接, server 推送 endpoint URL"""
        session_id = str(id(request))
        resp = web.StreamResponse(
            status=200,
            headers={
                "Content-Type": "text/event-stream",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
            }
        )
        await resp.prepare(request)
        # 推送 endpoint 给 client
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

    async def messages_handler(request: web.Request) -> web.Response:
        """POST /messages - 客户端发送 JSON-RPC 请求"""
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

    async def health_handler(request: web.Request) -> web.Response:
        return web.Response(
            text=json.dumps({"status": "ok", "server": SERVER_NAME, "version": SERVER_VERSION}),
            content_type="application/json"
        )

    app = web.Application()
    app.router.add_get("/sse", sse_handler)
    app.router.add_post("/messages", messages_handler)
    app.router.add_get("/health", health_handler)

    print(f"[star-search-mcp] HTTP/SSE transport, port {port}", file=sys.stderr, flush=True)
    print(f"[star-search-mcp] API: {STAR_SEARCH_API}", file=sys.stderr, flush=True)
    print(f"[star-search-mcp] Endpoints: GET /sse, POST /messages?session_id=X, GET /health", file=sys.stderr, flush=True)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"[star-search-mcp] Listening on 0.0.0.0:{port}", file=sys.stderr, flush=True)
    while True:
        await asyncio.sleep(3600)


# ============ Main ============
def main():
    parser = argparse.ArgumentParser(description="star-search MCP server v17.2")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio")
    parser.add_argument("--port", type=int, default=8765, help="HTTP port (only for --transport http)")
    parser.add_argument("--api", type=str, default=None, help="star-search API URL override")
    args = parser.parse_args()

    global STAR_SEARCH_API
    if args.api:
        STAR_SEARCH_API = args.api

    if args.transport == "stdio":
        asyncio.run(run_stdio())
    else:
        asyncio.run(run_http(args.port))


if __name__ == "__main__":
    main()
