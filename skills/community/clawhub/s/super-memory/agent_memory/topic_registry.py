"""
topic_registry.py - 动态主题注册表
支持自动发现新主题并注册到 dimensions.json
"""

from __future__ import annotations

import json
import os
import re
import time
from pathlib import Path


class TopicRegistry:
    """管理动态主题的注册、相似度计算、持久化"""

    REGISTRY_PATH = Path(__file__).parent / "dimensions.json"

    # 相似度阈值：低于此值创建新主题
    SIMILARITY_THRESHOLD = 0.5

    # 新主题创建时的默认父路径
    DEFAULT_PARENT = "misc"

    def __init__(self, registry_path: str = None):
        self.path = Path(registry_path) if registry_path else self.REGISTRY_PATH
        self._load()

    def _load(self):
        with open(self.path, "r", encoding="utf-8") as f:
            self.registry = json.load(f)
        # 构建关键词索引
        self._topic_keywords: dict[str, list[str]] = {}
        self._build_keyword_index(self.registry["topics"], "")

    def _build_keyword_index(self, node: dict, prefix: str):
        """递归构建 topic_path → [keywords] 索引"""
        for key, val in node.items():
            full_path = f"{prefix}.{key}" if prefix else key
            # 叶子节点或有显式 keywords 的节点
            if "keywords" in val:
                self._topic_keywords[full_path] = val["keywords"]
            # 递归子节点
            if "children" in val:
                self._build_keyword_index(val["children"], full_path)

    def merge_keywords(self, keyword_map: dict[str, list[str]]):
        """合并外部关键词映射（如 TopicDetector 的 keyword_map）"""
        for topic, kws in keyword_map.items():
            if topic not in self._topic_keywords:
                self._topic_keywords[topic] = kws
            else:
                # 合并去重
                existing = set(self._topic_keywords[topic])
                existing.update(kws)
                self._topic_keywords[topic] = list(existing)

    def _save(self):
        """写回 dimensions.json（原子写入）"""
        tmp = str(self.path) + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(self.registry, f, ensure_ascii=False, indent=4)
        os.replace(tmp, str(self.path))

    # ── 相似度计算 ────────────────────────────────────────

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        """分词：英文词 + 中文 bigram"""
        en_words = set(re.findall(r"[a-zA-Z_][a-zA-Z0-9_]*", text.lower()))
        cn_bigrams = set()
        for seg in re.findall(r"[\u4e00-\u9fff]+", text):
            for i in range(len(seg) - 1):
                cn_bigrams.add(seg[i:i+2])
        return en_words | cn_bigrams

    def similarity(self, text: str, topic_path: str) -> float:
        """
        计算文本与主题的相似度。

        关键词子串匹配，命中即得分。
        1个命中 = 0.5，2个 = 0.7，3个+ = 0.9
        """
        keywords = self._topic_keywords.get(topic_path, [])
        if not keywords:
            return 0.0

        text_lower = text.lower()
        hits = sum(1 for kw in keywords if kw.lower() in text_lower)

        if hits == 0:
            return 0.0
        elif hits == 1:
            return 0.5
        elif hits == 2:
            return 0.7
        else:
            return 0.9

    def find_best_match(self, text: str, existing_topics: list[str] = None) -> tuple[str, float]:
        """
        找到与文本最匹配的现有主题。

        返回: (topic_path, similarity_score)
        """
        candidates = existing_topics or list(self._topic_keywords.keys())
        if not candidates:
            candidates = self._all_topic_paths()

        best_path = ""
        best_score = 0.0

        for topic in candidates:
            score = self.similarity(text, topic)
            if score > best_score:
                best_score = score
                best_path = topic

        return (best_path, best_score)

    def _all_topic_paths(self) -> list[str]:
        """获取所有已注册的主题路径"""
        paths = []
        self._collect_paths(self.registry["topics"], "", paths)
        return paths

    def _collect_paths(self, node: dict, prefix: str, paths: list):
        for key, val in node.items():
            full = f"{prefix}.{key}" if prefix else key
            # 叶子节点（无 children 或 children 为空）
            if "children" not in val or not val["children"]:
                paths.append(full)
            if "children" in val:
                self._collect_paths(val["children"], full, paths)

    # ── 动态注册 ──────────────────────────────────────────

    def register_topic(
        self,
        topic_path: str,
        name: str = None,
        keywords: list[str] = None,
        parent_path: str = None,
    ) -> dict:
        """
        注册一个新主题到 dimensions.json。

        参数:
            topic_path: 完整路径，如 "ai.rag.vdb"
            name: 显示名称，不传则取路径最后一段
            keywords: 关键词列表
            parent_path: 父路径，不传则自动从 topic_path 推导

        返回: {"path": str, "name": str, "keywords": list, "is_new": bool}
        """
        # 检查是否已存在
        parts = topic_path.split(".")
        node = self.registry["topics"]
        exists = True
        for p in parts:
            if p not in node:
                exists = False
                break
            if "children" in node[p]:
                node = node[p]["children"]

        if exists:
            return {"path": topic_path, "name": name or parts[-1], "keywords": keywords or [], "is_new": False}

        # 确定父路径
        if parent_path is None:
            if len(parts) > 1:
                parent_path = ".".join(parts[:-1])
            else:
                parent_path = self.DEFAULT_PARENT
                topic_path = f"{parent_path}.{topic_path}"
                parts = topic_path.split(".")

        # 导航到父节点，创建缺失路径
        node = self.registry["topics"]
        parent_parts = parent_path.split(".") if parent_path else []

        # 先确保父路径存在
        for p in parent_parts:
            if p not in node:
                node[p] = {"name": p, "children": {}}
            if "children" not in node[p]:
                node[p]["children"] = {}
            node = node[p]["children"]

        # 创建新主题节点
        leaf_name = parts[-1]
        new_node = {"name": name or leaf_name}
        if keywords:
            new_node["keywords"] = keywords

        node[leaf_name] = new_node

        # 持久化
        self._save()

        # 更新本地索引
        self._topic_keywords[topic_path] = keywords or []

        return {"path": topic_path, "name": name or leaf_name, "keywords": keywords or [], "is_new": True}

    def auto_register(self, text: str, suggested_path: str = None, keywords: list[str] = None) -> dict:
        """
        自动注册逻辑：
        1. 先找最接近的现有主题
        2. 相似度 >= 阈值 → 返回匹配的主题
        3. 相似度 < 阈值 → 创建新主题

        参数:
            text: 原始对话文本
            suggested_path: LLM 建议的主题路径（可选）
            keywords: 从文本提取的关键词（可选）

        返回: {"path": str, "matched": bool, "similarity": float, "is_new": bool}
        """
        # 先尝试用 suggested_path 精确匹配
        if suggested_path:
            existing = self._all_topic_paths()
            if suggested_path in existing:
                return {"path": suggested_path, "matched": True, "similarity": 1.0, "is_new": False}

        # 计算与所有现有主题的相似度
        best_path, best_score = self.find_best_match(text)

        if best_score >= self.SIMILARITY_THRESHOLD:
            return {"path": best_path, "matched": True, "similarity": best_score, "is_new": False}

        # 相似度不足 → 创建新主题
        if suggested_path:
            new_path = suggested_path
        elif best_path:
            # 在最相似的主题下创建子主题
            new_keywords = keywords or self._extract_keywords(text)
            slug = self._make_slug(new_keywords)
            # 避免 slug 和 best_path 的最后一段重复
            path_parts = best_path.split(".")
            if slug == path_parts[-1]:
                slug = f"{slug}_sub"
            new_path = f"{best_path}.{slug}"
        else:
            # 完全没有匹配，放到 misc 下
            new_keywords = keywords or self._extract_keywords(text)
            slug = self._make_slug(new_keywords)
            new_path = f"misc.{slug}"

        result = self.register_topic(
            topic_path=new_path,
            keywords=keywords or self._extract_keywords(text),
        )

        return {"path": new_path, "matched": False, "similarity": best_score, "is_new": True}

    def _extract_keywords(self, text: str) -> list[str]:
        """从文本提取简单关键词（用于新主题命名）"""
        # 英文词
        en = re.findall(r"[a-zA-Z]{3,}", text.lower())
        # 中文2-4字词（简单提取）
        cn = re.findall(r"[\u4e00-\u9fff]{2,4}", text)

        # 去停用词
        stop_en = {"the", "and", "for", "are", "but", "not", "you", "all", "can", "her", "was", "one", "our"}
        stop_cn = {"的", "了", "是在", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好"}

        keywords = [w for w in en if w not in stop_en][:3]
        keywords += [w for w in cn if w not in stop_cn][:3]
        return keywords[:5]

    def _make_slug(self, keywords: list[str]) -> str:
        """
        从关键词生成合格的 topic slug。

        优先英文词，其次中文词转拼音风格，兜底时间戳。
        slug 只含 [a-z0-9_-]，长度 2-20。
        """
        if not keywords:
            return f"t{int(time.time()) % 100000}"

        # 优先选英文词
        for kw in keywords:
            clean = re.sub(r"[^a-zA-Z0-9_-]", "", kw.lower()).strip("-_")
            if len(clean) >= 2:
                return clean[:20]

        # 中文关键词：取前2字，用拼音风格缩写（取首字拼音首字母不够好，直接用原文hash短码）
        for kw in keywords:
            if len(kw) >= 2:
                # 简单方案：中文关键词直接用，去掉空格
                slug = re.sub(r"\s+", "_", kw.strip())[:10]
                if slug:
                    return slug

        # 兜底
        return f"t{int(time.time()) % 100000}"

    # ── 信息查询 ──────────────────────────────────────────

    def list_dynamic_topics(self) -> list[dict]:
        """列出所有带 keywords 的主题（即动态注册的）"""
        results = []
        for path, kws in self._topic_keywords.items():
            if kws:
                results.append({"path": path, "keywords": kws})
        return results

    def get_stats(self) -> dict:
        return {
            "total_topics": len(self._all_topic_paths()),
            "dynamic_topics": len(self._topic_keywords),
            "threshold": self.SIMILARITY_THRESHOLD,
        }

    def get_all_topic_codes(self) -> list[str]:
        """获取所有已注册的主题代码路径（别名方法）"""
        return self._all_topic_paths()
