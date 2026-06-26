#!/usr/bin/env python3
"""
Unified Web Search - Tavily (primary) + 智谱 Zhipu (fallback)
"""

import os
import sys
import json
import urllib.request
import urllib.error
import http.cookiejar

# ── Tavily ──────────────────────────────────────────────────────────────────

TAVILY_URL = "https://api.tavily.com/search"


def _tavily_key():
    return os.environ.get("TAVILY_API_KEY")


def tavily_search(query, max_results=5, days=3):
    key = _tavily_key()
    if not key:
        return None  # signal: not configured, try fallback

    payload = json.dumps({
        "api_key": key,
        "query": query,
        "max_results": max_results,
        "include_answer": True,
        "search_depth": "basic",
        "days": days,
    }).encode("utf-8")

    req = urllib.request.Request(TAVILY_URL, data=payload, headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"error": f"Tavily: {e}", "_engine": "tavily"}


# ── 智谱 Zhipu MCP ─────────────────────────────────────────────────────────

ZHIPU_MCP_URL = "https://open.bigmodel.cn/api/mcp/web_search_prime/mcp"


def _zhipu_key():
    key = os.environ.get("ZHIPU_API_KEY")
    if key:
        return key
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(config_path):
        try:
            with open(config_path) as f:
                cfg = json.load(f)
            for p in ["generic", "glm"]:
                k = cfg.get("models", {}).get("providers", {}).get(p, {}).get("apiKey", "")
                if k:
                    return k
        except Exception:
            pass
    return ""


def _zhipu_session(api_key):
    """Create MCP session, return (opener, headers, session_id)."""
    cj = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json, text/event-stream",
    }
    session_id = None

    try:
        init_payload = json.dumps({
            "jsonrpc": "2.0", "id": 0, "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "web-search", "version": "1.0"},
            },
        }).encode("utf-8")

        req = urllib.request.Request(ZHIPU_MCP_URL, data=init_payload, headers=headers, method="POST")
        with opener.open(req, timeout=10) as resp:
            session_id = resp.headers.get("mcp-session-id")
            if session_id:
                cj.set_cookie(http.cookiejar.Cookie(
                    name="mcp-session-id", value=session_id,
                    path="/", domain="open.bigmodel.cn",
                ))

            notif = json.dumps({
                "jsonrpc": "2.0", "method": "notifications/initialized",
            }).encode("utf-8")
            notif_req = urllib.request.Request(ZHIPU_MCP_URL, data=notif, headers=headers, method="POST")
            if session_id:
                notif_req.add_header("mcp-session-id", session_id)
            opener.open(notif_req, timeout=5)
    except Exception:
        pass

    return opener, headers, session_id


def zhipu_search(query, recency="noLimit"):
    api_key = _zhipu_key()
    if not api_key:
        return {"error": "ZHIPU_API_KEY not set", "_engine": "zhipu"}

    opener, headers, session_id = _zhipu_session(api_key)

    payload = json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
        "params": {
            "name": "web_search_prime",
            "arguments": {
                "search_query": query[:200],
                "search_recency_filter": recency,
                "content_size": "medium",
                "location": "cn",
            },
        },
    }).encode("utf-8")

    req = urllib.request.Request(ZHIPU_MCP_URL, data=payload, headers=headers, method="POST")
    if session_id:
        req.add_header("mcp-session-id", session_id)

    try:
        with opener.open(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            for line in raw.strip().split("\n"):
                if line.startswith("data:"):
                    result = json.loads(line[5:])
                    result["_engine"] = "zhipu"
                    return result
            return {"error": "Empty response from Zhipu", "_engine": "zhipu"}
    except Exception as e:
        return {"error": f"Zhipu: {e}", "_engine": "zhipu"}


# ── Unified ─────────────────────────────────────────────────────────────────

def search(query, max_results=5, days=3):
    """Search with Tavily (primary), fallback to Zhipu."""
    # 1) Try Tavily
    result = tavily_search(query, max_results=max_results, days=days)
    if result is None:
        # Tavily key not configured
        result = zhipu_search(query)
        if "error" in result:
            return {"error": "Neither Tavily nor Zhipu API key configured", "_engine": "none"}
        return result

    if "error" not in result:
        result["_engine"] = "tavily"
        return result

    # 2) Tavily failed → fallback
    zhipu_result = zhipu_search(query)
    zhipu_result["_tavily_error"] = result.get("error", "")
    return zhipu_result


# ── Formatting ──────────────────────────────────────────────────────────────

def format_results(result):
    if "error" in result:
        tavily_err = result.get("_tavily_error", "")
        extra = f"\n（Tavily 失败: {tavily_err}，已回退到智谱）" if tavily_err else ""
        return f"❌ 搜索失败{extra}: {result['error']}"

    engine = result.get("_engine", "?")
    lines = []

    if engine == "tavily":
        if result.get("answer"):
            lines.append(f"📝 **答案摘要**\n{result['answer']}\n")
        for i, item in enumerate(result.get("results", []), 1):
            lines.append(f"**{i}. {item.get('title', '')}**")
            lines.append(f"   {item.get('content', '')[:200]}")
            lines.append(f"   🔗 {item.get('url', '')}\n")
    else:
        # Zhipu MCP format
        try:
            content = result.get("result", {}).get("content", [])
            text = content[0].get("text", "") if content else ""
            parsed = json.loads(text)
            if isinstance(parsed, str):
                items = json.loads(parsed)
            elif isinstance(parsed, list):
                items = parsed
            else:
                items = []
            for i, item in enumerate(items, 1):
                lines.append(f"**{i}. {item.get('title', '')}**")
                lines.append(f"   {item.get('content', '')[:200]}")
                lines.append(f"   🔗 {item.get('link', '')}\n")
        except Exception:
            lines.append(str(result))

    tag = "Tavily" if engine == "tavily" else "智谱 Zhipu"
    return f"🔍 [{tag}] {len(lines)//3} 条结果\n\n" + "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("用法: search.py <query> [--days=N]")
        sys.exit(1)

    query_parts, days = [], 3
    for arg in sys.argv[1:]:
        if arg.startswith("--days="):
            try:
                days = min(7, max(1, int(arg.split("=")[1])))
            except ValueError:
                pass
        else:
            query_parts.append(arg)

    query = " ".join(query_parts)
    print(f"🔍 正在搜索: {query}\n")

    result = search(query, days=days)
    print(format_results(result))


if __name__ == "__main__":
    main()
