#!/usr/bin/env python3
"""
智谱工具 - 网络搜索、网页读取、仓库文档搜索和文件解析
默认使用 Z.AI Coding Plan MCP 端点（免费额度）
设置 ZHIPU_USE_MCP=false 切换到旧版 bigmodel API

使用方式:
    python3 zhipu_tool.py web_search "搜索关键词" [--count 10]
    python3 zhipu_tool.py web_reader "https://example.com"
    python3 zhipu_tool.py zread search "openai/openai" "how to use"
    python3 zhipu_tool.py zread structure "openai/openai" [--path src/]
    python3 zhipu_tool.py zread read "openai/openai" "README.md"
    python3 zhipu_tool.py file_parser /path/to/file [--file-type PDF]
    python3 zhipu_tool.py vision /path/to/media [--prompt "描述"] [--type image|video]
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("请安装 requests: pip install requests", file=sys.stderr)
    sys.exit(1)


def _load_dotenv():
    """自动加载脚本同目录或 SKILL 根目录下的 .env 文件"""
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    for env_path in [skill_dir / ".env", script_dir / ".env"]:
        if env_path.exists():
            with open(env_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if "=" not in line:
                        continue
                    key, _, value = line.partition("=")
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = value
            return


_load_dotenv()


class ZhipuTools:
    """智谱 AI 工具类 - 支持 MCP 和 Legacy 双模式"""

    API_KEY = os.environ.get("ZHIPU_API_KEY", "")
    USE_MCP = os.environ.get("ZHIPU_USE_MCP", "true").lower() != "false"

    MCP_BASE = "https://api.z.ai/api/mcp"
    LEGACY_BASE = "https://open.bigmodel.cn/api/paas/v4"

    # --- MCP Session Management ---

    @classmethod
    def _mcp_init(cls, endpoint: str) -> str:
        """MCP initialize → 获取 session id"""
        url = f"{cls.MCP_BASE}{endpoint}"
        headers = {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream, application/json",
        }
        body = {
            "jsonrpc": "2.0", "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "openclaw-zhipu-tools", "version": "1.1.0"},
            },
        }
        resp = requests.post(url, headers=headers, json=body, timeout=30)
        resp.raise_for_status()

        session_id = resp.headers.get("mcp-session-id", "")
        if not session_id:
            status = getattr(resp, 'status_code', 0)
            if status in (401, 403):
                raise RuntimeError(f"MCP 认证失败 (HTTP {status}): API Key 无效或已过期，请检查 ZHIPU_API_KEY")
            if status != 200:
                raise RuntimeError(f"MCP 初始化失败 (HTTP {status}): {resp.text[:300]}")
            raise RuntimeError("MCP 初始化失败: 响应中缺少 mcp-session-id，服务端可能暂时不可用")

        # 发送 initialized 通知
        notify_headers = {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Mcp-Session-Id": session_id,
        }
        requests.post(
            url,
            headers=notify_headers,
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
            timeout=10,
        )
        return session_id

    @classmethod
    def _mcp_call(cls, endpoint: str, tool_name: str, arguments: dict, max_retries: int = 2) -> dict:
        """MCP tools/call → 返回解析后的结果"""
        url = f"{cls.MCP_BASE}{endpoint}"

        for attempt in range(max_retries + 1):
            try:
                session_id = cls._mcp_init(endpoint)
                call_headers = {
                    "Authorization": f"Bearer {cls.API_KEY}",
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream, application/json",
                    "Mcp-Session-Id": session_id,
                }
                body = {
                    "jsonrpc": "2.0", "id": 2,
                    "method": "tools/call",
                    "params": {"name": tool_name, "arguments": arguments},
                }
                resp = requests.post(url, headers=call_headers, json=body, timeout=120)
                resp.raise_for_status()

                # 解析 SSE 响应
                raw = resp.text
                for line in raw.split("\n"):
                    line = line.strip()
                    if line.startswith("data:"):
                        data_str = re.sub(r"^data:\s*", "", line).strip()
                        if not data_str:
                            continue
                        try:
                            obj = json.loads(data_str)
                            if "result" in obj:
                                result = obj["result"]
                                # 检查 MCP isError 标志
                                if isinstance(result, dict) and result.get("isError"):
                                    error_text = ""
                                    for c in result.get("content", []):
                                        if c.get("type") == "text":
                                            error_text = c["text"]
                                            break
                                    raise RuntimeError(f"MCP error: {error_text}")
                                return result
                            if "error" in obj:
                                raise RuntimeError(f"MCP error: {obj['error']}")
                        except json.JSONDecodeError:
                            pass

                raise RuntimeError(f"MCP 响应解析失败: {raw[:500]}")
            except requests.exceptions.HTTPError as e:
                status = getattr(e.response, 'status_code', 'unknown') if e.response else 'unknown'
                body = e.response.text[:300] if e.response else ''
                if status in (401, 403):
                    raise RuntimeError(f"MCP 认证失败 (HTTP {status}): API Key 无效或已过期，请检查 ZHIPU_API_KEY")
                if attempt < max_retries:
                    import time
                    time.sleep(1 * (attempt + 1))
                    continue
                raise RuntimeError(f"MCP 请求失败 (HTTP {status}): {body}")
            except (requests.exceptions.SSLError, requests.exceptions.ConnectionError) as e:
                if attempt < max_retries:
                    import time
                    time.sleep(1 * (attempt + 1))
                    continue
                raise RuntimeError(f"MCP 网络连接失败（已重试 {max_retries} 次）: {type(e).__name__}: {e}")

        raise RuntimeError("MCP 调用失败: 未预期的重试循环退出")

    # --- Web Search (MCP: web_search_prime) ---

    @classmethod
    def web_search(
        cls,
        query: str,
        count: int = 10,
        search_engine: str = "search_std",
        search_intent: bool = False,
        domain_filter: str = None,
        recency_filter: str = "noLimit",
        content_size: str = "medium",
    ) -> dict:
        """网络搜索"""
        if cls.USE_MCP:
            try:
                return cls._web_search_mcp(query, content_size, 
                                              recency_filter=recency_filter,
                                              domain_filter=domain_filter)
            except RuntimeError as e:
                err_msg = str(e)
                # content filter 或业务错误不 fallback 到 Legacy（Legacy 走余额，注定失败）
                if "contentFilter" in err_msg or "1301" in err_msg:
                    # 不自动绕过内容安全策略，直接返回错误让用户修改搜索词
                    print(f"MCP 搜索被内容安全策略拦截，请修改搜索词重试: {e}", file=sys.stderr)
                    return {"content": json.dumps([]), "error": f"content_filter: {err_msg}"}
                # 不自动 fallback 到 Legacy（Legacy 走账户余额，可能产生费用）
                print(f"MCP 搜索连接失败: {e}", file=sys.stderr)
                print(f"提示: 如需使用 Legacy API，请设置 ZHIPU_USE_MCP=false 明确启用（注意可能产生费用）", file=sys.stderr)
                return {"content": json.dumps([]), "error": f"mcp_connection: {err_msg}"}

        # Legacy 模式需显式启用
        print("未启用 MCP 模式。Legacy API 走账户余额，可能产生费用。如需使用请设置 ZHIPU_USE_MCP=false", file=sys.stderr)
        return {"content": json.dumps([]), "error": "legacy_not_enabled: 需显式设置 ZHIPU_USE_MCP=false"}


    @classmethod
    def _web_search_mcp(cls, query: str, content_size: str, recency_filter: str = None, domain_filter: str = None) -> dict:
        """MCP 模式搜索 - 端点: /web_search_prime/mcp, 工具: web_search_prime
        
        注意: MCP 工具不支持 recency/domain 过滤参数。
        这里把 recency/domain 限制注入到 query 前缀中，让搜索引擎自行过滤。
        """
        # 将 recency/domain 注入 query
        enhanced_query = query
        if domain_filter:
            enhanced_query = f"site:{domain_filter} {query}"
        if recency_filter and recency_filter != "noLimit":
            recency_map = {"day": "今天", "week": "最近一周", "month": "最近一个月"}
            recency_hint = recency_map.get(recency_filter, "")
            if recency_hint:
                enhanced_query = f"{recency_hint} {enhanced_query}"
        
        arguments = {
            "search_query": enhanced_query,
            "content_size": content_size,
        }
        result = cls._mcp_call("/web_search_prime/mcp", "web_search_prime", arguments)
        return cls._extract_mcp_text(result)

    @classmethod
    def _web_search_legacy(
        cls, query, count, search_engine, search_intent,
        domain_filter, recency_filter, content_size,
    ) -> dict:
        """旧版 bigmodel API 搜索"""
        headers = {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "search_query": query,
            "search_engine": search_engine,
            "search_intent": search_intent,
            "count": count,
            "search_recency_filter": recency_filter,
            "content_size": content_size,
        }
        if domain_filter:
            payload["search_domain_filter"] = domain_filter

        resp = requests.post(f"{cls.LEGACY_BASE}/web_search", headers=headers, json=payload, timeout=30)
        if resp.status_code == 429:
            print("Legacy API 余额不足（429），请使用 Coding Plan MCP 模式或充值", file=sys.stderr)
            return {"content": json.dumps([]), "error": "legacy_429: 余额不足"}
        resp.raise_for_status()
        return resp.json()

    # --- Web Reader (MCP: webReader) ---

    @classmethod
    def web_reader(cls, url: str) -> dict:
        """网页读取"""
        if cls.USE_MCP:
            try:
                return cls._web_reader_mcp(url)
            except RuntimeError as e:
                err_msg = str(e)
                if "contentFilter" in err_msg or "1301" in err_msg:
                    print(f"MCP 网页读取被内容安全策略拦截: {e}", file=sys.stderr)
                    return {"content": "", "error": f"content_filter: {err_msg}"}
                # 不自动 fallback 到 Legacy（Legacy 走账户余额，可能产生费用）
                print(f"MCP 网页读取连接失败: {e}", file=sys.stderr)
                print(f"提示: 如需使用 Legacy API，请设置 ZHIPU_USE_MCP=false 明确启用（注意可能产生费用）", file=sys.stderr)
                return {"content": "", "error": f"mcp_connection: {err_msg}"}

        # Legacy 模式需显式启用
        print("未启用 MCP 模式。Legacy API 走账户余额，可能产生费用。如需使用请设置 ZHIPU_USE_MCP=false", file=sys.stderr)
        return {"content": "", "error": "legacy_not_enabled: 需显式设置 ZHIPU_USE_MCP=false"}


    @classmethod
    def _web_reader_mcp(cls, url: str) -> dict:
        """MCP 模式网页读取 - 端点: /web_reader/mcp, 工具: webReader"""
        result = cls._mcp_call("/web_reader/mcp", "webReader", {"url": url})
        return cls._extract_mcp_text(result)

    @classmethod
    def _web_reader_legacy(cls, url: str) -> dict:
        """旧版 bigmodel API 网页读取"""
        headers = {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json",
        }
        resp = requests.post(
            f"{cls.LEGACY_BASE}/reader",
            headers=headers,
            json={"url": url},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    # --- Zread (MCP: search_doc / get_repo_structure / read_file) ---

    @classmethod
    def zread_search(cls, repo: str, query: str, language: str = None) -> dict:
        """GitHub 仓库文档搜索 - 端点: /zread/mcp, 工具: search_doc"""
        if not cls.USE_MCP:
            raise RuntimeError("Zread 仅支持 MCP 模式，请确保 ZHIPU_USE_MCP=true")
        arguments = {"repo_name": repo, "query": query}
        if language:
            arguments["language"] = language
        result = cls._mcp_call("/zread/mcp", "search_doc", arguments)
        return cls._extract_mcp_text(result)

    @classmethod
    def zread_structure(cls, repo: str, path: str = None) -> dict:
        """GitHub 仓库目录结构 - 端点: /zread/mcp, 工具: get_repo_structure"""
        if not cls.USE_MCP:
            raise RuntimeError("Zread 仅支持 MCP 模式，请确保 ZHIPU_USE_MCP=true")
        arguments = {"repo_name": repo}
        if path:
            arguments["dir_path"] = path
        result = cls._mcp_call("/zread/mcp", "get_repo_structure", arguments)
        return cls._extract_mcp_text(result)

    @classmethod
    def zread_file(cls, repo: str, file_path: str) -> dict:
        """GitHub 仓库文件读取 - 端点: /zread/mcp, 工具: read_file"""
        if not cls.USE_MCP:
            raise RuntimeError("Zread 仅支持 MCP 模式，请确保 ZHIPU_USE_MCP=true")
        result = cls._mcp_call("/zread/mcp", "read_file", {"repo_name": repo, "file_path": file_path})
        return cls._extract_mcp_text(result)

    @classmethod
    def _extract_mcp_text(cls, result) -> dict:
        """从 MCP 响应中提取文本内容，确保返回 dict"""
        if not isinstance(result, dict):
            return {"content": str(result)}
        if "content" in result:
            for c in result["content"]:
                if c.get("type") == "text":
                    try:
                        parsed = json.loads(c["text"])
                        if isinstance(parsed, dict):
                            return parsed
                        return {"content": parsed}
                    except (json.JSONDecodeError, TypeError):
                        return {"content": c["text"]}
        return result

    # --- Vision Analysis ---
    # ⚠️ 逆向实现：从 @z_ai/mcp-server npm 包源码提取的 API 调用方式。
    # 官方未提供视觉 MCP 端点（返回 404），此实现直接调用底层 chat completions API。
    # 当前可能走 Coding Plan 资源池，后续智谱可能调整计费策略。
    VIDEO_EXTENSIONS = {"mp4", "mov", "m4v", "avi", "mkv", "webm", "flv", "wmv"}
    VIDEO_MAX_MB = 8

    @classmethod
    def _detect_media_type(cls, file_path: str) -> str:
        """检测媒体类型: image 或 video。URL 根据 extension 猜测，本地文件用 mime。"""
        import mimetypes as mt

        # 本地文件用 mime
        if not file_path.startswith(("http://", "https://")):
            p = Path(file_path)
            if p.exists():
                mime = mt.guess_type(str(p))[0] or ""
                if mime.startswith("video/"):
                    return "video"
                if mime.startswith("image/"):
                    return "image"
        # fallback: 扩展名
        ext = file_path.rsplit(".", 1)[-1].lower().lstrip("/") if "." in file_path else ""
        if ext in cls.VIDEO_EXTENSIONS:
            return "video"
        return "image"

    @classmethod
    def _encode_media(cls, file_path: str, media_type: str) -> str:
        """将本地文件编码为 data URI。URL 直接返回。"""
        import base64
        import mimetypes as mt

        if file_path.startswith(("http://", "https://")):
            return file_path

        p = Path(file_path)
        if not p.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        if media_type == "video":
            size_mb = p.stat().st_size / (1024 * 1024)
            if size_mb > cls.VIDEO_MAX_MB:
                raise ValueError(f"视频文件过大: {size_mb:.1f}MB，最大支持 {cls.VIDEO_MAX_MB}MB")
        mime = mt.guess_type(str(p))[0] or ("video/mp4" if media_type == "video" else "image/png")
        with open(p, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return f"data:{mime};base64,{b64}"

    @classmethod
    def vision(cls, media_path: str, prompt: str = "请描述这个文件的内容", model: str = None, media_type: str = None) -> str:
        """视觉理解 - 使用 GLM-4.6V 分析图片或视频

        自动识别输入类型（图片/视频），也支持 --type 手动指定。

        Args:
            media_path: 文件路径（本地文件或 URL）
            prompt: 分析提示词
            model: 模型名称，默认 glm-4.6v
            media_type: 手动指定类型 'image' 或 'video'，默认自动检测

        Returns:
            分析结果文本

        支持格式:
            图片: jpg/png/gif/webp/bmp/svg 等（本地 + URL）
            视频: mp4/mov/m4v/avi/mkv/webm 等（本地 ≤8MB + URL）
        """
        model = model or "glm-4.6v"
        media_type = media_type or cls._detect_media_type(media_path)

        encoded = cls._encode_media(media_path, media_type)

        if media_type == "video":
            content_type_field = "video_url"
            timeout = 120
            max_tokens = 4096
        else:
            content_type_field = "image_url"
            timeout = 60
            max_tokens = 1024

        headers = {
            "Authorization": f"Bearer {cls.API_KEY}",
            "Content-Type": "application/json",
        }
        body = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": content_type_field, content_type_field: {"url": encoded}},
                    ],
                }
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7,
        }

        resp = requests.post(
            f"{cls.LEGACY_BASE}/chat/completions",
            headers=headers,
            json=body,
            timeout=timeout,
        )
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            raise RuntimeError(f"API 错误: {data['error']}")
        return data["choices"][0]["message"]["content"]

    # --- File Parser (Legacy only) ---

    @classmethod
    def file_parser(cls, file_path: str, file_type: str = "WPS", tool_type: str = "prime-sync") -> dict:
        """文件解析（仅 Legacy API）"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")

        headers = {"Authorization": f"Bearer {cls.API_KEY}"}
        with open(file_path, "rb") as f:
            resp = requests.post(
                f"{cls.LEGACY_BASE}/files/parser/sync",
                headers=headers,
                files={"file": (file_path.name, f)},
                data={"tool_type": tool_type, "file_type": file_type},
                timeout=120,
            )
            resp.raise_for_status()
        return resp.json()


