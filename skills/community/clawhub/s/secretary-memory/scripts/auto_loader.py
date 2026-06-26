#!/usr/bin/env python3
"""
OpenClaw 秘书式记忆系统 - 自动上下文加载器
会话开始时自动加载相关记忆并注入到 prompt

用法:
    from auto_loader import AutoContextLoader
    loader = AutoContextLoader()
    context = loader.load_on_start("项目X 架构设计")
    prompt = loader.inject_to_context(context, base_prompt)

触发时机: OpenClaw 会话开始时（配合 hooks 或 AGENTS.md）
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

# ============== 配置 ==============
MEMORY_DIR = Path(os.environ.get("OPENCLAW_MEMORY_DIR", "/root/.openclaw/workspace/memory"))
STATE_FILE = MEMORY_DIR / ".auto_loader_state.json"

# 加载配置
MAX_MEMORIES = 5           # 最大加载记忆条数
RECENCY_BONUS_DAYS = 7    # 7天内记忆获得时间加权
RECENCY_BONUS_FACTOR = 1.5  # 时间加权系数
PARTITION_WEIGHTS = {
    "agenda": 2.0,         # 待办权重最高
    "projects": 1.8,
    "profile": 1.5,
    "knowledge": 1.2,
    "daily": 1.0,
    "archive": 0.5          # 归档权重最低
}
MIN_SCORE_THRESHOLD = 0.1  # 最低得分阈值


# ============== 优先级排序器 ==============

class PriorityRanker:
    """记忆优先级排序器（时间 + 相关性）"""

    @staticmethod
    def calculate_score(
        memory: Dict,
        query: str,
        now: datetime = None
    ) -> float:
        """计算记忆的综合得分

        综合得分 = 相关性得分 × 分区权重 × 时间加权

        Args:
            memory: 记忆字典，包含 score, partition, date 等
            query: 当前查询
            now: 当前时间

        Returns:
            综合得分 (0-1)
        """
        if now is None:
            now = datetime.now()

        # 基础相关性得分（已由搜索器计算）
        base_score = memory.get("score", memory.get("relevance", 0))
        if base_score <= 0:
            return 0

        # 归一化到 0-1
        normalized_score = min(base_score / 10, 1.0)

        # 分区权重
        partition = memory.get("partition", "unknown")
        partition_weight = PARTITION_WEIGHTS.get(partition, 1.0)

        # 时间加权
        date_str = memory.get("date", "")
        days_old = 0
        if date_str:
            try:
                memory_date = datetime.strptime(date_str[:10], "%Y-%m-%d")
                days_old = (now - memory_date).days
            except Exception:
                pass

        # 指数衰减：越新权重越高
        if days_old <= RECENCY_BONUS_DAYS:
            time_weight = RECENCY_BONUS_FACTOR
        else:
            time_weight = max(0.3, 1.0 - (days_old - RECENCY_BONUS_DAYS) / 365)

        # 综合得分
        final_score = normalized_score * partition_weight * time_weight

        return min(final_score, 1.0)

    @staticmethod
    def rank(memories: List[Dict], query: str) -> List[Dict]:
        """对记忆列表排序

        Args:
            memories: 记忆列表
            query: 当前查询

        Returns:
            排序后的记忆列表（附带 score 字段）
        """
        for memory in memories:
            memory["priority_score"] = PriorityRanker.calculate_score(memory, query)

        # 过滤低于阈值的
        filtered = [m for m in memories if m["priority_score"] >= MIN_SCORE_THRESHOLD]

        # 排序：得分高的在前
        filtered.sort(key=lambda x: -x["priority_score"])

        return filtered


# ============== 自动上下文加载器 ==============

class AutoContextLoader:
    """会话开始时自动加载上下文"""

    def __init__(self, memory_dir: Path = MEMORY_DIR):
        self.memory_dir = memory_dir
        self.state_file = STATE_FILE
        self.state = self._load_state()
        self.llm_summarizer = None  # 延迟加载

    def _load_state(self) -> Dict:
        """加载状态"""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "last_session_id": None,
            "last_topic": None,
            "loaded_count": 0,
            "last_load_time": None
        }

    def _save_state(self):
        """保存状态"""
        try:
            self.state_file.write_text(
                json.dumps(self.state, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
        except Exception:
            pass

    def _get_llm_summarizer(self):
        """延迟加载 LLM 摘要器"""
        if self.llm_summarizer is None:
            from fts5_index import LLMSummarizer
            self.llm_summarizer = LLMSummarizer()
        return self.llm_summarizer

    def load_on_start(self, session_topic: str = "", session_id: str = "") -> List[Dict]:
        """会话开始时加载相关记忆

        Args:
            session_topic: 当前会话话题/查询
            session_id: 会话 ID（可选）

        Returns:
            加载的记忆列表（已排序）
        """
        if not session_topic and not session_id:
            return []

        # 避免重复加载同一会话
        if session_id and session_id == self.state.get("last_session_id"):
            return []

        # 保存状态
        if session_id:
            self.state["last_session_id"] = session_id
        if session_topic:
            self.state["last_topic"] = session_topic

        # 执行搜索
        memories = self._search_memories(session_topic)

        # 优先级排序
        ranked = PriorityRanker.rank(memories, session_topic)

        # 限制数量
        result = ranked[:MAX_MEMORIES]

        # 更新状态
        self.state["loaded_count"] = len(result)
        self.state["last_load_time"] = datetime.now().isoformat()
        self._save_state()

        return result

    def _search_memories(self, query: str) -> List[Dict]:
        """搜索相关记忆"""
        memories = []

        # 优先使用 FTS5
        try:
            from fts5_index import FTS5Index
            fts = FTS5Index(self.memory_dir)
            results = fts.search(query, limit=20)

            for r in results:
                memories.append({
                    "path": r["path"],
                    "title": r.get("title", ""),
                    "content": r.get("content", ""),
                    "partition": r.get("partition", "unknown"),
                    "date": r.get("date", ""),
                    "score": abs(r.get("rank", 0)),  # BM25 rank 转正值
                    "source": "fts5"
                })
        except Exception as e:
            print(f"[AutoLoader] FTS5 搜索失败: {e}")

        # 如果 FTS5 没有结果，回退到经典搜索
        if not memories:
            try:
                from memory_search import MemorySearch
                searcher = MemorySearch(self.memory_dir, per_partition_limit=3)
                results = searcher.search(query, max_results=20)

                for r in results:
                    memories.append({
                        "path": r["file"],
                        "title": r.get("file", ""),
                        "content": r.get("context", ""),
                        "partition": r.get("partition", "unknown"),
                        "date": "",
                        "score": r.get("relevance", 0),
                        "source": "classic"
                    })
            except Exception as e:
                print(f"[AutoLoader] 经典搜索失败: {e}")

        return memories

    def inject_to_context(
        self,
        memories: List[Dict],
        base_prompt: str = "",
        use_llm_summary: bool = True
    ) -> str:
        """将记忆格式化并注入到 prompt

        Args:
            memories: load_on_start() 返回的记忆列表
            base_prompt: 原始 prompt（可选）

        Returns:
            注入上下文后的完整 prompt
        """
        if not memories:
            return base_prompt

        sections = []

        # 标题
        sections.append("\n\n<!-- 上下文记忆召回 -->\n")
        sections.append("## 📚 相关记忆\n")

        # LLM 摘要（如果可用）
        if use_llm_summary and len(memories) >= 2:
            try:
                summarizer = self._get_llm_summarizer()
                summary = summarizer.summarize(memories, query=self.state.get("last_topic", ""))
                if summary:
                    sections.append(f"\n### 智能摘要\n{summary}\n")
            except Exception as e:
                print(f"[AutoLoader] LLM 摘要失败: {e}")

        # 逐条记忆
        sections.append("\n### 详细记忆\n")
        for i, m in enumerate(memories, 1):
            title = m.get("title", m["path"][-50:])
            partition = m.get("partition", "unknown")
            date = m.get("date", "")
            content = m.get("content", "")[:300]

            sections.append(f"\n**{i}. [{partition}] {title}**")
            if date:
                sections.append(f"  📅 {date}")
            if content:
                clean = content.replace("\n", " ").strip()
                sections.append(f"  {clean}...")

        # 注入到 prompt
        if base_prompt:
            # 尝试插入到适当位置
            if "<!-- 上下文记忆召回 -->" in base_prompt:
                return base_prompt  # 已注入
            # 插入到开头
            return "".join(sections) + "\n\n" + base_prompt
        else:
            return "".join(sections)

    def get_context_for_prompt(self, session_topic: str = "") -> str:
        """获取上下文字符串（便捷方法）

        等同于 load_on_start() + inject_to_context()

        Args:
            session_topic: 会话话题

        Returns:
            上下文字符串（可直接追加到 system prompt）
        """
        memories = self.load_on_start(session_topic)
        return self.inject_to_context(memories, use_llm_summary=True)

    def format_memory_list(self, memories: List[Dict]) -> str:
        """格式化记忆列表（简洁模式）"""
        if not memories:
            return "无相关记忆"

        parts = []
        for m in memories[:MAX_MEMORIES]:
            partition = m.get("partition", "?")
            title = m.get("title", m.get("path", "?")[-30:])
            score = m.get("priority_score", 0)
            parts.append(f"[{partition}] {title} (优先级: {score:.2f})")

        return "\n".join(parts)


# ============== Hook 集成 ==============

def on_session_start(session_id: str = "", session_topic: str = ""):
    """会话开始时的 hook 函数

    用法（在 AGENTS.md 或 hooks 中）:
        python3 auto_loader.py --hook-start --session-id {session_id} --topic "xxx"
    """
    loader = AutoContextLoader()
    memories = loader.load_on_start(session_topic, session_id)

    if memories:
        print(f"[AutoLoader] 已加载 {len(memories)} 条相关记忆:")
        print(loader.format_memory_list(memories))

        # 输出注入格式
        context = loader.inject_to_context(memories)
        print("\n--- 注入上下文 ---")
        print(context[:500] + "..." if len(context) > 500 else context)
    else:
        print("[AutoLoader] 未找到相关记忆")

    return memories


# ============== CLI 主程序 ==============

def main():
    import argparse

    parser = argparse.ArgumentParser(description="OpenClaw 自动上下文加载器")
    parser.add_argument("--topic", "-t", default="", help="会话话题/查询")
    parser.add_argument("--session-id", "-s", default="", help="会话 ID")
    parser.add_argument("--hook-start", action="store_true", help="Hook: 会话开始")
    parser.add_argument("--hook-end", action="store_true", help="Hook: 会话结束")
    parser.add_argument("--inject", "-i", action="store_true", help="输出注入格式")
    parser.add_argument("--list", "-l", action="store_true", help="简洁列表模式")
    parser.add_argument("--stats", action="store_true", help="显示加载统计")
    args = parser.parse_args()

    loader = AutoContextLoader()

    if args.hook_start:
        memories = on_session_start(args.session_id, args.topic)
        return

    if args.stats:
        state = loader.state
        print("## 自动加载器状态\n")
        print(f"  上次会话: {state.get('last_session_id', 'N/A')}")
        print(f"  上次话题: {state.get('last_topic', 'N/A')}")
        print(f"  加载条数: {state.get('loaded_count', 0)}")
        print(f"  上次时间: {state.get('last_load_time', 'N/A')}")
        return

    # 常规加载
    if not args.topic:
        parser.print_help()
        print("\n[Error] 请提供 --topic 参数")
        return

    memories = loader.load_on_start(args.topic, args.session_id)

    if args.list:
        print(loader.format_memory_list(memories))
    elif args.inject:
        context = loader.inject_to_context(memories)
        print(context)
    else:
        if not memories:
            print(f"未找到与「{args.topic}」相关的记忆")
        else:
            print(f"## 加载了 {len(memories)} 条相关记忆:\n")
            for i, m in enumerate(memories, 1):
                print(f"{i}. [{m.get('partition', '?')}] {m.get('title', m['path'][-30:])} "
                      f"(优先级: {m.get('priority_score', 0):.2f})")


if __name__ == "__main__":
    main()