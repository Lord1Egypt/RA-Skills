"""
distill.py - 记忆蒸馏系统
将对话碎片逐层抽象为结构化知识

管道（在智能归档之后触发）:
    原始记忆（1000条对话碎片）
     ↓ _distill_topics() — 聚类 + 摘要
    主题记忆（50个主题摘要）
     ↓ _distill_entities() — 实体/关系/属性提取
    知识图谱（实体 + 关系 + 属性）
     ↓ _distill_encyclopedia() — 再压缩为结构化文档
    个人百科（结构化文档）
"""

from __future__ import annotations

import os
import re
import json
import time
import hashlib
import logging
import sqlite3
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)

_VALID_IDENTIFIER = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')

from .store import _chunked_placeholders, SQLITE_MAX_VARIABLES


# ═══════════════════════════════════════════════════════════
# 蒸馏数据库 Schema（独立表，不污染主 schema）
# ═══════════════════════════════════════════════════════════
DISTILL_SCHEMA = """
-- 主题摘要层
CREATE TABLE IF NOT EXISTS distill_topics (
    topic_id        TEXT PRIMARY KEY,
    topic_code      TEXT NOT NULL,
    summary         TEXT NOT NULL,           -- 摘要全文
    source_count    INTEGER DEFAULT 0,       -- 聚合了多少条原始记忆
    source_ids      TEXT DEFAULT '[]',       -- JSON: 原始 memory_id 列表
    importance      TEXT DEFAULT 'medium',
    time_range_start INTEGER,               -- 覆盖的时间范围
    time_range_end   INTEGER,
    version         INTEGER DEFAULT 1,      -- 版本号（每次重新蒸馏递增）
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- 知识实体
CREATE TABLE IF NOT EXISTS distill_entities (
    entity_id       TEXT PRIMARY KEY,
    name            TEXT NOT NULL,            -- 实体名
    entity_type     TEXT NOT NULL,            -- person / concept / tool / project / decision / fact
    attributes      TEXT DEFAULT '{}',        -- JSON: 属性键值对
    source_topics   TEXT DEFAULT '[]',        -- JSON: 来自哪些 topic_id
    importance      TEXT DEFAULT 'medium',
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- 知识关系
CREATE TABLE IF NOT EXISTS distill_relations (
    relation_id     TEXT PRIMARY KEY,
    source_entity   TEXT NOT NULL,
    target_entity   TEXT NOT NULL,
    relation_type   TEXT NOT NULL,            -- uses / depends_on / contradicts / part_of / decided_by / evolved_to
    attributes      TEXT DEFAULT '{}',        -- JSON: 关系属性
    source_topics   TEXT DEFAULT '[]',        -- JSON
    confidence      REAL DEFAULT 0.8,
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    FOREIGN KEY (source_entity) REFERENCES distill_entities(entity_id),
    FOREIGN KEY (target_entity) REFERENCES distill_entities(entity_id)
);

-- 个人百科条目
CREATE TABLE IF NOT EXISTS distill_encyclopedia (
    entry_id        TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    content         TEXT NOT NULL,            -- 结构化 Markdown
    category        TEXT DEFAULT 'general',   -- decisions / tools / projects / concepts / people / facts
    source_entities TEXT DEFAULT '[]',        -- JSON: 来自哪些 entity_id
    source_topics   TEXT DEFAULT '[]',        -- JSON: 来自哪些 topic_id
    last_updated    INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    created_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- 蒸馏状态追踪
CREATE TABLE IF NOT EXISTS distill_state (
    key             TEXT PRIMARY KEY,
    value           TEXT,
    updated_at      INTEGER NOT NULL DEFAULT (strftime('%s','now'))
);

-- 蒸馏批次追踪（v8.2 安全：支持回滚）
CREATE TABLE IF NOT EXISTS distill_batches (
    batch_id        TEXT PRIMARY KEY,
    started_at      INTEGER NOT NULL,
    completed_at    INTEGER,
    topic_ids       TEXT DEFAULT '[]',       -- JSON: 本次蒸馏创建的 topic_id 列表
    entity_ids      TEXT DEFAULT '[]',       -- JSON: 本次蒸馏创建的 entity_id 列表
    relation_ids    TEXT DEFAULT '[]',       -- JSON: 本次蒸馏创建的 relation_id 列表
    entry_ids       TEXT DEFAULT '[]',       -- JSON: 本次蒸馏创建的 encyclopedia entry_id 列表
    source_count    INTEGER DEFAULT 0,       -- 消耗的原始记忆数
    status          TEXT DEFAULT 'completed' -- completed / rolled_back
);

-- 低置信度隔离标记（v8.2 安全：防止低质量记忆级联污染）
CREATE TABLE IF NOT EXISTS distill_quarantine (
    item_id         TEXT PRIMARY KEY,
    item_type       TEXT NOT NULL,           -- topic / entity / relation / entry
    confidence      REAL DEFAULT 0.0,
    reason          TEXT DEFAULT '',         -- 隔离原因
    quarantined_at  INTEGER NOT NULL DEFAULT (strftime('%s','now')),
    released_at     INTEGER                  -- 释放时间（审核通过后设置）
);

CREATE INDEX IF NOT EXISTS idx_distill_topic_code ON distill_topics(topic_code);
CREATE INDEX IF NOT EXISTS idx_distill_entity_type ON distill_entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_distill_entity_name ON distill_entities(name);
CREATE INDEX IF NOT EXISTS idx_distill_rel_source ON distill_relations(source_entity);
CREATE INDEX IF NOT EXISTS idx_distill_rel_target ON distill_relations(target_entity);
CREATE INDEX IF NOT EXISTS idx_distill_rel_type ON distill_relations(relation_type);
CREATE INDEX IF NOT EXISTS idx_distill_enc_cat ON distill_encyclopedia(category);
"""


