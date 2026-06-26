#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 统一搜索入口
整合 FTS5 全文搜索 + 传统分区搜索 + LLM 摘要

用法:
    python3 session_search.py "项目X 架构"          # FTS5 + LLM 摘要
    python3 session_search.py "项目X" --classic   # 传统分区搜索
    python3 session_search.py "项目X" --no-llm    # FTS5 无摘要
    python3 session_search.py --build-index       # 构建 FTS5 索引
    python3 session_search.py --stats             # 索引统计
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))


# ============== 搜索策略 ==============

class SearchStrategy:
    """搜索策略基类"""

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        raise NotImplementedError


class ClassicSearch(SearchStrategy):
    """传统分区搜索（兼容模式）"""

    def __init__(self):
        from memory_search import MemorySearch
        self.searcher = MemorySearch(MEMORY_DIR, per_partition_limit=3)

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        results = self.searcher.search(query, max_results=limit)
        # 转换格式
        return [
            {
                "path": r["file"],
                "title": r["file"],
                "content": r["context"],
                "partition": r["partition"],
                "rank": r["relevance"],
                "source": "classic"
            }
            for r in results
        ]


class FTS5Search(SearchStrategy):
    """FTS5 全文搜索"""

    def __init__(self):
        from fts5_index import FTS5Index
        self.index = FTS5Index(MEMORY_DIR)

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        results = self.index.search(query, limit=limit)
        # 转换格式
        return [
            {
                "path": r["path"],
                "title": r["title"],
                "content": r["content"],
                "partition": r["partition"],
                "date": r.get("date", ""),
                "rank": r["rank"],
                "snippet": r.get("snippet", ""),
                "source": "fts5"
            }
            for r in results
        ]


class HybridSearch(SearchStrategy):
    """混合搜索：FTS5 + 经典搜索合并"""

    def __init__(self):
        self.fts5 = FTS5Search()
        self.classic = ClassicSearch()

    def search(self, query: str, limit: int = 10) -> List[Dict]:
        # 并发搜索
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            fts5_future = executor.submit(self.fts5.search, query, limit)
            classic_future = executor.submit(self.classic.search, query, limit)

            fts5_results = fts5_future.result()
            classic_results = classic_future.result()

        # 合并去重（按 path）
        seen = {}
        for r in fts5_results:
            seen[r["path"]] = r
        for r in classic_results:
            if r["path"] not in seen:
                seen[r["path"]] = r

        results = list(seen.values())

        # 按 rank 排序
        results.sort(key=lambda x: x.get("rank", 0))

        return results[:limit]


# ============== 主搜索器 ==============

class SessionSearch:
    """统一搜索入口"""

    def __init__(self, strategy: str = "hybrid"):
        """
        Args:
            strategy: "fts5", "classic", "hybrid"
        """
        self.strategy_name = strategy
        if strategy == "fts5":
            self.strategy = FTS5Search()
        elif strategy == "classic":
            self.strategy = ClassicSearch()
        else:  # hybrid
            self.strategy = HybridSearch()

        # LLM 摘要器
        from fts5_index import LLMSummarizer
        self.llm = LLMSummarizer()

    def search(self, query: str, use_llm: bool = True, limit: int = 10,
               partition: str = None) -> Dict:
        """执行搜索

        Returns:
            {
                "query": str,
                "results": [...],
                "count": int,
                "summary": str (if use_llm),
                "strategy": str,
                "stats": {...}
            }
        """
        results = self.strategy.search(query, limit=limit)

        # 过滤分区
        if partition:
            results = [r for r in results if r.get("partition") == partition]

        response = {
            "query": query,
            "results": results,
            "count": len(results),
            "strategy": self.strategy_name
        }

        # LLM 摘要
        if use_llm and results:
            try:
                response["summary"] = self.llm.summarize(results, query)
            except Exception as e:
                # 提取友好提示
                error_msg = str(e)
                if "LLM API" in error_msg or "Connection" in error_msg:
                    response["llm_error"] = "LLM API 不可用，请配置 OpenClaw 的 API"
                else:
                    response["llm_error"] = error_msg[:100]

        # 索引统计
        if hasattr(self.strategy, 'index'):
            response["stats"] = self.strategy.index.get_stats()
        elif hasattr(self.strategy, 'fts5'):
            response["stats"] = self.strategy.fts5.index.get_stats()

        return response

    def format_results(self, response: Dict, format: str = "text") -> str:
        """格式化输出"""
        if format == "json":
            import json
            # 移除不可序列化的部分
            output = {k: v for k, v in response.items() if k != "stats"}
            return json.dumps(output, ensure_ascii=False, indent=2)

        query = response["query"]
        results = response["results"]

        if not results:
            return f"未找到与「{query}」相关的记忆"

        parts = []

        # LLM 摘要
        if "summary" in response:
            parts.append("## 📋 LLM 摘要\n")
            parts.append(response["summary"])
            parts.append("")

        # 结果列表
        parts.append(f"## 🔍 搜索结果 ({response['count']} 条)")

        current_partition = None
        for i, r in enumerate(results, 1):
            partition = r.get("partition", "unknown")
            if partition != current_partition:
                current_partition = partition
                parts.append(f"\n### [{partition}]\n")

            title = r.get("title", r["path"][-50:])
            path = r.get("path", "")
            date = r.get("date", "")
            snippet = r.get("snippet") or r.get("content", "")[:200]

            parts.append(f"{i}. **{title}**")
            parts.append(f"   📁 {path}")
            if date:
                parts.append(f"   📅 {date}")
            if snippet:
                clean_snippet = snippet.replace("\n", " ").strip()[:150]
                parts.append(f"   💬 {clean_snippet}...")
            parts.append("")

        # 策略信息
        parts.append(f"---\n搜索策略: {response['strategy']}")

        # 索引统计
        if "stats" in response and "error" not in response["stats"]:
            stats = response["stats"]
            parts.append(f"FTS5索引: {stats.get('document_count', 'N/A')} 文档")

        return "\n".join(parts)


