#!/usr/bin/env python3
"""
Shared Memory Knowledge Base - Main Script

提供跨身份共享记忆的核心功能：
- store: 写入记忆
- query: 检索记忆
- list: 浏览知识体系
- link: 关联记忆
- reflect: 定期回顾
"""

import argparse
import json
import os
import random
import string
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


class MemoryKB:
    """共享记忆知识库主类"""

    def __init__(self, custom_path: Optional[str] = None):
        """
        初始化知识库

        Args:
            custom_path: 自定义存储路径（可选）
        """
        self.base_path = Path(custom_path or os.environ.get("MEMORY_KB_PATH", "~/.openclaw/memory"))
        self.base_path = self.base_path.expanduser()
        self.memories_file = self.base_path / "memories.jsonl"
        self.index_dir = self.base_path / "index"
        self.meta_file = self.base_path / "meta.json"

        # 确保目录结构存在
        self._ensure_structure()

    def _ensure_structure(self) -> None:
        """确保目录结构和文件存在"""
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.index_dir.mkdir(exist_ok=True)

        # 初始化 meta.json
        if not self.meta_file.exists():
            meta = {
                "version": "1.0.0",
                "total_entries": 0,
                "active_entries": 0,
                "deleted_entries": 0,
                "last_updated": datetime.now(timezone.utc).isoformat(),
                "personas": {},
                "categories": {},
                "top_tags": [],
            }
            self._write_meta(meta)

        # 初始化索引文件
        index_files = ["by_persona.json", "by_category.json", "by_tag.json", "by_date.json"]
        for index_file in index_files:
            index_path = self.index_dir / index_file
            if not index_path.exists():
                index_path.write_text("{}")

        # 初始化配置文件（如果不存在）
        self.config_file = self.base_path / "config.json"
        self._load_config()

    def _load_config(self) -> None:
        """加载配置文件"""
        default_config = {
            "auto_write_sensitivity": "medium",
            "min_content_length": 20,
            "max_content_length": 2000,
            "max_tags_count": 10,
            "max_tag_length": 20,
            "auto_link_threshold": 0.5,
            "importance_auto_adjust": True,
            "importance_recalc_days": 30,
        }

        if self.config_file.exists():
            try:
                user_config = json.loads(self.config_file.read_text(encoding="utf-8"))
                default_config.update(user_config)
            except (json.JSONDecodeError, IOError):
                pass

        self.config = default_config

    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置项"""
        return self.config.get(key, default)

    def _generate_id(self) -> str:
        """生成唯一的记忆 ID"""
        date_str = datetime.now().strftime("%Y%m%d")
        chars = string.ascii_lowercase + string.digits
        random_str = "".join(random.choices(chars, k=6))
        return f"mem_{date_str}_{random_str}"

    def _read_memories(self) -> List[Dict[str, Any]]:
        """读取所有活跃记忆（过滤已删除）"""
        if not self.memories_file.exists():
            return []

        memories = []
        with open(self.memories_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    entry = json.loads(line)
                    if not entry.get("deleted", False):
                        memories.append(entry)

        return memories

    def _write_memory(self, entry: Dict[str, Any]) -> None:
        """追加写入记忆到主文件"""
        with open(self.memories_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def _read_index(self, index_name: str) -> Dict[str, List[str]]:
        """读取索引文件"""
        index_path = self.index_dir / index_name
        if index_path.exists():
            return json.loads(index_path.read_text(encoding="utf-8"))
        return {}

    def _write_index(self, index_name: str, data: Dict[str, List[str]]) -> None:
        """写入索引文件"""
        index_path = self.index_dir / index_name
        index_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _read_meta(self) -> Dict[str, Any]:
        """读取元数据"""
        if self.meta_file.exists():
            return json.loads(self.meta_file.read_text(encoding="utf-8"))
        return {}

    def _write_meta(self, meta: Dict[str, Any]) -> None:
        """写入元数据"""
        self.meta_file.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")

    def _update_indexes(self, entry: Dict[str, Any]) -> None:
        """更新所有索引"""
        # 更新 by_persona
        persona_index = self._read_index("by_persona.json")
        persona = entry["persona"]
        if persona not in persona_index:
            persona_index[persona] = []
        persona_index[persona].append(entry["id"])
        self._write_index("by_persona.json", persona_index)

        # 更新 by_category
        category_index = self._read_index("by_category.json")
        category = entry["category"]
        if category not in category_index:
            category_index[category] = []
        category_index[category].append(entry["id"])
        self._write_index("by_category.json", category_index)

        # 更新 by_tag
        tag_index = self._read_index("by_tag.json")
        for tag in entry.get("tags", []):
            if tag not in tag_index:
                tag_index[tag] = []
            tag_index[tag].append(entry["id"])
        self._write_index("by_tag.json", tag_index)

        # 更新 by_date
        date_index = self._read_index("by_date.json")
        date_str = entry["created_at"][:10]
        if date_str not in date_index:
            date_index[date_str] = []
        date_index[date_str].append(entry["id"])
        self._write_index("by_date.json", date_index)

    def _update_meta(self, entry: Dict[str, Any]) -> None:
        """更新元数据统计"""
        meta = self._read_meta()

        meta["total_entries"] += 1
        meta["active_entries"] += 1
        meta["last_updated"] = datetime.now(timezone.utc).isoformat()

        # 更新 personas 统计
        persona = entry["persona"]
        meta["personas"][persona] = meta["personas"].get(persona, 0) + 1

        # 更新 categories 统计
        category = entry["category"]
        meta["categories"][category] = meta["categories"].get(category, 0) + 1

        # 更新 top_tags（需要重新计算）
        all_memories = self._read_memories()
        tag_counts = {}
        for mem in all_memories:
            for tag in mem.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

        meta["top_tags"] = sorted(tag_counts.keys(), key=lambda x: tag_counts[x], reverse=True)[:10]

        self._write_meta(meta)

    def store(
        self,
        content: str,
        persona: str = "通用",
        category: str = "",
        tags: Optional[List[str]] = None,
        type_: str = "经验",
        importance: int = 3,
        scene: str = "",
        source_context: str = "",
    ) -> Dict[str, Any]:
        """
        写入记忆

        Args:
            content: 记忆正文，20-2000 字符
            persona: 来源身份
            category: 知识分类
            tags: 标签列表
            type_: 记忆类型
            importance: 重要度 1-5
            scene: 场景描述
            source_context: 来源描述

        Returns:
            包含写入结果的字典
        """
        # 验证内容长度（使用配置值）
        content_len = len(content)
        min_content_len = self.get_config("min_content_length", 20)
        max_content_len = self.get_config("max_content_length", 2000)
        if content_len < min_content_len:
            return {"success": False, "error": f"内容长度不足 {min_content_len} 字符（当前 {content_len} 字符）"}
        if content_len > max_content_len:
            return {"success": False, "error": f"内容长度超过 {max_content_len} 字符（当前 {content_len} 字符），建议拆分为多条存储"}

        # 验证重要度
        if not 1 <= importance <= 5:
            return {"success": False, "error": f"重要度必须在 1-5 之间（当前 {importance}）"}

        # 验证标签数量和长度（使用配置值）
        max_tags_count = self.get_config("max_tags_count", 10)
        max_tag_length = self.get_config("max_tag_length", 20)
        if tags and len(tags) > max_tags_count:
            return {"success": False, "error": f"标签数量不能超过 {max_tags_count} 个（当前 {len(tags)} 个）"}
        if tags:
            for tag in tags:
                if len(tag) > max_tag_length:
                    return {"success": False, "error": f"标签长度不能超过 {max_tag_length} 字符（当前 '{tag}' 有 {len(tag)} 字符）"}

        # 默认值处理
        if not category:
            category = "思考"
        if tags is None:
            tags = []

        # 生成记忆条目
        now = datetime.now(timezone.utc)
        entry = {
            "id": self._generate_id(),
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "deleted": False,
            "persona": persona,
            "category": category,
            "scene": scene[:100] if scene else "",
            "content": content,
            "tags": tags,
            "type": type_,
            "importance": importance,
            "linked_ids": [],
            "source_context": source_context[:200] if source_context else "",
        }

        # 写入主文件
        self._write_memory(entry)

        # 更新索引和元数据
        self._update_indexes(entry)
        self._update_meta(entry)

        # 检查相似记忆（简单关键词匹配）
        similar_memories = self._find_similar(entry)

        return {
            "success": True,
            "id": entry["id"],
            "tags": tags,
            "similar_memories": similar_memories,
            "message": "记忆已成功写入",
        }

    def _find_similar(self, entry: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
        """
        查找相似记忆（增强版）

        综合考虑标签匹配和内容关键词重叠，计算相似度分数

        Args:
            entry: 要查找相似记忆的条目
            limit: 返回结果数量限制

        Returns:
            相似记忆列表，每条包含 similarity_score 字段
        """
        all_memories = self._read_memories()
        entry_tags = set(entry.get("tags", []))
        entry_keywords = self._extract_keywords(entry["content"])

        threshold = self.get_config("auto_link_threshold", 0.5)
        scored = []

        for mem in all_memories:
            if mem["id"] == entry["id"]:
                continue

            mem_tags = set(mem.get("tags", []))
            mem_keywords = self._extract_keywords(mem["content"])

            # 计算标签相似度（权重 0.6）
            if entry_tags and mem_tags:
                tag_intersection = entry_tags & mem_tags
                tag_union = entry_tags | mem_tags
                tag_similarity = len(tag_intersection) / len(tag_union) if tag_union else 0
            else:
                tag_similarity = 0

            # 计算内容关键词相似度（权重 0.4）
            if entry_keywords and mem_keywords:
                keyword_intersection = entry_keywords & mem_keywords
                keyword_union = entry_keywords | mem_keywords
                keyword_similarity = len(keyword_intersection) / len(keyword_union) if keyword_union else 0
            else:
                keyword_similarity = 0

            # 综合相似度
            similarity = (tag_similarity * 0.6) + (keyword_similarity * 0.4)

            # 只返回超过阈值的相似记忆
            if similarity >= threshold:
                mem_copy = mem.copy()
                mem_copy["similarity_score"] = round(similarity, 3)
                scored.append((similarity, mem_copy))

        # 按相似度排序
        scored.sort(key=lambda x: x[0], reverse=True)

        return [mem for score, mem in scored[:limit]]

    def _extract_keywords(self, text: str) -> Set[str]:
        """
        从文本中提取关键词

        简单实现：提取长度>=2的词汇，去除停用词
        未来可使用更复杂的 NLP 算法

        Args:
            text: 输入文本

        Returns:
            关键词集合
        """
        import re
        words = re.findall(r'\w+', text.lower())

        # 停用词（中英文）
        stop_words = {
            '的', '了', '是', '在', '我', '你', '他', '她', '它', '我们', '你们', '他们',
            '这', '那', '这个', '那个', '一个', '一些', '有', '没有', '不', '也', '就',
            'and', 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'into',
        }

        # 过滤停用词和短词
        keywords = {word for word in words if len(word) >= 2 and word not in stop_words}

        return keywords

    def query(
        self,
        q: str = "",
        persona: str = "all",
        category: str = "",
        tags: Optional[List[str]] = None,
        type_: str = "",
        since: str = "",
        until: str = "",
        limit: int = 10,
        importance_min: int = 0,
    ) -> Dict[str, Any]:
        """
        检索记忆

        Args:
            q: 关键词搜索
            persona: 身份过滤，"all" 为全局
            category: 分类过滤
            tags: 标签过滤（AND 逻辑）
            type_: 类型过滤
            since: 时间起点（ISO8601 或 "7d"/"30d"）
            until: 时间终点
            limit: 返回数量，最大 50
            importance_min: 最低重要度

        Returns:
            包含检索结果的字典
        """
        # 解析时间范围
        since_dt, until_dt = self._parse_time_range(since, until)

        # 获取候选集
        candidate_ids = self._get_candidate_ids(persona, category, tags, since_dt, until_dt)

        # 读取记忆并过滤
        all_memories = self._read_memories()
        memory_map = {mem["id"]: mem for mem in all_memories}

        # 过滤候选集
        filtered = []
        for mem_id in candidate_ids:
            if mem_id not in memory_map:
                continue
            mem = memory_map[mem_id]

            # 应用时间过滤
            if since_dt and mem["created_at"] < since_dt.isoformat():
                continue
            if until_dt and mem["created_at"] > until_dt.isoformat():
                continue

            # 应用类型过滤
            if type_ and mem["type"] != type_:
                continue

            # 应用重要度过滤
            if importance_min > 0 and mem["importance"] < importance_min:
                continue

            filtered.append(mem)

        # 关键词匹配
        if q:
            filtered = [mem for mem in filtered if q.lower() in mem["content"].lower()]

        # 计算相关度并排序
        scored = self._calculate_relevance(filtered, q, importance_min)

        # 限制返回数量
        limit = min(limit, 50)
        results = scored[:limit]

        return {
            "total": len(results),
            "results": results,
        }

    def _parse_time_range(self, since: str, until: str) -> tuple[Optional[datetime], Optional[datetime]]:
        """解析时间范围"""
        now = datetime.now(timezone.utc)

        since_dt = None
        if since:
            if since.endswith("d"):
                days = int(since[:-1])
                since_dt = now - timedelta(days=days)
            else:
                try:
                    since_dt = datetime.fromisoformat(since)
                except ValueError:
                    pass

        until_dt = None
        if until:
            try:
                until_dt = datetime.fromisoformat(until)
            except ValueError:
                pass

        return since_dt, until_dt

    def _get_candidate_ids(
        self,
        persona: str,
        category: str,
        tags: Optional[List[str]],
        since_dt: Optional[datetime],
        until_dt: Optional[datetime],
    ) -> Set[str]:
        """获取候选记忆 ID 集合（利用索引）"""
        candidate_sets = []

        # 按身份过滤
        if persona != "all":
            persona_index = self._read_index("by_persona.json")
            if persona in persona_index:
                candidate_sets.append(set(persona_index[persona]))
            else:
                return set()  # 无匹配，直接返回空集
        else:
            # 全局检索，不使用身份索引
            candidate_sets.append(None)

        # 按分类过滤
        if category:
            category_index = self._read_index("by_category.json")
            if category in category_index:
                candidate_sets.append(set(category_index[category]))
            else:
                return set()

        # 按标签过滤（AND 逻辑）
        if tags:
            tag_index = self._read_index("by_tag.json")
            tag_sets = []
            for tag in tags:
                if tag in tag_index:
                    tag_sets.append(set(tag_index[tag]))
                else:
                    return set()  # 某个标签不存在，无匹配
            if tag_sets:
                candidate_sets.append(set.intersection(*tag_sets))

        # 合并候选集
        valid_sets = [s for s in candidate_sets if s is not None]
        if not valid_sets:
            # 无索引过滤条件，返回所有记忆 ID
            all_memories = self._read_memories()
            return {mem["id"] for mem in all_memories}

        # 取交集
        return set.intersection(*valid_sets)

    def _calculate_relevance(self, memories: List[Dict[str, Any]], q: str, importance_min: int) -> List[Dict[str, Any]]:
        """计算相关度并排序"""
        for mem in memories:
            score = 0

            # 关键词命中
            if q:
                content_lower = mem["content"].lower()
                hits = content_lower.count(q.lower())
                score += hits * 10

            # 重要度加权
            if importance_min > 0:
                if mem["importance"] >= importance_min:
                    score += mem["importance"] * 5
            else:
                score += mem["importance"]

            # 标签数量加权
            score += len(mem.get("tags", [])) * 2

            mem["_relevance_score"] = score

        # 按相关度排序（降序）
        return sorted(memories, key=lambda x: x["_relevance_score"], reverse=True)

    def list_aggregate(self, by: str, persona: Optional[str] = None) -> Dict[str, Any]:
        """
        按指定维度聚合展示知识体系

        Args:
            by: 聚合维度（persona / category / tag / type / date）
            persona: 指定身份（可选）

        Returns:
            聚合结果
        """
        all_memories = self._read_memories()

        # 如果指定了身份，先过滤
        if persona:
            all_memories = [mem for mem in all_memories if mem["persona"] == persona]

        result = {}

        if by == "persona":
            for mem in all_memories:
                persona = mem["persona"]
                if persona not in result:
                    result[persona] = 0
                result[persona] += 1

        elif by == "category":
            for mem in all_memories:
                category = mem["category"]
                if category not in result:
                    result[category] = 0
                result[category] += 1

        elif by == "tag":
            for mem in all_memories:
                for tag in mem.get("tags", []):
                    if tag not in result:
                        result[tag] = 0
                    result[tag] += 1

        elif by == "type":
            for mem in all_memories:
                type_ = mem["type"]
                if type_ not in result:
                    result[type_] = 0
                result[type_] += 1

        elif by == "date":
            for mem in all_memories:
                date_str = mem["created_at"][:10]
                if date_str not in result:
                    result[date_str] = 0
                result[date_str] += 1

        else:
            return {"error": f"无效的聚合维度: {by}"}

        # 获取最近记录预览（最多 5 条）
        recent_memories = sorted(all_memories, key=lambda x: x["created_at"], reverse=True)[:5]

        return {
            "aggregate": result,
            "recent_memories": recent_memories,
        }

    def link(self, id_a: str, id_b: str, relation: str = "") -> Dict[str, Any]:
        """
        关联两条记忆

        Args:
            id_a: 第一条记忆 ID
            id_b: 第二条记忆 ID
            relation: 关联描述

        Returns:
            关联结果
        """
        all_memories = self._read_memories()
        memory_map = {mem["id"]: mem for mem in all_memories}

        # 验证 ID
        if id_a not in memory_map:
            return {"success": False, "error": f"记忆 ID {id_a} 不存在"}
        if id_b not in memory_map:
            return {"success": False, "error": f"记忆 ID {id_b} 不存在"}
        if id_a == id_b:
            return {"success": False, "error": "不能关联同一条记忆"}

        mem_a = memory_map[id_a]
        mem_b = memory_map[id_b]

        # 双向关联
        if id_b not in mem_a.get("linked_ids", []):
            mem_a.setdefault("linked_ids", []).append(id_b)
        if id_a not in mem_b.get("linked_ids", []):
            mem_b.setdefault("linked_ids", []).append(id_a)

        # 更新关联描述（可选）
        if relation:
            mem_a["_relation_" + id_b] = relation
            mem_b["_relation_" + id_a] = relation

        # 更新记录（创建新版本）
        self._update_entry(mem_a)
        self._update_entry(mem_b)

        return {
            "success": True,
            "message": f"已关联记忆 {id_a} 和 {id_b}",
            "relation": relation,
        }

    def _update_entry(self, entry: Dict[str, Any]) -> None:
        """更新记忆条目（创建新版本）"""
        # 标记旧版本为已删除
        entry["deleted"] = True
        entry["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._write_memory(entry)

        # 创建新版本
        new_entry = entry.copy()
        new_entry.pop("deleted", None)
        new_entry["updated_at"] = datetime.now(timezone.utc).isoformat()
        self._write_memory(new_entry)

    def reflect(
        self,
        period: str,
        since: Optional[str] = None,
        until: Optional[str] = None,
        persona: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        生成时间段内的知识回顾

        Args:
            period: 周期类型（"week" / "month" / "custom"）
            since: 自定义周期起点
            until: 自定义周期终点
            persona: 指定身份

        Returns:
            回顾数据（供 LLM 生成摘要）
        """
        now = datetime.now(timezone.utc)

        # 计算时间范围
        if period == "week":
            since_dt = now - timedelta(days=7)
            until_dt = now
        elif period == "month":
            since_dt = now - timedelta(days=30)
            until_dt = now
        elif period == "custom":
            if not since or not until:
                return {"error": "自定义周期需要提供 since 和 until 参数"}
            since_dt = datetime.fromisoformat(since)
            until_dt = datetime.fromisoformat(until)
        else:
            return {"error": f"无效的周期类型: {period}"}

        # 获取时间段内的记忆
        all_memories = self._read_memories()
        period_memories = []
        for mem in all_memories:
            mem_dt = datetime.fromisoformat(mem["created_at"])
            if since_dt <= mem_dt <= until_dt:
                if persona is None or mem["persona"] == persona:
                    period_memories.append(mem)

        # 统计数据
        total_entries = len(period_memories)

        personas_dist = {}
        categories_dist = {}
        tag_counts = {}
        important_entries = []

        for mem in period_memories:
            # 身份分布
            personas_dist[mem["persona"]] = personas_dist.get(mem["persona"], 0) + 1

            # 分类分布
            categories_dist[mem["category"]] = categories_dist.get(mem["category"], 0) + 1

            # 标签统计
            for tag in mem.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1

            # 重要记录
            if mem["importance"] >= 4:
                important_entries.append(mem)

        # 高频标签 Top 5
        top_tags = sorted(tag_counts.keys(), key=lambda x: tag_counts[x], reverse=True)[:5]

        return {
            "period": period,
            "since": since_dt.isoformat(),
            "until": until_dt.isoformat(),
            "total_entries": total_entries,
            "personas_dist": personas_dist,
            "categories_dist": categories_dist,
            "top_tags": top_tags,
            "important_entries": important_entries,
            "all_entries": period_memories,
        }

    def rebuild_index(self) -> Dict[str, Any]:
        """重建所有索引"""
        print("开始重建索引...")

        # 读取所有记忆（包括已删除）
        all_entries = []
        if self.memories_file.exists():
            with open(self.memories_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        all_entries.append(json.loads(line))

        # 清空索引
        persona_index = {}
        category_index = {}
        tag_index = {}
        date_index = {}

        # 重建索引（仅包含活跃记录）
        active_entries = [e for e in all_entries if not e.get("deleted", False)]

        for entry in active_entries:
            # by_persona
            persona = entry["persona"]
            if persona not in persona_index:
                persona_index[persona] = []
            persona_index[persona].append(entry["id"])

            # by_category
            category = entry["category"]
            if category not in category_index:
                category_index[category] = []
            category_index[category].append(entry["id"])

            # by_tag
            for tag in entry.get("tags", []):
                if tag not in tag_index:
                    tag_index[tag] = []
                tag_index[tag].append(entry["id"])

            # by_date
            date_str = entry["created_at"][:10]
            if date_str not in date_index:
                date_index[date_str] = []
            date_index[date_str].append(entry["id"])

        # 写入索引文件
        self._write_index("by_persona.json", persona_index)
        self._write_index("by_category.json", category_index)
        self._write_index("by_tag.json", tag_index)
        self._write_index("by_date.json", date_index)

        # 重建 meta.json
        meta = {
            "version": "1.0.0",
            "total_entries": len(all_entries),
            "active_entries": len(active_entries),
            "deleted_entries": len(all_entries) - len(active_entries),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "personas": {k: len(v) for k, v in persona_index.items()},
            "categories": {k: len(v) for k, v in category_index.items()},
            "top_tags": sorted(tag_index.keys(), key=lambda x: len(tag_index[x]), reverse=True)[:10],
        }
        self._write_meta(meta)

        print(f"索引重建完成！共处理 {len(active_entries)} 条活跃记录。")

        return {
            "success": True,
            "active_entries": len(active_entries),
            "deleted_entries": len(all_entries) - len(active_entries),
        }

    def recalc_importance(self, dry_run: bool = False) -> Dict[str, Any]:
        """
        自动调整重要度

        基于检索频率、关联频率、时间衰减等因素重新计算重要度

        Args:
            dry_run: 是否仅预览不实际更新

        Returns:
            调整结果
        """
        if not self.get_config("importance_auto_adjust", True):
            return {
                "success": False,
                "error": "重要度自动调整功能未启用，请在 config.json 中设置 importance_auto_adjust=true"
            }

        print("开始重新计算重要度...")

        all_memories = self._read_memories()
        updated_entries = []

        for mem in all_memories:
            base_importance = mem["importance"]

            # 检索频率加成（从 meta.json 获取）
            meta = self._read_meta()
            query_stats = meta.get("query_stats", {})
            query_count = query_stats.get(mem["id"], 0)
            query_bonus = min(query_count * 0.5, 2.0)

            # 关联频率加成
            link_count = len(mem.get("linked_ids", []))
            link_bonus = link_count * 0.3

            # 时间衰减（天数 / 365 * 0.5）
            created_dt = datetime.fromisoformat(mem["created_at"])
            days_since_creation = (datetime.now(timezone.utc) - created_dt).days
            time_decay = (days_since_creation / 365) * 0.5

            # 计算新重要度
            new_importance = base_importance + query_bonus + link_bonus - time_decay

            # 限制在 1-5 范围内
            new_importance = max(1, min(5, round(new_importance)))

            # 记录变化
            if new_importance != base_importance:
                updated_entries.append({
                    "id": mem["id"],
                    "old_importance": base_importance,
                    "new_importance": new_importance,
                    "reason": f"检索次数:{query_count}, 关联数:{link_count}, 时间衰减:{time_decay:.2f}"
                })

                if not dry_run:
                    # 更新记录（创建新版本）
                    mem["importance"] = new_importance
                    mem["updated_at"] = datetime.now(timezone.utc).isoformat()
                    self._update_entry(mem)

        print(f"重要度重新计算完成！共调整 {len(updated_entries)} 条记忆。")

        return {
            "success": True,
            "updated_count": len(updated_entries),
            "dry_run": dry_run,
            "changes": updated_entries,
        }


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="Shared Memory Knowledge Base")
    parser.add_argument("action", choices=["store", "query", "list", "link", "reflect", "rebuild-index", "recalc-importance"], help="操作类型")
    parser.add_argument("--content", help="记忆正文")
    parser.add_argument("--persona", default="", help="来源身份")
    parser.add_argument("--category", default="", help="知识分类")
    parser.add_argument("--tags", help="标签列表（JSON 数组）")
    parser.add_argument("--type", dest="type_", default="经验", help="记忆类型")
    parser.add_argument("--importance", type=int, default=3, help="重要度 1-5")
    parser.add_argument("--scene", default="", help="场景描述")
    parser.add_argument("--source-context", dest="source_context", default="", help="来源描述")
    parser.add_argument("--q", default="", help="查询关键词")
    parser.add_argument("--since", default="", help="时间起点")
    parser.add_argument("--until", default="", help="时间终点")
    parser.add_argument("--limit", type=int, default=10, help="返回数量")
    parser.add_argument("--importance-min", type=int, default=0, help="最低重要度")
    parser.add_argument("--by", help="聚合维度")
    parser.add_argument("--id-a", help="第一条记忆 ID")
    parser.add_argument("--id-b", help="第二条记忆 ID")
    parser.add_argument("--relation", default="", help="关联描述")
    parser.add_argument("--period", help="周期类型")
    parser.add_argument("--custom-path", help="自定义存储路径")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际更新")

    return parser.parse_args()


