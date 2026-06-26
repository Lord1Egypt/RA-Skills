from __future__ import annotations
"""
recording_card.py - 录音卡导出
将检索结果或会话数据转成结构化 Markdown 录音卡（类似钉钉 A1）
"""

import time
from datetime import datetime


class RecordingCardExporter:
    """录音卡导出器"""

    # 性质 ID → 中文名
    NATURE_NAMES = {
        "D01": "碎片", "D02": "日志", "D03": "任务", "D04": "探索",
        "D05": "笔记", "D06": "交付", "D07": "待办", "D08": "典藏",
        "D09": "回溯", "D10": "配置", "D11": "漫谈", "D12": "解惑",
    }

    # 状态图标
    STATUS_ICONS = {
        "pending": "⚪",
        "in_progress": "🟡",
        "done": "🟢",
        "overdue": "🔴",
    }

    IMPARTANCE_ICONS = {
        "high": "⚡",
        "medium": "",
        "low": "🔻",
    }

    def __init__(self, store=None, encoder=None):
        self.store = store
        self.encoder = encoder

    def from_recall_result(
        self,
        recall_result: dict,
        title: str = "对话录音卡",
        session_id: str = None,
    ) -> str:
        """
        从检索结果生成录音卡 Markdown。

        参数:
            recall_result: RecallEngine.recall() 的返回值
            title: 录音卡标题
            session_id: 会话 ID（可选）

        返回: Markdown 字符串
        """
        primary = recall_result.get("primary", [])
        related = recall_result.get("related", [])
        query = recall_result.get("query", "")
        mode = recall_result.get("search_mode", "")

        if not primary:
            return f"# 📋 {title}\n\n_无检索结果_\n"

        # 时间范围
        timestamps = [m.get("time_ts", 0) for m in primary if m.get("time_ts")]
        if timestamps:
            start = datetime.fromtimestamp(min(timestamps))
            end = datetime.fromtimestamp(max(timestamps))
            time_range = f"{start.strftime('%Y-%m-%d %H:%M')} - {end.strftime('%H:%M')}"
        else:
            time_range = "未知"

        # 按性质分组
        by_nature = {}
        for mem in primary:
            nid = mem.get("nature_id", "D11")
            by_nature.setdefault(nid, []).append(mem)

        # 按主题分组
        by_topic = {}
        for mem in primary:
            topics = mem.get("topics", [])
            topic_key = topics[0]["code"] if topics and isinstance(topics[0], dict) else (topics[0] if topics else "未分类")
            by_topic.setdefault(topic_key, []).append(mem)

        # 生成 Markdown
        lines = []
        lines.append(f"# 📋 {title}")
        lines.append("")

        if session_id:
            lines.append(f"**会话 ID**: {session_id}")
        lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        lines.append(f"**检索模式**: {mode}")
        if query:
            lines.append(f"**检索词**: {query}")
        lines.append(f"**时间范围**: {time_range}")
        lines.append(f"**记录数**: {len(primary)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # ── 按性质分组展示 ──────────────────────────────
        for nid in sorted(by_nature.keys()):
            name = self.NATURE_NAMES.get(nid, nid)
            mems = by_nature[nid]
            lines.append(f"## {name} ({len(mems)} 条)")
            lines.append("")

            for mem in mems:
                imp_icon = self.IMPARTANCE_ICONS.get(mem.get("importance", "medium"), "")
                time_id = mem.get("time_id", "")
                content = mem.get("content", "")

                # 主题标签
                topics = mem.get("topics", [])
                topic_str = ""
                if topics:
                    codes = [t["code"] if isinstance(t, dict) else t for t in topics[:2]]
                    topic_str = " `" + "` `".join(codes) + "`"

                lines.append(f"- {imp_icon}**{content}**{topic_str}")
                lines.append(f"  - 📅 {time_id}")

            lines.append("")

        # ── 待办任务汇总 ──────────────────────────────
        todo_mems = by_nature.get("D07", [])
        if todo_mems and self.store:
            tasks = self.store.get_tasks(limit=20)
            if tasks:
                lines.append("## ✅ 待办任务")
                lines.append("")
                lines.append("| 状态 | 任务 | 主题 |")
                lines.append("|------|------|------|")
                for t in tasks:
                    icon = self.STATUS_ICONS.get(t["status"], "❓")
                    title_str = t["title"][:50]
                    topic = t.get("topic_code", "-")
                    lines.append(f"| {icon} {t['status']} | {title_str} | {topic} |")
                lines.append("")

        # ── 关联记录 ──────────────────────────────────
        if related:
            lines.append("## 🔗 关联记录")
            lines.append("")
            for r in related[:5]:
                link_type = r.get("_link_type", "")
                content = r.get("content", "")[:60]
                lines.append(f"- [{link_type}] {content}")
            lines.append("")

        # ── 统计摘要 ──────────────────────────────────
        lines.append("## 📊 统计")
        lines.append("")
        lines.append(f"- 总记录数: {len(primary)}")
        lines.append(f"- 主题分布: {', '.join(f'{k}({len(v)})' for k, v in sorted(by_topic.items()))}")
        lines.append(f"- 性质分布: {', '.join(f'{self.NATURE_NAMES.get(k, k)}({len(v)})' for k, v in sorted(by_nature.items()))}")

        high_count = sum(1 for m in primary if m.get("importance") == "high")
        if high_count:
            lines.append(f"- ⚡高优先: {high_count} 条")

        lines.append("")
        lines.append("---")
        lines.append(f"_由 Agent Memory System 自动生成_")

        return "\n".join(lines)

    def from_session(
        self,
        person_id: str = None,
        time_from: int = None,
        time_to: int = None,
        title: str = "会话录音卡",
    ) -> str:
        """从存储层直接查询生成录音卡"""
        if not self.store:
            return "# 📋 录音卡\n\n_未配置存储层_\n"

        memories = self.store.query(
            person_id=person_id,
            time_from=time_from,
            time_to=time_to,
            limit=100,
        )

        # 包装成 recall_result 格式
        return self.from_recall_result(
            recall_result={"primary": memories, "related": [], "query": "", "search_mode": "structured"},
            title=title,
        )

    def save(self, markdown: str, output_path: str) -> str:
        """保存录音卡到文件"""
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown)
        return output_path