# --- Formatting Helpers ---

def format_search_result(result: dict) -> str:
    output = []
    # content 可能是 JSON 编码的搜索结果数组
    content = result.get("content", "")
    if isinstance(content, str):
        try:
            search_results = json.loads(content)
            if isinstance(search_results, list):
                content = search_results
        except (json.JSONDecodeError, TypeError):
            pass

    if isinstance(content, list):
        for i, item in enumerate(content, 1):
            output.append(f"\n### 结果 {i}")
            output.append(f"**标题**: {item.get('title', 'N/A')}")
            output.append(f"**链接**: {item.get('link', 'N/A')}")
            snippet = item.get("content", "N/A")
            output.append(f"**摘要**: {snippet[:200]}{'...' if len(snippet) > 200 else ''}")
    elif isinstance(content, str):
        output.append(content)
    else:
        output.append(json.dumps(result, ensure_ascii=False, indent=2))
    return "\n".join(output)


def format_web_reader_result(result: dict) -> str:
    output = ["# 网页读取结果\n"]
    content = result.get("content", "")
    # content 可能是 JSON 编码的完整响应
    if isinstance(content, str):
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                result = parsed
                content = result.get("content", "")
        except (json.JSONDecodeError, TypeError):
            pass

    if "title" in result:
        output.append(f"**标题**: {result['title']}\n")
    if isinstance(content, str):
        output.append(content)
    elif "markdown" in result:
        output.append(result["markdown"])
    elif "text" in result:
        output.append(result["text"])
    else:
        output.append(json.dumps(result, ensure_ascii=False, indent=2))
    return "\n".join(output)


