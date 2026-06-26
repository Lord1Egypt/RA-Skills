#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 多分区并发搜索
并行搜索 memory/ 下的多个分区，然后合并结果

用法:
    python3 memory_search.py <query>                    # 搜索所有分区
    python3 memory_search.py <query> --deep            # 深度搜索（包含 archive）
    python3 memory_search.py <query> --archive-only    # 仅搜索历史归档
    python3 memory_search.py <query> -p profile,agenda  # 指定分区
    python3 memory_search.py <query> --json            # JSON 输出

目录结构:
    memory/
    ├── daily/           # 每日日志（7天内）
    ├── archive/         # 历史归档
    │   ├── daily/      # 归档日志
    │   ├── projects/   # 归档项目
    │   └── decisions/  # 归档决策
    ├── agenda/          # 待办事项
    ├── profile/         # 用户偏好
    ├── projects/        # 进行中项目
    └── knowledge/       # 知识沉淀
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))

# 分区配置 - priority 越小越靠前
PARTITIONS = {
    "profile": {
        "path": "profile",
        "priority": 1,
        "description": "用户偏好档案"
    },
    "agenda": {
        "path": "agenda",
        "priority": 2,
        "description": "待办事项"
    },
    "projects": {
        "path": "projects",
        "priority": 3,
        "description": "进行中项目"
    },
    "knowledge": {
        "path": "knowledge",
        "priority": 4,
        "description": "知识沉淀"
    },
    "daily": {
        "path": "daily",
        "priority": 5,
        "description": "每日日志"
    },
    "archive": {
        "path": "archive",
        "priority": 6,
        "description": "历史归档"
    },
}

# ============== 搜索类 ==============

class MemorySearch:
    def __init__(self, memory_dir: Path, per_partition_limit: int = 3):
        self.memory_dir = memory_dir
        self.per_partition_limit = per_partition_limit

    def search_file(self, file_path: Path, query: str) -> Tuple[str, str, float]:
        """搜索单个文件，返回 (相对路径, 匹配片段, 相关度)"""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split('\n')
            query_lower = query.lower()

            matched_lines = []
            for i, line in enumerate(lines):
                if query_lower in line.lower():
                    # 获取上下文（前1行 + 当前行 + 后2行）
                    start = max(0, i - 1)
                    end = min(len(lines), i + 3)
                    context = '\n'.join(lines[start:end])
                    score = line.lower().count(query_lower)
                    matched_lines.append((i, context, score))

            if matched_lines:
                best = max(matched_lines, key=lambda x: x[2])
                relevance = best[2] / max(len(query.split()), 1)
                return (str(file_path.relative_to(self.memory_dir)), best[1], relevance)
        except Exception:
            pass
        return None

    def search_partition(self, partition_name: str, partition_info: Dict, query: str) -> List[Dict]:
        """搜索单个分区"""
        partition_path = self.memory_dir / partition_info["path"]
        if not partition_path.exists():
            return []

        results = []
        for md_file in partition_path.rglob("*.md"):
            if md_file.name.startswith('.'):
                continue
            result = self.search_file(md_file, query)
            if result:
                results.append({
                    "file": result[0],
                    "context": result[1],
                    "relevance": result[2],
                    "partition": partition_name,
                    "priority": partition_info["priority"]
                })

        # 按相关性排序，每分区只取前 N 条
        results.sort(key=lambda x: -x["relevance"])
        return results[:self.per_partition_limit]

    def search(self, query: str, partitions: List[str] = None, max_results: int = 20) -> List[Dict]:
        """并发搜索多个分区"""
        if partitions is None:
            partitions = list(PARTITIONS.keys())

        # 只搜索存在的分区
        active_partitions = {
            k: v for k, v in PARTITIONS.items()
            if k in partitions and (self.memory_dir / v["path"]).exists()
        }

        all_results = []

        # 并发搜索
        with ThreadPoolExecutor(max_workers=min(6, len(active_partitions))) as executor:
            futures = {
                executor.submit(self.search_partition, name, info, query): name
                for name, info in active_partitions.items()
            }

            for future in as_completed(futures):
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    print(f"搜索分区 {futures[future]} 时出错: {e}", file=sys.stderr)

        # 按优先级和相关性排序
        all_results.sort(key=lambda x: (-x["priority"], -x["relevance"]))
        return all_results[:max_results]

    def format_results(self, results: List[Dict], query: str) -> str:
        """格式化搜索结果"""
        if not results:
            return f"未找到与「{query}」相关的记忆"

        output = [f"找到 {len(results)} 条相关记忆:\n"]

        current_partition = None
        for i, r in enumerate(results, 1):
            if r["partition"] != current_partition:
                current_partition = r["partition"]
                desc = PARTITIONS.get(current_partition, {}).get("description", current_partition)
                output.append(f"\n## [{desc}]\n")

            context = r["context"].strip()
            if len(context) > 200:
                context = context[:200] + "..."

            output.append(f"{i}. {r['file']}\n   {context}\n")

        return '\n'.join(output)


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 秘书式记忆系统 - 搜索")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--partitions", "-p",
                        default="profile,agenda,projects,knowledge,daily,archive",
                        help="要搜索的分区（逗号分隔）")
    parser.add_argument("--max", "-m", type=int, default=20, help="最大结果数")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--deep", "-d", action="store_true",
                        help="深度搜索模式：包含 archive/ 的所有历史归档")
    parser.add_argument("--archive-only", action="store_true",
                        help="仅搜索历史归档（用于查询已结束的项目/话题）")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="简洁模式：只输出关键摘要，不输出完整上下文")
    parser.add_argument("--per-partition-limit", "-l", type=int, default=3,
                        help="每分区最大结果数 (默认3)")
    args = parser.parse_args()

    partitions = [x.strip() for x in args.partitions.split(",")]

    # --archive-only 模式下只搜索 archive
    if args.archive_only:
        partitions = ["archive"]
    # --deep 模式下包含 archive
    elif args.deep:
        if "archive" not in partitions:
            partitions.append("archive")
        print("[深度搜索] 正在检索所有历史归档...")

    search = MemorySearch(MEMORY_DIR, per_partition_limit=args.per_partition_limit)
    results = search.search(args.query, partitions=partitions, max_results=args.max)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        if args.quiet:
            # 简洁模式：只输出关键摘要
            if not results:
                print(f"未找到与「{args.query}」相关的记忆")
            else:
                summary_parts = []
                for r in results[:6]:
                    desc = PARTITIONS.get(r["partition"], {}).get("description", r["partition"])
                    matched_kw = args.query[:10]
                    summary_parts.append(f"{r['file']}[{desc}]")
                print(f"相关记忆 ({len(results)} 条): {'; '.join(summary_parts)}")
        else:
            output = search.format_results(results, args.query)
            if args.deep and results:
                output += "\n\n💡 提示: 使用 --archive-only 可仅搜索历史归档"
            print(output)


if __name__ == "__main__":
    main()