def main():
    """主函数"""
    args = parse_args()

    # 初始化知识库
    kb = MemoryKB(custom_path=args.custom_path)

    # 执行操作
    result = {}

    if args.action == "store":
        tags = json.loads(args.tags) if args.tags else None
        result = kb.store(
            content=args.content,
            persona=args.persona or "通用",
            category=args.category,
            tags=tags,
            type_=args.type_,
            importance=args.importance,
            scene=args.scene,
            source_context=args.source_context,
        )

    elif args.action == "query":
        tags = json.loads(args.tags) if args.tags else None
        result = kb.query(
            q=args.q,
            persona=args.persona,
            category=args.category,
            tags=tags,
            type_=args.type_,
            since=args.since,
            until=args.until,
            limit=args.limit,
            importance_min=args.importance_min,
        )

    elif args.action == "list":
        if not args.by:
            result = {"error": "list 操作需要提供 --by 参数（persona/category/tag/type/date）"}
        else:
            result = kb.list_aggregate(by=args.by, persona=args.persona)

    elif args.action == "link":
        result = kb.link(id_a=args.id_a, id_b=args.id_b, relation=args.relation)

    elif args.action == "reflect":
        result = kb.reflect(
            period=args.period,
            since=args.since,
            until=args.until,
            persona=args.persona,
        )

    elif args.action == "rebuild-index":
        result = kb.rebuild_index()

    elif args.action == "recalc-importance":
        result = kb.recalc_importance(dry_run=args.dry_run)

    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
