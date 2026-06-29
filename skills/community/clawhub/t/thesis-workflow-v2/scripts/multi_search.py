#!/usr/bin/env python3
"""
multi_search.py - 多工具并行检索引擎

设计原则：
  1. 并行发出所有工具请求，不等待、不串行
  2. 各工具独立降级，任意工具失败不影响整体
  3. 结果统一为 SearchResult 列表，合并去重后按相关性排序
  4. 对 Agent 透明：Agent 可继续使用 web_search 等内置工具，
     Python 层只补充 MCP/学术工具的能力

工具清单：
  - web_search    ：头条搜索（通过 subprocess 调用 OpenClaw CLI）
  - tavily_search：Tavily MCP（通过 mcporter）
  - arxiv_search ：arXiv 论文搜索（通过 mcporter）
  - openalex_search：学术文献（通过 scholar-search.py）

用法：
  from multi_search import multi_search
  results = multi_search("竞争战略 市场规模 2024")
  for r in results:
      print(r.source, r.title, r.snippet)
"""

import json
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from typing import List, Optional

# 超时配置（秒）
TOUTILVY = 25
TOARXIV = 20
TOOPENALEX = 20
TOTIDY = 10  # 工具响应清洗超时

# 并行数量上限
MAX_PARALLEL = 4


# ============================================================
# 数据结构
# ============================================================

@dataclass
class SearchResult:
    """统一格式的检索结果"""
    title: str
    url: str
    snippet: str
    source: str          # 工具名：web_search | tavily | arxiv | openalex
    score: float = 0.5  # 0-1 相关性分，人工标定或工具原生分
    raw: dict = field(default_factory=dict)  # 原始数据，保留以备扩展

    def __hash__(self):
        return hash(self.url)

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "url": self.url,
            "snippet": self.snippet,
            "source": self.source,
            "score": self.score,
        }


# ============================================================
# 工具函数
# ============================================================

def _tidy_result(r: SearchResult) -> Optional[SearchResult]:
    """清洗单条结果：去空、去极短内容"""
    try:
        if not r or not r.title or len(r.title) < 5:
            return None
        r.snippet = (r.snippet or "").strip()
        if len(r.snippet) < 10:
            r.snippet = r.title  # fallback
        return r
    except Exception:
        return None


def _tavily_search(query: str, max_results: int = 3) -> List[SearchResult]:
    """Tavily MCP 搜索（通过 mcporter）"""
    try:
        cmd = [
            "mcporter", "call", "tavily-mcp.tavily_search",
            json.dumps({"query": query, "max_results": max_results})
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=TOUTILVY
        )
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        results = data.get("results", [])
        out = []
        for item in results[:max_results]:
            r = SearchResult(
                title=item.get("title", "") or "",
                url=item.get("url", "") or "",
                snippet=item.get("description", "") or item.get("snippet", "") or "",
                source="tavily",
                score=0.7,
                raw=item,
            )
            if _tidy_result(r):
                out.append(r)
        return out
    except FileNotFoundError:
        return []
    except subprocess.TimeoutExpired:
        return []
    except Exception:
        return []


def _arxiv_search(query: str, max_results: int = 3) -> List[SearchResult]:
    """arXiv 论文搜索（通过 mcporter arxiv-search-collector）"""
    try:
        cmd = [
            "mcporter", "call", "arxiv-search-collector.search_papers",
            json.dumps({"query": query, "max_count": max_results})
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=TOARXIV
        )
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        papers = data.get("papers", [])
        out = []
        for item in papers[:max_results]:
            r = SearchResult(
                title=item.get("title", "") or "",
                url=item.get("url", "") or item.get("pdf_url", "") or "",
                snippet=item.get("abstract", "")[:200] or "",
                source="arxiv",
                score=0.6,
                raw=item,
            )
            if _tidy_result(r):
                out.append(r)
        return out
    except FileNotFoundError:
        return []
    except subprocess.TimeoutExpired:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []


