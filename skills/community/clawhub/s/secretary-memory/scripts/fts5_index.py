#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - FTS5 全文搜索索引
基于 SQLite FTS5 的快速全文搜索，支持 LLM 摘要

用法:
    from fts5_index import FTS5Index
    idx = FTS5Index()
    idx.build_index()           # 构建索引
    results = idx.search("项目X")  # 搜索
    summary = idx.summarize(results, query)  # LLM 摘要
"""

import os
import re
import json
import sqlite3
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
FTS_DB = MEMORY_DIR / ".fts5_index.db"
FTS_LOCK = threading.Lock()

# LLM 配置（可通过环境变量覆盖）
LLM_API_URL = os.environ.get("LLM_API_URL", "http://localhost:11434/api/generate")
LLM_MODEL = os.environ.get("LLM_MODEL", "llama3")


# ============== LLM 摘要异常 ==============

class LLMSummarizationError(Exception):
    """LLM 摘要失败异常"""

    def __init__(self, message: str, hint: str = ""):
        self.message = message
        self.hint = hint
        super().__init__(f"{message}\n\n{hint}")


# ============== FTS5 索引类 ==============

class FTS5Index:
    """FTS5 全文搜索索引"""

    def __init__(self, memory_dir: Path = MEMORY_DIR):
        self.memory_dir = memory_dir
        self.db_path = memory_dir / ".fts5_index.db"
        self._ensure_db()

    def _ensure_db(self):
        """确保数据库和表存在"""
        with FTS_LOCK:
            conn = sqlite3.connect(str(self.db_path))
            cursor = conn.cursor()

            # 创建 FTS5 虚拟表
            cursor.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                    path,
                    title,
                    content,
                    partition,
                    date,
                    tokenize='unicode61 remove_diacritics 2'
                )
            """)

            # 创建元数据表（跟踪索引状态）
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fts_meta (
                    path TEXT PRIMARY KEY,
                    title TEXT,
                    partition TEXT,
                    date TEXT,
                    indexed_at TEXT,
                    file_mtime REAL,
                    file_size INTEGER
                )
            """)

            conn.commit()
            conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def index_file(self, file_path: Path, partition: str = "unknown") -> bool:
        """索引单个文件"""
        try:
            if not file_path.exists() or file_path.is_dir():
                return False

            stat = file_path.stat()
            content = file_path.read_text(encoding="utf-8", errors="ignore")

            lines = content.split('\n')
            title = lines[0].strip('# \n') if lines else file_path.stem
            if len(title) > 200:
                title = title[:200]

            date_match = re.match(r'^(\d{4}-\d{2}-\d{2})', file_path.stem)
            date_str = date_match.group(1) if date_match else datetime.now().strftime("%Y-%m-%d")

            clean_content = self._clean_content(content)

            with FTS_LOCK:
                conn = self._get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT OR REPLACE INTO memory_fts (path, title, content, partition, date)
                    VALUES (?, ?, ?, ?, ?)
                """, (str(file_path), title, clean_content, partition, date_str))

                cursor.execute("""
                    INSERT OR REPLACE INTO fts_meta (path, title, partition, date, indexed_at, file_mtime, file_size)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(file_path), title, partition, date_str,
                    datetime.now().isoformat(), stat.st_mtime, stat.st_size
                ))

                conn.commit()
                conn.close()

            return True
        except Exception as e:
            print(f"[FTS] 索引文件失败 {file_path}: {e}")
            return False

    def _clean_content(self, content: str) -> str:
        """清理内容，移除 markdown 格式"""
        content = re.sub(r'^#+\s+', '', content, flags=re.MULTILINE)
        content = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', content)
        content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
        content = re.sub(r'```[^`]*```', '', content, flags=re.DOTALL)
        content = re.sub(r'`([^`]+)`', r'\1', content)
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'\n{3,}', '\n\n', content)
        return content.strip()

    def build_index(self, partitions: List[str] = None, verbose: bool = False) -> Dict:
        """构建或更新索引"""
        if partitions is None:
            partitions = ["daily", "archive/daily", "archive/projects", "archive/decisions",
                         "agenda", "profile", "projects", "knowledge"]

        stats = {"total": 0, "indexed": 0, "skipped": 0, "errors": 0}

        for partition in partitions:
            partition_path = self.memory_dir / partition
            if not partition_path.exists():
                continue

            for md_file in partition_path.rglob("*.md"):
                if md_file.name.startswith('.'):
                    continue

                stats["total"] += 1

                if self._needs_reindex(md_file):
                    if self.index_file(md_file, partition):
                        stats["indexed"] += 1
                        if verbose:
                            print(f"[FTS] 索引: {md_file.relative_to(self.memory_dir)}")
                    else:
                        stats["errors"] += 1
                else:
                    stats["skipped"] += 1

        if verbose:
            print(f"\n[FTS] 索引构建完成: {stats['indexed']}/{stats['total']} 文件已索引 "
                  f"({stats['skipped']} 跳过, {stats['errors']} 错误)")

        return stats

    def _needs_reindex(self, file_path: Path) -> bool:
        """检查文件是否需要重新索引"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT file_mtime, file_size FROM fts_meta WHERE path = ?", (str(file_path),))
            row = cursor.fetchone()
            conn.close()

            if not row:
                return True

            stat = file_path.stat()
            return row['file_mtime'] != stat.st_mtime or row['file_size'] != stat.st_size
        except Exception:
            return True

    def search(self, query: str, limit: int = 20, partition: str = None) -> List[Dict]:
        """FTS5 搜索"""
        if not query.strip():
            return []

        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            fts_query = self._build_fts_query(query)

            if partition:
                sql = """
                    SELECT path, title, content, partition, date,
                           bm25(memory_fts) as rank,
                           highlight(memory_fts, 2, '**', '**') as snippet
                    FROM memory_fts
                    WHERE partition = ? AND memory_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                """
                cursor.execute(sql, (partition, fts_query, limit))
            else:
                sql = """
                    SELECT path, title, content, partition, date,
                           bm25(memory_fts) as rank,
                           highlight(memory_fts, 2, '**', '**') as snippet
                    FROM memory_fts
                    WHERE memory_fts MATCH ?
                    ORDER BY rank
                    LIMIT ?
                """
                cursor.execute(sql, (fts_query, limit))

            rows = cursor.fetchall()
            conn.close()

            results = []
            for row in rows:
                results.append({
                    "path": row['path'],
                    "title": row['title'],
                    "content": row['content'][:500],
                    "partition": row['partition'],
                    "date": row['date'],
                    "rank": row['rank'],
                    "snippet": row['snippet']
                })

            return results

        except Exception as e:
            print(f"[FTS] 搜索失败: {e}")
            return []

    def _build_fts_query(self, query: str) -> str:
        """构建 FTS5 查询字符串"""
        tokens = []
        for word in query.split():
            word = word.strip()
            if word:
                if len(word) > 1:
                    tokens.append(f'"{word}"')
                else:
                    tokens.append(word)
        return " OR ".join(tokens) if tokens else query

    def get_stats(self) -> Dict:
        """获取索引统计"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) as count FROM memory_fts")
            doc_count = cursor.fetchone()['count']

            cursor.execute("SELECT COUNT(*) as count FROM fts_meta")
            meta_count = cursor.fetchone()['count']

            cursor.execute("SELECT MAX(indexed_at) as last_index FROM fts_meta")
            last_index = cursor.fetchone()['last_index']

            conn.close()

            return {
                "document_count": doc_count,
                "meta_count": meta_count,
                "last_index": last_index,
                "db_size_mb": round(self.db_path.stat().st_size / (1024 * 1024), 2) if self.db_path.exists() else 0
            }
        except Exception as e:
            return {"error": str(e)}

    def delete_file(self, file_path: Path) -> bool:
        """从索引中删除文件"""
        try:
            with FTS_LOCK:
                conn = self._get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM memory_fts WHERE path = ?", (str(file_path),))
                cursor.execute("DELETE FROM fts_meta WHERE path = ?", (str(file_path),))
                conn.commit()
                conn.close()
            return True
        except Exception:
            return False

    def vacuum(self):
        """优化数据库"""
        try:
            with FTS_LOCK:
                conn = self._get_connection()
                conn.execute("VACUUM")
                conn.close()
            print("[FTS] 数据库已优化")
        except Exception as e:
            print(f"[FTS] 优化失败: {e}")


# ============== LLM 摘要 ==============

class LLMSummarizer:
    """LLM 搜索结果摘要"""

    def __init__(self, api_url: str = LLM_API_URL, model: str = LLM_MODEL):
        self.api_url = api_url
        self.model = model

    def summarize(self, results: List[Dict], query: str, max_context: int = 3000) -> str:
        """用 LLM 总结搜索结果"""
        if not results:
            return f"未找到与「{query}」相关的记忆"

        context = self._build_context(results, max_context)

        prompt = f"""你是一个秘书式记忆系统的助手。请根据以下搜索结果，总结与用户查询「{query}」相关的信息。

