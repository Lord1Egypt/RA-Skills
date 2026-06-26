"""
memory_graph.py - 记忆图谱生成器
将记忆、主题、因果关系可视化为图谱
"""

from __future__ import annotations

import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class MemoryGraph:
    """
    生成记忆关系图谱数据，支持多种输出格式：
    1. Mermaid 图表 — 可嵌入 Markdown
    2. DOT 格式 — Graphviz 渲染
    3. JSON 节点-边格式 — 前端 D3.js / Cytoscape.js 渲染
    4. ASCII 树 — 终端可视化
    """

    def __init__(self, store, topic_registry=None):
        self.store = store
        self.topic_registry = topic_registry

    def generate(
        self,
        center_topic: str = None,
        center_memory_id: str = None,
        depth: int = 2,
        max_nodes: int = 50,
        format: str = "mermaid",
    ) -> str:
        """
        生成记忆图谱。

        参数:
            center_topic: 以某个主题为中心
            center_memory_id: 以某条记忆为中心
            depth: 展开深度
            max_nodes: 最大节点数
            format: 输出格式 mermaid / dot / json / ascii

        返回: 图谱文本
        """
        nodes, edges = self._build_graph(center_topic, center_memory_id, depth, max_nodes)

        if format == "mermaid":
            return self._to_mermaid(nodes, edges)
        elif format == "dot":
            return self._to_dot(nodes, edges)
        elif format == "json":
            return self._to_json(nodes, edges)
        elif format == "ascii":
            return self._to_ascii(nodes, edges, center_topic or center_memory_id)
        else:
            return self._to_mermaid(nodes, edges)

    def _build_graph(self, center_topic, center_memory_id, depth, max_nodes) -> tuple[list, list]:
        """构建图谱数据"""
        nodes = []
        edges = []
        node_ids = set()

        if center_memory_id:
            # 以记忆为中心
            center = self.store.get_memory(center_memory_id)
            if center:
                nodes.append(self._memory_to_node(center, is_center=True))
                node_ids.add(center_memory_id)
                self._expand_from_memory(center_memory_id, depth, max_nodes, nodes, edges, node_ids)

        elif center_topic:
            # 以主题为中心
            memories = self.store.query(topic_code=center_topic, limit=max_nodes)
            for mem in memories:
                if mem["memory_id"] not in node_ids:
                    nodes.append(self._memory_to_node(mem))
                    node_ids.add(mem["memory_id"])

            # 找关联边
            for mem in memories:
                links = self.store.conn.execute(
                    "SELECT * FROM memory_links WHERE source_id = ? OR target_id = ?",
                    (mem["memory_id"], mem["memory_id"]),
                ).fetchall()
                for link in links:
                    edges.append(self._link_to_edge(link))

        else:
            # 全局视图：按主题聚合
            memories = self.store.query(limit=max_nodes)

            # 主题节点
            topic_nodes = {}
            for mem in memories:
                for t in mem.get("topics", []):
                    code = t.get("code", "") if isinstance(t, dict) else t
                    if code and code not in topic_nodes:
                        top = code.split(".")[0]
                        topic_nodes[code] = {
                            "id": f"topic:{code}",
                            "label": code,
                            "type": "topic",
                            "level": top,
                        }

            nodes.extend(topic_nodes.values())

            # 记忆节点 + 边
            for mem in memories[:max_nodes]:
                node = self._memory_to_node(mem)
                nodes.append(node)

                # 记忆 → 主题 边
                for t in mem.get("topics", []):
                    code = t.get("code", "") if isinstance(t, dict) else t
                    if code:
                        edges.append({
                            "source": mem["memory_id"],
                            "target": f"topic:{code}",
                            "type": "belongs_to",
                            "weight": 1.0,
                        })

                # 记忆间关联边
                for link in mem.get("links", []):
                    edges.append({
                        "source": link["source_id"],
                        "target": link["target_id"],
                        "type": link["link_type"],
                        "weight": link.get("weight", 1.0),
                    })

        return nodes, edges

    def _expand_from_memory(self, memory_id, depth, max_nodes, nodes, edges, node_ids):
        """从一条记忆展开关联"""
        if depth <= 0 or len(nodes) >= max_nodes:
            return

        links = self.store.conn.execute(
            "SELECT * FROM memory_links WHERE source_id = ? OR target_id = ?",
            (memory_id, memory_id),
        ).fetchall()

        for link in links:
            other_id = link["target_id"] if link["source_id"] == memory_id else link["source_id"]

            if other_id not in node_ids and len(nodes) < max_nodes:
                mem = self.store.get_memory(other_id)
                if mem:
                    nodes.append(self._memory_to_node(mem))
                    node_ids.add(other_id)
                    self._expand_from_memory(other_id, depth - 1, max_nodes, nodes, edges, node_ids)

            edges.append(self._link_to_edge(link))

    def _memory_to_node(self, mem: dict, is_center: bool = False) -> dict:
        """记忆 → 节点"""
        content = mem.get("content", "")
        topics = mem.get("topics", [])
        topic_str = ",".join(
            t.get("code", "") if isinstance(t, dict) else t for t in topics[:2]
        )

        return {
            "id": mem["memory_id"],
            "label": content[:30] + ("..." if len(content) > 30 else ""),
            "type": "memory",
            "importance": mem.get("importance", "medium"),
            "nature": mem.get("nature_id", ""),
            "topic": topic_str,
            "is_center": is_center,
            "time": self._format_time(mem.get("time_ts", 0)),
        }

    def _link_to_edge(self, link) -> dict:
        """关联 → 边"""
        if hasattr(link, 'keys'):
            link = dict(link)
        return {
            "source": link["source_id"],
            "target": link["target_id"],
            "type": link["link_type"],
            "weight": link.get("weight", 1.0) if isinstance(link, dict) else 1.0,
        }

    # ── Mermaid 输出 ────────────────────────────────────

    def _to_mermaid(self, nodes: list, edges: list) -> str:
        lines = ["graph LR"]

        for node in nodes:
            nid = self._mermaid_id(node["id"])
            label = node["label"].replace('"', "'")

            if node["type"] == "topic":
                lines.append(f'    {nid}["🏷️ {label}"]')
            elif node.get("is_center"):
                lines.append(f'    {nid}["🎯 {label}"]')
            elif node.get("importance") == "high":
                lines.append(f'    {nid}["⚡ {label}"]')
            else:
                lines.append(f'    {nid}["📝 {label}"]')

        for edge in edges:
            src = self._mermaid_id(edge["source"])
            tgt = self._mermaid_id(edge["target"])
            etype = edge["type"]

            if "causal" in etype or etype == "decision_based_on":
                lines.append(f"    {src} ==>|{etype}| {tgt}")
            elif etype == "contradicts":
                lines.append(f"    {src} -.-x {tgt}")
            elif etype == "temporal":
                lines.append(f"    {src} --> {tgt}")
            else:
                lines.append(f"    {src} -->|{etype}| {tgt}")

        return "\n".join(lines)

    def _mermaid_id(self, raw_id: str) -> str:
        return "n" + raw_id.replace(".", "_").replace(":", "_")[:20]

    # ── DOT 输出 ────────────────────────────────────────

    def _to_dot(self, nodes: list, edges: list) -> str:
        lines = ['digraph MemoryGraph {', '    rankdir=LR;', '    node [shape=box, fontsize=10];']

        for node in nodes:
            nid = node["id"].replace(".", "_").replace(":", "_")
            label = node["label"].replace('"', '\\"')
            color = {"high": "red", "medium": "orange", "low": "gray"}.get(node.get("importance"), "lightblue")

            if node["type"] == "topic":
                lines.append(f'    "{nid}" [label="🏷️ {label}", shape=ellipse, color=blue];')
            else:
                lines.append(f'    "{nid}" [label="{label}", color={color}];')

        for edge in edges:
            src = edge["source"].replace(".", "_").replace(":", "_")
            tgt = edge["target"].replace(".", "_").replace(":", "_")
            etype = edge["type"]
            style = "bold" if "causal" in etype else "dashed" if etype == "contradicts" else "solid"
            lines.append(f'    "{src}" -> "{tgt}" [label="{etype}", style={style}];')

        lines.append("}")
        return "\n".join(lines)

    # ── JSON 输出 ───────────────────────────────────────

    def _to_json(self, nodes: list, edges: list) -> str:
        return json.dumps({"nodes": nodes, "edges": edges}, ensure_ascii=False, indent=2)

    # ── ASCII 树输出 ────────────────────────────────────

    def _to_ascii(self, nodes: list, edges: list, center: str = None) -> str:
        """ASCII 树形可视化"""
        lines = []

        # 按类型分组
        topics = [n for n in nodes if n["type"] == "topic"]
        memories = [n for n in nodes if n["type"] == "memory"]

        # 高优先
        high = [m for m in memories if m.get("importance") == "high"]
        normal = [m for m in memories if m.get("importance") != "high"]

        if center:
            lines.append(f"🎯 中心: {center}")
            lines.append("")

        if topics:
            lines.append("🏷️ 主题:")
            for t in topics[:10]:
                lines.append(f"  ├─ {t['label']}")
            lines.append("")

        if high:
            lines.append("⚡ 高优先记忆:")
            for m in high[:10]:
                lines.append(f"  ├─ [{m.get('time', '?')}] {m['label']}")
            lines.append("")

        if normal:
            lines.append("📝 普通记忆:")
            for m in normal[:15]:
                lines.append(f"  ├─ [{m.get('time', '?')}] {m['label']}")
            lines.append("")

        if edges:
            lines.append(f"🔗 关联: {len(edges)} 条")
            type_counts = {}
            for e in edges:
                t = e["type"]
                type_counts[t] = type_counts.get(t, 0) + 1
            for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
                lines.append(f"  ├─ {t}: {c}")

        return "\n".join(lines) if lines else "（空图谱）"

    @staticmethod
    def _format_time(ts: int) -> str:
        if not ts:
            return "?"
        dt = datetime.fromtimestamp(ts)
        now = datetime.now()
        if dt.date() == now.date():
            return dt.strftime("%H:%M")
        return dt.strftime("%m-%d")

    def generate_full_report(self) -> str:
        """生成完整的记忆图谱报告"""
        stats = self.store.conn.execute(
            "SELECT COUNT(*) as cnt FROM memories"
        ).fetchone()
        mem_count = stats["cnt"] if stats else 0

        link_stats = self.store.conn.execute(
            "SELECT link_type, COUNT(*) as cnt FROM memory_links GROUP BY link_type"
        ).fetchall()

        topic_stats = self.store.conn.execute(
            "SELECT topic_code, COUNT(*) as cnt FROM memory_topics GROUP BY topic_code ORDER BY cnt DESC LIMIT 10"
        ).fetchall()

        lines = [
            "# 🗺️ 记忆图谱报告",
            "",
            f"**总记忆数**: {mem_count}",
            f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## 关联类型分布",
            "",
        ]
        for r in link_stats:
            lines.append(f"- {r['link_type']}: {r['cnt']}")

        lines.extend(["", "## Top 主题", ""])
        for r in topic_stats:
            bar = "█" * min(r["cnt"], 20)
            lines.append(f"- {r['topic_code']}: {r['cnt']} {bar}")

        # ASCII 图谱
        lines.extend(["", "## 图谱", ""])
        ascii_graph = self.generate(format="ascii")
        lines.append(f"```\n{ascii_graph}\n```")

        return "\n".join(lines)
