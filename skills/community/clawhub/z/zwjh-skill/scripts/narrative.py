# -*- coding: utf-8 -*-
"""
时间线叙事生成 —— 把分散的记忆组织成连贯的叙事。

功能：
  - 项目进展时间线：从立项到当前的关键节点
  - 人脉交互历史：与某人的所有互动时间线
  - 知识成长轨迹：对某个主题的认知变化
  - 周期性回顾：每周/每月自动生成的记忆回顾报告

所有叙事生成使用 LLM（基于记忆数据构建 prompt），支持可插拔 LLM 适配器。
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable

from . import config, store, graph


# ── LLM 适配器（可插拔） ────────────────────────────────────────────────
class LLMAdapter:
    """LLM 适配器接口。"""

    def generate(self, prompt: str) -> str:
        """给定 prompt，返回生成的文本。"""
        raise NotImplementedError


class DefaultLLMAdapter(LLMAdapter):
    """
    默认 LLM 适配器（占位实现）。
    用户可替换为实际的 LLM 客户端（OpenAI / Claude / 本地模型等）。
    """

    def generate(self, prompt: str) -> str:
        # 返回一个占位响应，表示 LLM 未配置
        return (
            "⚠️ LLM 未配置。请在 config.json 中配置 llm.provider 和 llm.api_key，"
            "或调用 set_llm_adapter() 注册自定义适配器。\n\n"
            f"原始 prompt 长度：{len(prompt)} 字符"
        )


# ── 全局 LLM 适配器 ──────────────────────────────────────────────────────
_llm_adapter: LLMAdapter = DefaultLLMAdapter()


def set_llm_adapter(adapter: LLMAdapter) -> None:
    """注册全局 LLM 适配器。"""
    global _llm_adapter
    _llm_adapter = adapter


def get_llm_adapter() -> LLMAdapter:
    """获取当前 LLM 适配器。"""
    return _llm_adapter


# ── 叙事生成器 ────────────────────────────────────────────────────────────
@dataclass
class TimelineEvent:
    """时间线事件。"""
    date: str
    type: str       # memory / fact / relation
    content: str
    source: str = ""


class NarrativeGenerator:
    """叙事生成器。"""

    def __init__(self, llm_adapter: LLMAdapter | None = None):
        self.llm = llm_adapter or get_llm_adapter()

    # ── 项目进展时间线 ─────────────────────────────────────────────────
    def project_timeline(self, project_name: str) -> str:
        """生成项目进展时间线。"""
        # 找到项目实体
        conn = store.get_conn()
        row = conn.execute(
            "SELECT * FROM entities WHERE type='project' AND name LIKE ?",
            (f"%{project_name}%",)
        ).fetchone()
        if not row:
            return f"未找到项目「{project_name}」"

        project = dict(row)
        project_id = project["id"]

        # 收集相关记忆
        related_memories = self._find_related_memories(project_name, project_id)

        # 收集相关事实和关系
        facts = store.current_facts(project_id)
        relations = store.relations_of(project_id, direction="both")

        # 构建 prompt
        prompt = self._build_prompt(
            title=f"项目「{project_name}」进展时间线",
            context=f"以下是关于项目 {project_name} 的记忆数据：",
            data={
                "project": project,
                "memories": related_memories,
                "facts": facts,
                "relations": relations,
            },
            instruction="请根据以上数据，按时间顺序组织成项目进展时间线。"
                       "包括：立项、关键节点、当前状态、下一步计划。"
                       "用简洁的中文叙述，标注日期。"
        )

        return self.llm.generate(prompt)

    # ── 人脉交互历史 ───────────────────────────────────────────────────
    def person_interaction(self, person_name: str) -> str:
        """生成人脉交互时间线。"""
        conn = store.get_conn()
        row = conn.execute(
            "SELECT * FROM entities WHERE type='person' AND name LIKE ?",
            (f"%{person_name}%",)
        ).fetchone()
        if not row:
            return f"未找到人物「{person_name}」"

        person = dict(row)
        person_id = person["id"]

        # 收集相关记忆
        related_memories = self._find_related_memories(person_name, person_id)

        # 收集关系和事实
        facts = store.current_facts(person_id)
        relations = store.relations_of(person_id, direction="both")

        prompt = self._build_prompt(
            title=f"与「{person_name}」的交互时间线",
            context=f"以下是与 {person_name} 相关的记忆数据：",
            data={
                "person": person,
                "memories": related_memories,
                "facts": facts,
                "relations": relations,
            },
            instruction="请根据以上数据，按时间顺序组织成人脉交互时间线。"
                       "包括：初次认识、关键互动、关系变化、最近联系。"
                       "用简洁的中文叙述，标注日期。"
        )

        return self.llm.generate(prompt)

    # ── 知识成长轨迹 ─────────────────────────────────────────────────
    def knowledge_growth(self, topic: str) -> str:
        """生成知识成长轨迹。"""
        # 搜索相关记忆
        conn = store.get_conn()
        rows = conn.execute(
            "SELECT * FROM memories WHERE raw_text LIKE ? ORDER BY day",
            (f"%{topic}%",)
        ).fetchall()
        related_memories = [dict(r) for r in rows]

        # 查找相关实体
        entities = conn.execute(
            "SELECT * FROM entities WHERE name LIKE ? OR type LIKE ?",
            (f"%{topic}%", f"%{topic}%")
        ).fetchall()
        entities = [dict(e) for e in entities]

        prompt = self._build_prompt(
            title=f"「{topic}」知识成长轨迹",
            context=f"以下是与 {topic} 相关的记忆数据：",
            data={
                "memories": related_memories,
                "entities": entities,
            },
            instruction="请根据以上数据，按时间顺序组织成知识成长轨迹。"
                       "包括：入门阶段、深入学习、实践应用、当前理解。"
                       "用简洁的中文叙述，标注日期。"
        )

        return self.llm.generate(prompt)

    # ── 周期性回顾 ────────────────────────────────────────────────────
    def weekly_review(self) -> str:
        """生成本周回顾报告。"""
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        return self._generate_periodic_review(
            "本周回顾",
            week_ago.strftime("%Y-%m-%d"),
            today.strftime("%Y-%m-%d")
        )

    def monthly_review(self) -> str:
        """生成本月回顾报告。"""
        today = datetime.now()
        month_ago = today - timedelta(days=30)
        return self._generate_periodic_review(
            "本月回顾",
            month_ago.strftime("%Y-%m-%d"),
            today.strftime("%Y-%m-%d")
        )

    def _generate_periodic_review(self, title: str, day_from: str, day_to: str) -> str:
        """生成周期性回顾报告。"""
        conn = store.get_conn()

        # 统计
        mem_count = conn.execute(
            "SELECT COUNT(*) FROM memories WHERE day >= ? AND day <= ?",
            (day_from, day_to)
        ).fetchone()[0]

        entity_count = conn.execute(
            "SELECT COUNT(*) FROM entities"
        ).fetchone()[0]

        relation_count = conn.execute(
            "SELECT COUNT(*) FROM relations"
        ).fetchone()[0]

        # 新增实体
        new_entities = conn.execute(
            "SELECT * FROM entities WHERE created_at >= ? AND created_at <= ? ORDER BY importance DESC LIMIT 10",
            (day_from, day_to)
        ).fetchall()
        new_entities = [dict(e) for e in new_entities]

        # 新增记忆
        new_memories = conn.execute(
            "SELECT * FROM memories WHERE day >= ? AND day <= ? ORDER BY importance DESC LIMIT 20",
            (day_from, day_to)
        ).fetchall()
        new_memories = [dict(m) for m in new_memories]

        prompt = self._build_prompt(
            title=title,
            context=f"以下是 {day_from} 到 {day_to} 期间的统计数据：",
            data={
                "statistics": {
                    "memories_added": mem_count,
                    "entities_total": entity_count,
                    "relations_total": relation_count,
                },
                "new_entities": new_entities,
                "new_memories": new_memories,
            },
            instruction=f"请根据以上数据，生成{title}报告。"
                       f"包括：关键数据概览、新增重要实体、新增记忆摘要、趋势分析。"
                       f"用简洁的中文叙述。"
        )

        return self.llm.generate(prompt)

    # ── 辅助方法 ─────────────────────────────────────────────────────
    def _find_related_memories(self, name: str, entity_id: int) -> list[dict]:
        """查找与实体相关的记忆（通过 mention 和直接匹配）。"""
        conn = store.get_conn()

        # 通过 mention 查找
        rows = conn.execute(
            "SELECT m.* FROM memories m JOIN facts f ON f.source_memory_id = m.id "
            "WHERE f.entity_id = ? ORDER BY m.day LIMIT 20",
            (entity_id,)
        ).fetchall()
        if rows:
            return [dict(r) for r in rows]

        # 回退：直接文本匹配
        rows = conn.execute(
            "SELECT * FROM memories WHERE raw_text LIKE ? ORDER BY day LIMIT 20",
            (f"%{name}%",)
        ).fetchall()
        return [dict(r) for r in rows]

    def _build_prompt(self, title: str, context: str, data: dict,
                      instruction: str) -> str:
        """构建 LLM prompt。"""
        data_json = json.dumps(data, ensure_ascii=False, default=str, indent=2)
        return f"""# {title}

{context}

```json
{data_json}
```

{instruction}
"""


# ── 便捷函数 ──────────────────────────────────────────────────────────────
def generate_project_timeline(project_name: str) -> str:
    """生成项目进展时间线。"""
    gen = NarrativeGenerator()
    return gen.project_timeline(project_name)


def generate_person_interaction(person_name: str) -> str:
    """生成人脉交互时间线。"""
    gen = NarrativeGenerator()
    return gen.person_interaction(person_name)


def generate_knowledge_growth(topic: str) -> str:
    """生成知识成长轨迹。"""
    gen = NarrativeGenerator()
    return gen.knowledge_growth(topic)


def generate_weekly_review() -> str:
    """生成本周回顾报告。"""
    gen = NarrativeGenerator()
    return gen.weekly_review()


def generate_monthly_review() -> str:
    """生成本月回顾报告。"""
    gen = NarrativeGenerator()
    return gen.monthly_review()


if __name__ == "__main__":
    print("=== 项目时间线示例 ===")
    print(generate_project_timeline("机器学习"))
    print("\n=== 人脉交互示例 ===")
    print(generate_person_interaction("张三"))