# ============== 上下文加载集成 ==============

def load_context_for_query(query: str, use_llm: bool = True) -> str:
    """为新会话加载相关上下文（集成 FTS5）

    Args:
        query: 会话查询/话题
        use_llm: 是否使用 LLM 摘要

    Returns:
        可注入 prompt 的上下文字符串
    """
    searcher = SessionSearch(strategy="hybrid")
    response = searcher.search(query, use_llm=use_llm, limit=5)

    if not response["results"]:
        return ""

    parts = ["<!-- 相关记忆召回 -->"]

    if "summary" in response:
        parts.append(f"\n## 记忆摘要\n{response['summary']}\n")

    parts.append("\n## 原始记忆")

    for r in response["results"][:3]:
        parts.append(f"\n### {r['title']}")
        content = r.get("content", "") or r.get("snippet", "")
        if len(content) > 300:
            content = content[:300] + "..."
        parts.append(content)

    return "\n".join(parts)


# ============== 主程序 ==============

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="OpenClaw 秘书式记忆系统 - 统一搜索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    python3 session_search.py "项目X 架构"        # FTS5 + LLM 摘要
    python3 session_search.py "项目X" --classic # 传统分区搜索
    python3 session_search.py "项目X" --no-llm  # FTS5 无摘要
    python3 session_search.py --build-index     # 构建索引
        """
    )
    parser.add_argument("query", nargs="?", help="搜索查询")
    parser.add_argument("--classic", action="store_true", help="使用传统分区搜索")
    parser.add_argument("--fts5", action="store_true", help="仅使用 FTS5 搜索")
    parser.add_argument("--no-llm", action="store_true", help="不使用 LLM 摘要")
    parser.add_argument("--limit", "-l", type=int, default=10, help="结果数量")
    parser.add_argument("--partition", "-p", help="限定分区")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    parser.add_argument("--build-index", "-b", action="store_true", help="构建 FTS5 索引")
    parser.add_argument("--stats", "-s", action="store_true", help="显示索引统计")
    parser.add_argument("--context", "-c", action="store_true", help="加载上下文（用于会话开始）")

    args = parser.parse_args()

    # 索引操作
    if args.build_index or args.stats:
        from fts5_index import FTS5Index
        fts = FTS5Index(MEMORY_DIR)

        if args.build_index:
            print("[FTS5] 构建索引...")
            stats = fts.build_index(verbose=True)
            print(f"[OK] 完成: {stats}")

        if args.stats:
            stats = fts.get_stats()
            print(f"\n## FTS5 索引统计")
            print(f"  文档: {stats.get('document_count', 'N/A')}")
            print(f"  数据库: {stats.get('db_size_mb', 'N/A')} MB")
            print(f"  最后更新: {stats.get('last_index', 'N/A')}")
        return

    if not args.query and not args.context:
        parser.print_help()
        return

    # 确定策略
    if args.classic:
        strategy = "classic"
    elif args.fts5:
        strategy = "fts5"
    else:
        strategy = "hybrid"

    searcher = SessionSearch(strategy=strategy)

    # 上下文加载模式
    if args.context:
        context = load_context_for_query(args.query or "", use_llm=not args.no_llm)
        if context:
            print(context)
        else:
            print("未找到相关记忆")
        return

    # 常规搜索
    response = searcher.search(
        args.query,
        use_llm=not args.no_llm,
        limit=args.limit,
        partition=args.partition
    )

    if args.json:
        print(searcher.format_results(response, format="json"))
    else:
        print(searcher.format_results(response))


if __name__ == "__main__":
    main()