class MemoryDistiller:
    """
    记忆蒸馏器。

    将原始对话记忆逐层抽象：
    L1 Raw → L2 Topics → L3 Entities → L4 Encyclopedia

    设计原则：
    - 蒸馏在智能归档之后触发（不在写入管道中阻塞）
    - 支持增量蒸馏（只处理新写入的记忆）
    - LLM 辅助但不强依赖（无 LLM 时用启发式 fallback）
    - 每层独立可查、可回溯到原始记忆
    """

    # 实体类型
    ENTITY_TYPES = {
        "person":    {"icon": "👤", "desc": "人物"},
        "concept":   {"icon": "💡", "desc": "概念/想法"},
        "tool":      {"icon": "🔧", "desc": "工具/技术"},
        "project":   {"icon": "📂", "desc": "项目"},
        "decision":  {"icon": "🎯", "desc": "决策"},
        "fact":      {"icon": "📌", "desc": "事实"},
        "preference":{"icon": "⭐", "desc": "偏好"},
    }

    # 关系类型
    RELATION_TYPES = {
        "uses":          {"weight": 0.8, "desc": "使用"},
        "depends_on":    {"weight": 0.9, "desc": "依赖"},
        "contradicts":   {"weight": 0.3, "desc": "矛盾"},
        "part_of":       {"weight": 0.7, "desc": "属于"},
        "decided_by":    {"weight": 0.9, "desc": "由…决定"},
        "evolved_to":    {"weight": 0.6, "desc": "演变为"},
        "related_to":    {"weight": 0.5, "desc": "相关"},
        "caused_by":     {"weight": 0.8, "desc": "由…导致"},
    }

    # 蒸馏触发阈值
    MIN_MEMORIES_FOR_DISTILL = 5      # 至少 N 条新记忆才触发蒸馏
    TOPIC_BATCH_SIZE = 20              # 每次蒸馏最多处理的主题数
    MAX_CONTENT_PREVIEW = 800          # 输入给 LLM 的每条记忆最大长度

    def __init__(self, store, encoder=None, llm_fn=None, embedding_store=None):
        """
        参数:
            store: MemoryStore 实例
            encoder: DimensionEncoder 实例
            llm_fn: LLM 函数 fn(prompt) -> str，None 则用启发式
            embedding_store: EmbeddingStore 可选，用于语义聚类
        """
        self.store = store
        self.encoder = encoder
        self.llm_fn = llm_fn
        self.embedding_store = embedding_store

        # 初始化蒸馏表
        self._ensure_distill_schema()

    def _ensure_distill_schema(self):
        """创建蒸馏专用表"""
        self.store.register_schema("distill", DISTILL_SCHEMA)

    # ══════════════════════════════════════════════════════
    # 主入口：增量蒸馏
    # ══════════════════════════════════════════════════════

    def distill(self, force: bool = False, since_ts: int = None) -> dict:
        """
        执行增量蒸馏。

        流程：
        1. 检查自上次蒸馏以来是否有足够新记忆
        2. L1→L2: 主题蒸馏（聚类 + 摘要）
        3. L2→L3: 实体/关系提取
        4. L3→L4: 百科条目生成

        参数:
            force: 强制全量重新蒸馏
            since_ts: 只蒸馏此时间之后的记忆（None=自动）

        返回: 各层蒸馏结果
        """
        # 检查是否有足够新记忆
        last_distill_ts = self._get_state("last_distill_ts", 0)
        if not since_ts:
            since_ts = last_distill_ts

        new_memories = self._get_new_memories(since_ts)
        if len(new_memories) < self.MIN_MEMORIES_FOR_DISTILL and not force:
            return {
                "skipped": True,
                "reason": f"新记忆不足: {len(new_memories)}/{self.MIN_MEMORIES_FOR_DISTILL}",
                "new_count": len(new_memories),
            }

        logger.info(f"🧪 开始蒸馏: {len(new_memories)} 条新记忆 (since={since_ts})")

        batch_id = f"batch_{int(time.time())}_{hashlib.md5(str(since_ts).encode()).hexdigest()[:6]}"
        batch_start = int(time.time())

        result = {
            "new_memories": len(new_memories),
            "topics": {},
            "entities": {},
            "encyclopedia": {},
            "batch_id": batch_id,
        }

        # L1→L2: 主题蒸馏
        result["topics"] = self._distill_topics(new_memories, force)

        # L2→L3: 实体提取
        result["entities"] = self._distill_entities(result["topics"].get("topic_ids", []), force)

        # L3→L4: 百科条目
        result["encyclopedia"] = self._distill_encyclopedia(
            result["entities"].get("entity_ids", []),
            result["topics"].get("topic_ids", []),
            force,
        )

        # 更新状态
        self._set_state("last_distill_ts", str(int(time.time())))
        self._set_state("last_distill_count", str(len(new_memories)))

        # v8.2 安全：记录蒸馏批次（支持回滚）
        try:
            self.store.execute_sql(
                "INSERT INTO distill_batches (batch_id, started_at, completed_at, topic_ids, entity_ids, relation_ids, entry_ids, source_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    batch_id,
                    batch_start,
                    int(time.time()),
                    json.dumps(result["topics"].get("topic_ids", [])),
                    json.dumps(result["entities"].get("entity_ids", [])),
                    json.dumps(result["entities"].get("relation_ids", [])),
                    json.dumps(result["encyclopedia"].get("entry_ids", [])),
                    len(new_memories),
                )
            )
        except Exception as e:
            logger.debug(f"Batch tracking skipped: {e}")

        logger.info(
            f"✅ 蒸馏完成: "
            f"{result['topics'].get('created', 0)} 主题, "
            f"{result['entities'].get('created', 0)} 实体, "
            f"{result['encyclopedia'].get('created', 0)} 百科条目"
        )

        return result

    # ══════════════════════════════════════════════════════
    # L1→L2: 主题蒸馏
    # ══════════════════════════════════════════════════════

    def _distill_topics(self, memories: list[dict], force: bool = False) -> dict:
        """
        按主题聚类原始记忆，生成主题摘要。

        策略：
        1. 按 primary topic 分组
        2. 每组内按时间排序
        3. 调用 LLM 生成该主题的结构化摘要
        4. 写入 distill_topics 表
        """
        # 按主题分组
        topic_groups = defaultdict(list)
        for mem in memories:
            topics = mem.get("topics", [])
            primary = "misc"
            for t in topics:
                if isinstance(t, dict) and t.get("is_primary"):
                    primary = t["code"]
                    break
                elif isinstance(t, str):
                    primary = t
                    break
            topic_groups[primary].append(mem)

        created = 0
        updated = 0
        topic_ids = []

        for topic_code, topic_memories in topic_groups.items():
            if len(topic_memories) < 2:
                # 太少不值得蒸馏，但也记录
                topic_memories_sorted = topic_memories
            else:
                topic_memories_sorted = sorted(topic_memories, key=lambda m: m.get("time_ts", 0))

            # 检查是否已有该主题的摘要
            existing = self._get_distill_topic(topic_code)

            if existing and not force:
                # 增量合并：将新记忆合并到已有摘要
                merged = self._merge_topic_summary(existing, topic_memories_sorted)
                topic_id = existing["topic_id"]
                self._update_distill_topic(topic_id, merged)
                updated += 1
            else:
                # 新建摘要
                summary = self._generate_topic_summary(topic_code, topic_memories_sorted)
                topic_id = self._make_topic_id(topic_code)
                ts_list = [m.get("time_ts", 0) for m in topic_memories_sorted if m.get("time_ts")]
                source_ids = [m["memory_id"] for m in topic_memories_sorted]

                self._insert_distill_topic(
                    topic_id=topic_id,
                    topic_code=topic_code,
                    summary=summary,
                    source_count=len(topic_memories_sorted),
                    source_ids=source_ids,
                    importance=self._dominant_importance(topic_memories_sorted),
                    time_range_start=min(ts_list) if ts_list else None,
                    time_range_end=max(ts_list) if ts_list else None,
                )
                created += 1

            topic_ids.append(topic_id)

        return {"created": created, "updated": updated, "total": len(topic_groups), "topic_ids": topic_ids}

    def _generate_topic_summary(self, topic_code: str, memories: list[dict]) -> str:
        """为一组同主题记忆生成摘要"""
        if self.llm_fn:
            return self._llm_topic_summary(topic_code, memories)
        logger.debug(f"蒸馏 heuristic 模式 (无 LLM): topic={topic_code}, {len(memories)} 条")
        return self._heuristic_topic_summary(topic_code, memories)

    def _llm_topic_summary(self, topic_code: str, memories: list[dict]) -> str:
        """用 LLM 生成主题摘要"""
        mem_texts = []
        for i, mem in enumerate(memories[:30]):  # 最多 30 条
            content = mem.get("content", "")[:self.MAX_CONTENT_PREVIEW]
            ts = mem.get("time_ts", 0)
            dt = datetime.fromtimestamp(ts).strftime("%m-%d %H:%M") if ts else "?"
            mem_texts.append(f"[{i+1}] ({dt}) {content}")

        prompt = f"""你是一个知识蒸馏器。请将以下关于主题"{topic_code}"的多条对话记忆，蒸馏为一个结构化的主题摘要。

记忆条数: {len(memories)}
时间跨度: {self._format_time_range(memories)}

原始记忆:
{chr(10).join(mem_texts)}

要求：
1. 提炼出这个主题的核心知识：关键决策、重要事实、发展趋势、个人偏好
2. 去除闲聊和重复
3. 按时间线或逻辑顺序组织
4. 输出结构化 Markdown，不超过 500 字

输出格式:
## 主题概述
[一段话概括]

## 关键决策
- ...

## 重要事实
- ...

## 趋势/演变
- ...

## 个人偏好/立场
- ...
"""
        try:
            return self.llm_fn(prompt)
        except Exception as e:
            logger.warning("distill: %s", e)
            return self._heuristic_topic_summary(topic_code, memories)

    def _heuristic_topic_summary(self, topic_code: str, memories: list[dict]) -> str:
        """无 LLM 的启发式主题摘要（增强版：提取决策/事实/偏好 + 文件路径 + 数值 + 代码引用）"""
        lines = [f"## {topic_code}", ""]

        # 关键词分类
        decision_kw = ["决定", "选择", "采用", "用", "改为", "放弃", "推荐", "结论", "总结", "选", "确定"]
        fact_kw = ["发现", "确认", "数据显示", "结果", "验证", "注意", "踩坑", "报错", "问题", "bug", "error"]
        pref_kw = ["偏好", "喜欢", "不喜欢", "习惯", "风格", "倾向", "偏好"]

        decisions, facts, prefs, files, numbers = [], [], [], [], []
        import re as _re

        for mem in memories:
            content = mem.get("content", "")

            # 提取文件路径
            for fp in _re.findall(r'[\w/._-]+\.\w{1,6}', content):
                if '/' in fp or '\\' in fp:
                    files.append(fp)

            # 提取关键数值（版本号、百分比、指标）
            for num in _re.findall(r'v?\d+\.\d+(\.\d+)?|\d+%|\d+\s*(ms|s|MB|GB|KB|条|次)', content):
                pass  # 数值本身太碎片化，跳过

            for sent in content.replace("!", "。").replace("?", "。").split("。"):
                sent = sent.strip()
                if len(sent) < 5 or len(sent) > 200:
                    continue
                if any(k in sent for k in decision_kw):
                    decisions.append(sent[:150])
                elif any(k in sent for k in fact_kw):
                    facts.append(sent[:150])
                elif any(k in sent for k in pref_kw):
                    prefs.append(sent[:150])

        lines.append(f"**记忆条数**: {len(memories)}")
        lines.append(f"**时间跨度**: {self._format_time_range(memories)}")
        lines.append("")

        if decisions:
            lines.append("### 关键决策")
            for d in decisions[:10]:
                lines.append(f"- {d}")
            lines.append("")

        if facts:
            lines.append("### 重要事实")
            for f in facts[:10]:
                lines.append(f"- {f}")
            lines.append("")

        if prefs:
            lines.append("### 偏好")
            for p in prefs[:5]:
                lines.append(f"- {p}")
            lines.append("")

        if files:
            lines.append("### 涉及文件")
            for f in sorted(set(files))[:10]:
                lines.append(f"- `{f}`")
            lines.append("")

        return "\n".join(lines)

    def _merge_topic_summary(self, existing: dict, new_memories: list[dict]) -> dict:
        """增量合并：将新记忆合并到已有主题摘要"""
        # 获取已有 source_ids
        existing_ids = set(json.loads(existing.get("source_ids", "[]")))
        new_ids = [m["memory_id"] for m in new_memories if m["memory_id"] not in existing_ids]

        if not new_ids:
            return {"source_count": existing["source_count"]}

        # 重新生成摘要（基于所有记忆）
        all_ids = list(existing_ids | set(new_ids))
        all_memories = []
        for mid in all_ids:
            mem = self.store.get_memory(mid)
            if mem:
                all_memories.append(mem)

        new_summary = self._generate_topic_summary(existing["topic_code"], all_memories)

        return {
            "summary": new_summary,
            "source_count": len(all_memories),
            "source_ids": json.dumps(all_memories and [m["memory_id"] for m in all_memories] or [], ensure_ascii=False),
            "version": existing.get("version", 0) + 1,
        }

    # ══════════════════════════════════════════════════════
    # L2→L3: 实体/关系提取
    # ══════════════════════════════════════════════════════

    def _distill_entities(self, topic_ids: list[str], force: bool = False) -> dict:
        """
        从主题摘要中提取实体和关系。

        实体类型: person / concept / tool / project / decision / fact / preference
        关系类型: uses / depends_on / contradicts / part_of / decided_by / evolved_to
        """
        # 获取主题摘要
        topics = []
        for tid in topic_ids:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_topics WHERE topic_id = ?", (tid,),
                fetch=True,
            )
            if rows:
                topics.append(rows[0])

        if not topics:
            return {"created": 0, "relations_created": 0, "entity_ids": []}

        all_entities = []
        all_relations = []

        for topic in topics:
            entities, relations = self._extract_entities_from_topic(topic)
            all_entities.extend(entities)
            all_relations.extend(relations)

        # 去重合并
        entity_map = {}  # name+type -> entity
        for ent in all_entities:
            key = f"{ent['entity_type']}:{ent['name']}"
            if key in entity_map:
                # 合并 source_topics
                existing = entity_map[key]
                existing_topics = set(json.loads(existing.get("source_topics", "[]")))
                new_topics = set(json.loads(ent.get("source_topics", "[]")))
                existing_topics |= new_topics
                existing["source_topics"] = json.dumps(list(existing_topics), ensure_ascii=False)
                # 合并 attributes
                existing_attrs = json.loads(existing.get("attributes", "{}"))
                new_attrs = json.loads(ent.get("attributes", "{}"))
                existing_attrs.update(new_attrs)
                existing["attributes"] = json.dumps(existing_attrs, ensure_ascii=False)
            else:
                entity_map[key] = ent

        # 写入数据库
        created_entities = 0
        entity_ids = []
        for key, ent in entity_map.items():
            if not force:
                existing_rows = self.store.execute_sql(
                    "SELECT entity_id FROM distill_entities WHERE entity_id = ?",
                    (ent["entity_id"],),
                    fetch=True,
                )
                if existing_rows:
                    self._update_entity(ent)
                    entity_ids.append(ent["entity_id"])
                    continue

            self._insert_entity(ent)
            entity_ids.append(ent["entity_id"])
            created_entities += 1

        # 写入关系
        created_relations = 0
        for rel in all_relations:
            # 检查源/目标实体是否存在
            if rel["source_entity"] in entity_ids or self._entity_exists(rel["source_entity"]):
                if rel["target_entity"] in entity_ids or self._entity_exists(rel["target_entity"]):
                    existing_rel_rows = self.store.execute_sql(
                        """SELECT relation_id FROM distill_relations
                           WHERE source_entity = ? AND target_entity = ? AND relation_type = ?""",
                        (rel["source_entity"], rel["target_entity"], rel["relation_type"]),
                        fetch=True,
                    )
                    if not existing_rel_rows:
                        self._insert_relation(rel)
                        created_relations += 1

        return {
            "created": created_entities,
            "relations_created": created_relations,
            "total_entities": len(entity_map),
            "total_relations": len(all_relations),
            "entity_ids": entity_ids,
        }

    def _extract_entities_from_topic(self, topic: dict) -> tuple[list[dict], list[dict]]:
        """从一个主题摘要中提取实体和关系"""
        summary = topic.get("summary", "")
        topic_code = topic.get("topic_code", "")
        topic_id = topic.get("topic_id", "")

        if self.llm_fn:
            return self._llm_extract_entities(summary, topic_code, topic_id)
        return self._heuristic_extract_entities(summary, topic_code, topic_id)

    def _llm_extract_entities(self, summary: str, topic_code: str, topic_id: str) -> tuple[list[dict], list[dict]]:
        """用 LLM 提取实体和关系"""
        prompt = f"""从以下主题摘要中提取知识实体和关系。

主题: {topic_code}

摘要:
{summary}

请按以下 JSON 格式输出（只输出 JSON，不要其他内容）:

```json
{{
  "entities": [
    {{
      "name": "实体名",
      "type": "person|concept|tool|project|decision|fact|preference",
      "attributes": {{"key": "value"}},
      "importance": "high|medium|low"
    }}
  ],
  "relations": [
    {{
      "source": "源实体名",
      "target": "目标实体名",
      "type": "uses|depends_on|contradicts|part_of|decided_by|evolved_to|related_to|caused_by",
      "attributes": {{"context": "..."}}
    }}
  ]
}}
```
"""
        try:
            response = self.llm_fn(prompt)
            return self._parse_entity_response(response, topic_code, topic_id)
        except Exception as e:
            logger.warning("distill: %s", e)
            return self._heuristic_extract_entities(summary, topic_code, topic_id)

    def _parse_entity_response(self, response: str, topic_code: str, topic_id: str) -> tuple[list[dict], list[dict]]:
        """解析 LLM 返回的实体/关系 JSON"""
        entities = []
        relations = []

        try:
            # 提取 JSON 块
            json_str = response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0]

            data = json.loads(json_str.strip())

            for ent in data.get("entities", []):
                name = ent.get("name", "").strip()
                entity_type = ent.get("type", "concept")
                if not name or entity_type not in self.ENTITY_TYPES:
                    continue

                entity_id = self._make_entity_id(name, entity_type)
                entities.append({
                    "entity_id": entity_id,
                    "name": name,
                    "entity_type": entity_type,
                    "attributes": json.dumps(ent.get("attributes", {}), ensure_ascii=False),
                    "source_topics": json.dumps([topic_id], ensure_ascii=False),
                    "importance": ent.get("importance", "medium"),
                })

            entity_name_to_id = {e["name"]: e["entity_id"] for e in entities}

            for rel in data.get("relations", []):
                source = rel.get("source", "").strip()
                target = rel.get("target", "").strip()
                rel_type = rel.get("type", "related_to")
                if not source or not target or rel_type not in self.RELATION_TYPES:
                    continue

                src_id = entity_name_to_id.get(source, self._make_entity_id(source, "concept"))
                tgt_id = entity_name_to_id.get(target, self._make_entity_id(target, "concept"))

                relations.append({
                    "relation_id": self._make_relation_id(src_id, tgt_id, rel_type),
                    "source_entity": src_id,
                    "target_entity": tgt_id,
                    "relation_type": rel_type,
                    "attributes": json.dumps(rel.get("attributes", {}), ensure_ascii=False),
                    "source_topics": json.dumps([topic_id], ensure_ascii=False),
                    "confidence": 0.85,
                })

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            logger.warning(f"实体 JSON 解析失败: {e}")
            return self._heuristic_extract_entities("", topic_code, topic_id)

        return entities, relations

    def _heuristic_extract_entities(self, summary: str, topic_code: str, topic_id: str) -> tuple[list[dict], list[dict]]:
        """启发式实体提取（无 LLM fallback）"""
        entities = []
        relations = []

        # 从主题名创建一个 concept 实体
        topic_entity_id = self._make_entity_id(topic_code, "concept")
        entities.append({
            "entity_id": topic_entity_id,
            "name": topic_code,
            "entity_type": "concept",
            "attributes": json.dumps({"source": "topic_code"}, ensure_ascii=False),
            "source_topics": json.dumps([topic_id], ensure_ascii=False),
            "importance": "medium",
        })

        # 从摘要中提取关键名词
        if summary:
            import re
            # 提取 ## 标题下的内容
            sections = re.split(r'###?\s+', summary)
            for section in sections:
                lines = section.strip().split("\n")
                header = lines[0].strip() if lines else ""

                # 决策 → decision 实体
                if "决策" in header or "决定" in header:
                    for line in lines[1:]:
                        line = line.strip().lstrip("- ")
                        if len(line) > 5:
                            dec_id = self._make_entity_id(line[:50], "decision")
                            entities.append({
                                "entity_id": dec_id,
                                "name": line[:80],
                                "entity_type": "decision",
                                "attributes": json.dumps({"topic": topic_code}, ensure_ascii=False),
                                "source_topics": json.dumps([topic_id], ensure_ascii=False),
                                "importance": "high",
                            })
                            relations.append({
                                "relation_id": self._make_relation_id(dec_id, topic_entity_id, "part_of"),
                                "source_entity": dec_id,
                                "target_entity": topic_entity_id,
                                "relation_type": "part_of",
                                "attributes": "{}",
                                "source_topics": json.dumps([topic_id], ensure_ascii=False),
                                "confidence": 0.7,
                            })

                # 事实 → fact 实体
                elif "事实" in header or "发现" in header:
                    for line in lines[1:]:
                        line = line.strip().lstrip("- ")
                        if len(line) > 5:
                            fact_id = self._make_entity_id(line[:50], "fact")
                            entities.append({
                                "entity_id": fact_id,
                                "name": line[:80],
                                "entity_type": "fact",
                                "attributes": json.dumps({"topic": topic_code}, ensure_ascii=False),
                                "source_topics": json.dumps([topic_id], ensure_ascii=False),
                                "importance": "medium",
                            })

        return entities, relations

    # ══════════════════════════════════════════════════════
    # L3→L4: 百科条目生成
    # ══════════════════════════════════════════════════════

    def _distill_encyclopedia(self, entity_ids: list[str], topic_ids: list[str], force: bool = False) -> dict:
        """
        将实体和主题摘要合并为个人百科条目。

        按类别组织：decisions / tools / projects / concepts / people / facts
        """
        # 获取所有实体
        entities = []
        for eid in entity_ids:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_entities WHERE entity_id = ?", (eid,),
                fetch=True,
            )
            if rows:
                entities.append(rows[0])

        # 获取所有主题
        topics = []
        for tid in topic_ids:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_topics WHERE topic_id = ?", (tid,),
                fetch=True,
            )
            if rows:
                topics.append(rows[0])

        if not entities and not topics:
            return {"created": 0, "entry_ids": []}

        # 按类别分组实体
        by_category = defaultdict(list)
        for ent in entities:
            cat = self._entity_type_to_category(ent["entity_type"])
            by_category[cat].append(ent)

        created = 0
        entry_ids = []

        # 为每个有内容的类别生成百科条目
        for category, cat_entities in by_category.items():
            if not cat_entities:
                continue

            # 检查是否已有此分类的条目
            existing_entry = self._get_encyclopedia_entry_by_category(category)

            if existing_entry and not force:
                # 增量更新
                content = self._merge_encyclopedia_content(existing_entry, cat_entities, topics)
                self._update_encyclopedia_entry(existing_entry["entry_id"], content)
                entry_ids.append(existing_entry["entry_id"])
            else:
                # 新建条目
                if self.llm_fn:
                    content = self._llm_generate_encyclopedia(category, cat_entities, topics)
                else:
                    content = self._heuristic_generate_encyclopedia(category, cat_entities, topics)

                title = self._category_title(category)
                entry_id = self._make_entry_id(title)

                self._insert_encyclopedia_entry(
                    entry_id=entry_id,
                    title=title,
                    content=content,
                    category=category,
                    source_entities=json.dumps([e["entity_id"] for e in cat_entities], ensure_ascii=False),
                    source_topics=json.dumps([t["topic_id"] for t in topics], ensure_ascii=False),
                )
                entry_ids.append(entry_id)
                created += 1

        # 生成总目录
        if topics or entities:
            toc_entry = self._generate_toc_entry(topics, by_category)
            existing_toc = self._get_encyclopedia_entry_by_category("_toc")
            if existing_toc:
                self._update_encyclopedia_entry(existing_toc["entry_id"], toc_entry["content"])
            else:
                self._insert_encyclopedia_entry(
                    entry_id=toc_entry["entry_id"],
                    title=toc_entry["title"],
                    content=toc_entry["content"],
                    category="_toc",
                    source_entities="[]",
                    source_topics=json.dumps([t["topic_id"] for t in topics], ensure_ascii=False),
                )
            entry_ids.append(toc_entry["entry_id"])

        return {"created": created, "entry_ids": entry_ids}

    def _llm_generate_encyclopedia(self, category: str, entities: list[dict], topics: list[dict]) -> str:
        """用 LLM 生成百科条目"""
        entity_texts = []
        for ent in entities:
            attrs = json.loads(ent.get("attributes", "{}"))
            entity_texts.append(f"- **{ent['name']}** ({ent['entity_type']}): {json.dumps(attrs, ensure_ascii=False)}")

        topic_texts = []
        for t in topics[:5]:
            topic_texts.append(f"### {t['topic_code']}\n{t.get('summary', '')[:300]}")

        prompt = f"""你是一个知识整理器。请将以下实体和主题信息整合为一篇结构化的百科条目。

类别: {category}

实体:
{chr(10).join(entity_texts[:20])}

相关主题:
{chr(10).join(topic_texts[:5])}

要求：
1. 将分散的实体整合为连贯的知识叙述
2. 保留所有关键事实和决策
3. 按逻辑顺序组织
4. 输出 Markdown 格式，不超过 800 字
5. 包含"核心要点"列表和"详细说明"章节
"""
        try:
            return self.llm_fn(prompt)
        except Exception as e:
            logger.debug("LLM encyclopedia generation failed: %s", e)
            return self._heuristic_generate_encyclopedia(category, entities, topics)

    def _heuristic_generate_encyclopedia(self, category: str, entities: list[dict], topics: list[dict]) -> str:
        """启发式百科条目生成"""
        lines = [
            f"# {self._category_title(category)}",
            "",
            f"*自动生成于 {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
        ]

        if entities:
            lines.append("## 核心要点")
            lines.append("")
            for ent in entities[:15]:
                icon = self.ENTITY_TYPES.get(ent["entity_type"], {}).get("icon", "•")
                attrs = json.loads(ent.get("attributes", "{}"))
                attr_str = ""
                if attrs:
                    attr_items = [f"{k}={v}" for k, v in list(attrs.items())[:3]]
                    attr_str = f" ({', '.join(attr_items)})"
                lines.append(f"- {icon} **{ent['name']}**{attr_str}")
            lines.append("")

        # 相关主题摘要
        related_topics = []
        for ent in entities:
            src_topics = json.loads(ent.get("source_topics", "[]"))
            for t in topics:
                if t["topic_id"] in src_topics and t not in related_topics:
                    related_topics.append(t)

        if related_topics:
            lines.append("## 相关主题")
            lines.append("")
            for t in related_topics[:5]:
                summary_preview = (t.get("summary") or "")[:200]
                lines.append(f"### {t['topic_code']}")
                lines.append(summary_preview)
                lines.append("")

        return "\n".join(lines)

    def _generate_toc_entry(self, topics: list[dict], by_category: dict) -> dict:
        """生成百科总目录"""
        lines = [
            "# 📖 个人知识手册",
            "",
            f"*自动维护 · 最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
            "## 知识地图",
            "",
        ]

        # 按类别统计
        lines.append("| 类别 | 条目数 | 典型内容 |")
        lines.append("|------|--------|---------|")
        for cat in ["decisions", "tools", "projects", "concepts", "people", "facts"]:
            ents = by_category.get(cat, [])
            if ents:
                sample = ents[0]["name"][:30]
                lines.append(f"| {self._category_title(cat)} | {len(ents)} | {sample}... |")
        lines.append("")

        # 主题列表
        if topics:
            lines.append("## 主题索引")
            lines.append("")
            for t in topics[:20]:
                count = t.get("source_count", 0)
                lines.append(f"- **{t['topic_code']}** ({count} 条记忆)")
            lines.append("")

        content = "\n".join(lines)
        entry_id = self._make_entry_id("个人知识手册")

        return {
            "entry_id": entry_id,
            "title": "📖 个人知识手册",
            "content": content,
        }

    # ══════════════════════════════════════════════════════
    # 查询接口
    # ══════════════════════════════════════════════════════

    def get_topic_summaries(self, topic_code: str = None, limit: int = 50) -> list[dict]:
        """获取主题摘要列表"""
        if topic_code:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_topics WHERE topic_code LIKE ? ORDER BY updated_at DESC LIMIT ?",
                (topic_code + "%", limit),
                fetch=True,
            )
        else:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_topics ORDER BY updated_at DESC LIMIT ?", (limit,),
                fetch=True,
            )
        return rows

    def _quarantined_ids(self, item_type: str = None) -> set:
        """获取当前被隔离的条目 ID 集合"""
        try:
            if item_type:
                rows = self.store.execute_sql(
                    "SELECT item_id FROM distill_quarantine WHERE released_at IS NULL AND item_type = ?",
                    (item_type,),
                    fetch=True,
                )
            else:
                rows = self.store.execute_sql(
                    "SELECT item_id FROM distill_quarantine WHERE released_at IS NULL",
                    fetch=True,
                )
            return {r["item_id"] for r in rows}
        except Exception as e:
            logger.debug("quarantined IDs query failed: %s", e)
            return set()

    def get_entities(self, entity_type: str = None, name_like: str = None, limit: int = 50) -> list[dict]:
        """查询知识实体（排除被隔离的条目）"""
        conditions = []
        params = []
        if entity_type:
            conditions.append("entity_type = ?")
            params.append(entity_type)
        if name_like:
            conditions.append("name LIKE ?")
            params.append(f"%{name_like}%")
        where = " AND ".join(conditions) if conditions else "1=1"
        rows = self.store.execute_sql(
            f"SELECT * FROM distill_entities WHERE {where} ORDER BY importance DESC, updated_at DESC LIMIT ?",
            params + [limit],
            fetch=True,
        )
        quarantined = self._quarantined_ids("entity")
        return [r for r in rows if r["entity_id"] not in quarantined]

    def get_entity_relations(self, entity_id: str) -> list[dict]:
        """获取一个实体的所有关系"""
        rows = self.store.execute_sql(
            """SELECT r.*, e1.name as source_name, e2.name as target_name
               FROM distill_relations r
               JOIN distill_entities e1 ON r.source_entity = e1.entity_id
               JOIN distill_entities e2 ON r.target_entity = e2.entity_id
               WHERE r.source_entity = ? OR r.target_entity = ?""",
            (entity_id, entity_id),
            fetch=True,
        )
        return rows

    def get_encyclopedia(self, category: str = None) -> list[dict]:
        """获取百科条目（排除被隔离的条目）"""
        if category:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_encyclopedia WHERE category = ? ORDER BY last_updated DESC",
                (category,),
                fetch=True,
            )
        else:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_encyclopedia WHERE category != '_toc' ORDER BY last_updated DESC",
                fetch=True,
            )
        quarantined = self._quarantined_ids("entry")
        return [r for r in rows if r["entry_id"] not in quarantined]

    def get_encyclopedia_toc(self) -> dict | None:
        """获取百科目录"""
        rows = self.store.execute_sql(
            "SELECT * FROM distill_encyclopedia WHERE category = '_toc' ORDER BY last_updated DESC LIMIT 1",
            fetch=True,
        )
        return rows[0] if rows else None

    def search_encyclopedia(self, query: str) -> list[dict]:
        """搜索百科条目（排除被隔离的条目）"""
        rows = self.store.execute_sql(
            """SELECT * FROM distill_encyclopedia
               WHERE category != '_toc' AND (title LIKE ? OR content LIKE ?)
               ORDER BY last_updated DESC""",
            (f"%{query}%", f"%{query}%"),
            fetch=True,
        )
        quarantined = self._quarantined_ids("entry")
        return [r for r in rows if r["entry_id"] not in quarantined]

    def get_distill_stats(self) -> dict:
        """蒸馏系统统计"""
        topics_rows = self.store.execute_sql("SELECT COUNT(*) as cnt FROM distill_topics", fetch=True)
        topics_count = topics_rows[0]["cnt"] if topics_rows else 0
        entities_rows = self.store.execute_sql("SELECT COUNT(*) as cnt FROM distill_entities", fetch=True)
        entities_count = entities_rows[0]["cnt"] if entities_rows else 0
        relations_rows = self.store.execute_sql("SELECT COUNT(*) as cnt FROM distill_relations", fetch=True)
        relations_count = relations_rows[0]["cnt"] if relations_rows else 0
        encyclopedia_rows = self.store.execute_sql(
            "SELECT COUNT(*) as cnt FROM distill_encyclopedia WHERE category != '_toc'",
            fetch=True,
        )
        encyclopedia_count = encyclopedia_rows[0]["cnt"] if encyclopedia_rows else 0

        entity_types = self.store.execute_sql(
            "SELECT entity_type, COUNT(*) as cnt FROM distill_entities GROUP BY entity_type",
            fetch=True,
        )

        last_ts = self._get_state("last_distill_ts", 0)

        quarantine_count = 0
        try:
            quarantine_rows = self.store.execute_sql(
                "SELECT COUNT(*) as cnt FROM distill_quarantine WHERE released_at IS NULL",
                fetch=True,
            )
            quarantine_count = quarantine_rows[0]["cnt"] if quarantine_rows else 0
        except Exception as e:
            logger.warning("distill: %s", e)

        batch_count = 0
        try:
            batch_rows = self.store.execute_sql(
                "SELECT COUNT(*) as cnt FROM distill_batches WHERE status = 'completed'",
                fetch=True,
            )
            batch_count = batch_rows[0]["cnt"] if batch_rows else 0
        except Exception as e:
            logger.warning("distill: %s", e)

        return {
            "topics": topics_count,
            "entities": entities_count,
            "relations": relations_count,
            "encyclopedia_entries": encyclopedia_count,
            "entity_types": {r["entity_type"]: r["cnt"] for r in entity_types},
            "last_distill_ts": int(last_ts) if last_ts else 0,
            "last_distill_time": datetime.fromtimestamp(int(last_ts)).strftime("%Y-%m-%d %H:%M") if last_ts else "never",
            "quarantined": quarantine_count,
            "completed_batches": batch_count,
        }

    # ══════════════════════════════════════════════════════
    # v8.2 安全：蒸馏回滚（可逆性保障）
    # ══════════════════════════════════════════════════════

    def rollback_batch(self, batch_id: str) -> dict:
        """
        回滚指定批次的蒸馏结果。

        蒸馏是可逆的：每个批次记录了创建的所有 topic/entity/relation/entry ID，
        回滚时删除这些记录，原始记忆不受影响。

        参数:
            batch_id: 蒸馏批次 ID

        返回: {"rolled_back": bool, "deleted": {...}, "batch_id": str}
        """
        rows = self.store.execute_sql(
            "SELECT * FROM distill_batches WHERE batch_id = ?",
            (batch_id,),
            fetch=True,
        )
        if not rows:
            return {"rolled_back": False, "error": f"批次 {batch_id} 未找到"}
        row = rows[0]
        if row["status"] == "rolled_back":
            return {"rolled_back": False, "error": f"批次 {batch_id} 已回滚"}

        deleted = {}
        for col, table in [
            ("topic_ids", "distill_topics"),
            ("entity_ids", "distill_entities"),
            ("relation_ids", "distill_relations"),
            ("entry_ids", "distill_encyclopedia"),
        ]:
            ids = json.loads(row[col] or "[]")
            if ids:
                TABLE_ID_MAP = {
                    "distill_topics": "topic_id",
                    "distill_entities": "entity_id",
                    "distill_relations": "relation_id",
                    "distill_encyclopedia": "entry_id",
                }
                id_col = TABLE_ID_MAP.get(table, "id")
                count = 0
                for placeholders, chunk_ids in _chunked_placeholders(ids):
                    try:
                        result = self.store.execute_sql(
                            f"DELETE FROM {table} WHERE {id_col} IN ({placeholders})",
                            chunk_ids,
                        )
                        count += result.rowcount
                    except Exception as e:
                        logger.debug("Rollback delete failed for %s: %s", table, e)
                        pass
                deleted[table] = count

        self.store.execute_sql(
            "UPDATE distill_batches SET status = 'rolled_back' WHERE batch_id = ?",
            (batch_id,)
        )

        logger.info(f"🔄 蒸馏批次 {batch_id} 已回滚: {deleted}")
        return {"rolled_back": True, "deleted": deleted, "batch_id": batch_id}

    def list_batches(self, limit: int = 20) -> list[dict]:
        """列出蒸馏批次"""
        rows = self.store.execute_sql(
            "SELECT batch_id, started_at, completed_at, source_count, status FROM distill_batches ORDER BY started_at DESC LIMIT ?",
            (limit,),
            fetch=True,
        )
        return [
            {
                "batch_id": r["batch_id"],
                "started_at": r["started_at"],
                "completed_at": r["completed_at"],
                "source_count": r["source_count"],
                "status": r["status"],
            }
            for r in rows
        ]

    def quarantine_item(self, item_id: str, item_type: str, confidence: float = 0.0, reason: str = "") -> dict:
        """
        将低置信度蒸馏结果隔离。

        被隔离的条目不会出现在检索结果和百科中，直到人工审核释放。

        参数:
            item_id: 蒸馏条目 ID（topic_id / entity_id / relation_id / entry_id）
            item_type: 条目类型（topic / entity / relation / entry）
            confidence: 置信度分数
            reason: 隔离原因

        返回: {"quarantined": bool, "item_id": str}
        """
        try:
            self.store.execute_sql(
                "INSERT OR REPLACE INTO distill_quarantine (item_id, item_type, confidence, reason) VALUES (?, ?, ?, ?)",
                (item_id, item_type, confidence, reason)
            )
            logger.info(f"🔒 蒸馏条目已隔离: {item_type}/{item_id} (confidence={confidence:.2f}, reason={reason})")
            return {"quarantined": True, "item_id": item_id}
        except Exception as e:
            return {"quarantined": False, "error": str(e)}

    def release_quarantine(self, item_id: str) -> dict:
        """
        释放被隔离的蒸馏条目（审核通过后）。

        参数:
            item_id: 被隔离的条目 ID

        返回: {"released": bool, "item_id": str}
        """
        try:
            now = int(time.time())
            result = self.store.execute_sql(
                "UPDATE distill_quarantine SET released_at = ? WHERE item_id = ? AND released_at IS NULL",
                (now, item_id)
            )
            count = result.rowcount
            if count > 0:
                logger.info(f"✅ 蒸馏条目已释放: {item_id}")
                return {"released": True, "item_id": item_id}
            return {"released": False, "error": f"条目 {item_id} 未找到或已释放"}
        except Exception as e:
            return {"released": False, "error": str(e)}

    def get_quarantined_items(self, item_type: str = None) -> list[dict]:
        """获取当前被隔离的蒸馏条目"""
        if item_type:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_quarantine WHERE released_at IS NULL AND item_type = ? ORDER BY quarantined_at DESC",
                (item_type,),
                fetch=True,
            )
        else:
            rows = self.store.execute_sql(
                "SELECT * FROM distill_quarantine WHERE released_at IS NULL ORDER BY quarantined_at DESC",
                fetch=True,
            )
        return [
            {
                "item_id": r["item_id"],
                "item_type": r["item_type"],
                "confidence": r["confidence"],
                "reason": r["reason"],
                "quarantined_at": r["quarantined_at"],
            }
            for r in rows
        ]

    def purge_by_source(self, source_memory_id: str) -> dict:
        """
        清除由指定源记忆派生的所有蒸馏内容。

        当一条原始记忆被删除或标记为不可信时，应调用此方法清除其所有传播内容，
        防止级联污染。此操作同时清除主题、实体、关系和百科条目。

        参数:
            source_memory_id: 原始记忆的 memory_id

        返回: {"purged": bool, "deleted": {table: count}, "source_memory_id": str}
        """
        deleted = {}
        target_id_str = f'"{source_memory_id}"'

        for table, id_col in [
            ("distill_topics", "topic_id"),
            ("distill_entities", "entity_id"),
            ("distill_relations", "relation_id"),
            ("distill_encyclopedia", "entry_id"),
        ]:
            if not _VALID_IDENTIFIER.match(table):
                raise ValueError(f"Invalid table name: {table!r}")
            if not _VALID_IDENTIFIER.match(id_col):
                raise ValueError(f"Invalid column name: {id_col!r}")
            try:
                rows = self.store.execute_sql(
                    f"SELECT {id_col}, source_ids FROM {table} LIMIT 10000",
                    fetch=True,
                )
                ids_to_delete = []
                for r in rows:
                    source_ids = json.loads(r["source_ids"] or "[]")
                    if source_memory_id in source_ids:
                        ids_to_delete.append(r[id_col])
                if ids_to_delete:
                    count = 0
                    for placeholders, chunk_ids in _chunked_placeholders(ids_to_delete):
                        result = self.store.execute_sql(
                            f"DELETE FROM {table} WHERE {id_col} IN ({placeholders})",
                            chunk_ids,
                        )
                        count += result.rowcount
                    deleted[table] = count
                    for item_id in ids_to_delete:
                        self.store.execute_sql(
                            "DELETE FROM distill_quarantine WHERE item_id = ?",
                            (item_id,)
                        )
            except Exception as e:
                logger.debug(f"purge_by_source scan {table}: %s", e)

        if deleted:
            logger.info(f"🗑️ Purged propagated content for source {source_memory_id}: {deleted}")
        return {
            "purged": bool(deleted),
            "deleted": deleted,
            "source_memory_id": source_memory_id,
        }

    def purge_by_sources(self, source_memory_ids: list[str]) -> dict:
        """
        批量清除多条源记忆的派生内容。

        参数:
            source_memory_ids: 原始记忆 ID 列表

        返回: {"purged": bool, "deleted": {table: count}, "count": int}
        """
        total_deleted = {}
        for mid in source_memory_ids:
            result = self.purge_by_source(mid)
            for table, count in result.get("deleted", {}).items():
                total_deleted[table] = total_deleted.get(table, 0) + count
        return {
            "purged": bool(total_deleted),
            "deleted": total_deleted,
            "count": len(source_memory_ids),
        }

    def export_encyclopedia(self, output_path: str = None) -> str:
        """导出完整百科为 Markdown 文件"""
        rows = self.store.execute_sql(
            "SELECT * FROM distill_encyclopedia ORDER BY category, last_updated DESC",
            fetch=True,
        )

        lines = [
            "# 📖 个人知识手册",
            "",
            f"*导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
            "",
            "---",
            "",
        ]

        # 先放目录
        toc = self.get_encyclopedia_toc()
        if toc:
            lines.append(toc["content"])
            lines.append("")
            lines.append("---")
            lines.append("")

        # 按类别输出条目
        current_cat = None
        for entry in rows:
            if entry["category"] == "_toc":
                continue
            if entry["category"] != current_cat:
                current_cat = entry["category"]
                lines.append(f"\n---\n\n# {self._category_title(current_cat)}\n")
            lines.append(entry["content"])
            lines.append("")

        content = "\n".join(lines)

        if output_path:
            os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(content)
            return output_path

        return content

    def distill_video_content(self, video_content: dict) -> str:
        """蒸馏视频内容
        
        Args:
            video_content: 视频内容，包含 transcript 和 description
        
        Returns:
            蒸馏后的知识内容
        """
        # 提取视频内容
        transcript = video_content.get("transcript", "")
        description = video_content.get("description", "")
        
        # 合并内容
        full_content = transcript + " " + description
        
        if not full_content:
            return ""
        
        # 生成视频主题
        video_topic = "video_content"
        
        # 创建临时记忆
        temp_memory = {
            "memory_id": f"temp_video_{int(time.time())}",
            "content": full_content,
            "topics": [video_topic],
            "importance": "medium",
            "time_ts": int(time.time())
        }
        
        # 蒸馏此记忆
        result = self._distill_topics([temp_memory], force=True)
        
        # 获取蒸馏结果
        if result.get("topic_ids"):
            topic_id = result["topic_ids"][0]
            topic_rows = self.store.execute_sql(
                "SELECT summary FROM distill_topics WHERE topic_id = ?", (topic_id,),
                fetch=True,
            )
            if topic_rows:
                return topic_rows[0]["summary"]
        
        # 无 LLM 时的启发式蒸馏
        return self._heuristic_video_summary(full_content)

    def _heuristic_video_summary(self, content: str) -> str:
        """视频内容的启发式摘要"""
        lines = ["## 视频内容摘要", ""]
        
        # 关键词分类
        key_kw = ["关键", "重要", "核心", "重点", "注意", "提醒"]
        step_kw = ["步骤", "方法", "技巧", "教程", "如何", "步骤"]
        fact_kw = ["发现", "确认", "数据", "结果", "验证", "事实"]
        
        key_points, steps, facts = [], [], []
        
        for sent in content.replace("!", "。").replace("?", "。").split("。"):
            sent = sent.strip()
            if len(sent) < 5 or len(sent) > 200:
                continue
            if any(k in sent for k in key_kw):
                key_points.append(sent[:150])
            elif any(k in sent for k in step_kw):
                steps.append(sent[:150])
            elif any(k in sent for k in fact_kw):
                facts.append(sent[:150])
        
        if key_points:
            lines.append("### 核心要点")
            for point in key_points[:5]:
                lines.append(f"- {point}")
            lines.append("")
        
        if steps:
            lines.append("### 步骤/方法")
            for i, step in enumerate(steps[:10], 1):
                lines.append(f"{i}. {step}")
            lines.append("")
        
        if facts:
            lines.append("### 重要事实")
            for fact in facts[:5]:
                lines.append(f"- {fact}")
            lines.append("")
        
        # 如果没有提取到结构化内容，返回原始内容的前500字
        if len(lines) <= 2:
            lines.append("### 内容概述")
            lines.append(content[:500] + ("..." if len(content) > 500 else ""))
        
        return "\n".join(lines)

    # ══════════════════════════════════════════════════════
    # 内部工具
    # ══════════════════════════════════════════════════════

    def _get_new_memories(self, since_ts: int) -> list[dict]:
        """获取自指定时间以来的新记忆"""
        if since_ts <= 0:
            return self.store.query(limit=500)
        return self.store.query(time_from=since_ts, limit=500)

    def _get_state(self, key: str, default=None):
        rows = self.store.execute_sql(
            "SELECT value FROM distill_state WHERE key = ?", (key,),
            fetch=True,
        )
        return rows[0]["value"] if rows else default

    def _set_state(self, key: str, value: str):
        self.store.execute_sql(
            "INSERT OR REPLACE INTO distill_state (key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, int(time.time())),
        )

    def _make_topic_id(self, topic_code: str) -> str:
        return f"dt_{hashlib.sha256(topic_code.encode()).hexdigest()[:12]}"

    def _make_entity_id(self, name: str, entity_type: str) -> str:
        raw = f"{entity_type}:{name}"
        return f"de_{hashlib.sha256(raw.encode()).hexdigest()[:12]}"

    def _make_relation_id(self, source: str, target: str, rel_type: str) -> str:
        raw = f"{source}>{rel_type}>{target}"
        return f"dr_{hashlib.sha256(raw.encode()).hexdigest()[:12]}"

    def _make_entry_id(self, title: str) -> str:
        return f"ency_{hashlib.sha256(title.encode()).hexdigest()[:12]}"

    def _dominant_importance(self, memories: list[dict]) -> str:
        counts = defaultdict(int)
        for m in memories:
            counts[m.get("importance", "medium")] += 1
        return max(counts, key=counts.get) if counts else "medium"

    def _format_time_range(self, memories: list[dict]) -> str:
        timestamps = [m.get("time_ts", 0) for m in memories if m.get("time_ts")]
        if not timestamps:
            return "?"
        earliest = datetime.fromtimestamp(min(timestamps)).strftime("%Y-%m-%d")
        latest = datetime.fromtimestamp(max(timestamps)).strftime("%Y-%m-%d")
        return earliest if earliest == latest else f"{earliest} ~ {latest}"

    def _entity_type_to_category(self, entity_type: str) -> str:
        mapping = {
            "decision": "decisions",
            "tool": "tools",
            "project": "projects",
            "concept": "concepts",
            "person": "people",
            "fact": "facts",
            "preference": "concepts",
        }
        return mapping.get(entity_type, "concepts")

    def _category_title(self, category: str) -> str:
        titles = {
            "decisions": "🎯 关键决策",
            "tools": "🔧 工具与技术",
            "projects": "📂 项目",
            "concepts": "💡 概念与偏好",
            "people": "👤 人物",
            "facts": "📌 事实记录",
        }
        return titles.get(category, category)

    def _entity_exists(self, entity_id: str) -> bool:
        rows = self.store.execute_sql(
            "SELECT 1 FROM distill_entities WHERE entity_id = ?", (entity_id,),
            fetch=True,
        )
        return len(rows) > 0

    # ── 数据库 CRUD ──────────────────────────────────────

    def _get_distill_topic(self, topic_code: str) -> dict | None:
        rows = self.store.execute_sql(
            "SELECT * FROM distill_topics WHERE topic_code = ? ORDER BY version DESC LIMIT 1",
            (topic_code,),
            fetch=True,
        )
        return rows[0] if rows else None

    def _insert_distill_topic(self, **kwargs):
        self.store.execute_sql(
            """INSERT OR REPLACE INTO distill_topics
               (topic_id, topic_code, summary, source_count, source_ids, importance,
                time_range_start, time_range_end, version, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, ?, ?)""",
            (kwargs["topic_id"], kwargs["topic_code"], kwargs["summary"],
             kwargs["source_count"], json.dumps(kwargs.get("source_ids", []), ensure_ascii=False),
             kwargs.get("importance", "medium"),
             kwargs.get("time_range_start"), kwargs.get("time_range_end"),
             int(time.time()), int(time.time())),
        )

    def _update_distill_topic(self, topic_id: str, updates: dict):
        sets = []
        params = []
        for k, v in updates.items():
            if k == "source_ids" and isinstance(v, list):
                v = json.dumps(v, ensure_ascii=False)
            sets.append(f"{k} = ?")
            params.append(v)
        sets.append("updated_at = ?")
        params.append(int(time.time()))
        params.append(topic_id)
        self.store.execute_sql(
            f"UPDATE distill_topics SET {', '.join(sets)} WHERE topic_id = ?", params
        )

    def _insert_entity(self, ent: dict):
        self.store.execute_sql(
            """INSERT OR REPLACE INTO distill_entities
               (entity_id, name, entity_type, attributes, source_topics, importance, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (ent["entity_id"], ent["name"], ent["entity_type"],
             ent.get("attributes", "{}"), ent.get("source_topics", "[]"),
             ent.get("importance", "medium"), int(time.time()), int(time.time())),
        )

    def _update_entity(self, ent: dict):
        self.store.execute_sql(
            """UPDATE distill_entities SET attributes = ?, source_topics = ?, updated_at = ?
               WHERE entity_id = ?""",
            (ent.get("attributes", "{}"), ent.get("source_topics", "[]"),
             int(time.time()), ent["entity_id"]),
        )

    def _insert_relation(self, rel: dict):
        self.store.execute_sql(
            """INSERT OR IGNORE INTO distill_relations
               (relation_id, source_entity, target_entity, relation_type, attributes, source_topics, confidence, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (rel["relation_id"], rel["source_entity"], rel["target_entity"],
             rel["relation_type"], rel.get("attributes", "{}"),
             rel.get("source_topics", "[]"), rel.get("confidence", 0.8),
             int(time.time())),
        )

    def _get_encyclopedia_entry_by_category(self, category: str) -> dict | None:
        rows = self.store.execute_sql(
            "SELECT * FROM distill_encyclopedia WHERE category = ? ORDER BY last_updated DESC LIMIT 1",
            (category,),
            fetch=True,
        )
        return rows[0] if rows else None

    def _insert_encyclopedia_entry(self, **kwargs):
        self.store.execute_sql(
            """INSERT OR REPLACE INTO distill_encyclopedia
               (entry_id, title, content, category, source_entities, source_topics, last_updated, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (kwargs["entry_id"], kwargs["title"], kwargs["content"],
             kwargs["category"], kwargs.get("source_entities", "[]"),
             kwargs.get("source_topics", "[]"), int(time.time()), int(time.time())),
        )

    def _update_encyclopedia_entry(self, entry_id: str, content: str):
        self.store.execute_sql(
            "UPDATE distill_encyclopedia SET content = ?, last_updated = ? WHERE entry_id = ?",
            (content, int(time.time()), entry_id),
        )

    def _merge_encyclopedia_content(self, existing: dict, new_entities: list[dict], topics: list[dict]) -> str:
        """将新实体合并到已有百科条目"""
        return self._heuristic_generate_encyclopedia(
            existing.get("category", "concepts"),
            new_entities,
            topics,
        )
