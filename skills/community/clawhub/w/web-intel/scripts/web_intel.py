#!/usr/bin/env python3
"""
web_intel.py — 统一网络检索入口

整合能力:
  • content-extraction router（URL 分类，WeChat/Feishu/YouTube/通用）
  • Jina Reader（r.jina.ai，最经济全文提取）
  • Firecrawl CLI（搜索 + 抓取）
  • web-access CDP Proxy（登录态/反爬，deep 模式）

用法:
  python3 web_intel.py --query "比亚迪财报" --mode fast --type finance
  python3 web_intel.py --url https://example.com --mode standard
  python3 web_intel.py --query "小米营销策略" --mode standard --type competitor
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

# ── 路径常量 ──────────────────────────────────────────────────
SKILLS_BASE = Path(__file__).resolve().parent.parent.parent  # workspace/skills/
CONTENT_EXTRACTION_SCRIPTS = SKILLS_BASE / "content-extraction" / "scripts"
CDP_PROXY_URL = "http://localhost:3456"
JINA_BASE = "https://r.jina.ai/"

# ── 注入 content-extraction router ────────────────────────────
sys.path.insert(0, str(CONTENT_EXTRACTION_SCRIPTS))
try:
    from extract_router import classify_url as _ce_classify
    _CE_OK = True
except ImportError:
    _CE_OK = False


# ── CDP 可用性检测 ─────────────────────────────────────────────
def _cdp_ok() -> bool:
    """检测 web-access CDP Proxy 是否运行中（localhost:3456）"""
    try:
        urllib.request.urlopen(f"{CDP_PROXY_URL}/targets", timeout=2)
        return True
    except Exception:
        return False


# ── Jina Reader ────────────────────────────────────────────────
def _jina(url: str, timeout: int = 12) -> str | None:
    """通过 r.jina.ai 提取页面 Markdown（最经济的全文提取）"""
    try:
        req = urllib.request.Request(
            JINA_BASE + url,
            headers={
                "Accept": "text/markdown",
                "User-Agent": "OpenClaw/web-intel",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read().decode("utf-8", errors="replace")
    except Exception:
        return None


# ── Firecrawl CLI ──────────────────────────────────────────────
def _fc_search(query: str, limit: int = 5, scrape: bool = False) -> list[dict]:
    """通过 firecrawl CLI 搜索，返回结果列表"""
    cmd = ["firecrawl", "search", query, "--limit", str(limit)]
    if scrape:
        cmd.append("--scrape")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        text = r.stdout.strip()
        for i, ch in enumerate(text):
            if ch in ("[", "{"):
                try:
                    data = json.loads(text[i:])
                    if isinstance(data, list):
                        return data
                    if isinstance(data, dict):
                        return data.get("results", data.get("data", []))
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
    return []


def _fc_scrape(url: str) -> str | None:
    """通过 firecrawl CLI 抓取单页内容"""
    try:
        r = subprocess.run(
            ["firecrawl", "scrape", url],
            capture_output=True, text=True, timeout=30,
        )
        return r.stdout.strip() or None
    except Exception:
        return None


# ── web-access CDP Proxy ───────────────────────────────────────
def _cdp_fetch(url: str, timeout: int = 15) -> str | None:
    """通过 web-access CDP Proxy 提取页面正文（需 Proxy 运行中）

    Proxy 启动命令：
        bash ~/.openclaw/workspace/skills/web-access/scripts/check-deps.sh
    """
    target_id = None
    try:
        # 创建后台 tab
        new_resp = urllib.request.urlopen(
            f"{CDP_PROXY_URL}/new?url={urllib.parse.quote(url, safe=':/?=#&')}",
            timeout=timeout,
        )
        data = json.loads(new_resp.read())
        target_id = data.get("targetId") or data.get("id")
        if not target_id:
            return None

        # 提取页面正文（JS eval）
        eval_req = urllib.request.Request(
            f"{CDP_PROXY_URL}/eval?target={target_id}",
            data=b"document.body ? document.body.innerText : ''",
            method="POST",
        )
        content = urllib.request.urlopen(eval_req, timeout=timeout).read().decode(
            "utf-8", errors="replace"
        )
        return content[:12000] if content else None

    except Exception:
        return None
    finally:
        # 关闭 tab，保持环境整洁
        if target_id:
            try:
                urllib.request.urlopen(
                    f"{CDP_PROXY_URL}/close?target={target_id}", timeout=5
                )
            except Exception:
                pass


# ── 搜索路由 ───────────────────────────────────────────────────
def _search(query: str, mode: str, search_type: str) -> dict:
    t0 = time.time()
    cdp = _cdp_ok()

    if mode == "fast":
        results = _fc_search(query, limit=5)
        return {
            "query": query,
            "mode": mode,
            "type": search_type,
            "tool_used": "firecrawl_search",
            "results": results[:5],
            "full_content": None,
            "web_access_available": cdp,
            "latency_ms": int((time.time() - t0) * 1000),
        }

    elif mode == "standard":
        results = _fc_search(query, limit=3)
        full_content = None
        tool = "firecrawl_search"
        if results and results[0].get("url"):
            full_content = _jina(results[0]["url"])
            if full_content:
                tool = "firecrawl_search+jina"
        return {
            "query": query,
            "mode": mode,
            "type": search_type,
            "tool_used": tool,
            "results": results[:3],
            "full_content": full_content[:8000] if full_content else None,
            "web_access_available": cdp,
            "latency_ms": int((time.time() - t0) * 1000),
        }

    else:  # deep
        results = _fc_search(query, limit=5, scrape=True)
        return {
            "query": query,
            "mode": mode,
            "type": search_type,
            "tool_used": "firecrawl_search_scrape",
            "results": results[:5],
            "full_content": None,
            "web_access_available": cdp,
            "note": "CDP 可用（web_access_available=true）时可进一步深度抓取特定 URL",
            "latency_ms": int((time.time() - t0) * 1000),
        }


# ── 提取路由 ───────────────────────────────────────────────────
def _extract(url: str, mode: str) -> dict:
    t0 = time.time()
    cdp = _cdp_ok()

    # Step 0：用 content-extraction router 分类 URL
    source_type, handler = "网页", "proxy_cascade"
    if _CE_OK:
        try:
            plan = _ce_classify(url)
            source_type = plan.source_type
            handler = plan.handler
        except Exception:
            pass

    # 特殊平台委托专用 handler（微信/飞书/YouTube）
    if handler in ("browser", "feishu", "transcript"):
        return {
            "url": url,
            "mode": mode,
            "source_type": source_type,
            "tool_used": f"delegate:{handler}",
            "full_content": None,
            "note": f"此 URL 类型需专用工具（handler={handler}），请调用 skills/content-extraction 处理",
            "web_access_available": cdp,
            "latency_ms": int((time.time() - t0) * 1000),
        }

    # 通用网页提取
    full_content, tool = None, "none"

    if mode == "fast":
        full_content = _jina(url)
        tool = "jina_reader" if full_content else "jina_failed"

    elif mode == "standard":
        full_content = _jina(url)
        tool = "jina_reader"
        if not full_content:
            full_content = _fc_scrape(url)
            tool = "firecrawl_scrape" if full_content else "all_failed"

    else:  # deep：CDP 优先，逐级降级
        if cdp:
            full_content = _cdp_fetch(url)
            tool = "web_access_cdp"
        if not full_content:
            full_content = _jina(url)
            tool = "jina_reader" if full_content else "jina_failed"
        if not full_content:
            full_content = _fc_scrape(url)
            tool = "firecrawl_scrape" if full_content else "all_failed"

    return {
        "url": url,
        "mode": mode,
        "source_type": source_type,
        "tool_used": tool,
        "full_content": full_content[:10000] if full_content else None,
        "web_access_available": cdp,
        "latency_ms": int((time.time() - t0) * 1000),
    }


# ── CLI 入口 ───────────────────────────────────────────────────
def main() -> int:
    p = argparse.ArgumentParser(
        description="web-intel: 统一网络检索入口（fast/standard/deep）",
        epilog=(
            "示例:\n"
            "  python3 web_intel.py --query '比亚迪财报' --mode fast --type finance\n"
            "  python3 web_intel.py --url https://example.com --mode standard\n"
            "  python3 web_intel.py --query '竞品营销' --mode standard --type competitor"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--query", help="搜索关键词")
    p.add_argument("--url", help="直接提取指定 URL（跳过搜索）")
    p.add_argument(
        "--mode",
        default="fast",
        choices=["fast", "standard", "deep"],
        help="fast(<2s,摘要) | standard(2-8s,全文) | deep(10-30s,CDP登录态)",
    )
    p.add_argument(
        "--type",
        default="web",
        choices=["web", "news", "finance", "competitor", "extract"],
        help="任务类型（影响结果优先级和提示）",
    )
    args = p.parse_args()

    if not args.query and not args.url:
        p.error("必须提供 --query 或 --url")

    result = (
        _extract(args.url, args.mode)
        if args.url
        else _search(args.query, args.mode, args.type)
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
