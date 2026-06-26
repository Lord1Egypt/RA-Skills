#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 上下文主动加载
在新会话开始时根据话题召回最相关的历史记忆（每分区3条）

用法:
    python3 context_loader.py "项目X 设计方案"
    python3 context_loader.py "项目X" --quiet
    python3 context_loader.py "项目X" --format prompt
"""

import os
import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
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
    "decisions": {
        "path": "archive/decisions",
        "priority": 5,
        "description": "历史决策"
    },
    "daily": {
        "path": "daily",
        "priority": 6,
        "description": "每日日志"
    },
    "archive_projects": {
        "path": "archive/projects",
        "priority": 7,
        "description": "归档项目"
    },
}


# ============== 上下文加载器 ==============

class ContextLoader:
    def __init__(self, memory_dir: Path, per_partition_limit: int = 3):
        self.memory_dir = memory_dir
        self.per_partition_limit = per_partition_limit

    def extract_keywords(self, query: str) -> List[str]:
        """从查询中提取关键词"""
        keywords = []

        # 技术栈
        tech_patterns = [
            r'(React|Flask|LangGraph|RAG|OpenClaw|Claude|MiniMax|Stm32|Python|JavaScript|TypeScript)',
            r'([A-Z][a-zA-Z]+)',  # CamelCase
        ]
        for pattern in tech_patterns:
            matches = re.findall(pattern, query)
            keywords.extend(matches)

        # 中文词汇（2-8字）
        chinese_pattern = r'([\u4e00-\u9fa5]{2,8})'
        matches = re.findall(chinese_pattern, query)
        keywords.extend(matches)

        # 过滤太短的词
        keywords = [k for k in keywords if len(k) >= 2]
        return list(dict.fromkeys(keywords))[:10]

    def search_file(self, file_path: Path, keywords: List[str]) -> Optional[Dict]:
        """搜索单个文件，返回匹配结果"""
        try:
            content = file_path.read_text(encoding="utf-8")
            content_lower = content.lower()

            # 计算匹配分数
            score = 0
            matched_keywords = []
            for kw in keywords:
                kw_lower = kw.lower()
                if kw_lower in content_lower:
                    score += content_lower.count(kw_lower)
                    matched_keywords.append(kw)

            if score > 0:
                # 获取匹配上下文
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if any(kw.lower() in line.lower() for kw in keywords):
                        # 获取前后2行作为上下文
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        context = '\n'.join(lines[start:end])
                        return {
                            "file": str(file_path.relative_to(self.memory_dir)),
                            "score": score,
                            "context": context,
                            "matched_keywords": matched_keywords
                        }
        except Exception:
            pass
        return None

    def search_partition(self, partition_name: str, partition_info: Dict, keywords: List[str]) -> List[Dict]:
        """搜索单个分区，返回最多 N 条结果"""
        partition_path = self.memory_dir / partition_info["path"]
        if not partition_path.exists():
            return []

        results = []
        for md_file in partition_path.rglob("*.md"):
            if md_file.name.startswith('.'):
                continue
            result = self.search_file(md_file, keywords)
            if result:
                result["partition"] = partition_name
                result["partition_priority"] = partition_info["priority"]
                results.append(result)

        # 按分数排序，每分区只取前 N 条
        results.sort(key=lambda x: -x["score"])
        return results[:self.per_partition_limit]

    def load_context(self, query: str) -> List[Dict]:
        """加载与查询相关的上下文"""
        keywords = self.extract_keywords(query)
        if not keywords:
            # 如果没提取到关键词，把整个查询作为关键词
            keywords = [query]

        all_results = []

        # 并发搜索所有分区
        with ThreadPoolExecutor(max_workers=min(6, len(PARTITIONS))) as executor:
            futures = {
                executor.submit(self.search_partition, name, info, keywords): name
                for name, info in PARTITIONS.items()
            }

            for future in as_completed(futures):
                try:
                    results = future.result()
                    all_results.extend(results)
                except Exception as e:
                    print(f"搜索分区 {futures[future]} 时出错: {e}", file=sys.stderr)

        # 按分区优先级和分数排序
        all_results.sort(key=lambda x: (x["partition_priority"], -x["score"]))
        return all_results

    def format_context_text(self, results: List[Dict], query: str) -> str:
        """格式化上下文为易读的文本"""
        if not results:
            return f"未找到与「{query}」相关的记忆\n"

        output = [f"## 相关记忆召回 (关键词: {', '.join(self.extract_keywords(query)[:5])})\n"]

        current_partition = None
        for r in results:
            if r["partition"] != current_partition:
                current_partition = r["partition"]
                desc = PARTITIONS.get(current_partition, {}).get("description", current_partition)
                output.append(f"\n### [{desc}]\n")

            context = r["context"].strip()
            if len(context) > 200:
                context = context[:200] + "..."

            output.append(f"**{r['file']}** (匹配度: {r['score']})\n{context}\n")

        return '\n'.join(output)

    def format_context_prompt(self, results: List[Dict], query: str) -> str:
        """格式化上下文为可直接注入 prompt 的格式"""
        if not results:
            return ""

        keywords = self.extract_keywords(query)[:5]
        sections = [f"<!-- 上下文召回 (query: {query[:30]}...) -->"]

        current_partition = None
        for r in results:
            if r["partition"] != current_partition:
                current_partition = r["partition"]
                desc = PARTITIONS.get(current_partition, {}).get("description", current_partition)
                sections.append(f"\n## [{desc}]")

            # 截取关键段落
            context = r["context"].strip()
            lines = context.split('\n')
            # 只保留包含关键词的行及其上下文
            filtered_lines = []
            for line in lines:
                if any(kw.lower() in line.lower() for kw in keywords):
                    filtered_lines.append(line.strip())

            if filtered_lines:
                sections.append(f"- *{r['file']}*: {' | '.join(filtered_lines[:3])}")

        return '\n'.join(sections)

    def format_context_quiet(self, results: List[Dict], query: str) -> str:
        """简洁格式：只输出关键摘要"""
        if not results:
            return f"未找到与「{query}」相关的记忆"

        keywords = self.extract_keywords(query)[:3]
        output = [f"相关记忆 ({len(results)} 条): "]

        summary_parts = []
        for r in results:
            desc = PARTITIONS.get(r["partition"], {}).get("description", r["partition"])
            matched = ', '.join(r['matched_keywords'][:2])
            summary_parts.append(f"{r['file']}[{desc}: {matched}]")

        output.append('; '.join(summary_parts[:6]))
        return '\n'.join(output)


# ============== 主程序 ==============

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 秘书式记忆系统 - 上下文加载")
    parser.add_argument("query", nargs="?", default="", help="查询话题")
    parser.add_argument("--quiet", "-q", action="store_true", help="简洁模式：只输出关键摘要")
    parser.add_argument("--format", "-f", choices=["text", "prompt", "json"], default="text", help="输出格式")
    parser.add_argument("--limit", "-l", type=int, default=3, help="每分区最大结果数 (默认3)")
    parser.add_argument("--json", "-j", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        print("\n[Error] 请提供查询话题")
        return

    loader = ContextLoader(MEMORY_DIR, per_partition_limit=args.limit)
    results = loader.load_context(args.query)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return

    if args.quiet:
        print(loader.format_context_quiet(results, args.query))
        return

    if args.format == "prompt":
        print(loader.format_context_prompt(results, args.query))
    else:
        print(loader.format_context_text(results, args.query))


if __name__ == "__main__":
    main()