def format_parser_result(result: dict) -> str:
    output = ["# 文件解析结果\n"]
    if "content" in result:
        output.append(result["content"])
    elif "text" in result:
        output.append(result["text"])
    else:
        output.append(json.dumps(result, ensure_ascii=False, indent=2))
    return "\n".join(output)


def format_zread_result(result: dict) -> str:
    if "content" in result:
        return result["content"]
    return json.dumps(result, ensure_ascii=False, indent=2)


# --- CLI ---

def main():
    parser = argparse.ArgumentParser(
        description="智谱 AI 工具 - 网络搜索、网页读取、仓库文档搜索和文件解析",
    )
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # web_search
    sp = subparsers.add_parser("web_search", help="网络搜索 (MCP: web_search_prime)")
    sp.add_argument("query", help="搜索关键词")
    sp.add_argument("--count", type=int, default=10)
    sp.add_argument("--engine", default="search_std")
    sp.add_argument("--recency", default="noLimit", choices=["noLimit", "day", "week", "month"])
    sp.add_argument("--domain")
    sp.add_argument("--raw", action="store_true")

    # web_reader
    rp = subparsers.add_parser("web_reader", help="网页读取 (MCP: webReader)")
    rp.add_argument("url", help="目标 URL")
    rp.add_argument("--raw", action="store_true")

    # zread
    zp = subparsers.add_parser("zread", help="GitHub 仓库文档搜索 (MCP: zread)")
    zsub = zp.add_subparsers(dest="zread_cmd", help="Zread 子命令")

    zs = zsub.add_parser("search", help="搜索仓库文档")
    zs.add_argument("repo", help="GitHub 仓库 (如 'openai/openai')")
    zs.add_argument("query", help="搜索关键词")

    zst = zsub.add_parser("structure", help="查看仓库目录结构")
    zst.add_argument("repo", help="GitHub 仓库")
    zst.add_argument("path", nargs="?", default=None, help="子目录路径")

    zr = zsub.add_parser("read", help="读取仓库文件")
    zr.add_argument("repo", help="GitHub 仓库")
    zr.add_argument("file_path", help="文件路径 (如 'README.md')")

    # vision (图片 + 视频)
    vp = subparsers.add_parser("vision", help="视觉理解 (GLM-4.6V) - 支持图片和视频")
    vp.add_argument("media_path", help="文件路径（本地文件或 URL），支持图片(jpg/png/gif/webp...)和视频(mp4/mov/m4v...，最大8MB)")
    vp.add_argument("--prompt", default="请描述这个文件的内容", help="分析提示词")
    vp.add_argument("--model", default=None, help="模型名称 (默认 glm-4.6v)")
    vp.add_argument("--type", choices=["image", "video"], default=None, help="手动指定媒体类型（默认自动识别）")

    # file_parser
    fp = subparsers.add_parser("file_parser", help="文件解析 (Legacy only)")
    fp.add_argument("file_path", help="文件路径")
    fp.add_argument("--file-type", default="WPS")
    fp.add_argument("--raw", action="store_true")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    if not ZhipuTools.API_KEY:
        print("错误: 请设置 ZHIPU_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    try:
        if args.command == "web_search":
            result = ZhipuTools.web_search(
                query=args.query, count=args.count, search_engine=args.engine,
                recency_filter=args.recency, domain_filter=args.domain,
            )
            print(json.dumps(result, ensure_ascii=False, indent=2) if args.raw else format_search_result(result))
            # 检查是否无结果，提示用户
            if not args.raw:
                content = result.get("content", "") if isinstance(result, dict) else str(result)
                if not content or content == "[]" or (isinstance(content, str) and "No results" in content):
                    print("⚠️ 未找到相关结果，建议换关键词重试。", file=sys.stderr)

        elif args.command == "web_reader":
            result = ZhipuTools.web_reader(url=args.url)
            print(json.dumps(result, ensure_ascii=False, indent=2) if args.raw else format_web_reader_result(result))

        elif args.command == "zread":
            if not args.zread_cmd:
                zp.print_help()
                sys.exit(1)
            if args.zread_cmd == "search":
                result = ZhipuTools.zread_search(repo=args.repo, query=args.query)
            elif args.zread_cmd == "structure":
                result = ZhipuTools.zread_structure(repo=args.repo, path=args.path)
            elif args.zread_cmd == "read":
                result = ZhipuTools.zread_file(repo=args.repo, file_path=args.file_path)
            print(format_zread_result(result))

        elif args.command == "vision":
            result = ZhipuTools.vision(
                media_path=args.media_path,
                prompt=args.prompt,
                model=args.model,
            )
            print(result)

        elif args.command == "vision":
            result = ZhipuTools.vision(
                media_path=args.media_path,
                prompt=args.prompt,
                model=args.model,
                media_type=args.type,
            )
            print(result)

        elif args.command == "file_parser":
            result = ZhipuTools.file_parser(file_path=args.file_path, file_type=args.file_type)
            print(json.dumps(result, ensure_ascii=False, indent=2) if args.raw else format_parser_result(result))

    except requests.HTTPError as e:
        print(f"API 错误: {e}", file=sys.stderr)
        if e.response is not None:
            print(f"响应: {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
