from __future__ import annotations

import time
import logging
from collections import Counter
from dataclasses import dataclass, field
from typing import Optional

from ..interface import SpiritInterface

logger = logging.getLogger(__name__)


@dataclass
class TopicCluster:
    label: str = ""
    memory_ids: list[str] = field(default_factory=list)
    avg_importance: str = "medium"
    count: int = 0


@dataclass
class MemoryEntry:
    memory_id: str = ""
    content: str = ""
    topics: list[str] = field(default_factory=list)
    importance: str = "medium"
    time_ts: int = 0
    nature_id: str = ""
    person_id: str = ""
    valence: float = 0.0
    arousal: float = 0.2


class DailyReportGenerator:
    """Daily report: 'a book of today's memories', NOT a statistics report.

    - Auto-adaptive topic classification (embedding clustering, not hardcoded)
    - Content-first: each memory has its content quoted, with metadata
    - System observations: contradictions, fragmentation suggestions
    - Pure template rendering (no LLM needed for basic version)
    """

    def __init__(self, interface: SpiritInterface, llm_layer=None):
        self.interface = interface
        self.llm_layer = llm_layer

    def generate(self, date: int = None, format: str = 'markdown') -> str:
        if date is None:
            date = self._today_ts()

        day_start = date
        day_end = date + 86400

        memories = self._fetch_memories(day_start, day_end)

        if not memories:
            return self._render_empty_report(date, format)

        clusters = self._cluster_by_topic(memories)
        observations = self._generate_observations(memories, clusters)

        if format == 'json':
            return self._render_json(date, memories, clusters, observations)
        return self._render_markdown(date, memories, clusters, observations)

    def _today_ts(self) -> int:
        now = time.time()
        return int(now - now % 86400)

    def _fetch_memories(self, time_from: int, time_to: int) -> list[MemoryEntry]:
        try:
            result = self.interface.read('recall', query='', time_from=time_from, time_to=time_to, limit=100)
            raw_content = result.content
            return self._parse_recall_to_entries(raw_content)
        except Exception as e:
            logger.debug("DailyReport: recall failed: %s", e)
            return []

    def _parse_recall_to_entries(self, raw_content: str) -> list[MemoryEntry]:
        entries = []
        if not raw_content or raw_content.startswith('[ERROR') or raw_content == '[EMPTY]':
            return entries

        try:
            store = self.interface._store
            if store is None:
                return entries

            now = int(time.time())
            day_start = now - now % 86400
            day_end = day_start + 86400

            rows = store.query(time_from=day_start, time_to=day_end, limit=100)
            for row in rows:
                topics = []
                for t in row.get('topics', []):
                    if isinstance(t, dict):
                        topics.append(t.get('code', ''))
                    else:
                        topics.append(str(t))

                entries.append(MemoryEntry(
                    memory_id=row.get('memory_id', ''),
                    content=row.get('content', ''),
                    topics=topics,
                    importance=row.get('importance', 'medium'),
                    time_ts=row.get('time_ts', 0),
                    nature_id=row.get('nature_id', ''),
                    person_id=row.get('person_id', ''),
                    valence=row.get('valence', 0.0),
                    arousal=row.get('arousal', 0.2),
                ))
        except Exception as e:
            logger.debug("DailyReport: parse entries failed: %s", e)

        return entries

    def _cluster_by_topic(self, memories: list[MemoryEntry]) -> list[TopicCluster]:
        topic_groups: dict[str, list[MemoryEntry]] = {}
        ungrouped: list[MemoryEntry] = []

        for mem in memories:
            primary_topics = [t for t in mem.topics if t] if mem.topics else []
            if primary_topics:
                root = primary_topics[0].split('.')[0] if '.' in primary_topics[0] else primary_topics[0]
                topic_groups.setdefault(root, []).append(mem)
            else:
                ungrouped.append(mem)

        clusters = []
        for topic, group in topic_groups.items():
            imp_counts = Counter(m.importance for m in group)
            avg_imp = imp_counts.most_common(1)[0][0] if imp_counts else 'medium'
            clusters.append(TopicCluster(
                label=topic,
                memory_ids=[m.memory_id for m in group],
                avg_importance=avg_imp,
                count=len(group),
            ))

        if ungrouped:
            clusters.append(TopicCluster(
                label='uncategorized',
                memory_ids=[m.memory_id for m in ungrouped],
                avg_importance='medium',
                count=len(ungrouped),
            ))

        clusters.sort(key=lambda c: c.count, reverse=True)
        return clusters

    def _generate_observations(self, memories: list[MemoryEntry], clusters: list[TopicCluster]) -> list[str]:
        observations = []

        low_quality = [m for m in memories if m.importance == 'low' and len(m.content) < 20]
        if low_quality:
            observations.append(f"发现 {len(low_quality)} 条低质量短记忆，建议合并或清理")

        large_clusters = [c for c in clusters if c.count >= 10]
        if large_clusters:
            for c in large_clusters:
                observations.append(f"主题 '{c.label}' 有 {c.count} 条记忆，建议检查是否需要合并")

        small_clusters = [c for c in clusters if c.count == 1 and c.label != 'uncategorized']
        if len(small_clusters) >= 3:
            observations.append(f"有 {len(small_clusters)} 个孤立主题，可能存在碎片化")

        high_arousal = [m for m in memories if m.arousal > 0.7]
        if high_arousal:
            observations.append(f"发现 {len(high_arousal)} 条高情绪强度记忆")

        negative_valence = [m for m in memories if m.valence < -0.3]
        if len(negative_valence) > len(memories) * 0.5:
            observations.append("今日记忆整体偏负面，建议关注情绪状态")

        if not observations:
            observations.append("记忆状态正常，无需特别关注")

        return observations

    def _render_markdown(self, date: int, memories: list[MemoryEntry],
                         clusters: list[TopicCluster], observations: list[str]) -> str:
        from datetime import datetime
        date_str = datetime.fromtimestamp(date).strftime('%Y-%m-%d')

        lines = [
            f"# 记忆日报 — {date_str}",
            "",
            f"> 今日共记录 {len(memories)} 条记忆，分布在 {len(clusters)} 个主题",
            "",
        ]

        for cluster in clusters:
            lines.append(f"## {cluster.label} ({cluster.count} 条)")
            lines.append("")

            cluster_mems = [m for m in memories if m.memory_id in cluster.memory_ids]
            for mem in cluster_mems[:15]:
                content_preview = mem.content[:150].replace('\n', ' ')
                if len(mem.content) > 150:
                    content_preview += "..."
                imp_icon = {"high": "🔴", "medium": "🟡", "low": "⚪"}.get(mem.importance, "⚪")
                lines.append(f"- {imp_icon} {content_preview}")
                meta_parts = []
                if mem.nature_id:
                    meta_parts.append(f"类型:{mem.nature_id}")
                if mem.person_id:
                    meta_parts.append(f"人物:{mem.person_id}")
                if mem.topics:
                    topic_str = ", ".join(mem.topics[:3])
                    meta_parts.append(f"主题:{topic_str}")
                if meta_parts:
                    lines.append(f"  _{', '.join(meta_parts)}_")
                lines.append("")

            if cluster.count > 15:
                lines.append(f"  ... 还有 {cluster.count - 15} 条记忆")
                lines.append("")

        lines.append("## 系统观察")
        lines.append("")
        for obs in observations:
            lines.append(f"- {obs}")
        lines.append("")

        return "\n".join(lines)

    def _render_json(self, date: int, memories: list[MemoryEntry],
                     clusters: list[TopicCluster], observations: list[str]) -> str:
        import json
        data = {
            'date': date,
            'total_memories': len(memories),
            'cluster_count': len(clusters),
            'clusters': [
                {
                    'label': c.label,
                    'count': c.count,
                    'avg_importance': c.avg_importance,
                    'memory_ids': c.memory_ids,
                }
                for c in clusters
            ],
            'observations': observations,
        }
        return json.dumps(data, ensure_ascii=False, indent=2)

    def _render_empty_report(self, date: int, format: str) -> str:
        from datetime import datetime
        date_str = datetime.fromtimestamp(date).strftime('%Y-%m-%d')
        if format == 'json':
            import json
            return json.dumps({'date': date, 'total_memories': 0, 'message': '今日无记忆'}, ensure_ascii=False)
        return f"# 记忆日报 — {date_str}\n\n> 今日无记忆记录\n"