## 搜索结果
{context}

## 要求
1. 提取与查询最相关的要点
2. 按重要程度排序
3. 注明每个要点的来源（文件路径）
4. 如果有矛盾信息，指出冲突
5. 总结应简洁明了，便于快速了解相关记忆

## 输出格式
请用中文回复，格式如下：

### 相关要点
- [要点1] (来源: xxx)
- [要点2] (来源: xxx)
...

### 简要结论
[2-3句话的总结]
"""

        try:
            summary = self._call_llm(prompt)
            return summary
        except LLMSummarizationError as e:
            return f"💡 {e.message}\n\n{e.hint}\n\n---\n原始结果:\n{self._format_simple_results(results)}"
        except Exception as e:
            return f"[LLM 摘要失败: {e}]\n\n原始结果:\n{self._format_simple_results(results)}"

    def _build_context(self, results: List[Dict], max_context: int) -> str:
        """构建 LLM 上下文"""
        context_parts = []
        total_len = 0

        for i, r in enumerate(results, 1):
            part = f"""
--- 结果 {i} ---
文件: {r['path']}
日期: {r['date']}
分区: {r['partition']}
内容:
{r['content'][:1000]}
"""
            part_len = len(part)
            if total_len + part_len > max_context:
                break
            context_parts.append(part)
            total_len += part_len

        return "\n".join(context_parts)

    def _call_llm(self, prompt: str) -> str:
        """调用 LLM API"""
        import urllib.request
        import urllib.error

        # 检查是否配置了 API URL
        if not self.api_url or self.api_url == "http://localhost:11434/api/generate":
            raise LLMSummarizationError(
                "LLM API 未配置或不可访问。",
                hint="请在你的 settings.json 中添加 OpenClaw 的 API 配置：\n"
                     "设置 LLM_API_URL 环境变量指向你的 LLM 服务（如 Ollama）。\n"
                     "例如：export LLM_API_URL='http://localhost:11434/api/generate'\n\n"
                     "提示：OpenClaw 可以直接使用自己的 API key，无需额外配置。"
            )

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 512
            }
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.api_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "").strip()
        except urllib.error.URLError as e:
            raise LLMSummarizationError(
                f"LLM API 连接失败: {e}",
                hint="请检查 LLM 服务是否运行，或更新 LLM_API_URL 环境变量。\n"
                     "OpenClaw 可以直接使用自己的 API key 来启用此功能。"
            )

    def _format_simple_results(self, results: List[Dict]) -> str:
        """简单格式化结果（LLM 失败时回退）"""
        lines = [f"找到 {len(results)} 条相关记忆:\n"]
        for i, r in enumerate(results, 1):
            lines.append(f"{i}. [{r['partition']}] {r['path']} - {r['title'][:50]}")
        return "\n".join(lines)


# ============== 搜索入口 ==============

class SessionSearch:
    """会话搜索（整合 FTS5 + LLM 摘要）"""

    def __init__(self):
        self.fts = FTS5Index()
        self.llm = LLMSummarizer()

    def search(self, query: str, use_llm: bool = True, limit: int = 10,
               partition: str = None) -> Dict:
        """搜索并总结"""
        results = self.fts.search(query, limit=limit, partition=partition)

        response = {
            "results": results,
            "query": query,
            "count": len(results),
            "strategy": "fts5"
        }

        if use_llm and results:
            try:
                response["summary"] = self.llm.summarize(results, query)
            except Exception as e:
                error_msg = str(e)
                if "LLM API" in error_msg or "Connection" in error_msg:
                    response["llm_error"] = "LLM API 不可用，请配置 OpenClaw 的 API"
                else:
                    response["llm_error"] = error_msg[:100]

        response["stats"] = self.fts.get_stats()
        return response

    def format_output(self, response: Dict, format: str = "text") -> str:
        """格式化输出"""
        if format == "json":
            return json.dumps(response, ensure_ascii=False, indent=2)

        if not response["results"]:
            return f"未找到与「{response['query']}」相关的记忆"

        parts = []

        if "summary" in response:
            parts.append("## LLM 摘要\n")
            parts.append(response["summary"])
            parts.append("")

        parts.append(f"## 搜索结果 ({response['count']} 条)")

        for i, r in enumerate(response["results"], 1):
            parts.append(f"\n### {i}. {r['title']}")
            parts.append(f"   路径: {r['path']}")
            parts.append(f"   日期: {r['date']}")
            if r.get("snippet"):
                parts.append(f"   摘要: {r['snippet'][:200]}...")

        stats = response.get("stats", {})
        if stats and "error" not in stats:
            parts.append(f"\n--- 索引状态: {stats.get('document_count', 0)} 文档, "
                         f"最后更新: {stats.get('last_index', 'N/A')[:19]} ---")

        return "\n".join(parts)


# ============== 主程序 ==============

def main():
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw FTS5 搜索索引")
    parser.add_argument("query", nargs="?", help="搜索查询")
    parser.add_argument("--build", "-b", action="store_true", help="构建索引")
    parser.add_argument("--rebuild", "-r", action="store_true", help="重建索引")
    parser.add_argument("--stats", "-s", action="store_true", help="索引统计")
    parser.add_argument("--vacuum", action="store_true", help="优化数据库")
    parser.add_argument("--limit", "-l", type=int, default=10, help="结果数量")
    parser.add_argument("--no-llm", action="store_true", help="不使用 LLM 摘要")
    parser.add_argument("--json", "-j", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    search = SessionSearch()

    if args.build or args.rebuild:
        if args.rebuild:
            print("[FTS] 清除旧索引...")
            try:
                search.fts.db_path.unlink()
                search.fts._ensure_db()
            except Exception:
                pass

        print("[FTS] 开始构建索引...")
        stats = search.fts.build_index(verbose=True)
        print(f"[FTS] 完成: {stats}")
        return

    if args.stats:
        stats = search.fts.get_stats()
        print(f"## FTS5 索引统计\n")
        print(f"  文档数: {stats.get('document_count', 'N/A')}")
        print(f"  元数据: {stats.get('meta_count', 'N/A')}")
        print(f"  数据库: {stats.get('db_size_mb', 'N/A')} MB")
        print(f"  最后更新: {stats.get('last_index', 'N/A')}")
        return

    if args.vacuum:
        search.fts.vacuum()
        return

    if args.query:
        response = search.search(args.query, use_llm=not args.no_llm, limit=args.limit)

        if args.json:
            print(search.format_output(response, format="json"))
        else:
            print(search.format_output(response))
        return

    parser.print_help()


if __name__ == "__main__":
    main()