def _openalex_search(query: str, max_results: int = 3) -> List[SearchResult]:
    """OpenAlex 学术文献搜索（通过 scholar-search.py）"""
    try:
        script_path = "/Users/hehe9737/.openclaw/workspace/skills/academic-research/scripts/scholar-search.py"
        cmd = [
            "python3", script_path,
            "search", query,
            "--limit", str(max_results),
            "--json",
        ]
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=TOOPENALEX
        )
        if result.returncode != 0:
            return []
        data = json.loads(result.stdout)
        works = data if isinstance(data, list) else data.get("results", [])
        out = []
        for item in works[:max_results]:
            authors = item.get("authors", [])
            author_str = ", ".join(authors[:2]) if authors else ""
            abstract = item.get("abstract", "")[:200] or ""
            snippet = f"{author_str} ({item.get('year', 'n.d.')})" + (f" — {abstract}" if abstract else "")
            r = SearchResult(
                title=item.get("title", "") or "",
                url=item.get("doi", "") or f"https://openalex.org/{item.get('id', '')}",
                snippet=snippet,
                source="openalex",
                score=0.6,
                raw=item,
            )
            if _tidy_result(r):
                out.append(r)
        return out
    except FileNotFoundError:
        return []
    except subprocess.TimeoutExpired:
        return []
    except json.JSONDecodeError:
        return []
    except Exception:
        return []


# ============================================================
# 核心接口
# ============================================================

def multi_search(
    query: str,
    max_results_per_tool: int = 3,
    include: Optional[List[str]] = None,
    exclude: Optional[List[str]] = None,
) -> List[SearchResult]:
    """
    并行多工具检索，合并去重后返回。

    参数：
      query               ：搜索词
      max_results_per_tool：每个工具最多返回几条（默认3）
      include             ：只启用指定工具，如 ["tavily","openalex"]
                             默认全部启用
      exclude             ：排除指定工具

    返回：
      List[SearchResult]，按 score 降序排列
    """
    tools = {
        "tavily":    (_tavily_search,    include, exclude),
        "arxiv":     (_arxiv_search,     include, exclude),
        "openalex":  (_openalex_search,  include, exclude),
    }

    # 过滤工具
    active = {}
    for name, (fn, inc, exc) in tools.items():
        if inc is not None and name not in inc:
            continue
        if exc is not None and name in exc:
            continue
        active[name] = fn

    if not active:
        return []

    # 并行执行
    results_all: List[SearchResult] = []
    lock = threading.Lock()

    def _run(name: str, fn, q: str, n: int):
        try:
            rs = fn(q, n)
            with lock:
                results_all.extend(rs)
        except Exception:
            pass

    with ThreadPoolExecutor(max_workers=MAX_PARALLEL) as ex:
        futures = {
            ex.submit(_run, name, fn, query, max_results_per_tool): name
            for name, fn in active.items()
        }
        for f in as_completed(futures):
            try:
                f.result()
            except Exception:
                pass

    # 去重规则（v2 升级）：
    #   1. 相同来源 + 相同标题 → 去重（标题完全一致就丢弃）
    #   2. 不同来源 + 相同标题 → 保留（来源不同信息可能不同）
    #   3. 无标题 → 按 URL 去重（兜底）
    seen_keys: set = set()
    unique: List[SearchResult] = []
    for r in results_all:
        if not r.title:
            continue
        # 优先用 title + source 组合键
        key = (r.source, r.title.strip().lower())
        if key in seen_keys:
            continue
        # 兜底：无标题时用 URL
        if not r.url:
            continue
        if r.url in seen_keys:
            continue
        seen_keys.add(key)
        seen_keys.add(r.url)
        unique.append(r)

    # 按 score 降序
    unique.sort(key=lambda x: x.score, reverse=True)

    return unique


def multi_search_text(query: str, max_results_per_tool: int = 3) -> str:
    """
    文本格式输出（供注入 prompt 使用）。
    每条结果格式：[来源] 标题\n  摘要（URL）
    """
    results = multi_search(query, max_results_per_tool)
    if not results:
        return f"[多工具检索无结果: {query}]"

    lines = []
    for r in results:
        src = {"web_search": "🌐  网页", "tavily": "🔍 Tavily",
               "arxiv": "📚 arXiv", "openalex": "🎓 学术"}.get(r.source, r.source)
        lines.append(f"[{src}] {r.title}")
        lines.append(f"  {r.snippet}")
        lines.append(f"  {r.url}")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python3 multi_search.py <查询词> [--max N]")
        sys.exit(1)

    query = sys.argv[1]
    max_n = 3
    if "--max" in sys.argv:
        idx = sys.argv.index("--max")
        try:
            max_n = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            pass

    print(f"🔍 多工具检索: {query}\n")
    text = multi_search_text(query, max_n)
    print(text)
    print(f"\n总计 {len(multi_search(query, max_n))} 条结果")