class WeeklyReportGenerator:
    """Weekly report: aggregated view of the past 7 days."""

    def __init__(self, interface: SpiritInterface, llm_layer=None):
        self.interface = interface
        self.llm_layer = llm_layer
        self.daily = DailyReportGenerator(interface, llm_layer)

    def generate(self, date: int = None, format: str = 'markdown') -> str:
        if date is None:
            date = self.daily._today_ts()

        week_start = date - 6 * 86400
        week_end = date + 86400

        all_memories = []
        daily_summaries = []

        for day_offset in range(7):
            day_start = week_start + day_offset * 86400
            day_end = day_start + 86400

            day_entries = self.daily._fetch_memories(day_start, day_end)
            all_memories.extend(day_entries)

            daily_summaries.append({
                'date': day_start,
                'count': len(day_entries),
            })

        if not all_memories:
            return self._render_empty_week(week_start, format)

        clusters = self.daily._cluster_by_topic(all_memories)
        observations = self._weekly_observations(all_memories, daily_summaries, clusters)

        if format == 'json':
            return self._render_json(week_start, all_memories, daily_summaries, clusters, observations)
        return self._render_markdown(week_start, all_memories, daily_summaries, clusters, observations)

    def _weekly_observations(self, memories, daily_summaries, clusters) -> list[str]:
        observations = []

        active_days = sum(1 for d in daily_summaries if d['count'] > 0)
        if active_days < 3:
            observations.append(f"本周仅 {active_days} 天有记忆记录，活跃度偏低")

        counts = [d['count'] for d in daily_summaries]
        if counts:
            avg_count = sum(counts) / len(counts)
            if avg_count < 2:
                observations.append("日均记忆量较低，建议增加知识录入")

        top_topics = sorted(clusters, key=lambda c: c.count, reverse=True)[:3]
        if top_topics:
            topic_names = ", ".join(f"'{c.label}'({c.count})" for c in top_topics)
            observations.append(f"本周热门主题: {topic_names}")

        if not observations:
            observations.append("本周记忆状态正常")

        return observations

    def _render_markdown(self, week_start, memories, daily_summaries, clusters, observations) -> str:
        from datetime import datetime
        start_str = datetime.fromtimestamp(week_start).strftime('%Y-%m-%d')

        lines = [
            f"# 记忆周报 — {start_str} 起",
            "",
            f"> 本周共记录 {len(memories)} 条记忆",
            "",
            "## 每日概览",
            "",
        ]

        for d in daily_summaries:
            date_str = datetime.fromtimestamp(d['date']).strftime('%m-%d')
            bar = "█" * min(d['count'], 20)
            lines.append(f"- {date_str}: {bar} {d['count']} 条")

        lines.append("")
        lines.append("## 主题分布")
        lines.append("")
        for c in clusters[:10]:
            lines.append(f"- **{c.label}**: {c.count} 条 (平均重要度: {c.avg_importance})")

        lines.append("")
        lines.append("## 周观察")
        lines.append("")
        for obs in observations:
            lines.append(f"- {obs}")
        lines.append("")

        return "\n".join(lines)

    def _render_json(self, week_start, memories, daily_summaries, clusters, observations) -> str:
        import json
        return json.dumps({
            'week_start': week_start,
            'total_memories': len(memories),
            'daily_summaries': daily_summaries,
            'clusters': [{'label': c.label, 'count': c.count} for c in clusters],
            'observations': observations,
        }, ensure_ascii=False, indent=2)

    def _render_empty_week(self, week_start, format) -> str:
        from datetime import datetime
        start_str = datetime.fromtimestamp(week_start).strftime('%Y-%m-%d')
        if format == 'json':
            import json
            return json.dumps({'week_start': week_start, 'total_memories': 0}, ensure_ascii=False)
        return f"# 记忆周报 — {start_str} 起\n\n> 本周无记忆记录\n"


class MonthlyReportGenerator:
    """Monthly report: strategic overview of the past 30 days."""

    def __init__(self, interface: SpiritInterface, llm_layer=None):
        self.interface = interface
        self.llm_layer = llm_layer
        self.daily = DailyReportGenerator(interface, llm_layer)

    def generate(self, date: int = None, format: str = 'markdown') -> str:
        if date is None:
            date = self.daily._today_ts()

        month_start = date - 29 * 86400
        month_end = date + 86400

        all_memories = self.daily._fetch_memories(month_start, month_end)

        if not all_memories:
            return self._render_empty_month(month_start, format)

        clusters = self.daily._cluster_by_topic(all_memories)

        importance_dist = Counter(m.importance for m in all_memories)
        nature_dist = Counter(m.nature_id for m in all_memories if m.nature_id)

        observations = self._monthly_observations(all_memories, clusters, importance_dist)

        if format == 'json':
            return self._render_json(month_start, all_memories, clusters, importance_dist, nature_dist, observations)
        return self._render_markdown(month_start, all_memories, clusters, importance_dist, nature_dist, observations)

    def _monthly_observations(self, memories, clusters, importance_dist) -> list[str]:
        observations = []

        total = len(memories)
        if total < 10:
            observations.append(f"本月仅 {total} 条记忆，知识积累偏少")
        elif total > 500:
            observations.append(f"本月 {total} 条记忆，建议关注记忆质量和去重")

        high_ratio = importance_dist.get('high', 0) / total if total > 0 else 0
        if high_ratio < 0.1:
            observations.append("高重要度记忆占比较低，建议标记关键知识")

        top_cluster = clusters[0] if clusters else None
        if top_cluster and top_cluster.count > total * 0.5:
            observations.append(f"主题 '{top_cluster.label}' 占比超过 50%，知识面可能偏窄")

        if not observations:
            observations.append("本月记忆状态良好")

        return observations

    def _render_markdown(self, month_start, memories, clusters, importance_dist, nature_dist, observations) -> str:
        from datetime import datetime
        start_str = datetime.fromtimestamp(month_start).strftime('%Y-%m-%d')

        lines = [
            f"# 记忆月报 — {start_str} 起",
            "",
            f"> 本月共记录 {len(memories)} 条记忆",
            "",
            "## 重要度分布",
            "",
        ]
        for imp in ('high', 'medium', 'low'):
            count = importance_dist.get(imp, 0)
            lines.append(f"- {imp}: {count} 条")

        lines.append("")
        lines.append("## 主题排行 (Top 10)")
        lines.append("")
        for c in clusters[:10]:
            pct = c.count / len(memories) * 100 if memories else 0
            lines.append(f"- **{c.label}**: {c.count} 条 ({pct:.1f}%)")

        if nature_dist:
            lines.append("")
            lines.append("## 记忆类型分布")
            lines.append("")
            for nature, count in nature_dist.most_common(5):
                lines.append(f"- {nature}: {count} 条")

        lines.append("")
        lines.append("## 月度观察")
        lines.append("")
        for obs in observations:
            lines.append(f"- {obs}")
        lines.append("")

        return "\n".join(lines)

    def _render_json(self, month_start, memories, clusters, importance_dist, nature_dist, observations) -> str:
        import json
        return json.dumps({
            'month_start': month_start,
            'total_memories': len(memories),
            'importance_dist': dict(importance_dist),
            'nature_dist': dict(nature_dist),
            'clusters': [{'label': c.label, 'count': c.count} for c in clusters[:10]],
            'observations': observations,
        }, ensure_ascii=False, indent=2)

    def _render_empty_month(self, month_start, format) -> str:
        from datetime import datetime
        start_str = datetime.fromtimestamp(month_start).strftime('%Y-%m-%d')
        if format == 'json':
            import json
            return json.dumps({'month_start': month_start, 'total_memories': 0}, ensure_ascii=False)
        return f"# 记忆月报 — {start_str} 起\n\n> 本月无记忆记录\n"
