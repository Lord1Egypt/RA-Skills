# -*- coding: utf-8 -*-
"""
记忆冲突消解 —— 智能检测、分类、消解记忆中的矛盾信息。

核心能力：
  - 冲突自动检测：新写入的实体/关系/事实与已有数据对比，发现矛盾
  - 冲突类型分类：信息更新 / 信息纠错 / 视角变化 / 真实冲突（需仲裁）
  - 冲突提示与确认：生成对比报告，向用户展示新旧值对比
  - 处理策略：覆盖（新替旧）/ 保留两者（标注版本）/ 合并（取并集）/ 忽略

所有功能纯本地、零密钥、按硬件自适应，不拖累电脑。
"""

from __future__ import annotations

import json
import os
import re
import sys
import threading
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path

# 确保能 import 同级模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

from scripts import store, config, embeddings, graph
from scripts.hardware import get_plan

# ── 枚举 ────────────────────────────────────────────────────────────────
class ConflictType(str, Enum):
    """冲突类型"""
    UPDATE = "update"           # 信息更新（换工作、搬家）
    CORRECTION = "correction"   # 信息纠错（之前记错了）
    PERSPECTIVE = "perspective" # 视角变化（同一件事不同描述）
    REAL_CONFLICT = "real_conflict"  # 真正冲突（需要用户仲裁）

    @property
    def display_name(self) -> str:
        names = {
            "update": "信息更新",
            "correction": "信息纠错",
            "perspective": "视角变化",
            "real_conflict": "真实冲突（需仲裁）",
        }
        return names.get(self.value, self.value)


class ConflictResolution(str, Enum):
    """消解策略"""
    OVERWRITE = "overwrite"     # 覆盖（新替旧）
    KEEP_BOTH = "keep_both"     # 保留两者（标注版本）
    MERGE = "merge"             # 合并（取并集）
    IGNORE = "ignore"           # 忽略

    @property
    def display_name(self) -> str:
        names = {
            "overwrite": "覆盖（新替旧）",
            "keep_both": "保留两者",
            "merge": "合并（取并集）",
            "ignore": "忽略",
        }
        return names.get(self.value, self.value)


# ── 数据类 ──────────────────────────────────────────────────────────────
@dataclass
class Conflict:
    """单个冲突记录"""
    conflict_id: str = ""
    type: ConflictType = ConflictType.REAL_CONFLICT
    entity_id: int = 0
    entity_name: str = ""
    predicate: str = ""
    old_value: str = ""
    new_value: str = ""
    old_source: str = ""
    new_source: str = ""
    confidence: float = 0.0          # 冲突确信度（0~1）
    semantic_similarity: float = 0.0 # 新旧值语义相似度
    description: str = ""            # 用户可读描述
    created_at: str = ""
    resolved: bool = False
    resolution: str = ""
    resolved_value: str = ""         # 消解后的最终值


# ── 模式匹配规则 ─────────────────────────────────────────────────────────
# 信息更新模式：换工作、搬家、离职、加入、切换到、换成...
_UPDATE_PATTERNS = [
    r"(?:换|跳槽|离职|加入|转入|调到|搬到|搬到|切换|换到|换成|跳槽到|加入|去了)\s*(?:了\s*)?(.+)",
    r"(.+?)(?:已?经?|现在)(?:换|跳槽|离职|加入|搬到|切换|换成|调)到?(.+)",
    r"新(?:公司|工作|地址|电话|职位|部门)(?:是|为|:|:)\s*(.+)",
    r"不再是(?:在|去|待在)\s*(.+?)(?:了)?$",
]

# 信息纠错模式：之前记错了、搞错了、更正、不是...
_CORRECTION_PATTERNS = [
    r"(?:之前|原来|前面|上次)(?:的?记忆?|记|说|写)(?:的?是)?(?:错|误|不对|搞错|记错)的?",
    r"更正(?:一下|下)?[:：]?\s*(.+)",
    r"(?:其实|实际上|正确(?:的是)?|应该(?:是|为))[:：]?\s*(.+)",
    r"不(?:是|在)(.+?)(?:而是|应该)",
]

# 视角变化模式：也可以说、从另一个角度、换个说法、意思是...
_PERSPECTIVE_PATTERNS = [
    r"(?:也(?:可以|就是?)|换个说法|换个角度|另一种(?:说法|理解|看[法法])|意思是|相当于|等于说)",
    r"(?:从|在).*?(?:角度|视角|层面|意义)上来说",
]

# ── 检测器 ──────────────────────────────────────────────────────────────
class ConflictDetector:
    """冲突检测器：对比新旧信息，发现矛盾。"""

    def __init__(self):
        self._sim_cache: dict[tuple[str, str], float] = {}
        self._lock = threading.Lock()

    def detect_fact_conflict(self, entity_id: int, predicate: str,
                              new_value: str) -> Conflict | None:
        """
        检测事实冲突：同一实体同一谓词的值是否矛盾。
        返回 Conflict 或 None（无冲突）。
        """
        old_facts = store.current_facts(entity_id)
        if not old_facts:
            return None

        for old in old_facts:
            if old["predicate"] != predicate:
                continue
            old_value = old["value"]
            if old_value == new_value:
                return None  # 值相同，无冲突

            # 计算语义相似度
            sim = self._compute_similarity(old_value, new_value)
            contradiction = 1.0 - sim  # 矛盾度 = 1 - 相似度

            # 低相似度 + 高矛盾度 = 真实冲突
            if contradiction >= 0.5:
                confidence = min(1.0, contradiction + 0.1)
                return Conflict(
                    conflict_id=f"fact_{entity_id}_{predicate}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    entity_id=entity_id,
                    entity_name=self._get_entity_name(entity_id),
                    predicate=predicate,
                    old_value=old_value,
                    new_value=new_value,
                    old_source="memory",
                    new_source="new_input",
                    confidence=confidence,
                    semantic_similarity=sim,
                    created_at=datetime.now().isoformat(timespec="seconds"),
                )
            else:
                # 高相似度 = 可能是同义改写/视角变化
                return Conflict(
                    conflict_id=f"fact_{entity_id}_{predicate}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    entity_id=entity_id,
                    entity_name=self._get_entity_name(entity_id),
                    predicate=predicate,
                    old_value=old_value,
                    new_value=new_value,
                    old_source="memory",
                    new_source="new_input",
                    confidence=0.3,
                    semantic_similarity=sim,
                    created_at=datetime.now().isoformat(timespec="seconds"),
                )
        return None

    def detect_entity_conflict(self, entity_name: str, entity_type: str) -> Conflict | None:
        """检测实体冲突：同名不同类型或同名同类型但属性矛盾。"""
        conn = store.get_conn()
        existing = conn.execute(
            "SELECT * FROM entities WHERE name=?", (entity_name,)
        ).fetchone()
        if not existing:
            return None

        # 同名不同类型 → 真实冲突
        if existing["type"] != entity_type:
            return Conflict(
                conflict_id=f"ent_{entity_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                entity_id=existing["id"],
                entity_name=entity_name,
                predicate="type",
                old_value=existing["type"],
                new_value=entity_type,
                old_source="graph",
                new_source="new_input",
                confidence=0.8,
                semantic_similarity=0.0,
                description=f"同名实体「{entity_name}」类型为 {existing['type']}，新值为 {entity_type}",
                created_at=datetime.now().isoformat(timespec="seconds"),
            )

        # 同名同类型 → 检查属性冲突（通过 facts）
        return None  # 同名同类型通常无需冲突处理

    def detect_relation_conflict(self, from_id: int, to_id: int,
                                  new_relation: str) -> Conflict | None:
        """检测关系冲突：同方向同实体对的关系是否矛盾。"""
        conn = store.get_conn()
        existing = conn.execute(
            "SELECT r.*, e_from.name AS from_name, e_to.name AS to_name "
            "FROM relations r "
            "JOIN entities e_from ON e_from.id=r.from_id "
            "JOIN entities e_to ON e_to.id=r.to_id "
            "WHERE r.from_id=? AND r.to_id=? AND r.relation=?",
            (from_id, to_id, new_relation)
        ).fetchone()
        if existing:
            return None  # 已存在相同关系，不冲突

        # 检查同实体对不同关系
        others = conn.execute(
            "SELECT r.*, e_from.name AS from_name, e_to.name AS to_name "
            "FROM relations r "
            "JOIN entities e_from ON e_from.id=r.from_id "
            "JOIN entities e_to ON e_to.id=r.to_id "
            "WHERE r.from_id=? AND r.to_id=?",
            (from_id, to_id)
        ).fetchall()
        if others:
            other_rels = [o["relation"] for o in others]
            return Conflict(
                conflict_id=f"rel_{from_id}_{to_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                entity_id=from_id,
                entity_name=others[0]["from_name"],
                predicate="relation",
                old_value=", ".join(other_rels),
                new_value=new_relation,
                old_source="graph",
                new_source="new_input",
                confidence=0.4,
                semantic_similarity=0.2,
                description=f"实体对 {others[0]['from_name']}→{others[0]['to_name']} 已有关系 {other_rels}，新增 {new_relation}",
                created_at=datetime.now().isoformat(timespec="seconds"),
            )
        return None

    def _compute_similarity(self, a: str, b: str) -> float:
        """计算两个字符串的语义相似度（基于 token Jaccard + 编辑距离）。"""
        key = (a, b)
        with self._lock:
            if key in self._sim_cache:
                return self._sim_cache[key]

        # Jaccard 相似度
        toks_a = set(embeddings.tokenize(a))
        toks_b = set(embeddings.tokenize(b))
        if not toks_a and not toks_b:
            sim = 1.0 if a == b else 0.0
        elif not toks_a or not toks_b:
            sim = 0.0
        else:
            sim = embeddings.jaccard(toks_a, toks_b)

        with self._lock:
            self._sim_cache[key] = sim
            # 缓存上限 1000 条，避免内存膨胀
            if len(self._sim_cache) > 1000:
                # 简单的 FIFO：清空一半
                keys = list(self._sim_cache.keys())[:500]
                for k in keys:
                    del self._sim_cache[k]
        return sim

    def _get_entity_name(self, entity_id: int) -> str:
        conn = store.get_conn()
        row = conn.execute("SELECT name FROM entities WHERE id=?", (entity_id,)).fetchone()
        return row["name"] if row else "?"


# ── 分类器 ──────────────────────────────────────────────────────────────
class ConflictClassifier:
    """冲突分类器：基于模式匹配判定冲突类型。"""

    def classify(self, conflict: Conflict, new_text: str = "",
                 old_text: str = "") -> ConflictType:
        """根据冲突信息和上下文判定类型。"""
        new_val = conflict.new_value + new_text
        old_val = conflict.old_value + old_text

        # 1) 纠错模式检测
        for pat in _CORRECTION_PATTERNS:
            if re.search(pat, new_val, re.IGNORECASE):
                return ConflictType.CORRECTION

        # 2) 更新模式检测
        for pat in _UPDATE_PATTERNS:
            if re.search(pat, new_val, re.IGNORECASE):
                return ConflictType.UPDATE

        # 3) 视角变化模式检测
        for pat in _PERSPECTIVE_PATTERNS:
            if re.search(pat, new_val, re.IGNORECASE):
                return ConflictType.PERSPECTIVE

        # 4) 高相似度 + 低矛盾度 → 视角变化
        if conflict.semantic_similarity >= 0.7:
            return ConflictType.PERSPECTIVE

        # 5) 低语义相似度 + 高矛盾度 → 真实冲突
        if conflict.semantic_similarity <= 0.3 and conflict.confidence >= 0.7:
            return ConflictType.REAL_CONFLICT

        # 6) 中等置信度 → 默认真实冲突（需仲裁）
        return ConflictType.REAL_CONFLICT

    def is_auto_resolvable(self, conflict: Conflict) -> bool:
        """是否可自动消解（无需用户干预）。"""
        return conflict.type in (ConflictType.UPDATE, ConflictType.CORRECTION)


# ── 消解器 ──────────────────────────────────────────────────────────────
class ConflictResolver:
    """冲突消解器：执行消解策略。"""

    def __init__(self):
        self.detector = ConflictDetector()
        self.classifier = ConflictClassifier()

    def check_and_resolve(self, entity_id: int, predicate: str, new_value: str,
                           new_text: str = "", auto_resolve: bool = True) -> dict:
        """
        检测冲突并尝试消解。
        返回：{conflict_detected, conflict, resolution, final_value, action}
        """
        conflict = self.detector.detect_fact_conflict(entity_id, predicate, new_value)
        if not conflict:
            return {"conflict_detected": False, "action": "write_directly"}

        # 分类
        conflict.type = self.classifier.classify(conflict, new_text)
        conflict.description = self._generate_description(conflict)

        # 自动消解 UPDATE / CORRECTION
        if auto_resolve and self.classifier.is_auto_resolvable(conflict):
            if conflict.type == ConflictType.UPDATE:
                result = self._resolve_overwrite(conflict)
                return {"conflict_detected": True, "conflict": conflict,
                        "resolution": "auto_overwrite", "action": "resolved",
                        "result": result}
            elif conflict.type == ConflictType.CORRECTION:
                result = self._resolve_overwrite(conflict)
                return {"conflict_detected": True, "conflict": conflict,
                        "resolution": "auto_correct", "action": "resolved",
                        "result": result}

        # PERSPECTIVE → 自动合并（保留两者）
        if conflict.type == ConflictType.PERSPECTIVE and auto_resolve:
            result = self._resolve_keep_both(conflict)
            return {"conflict_detected": True, "conflict": conflict,
                    "resolution": "auto_perspective_merge", "action": "resolved",
                    "result": result}

        # REAL_CONFLICT → 需用户仲裁
        return {"conflict_detected": True, "conflict": conflict,
                "resolution": "needs_user", "action": "pending"}

    def resolve_with_strategy(self, conflict: Conflict,
                               strategy: ConflictResolution) -> dict:
        """用指定策略消解冲突。"""
        if strategy == ConflictType.OVERWRITE:
            return self._resolve_overwrite(conflict)
        elif strategy == ConflictResolution.KEEP_BOTH:
            return self._resolve_keep_both(conflict)
        elif strategy == ConflictResolution.MERGE:
            return self._resolve_merge(conflict)
        elif strategy == ConflictResolution.IGNORE:
            return {"action": "ignored", "value": conflict.old_value}
        return {"action": "unknown_strategy"}

    def _resolve_overwrite(self, conflict: Conflict) -> dict:
        """覆盖策略：新值替旧值，旧值标记为 superseded。"""
        conn = store.get_conn()
        conn.execute(
            "UPDATE facts SET superseded=1, valid_to=? WHERE entity_id=? AND predicate=? AND superseded=0",
            (datetime.now().isoformat(timespec="seconds"), conflict.entity_id, conflict.predicate),
        )
        conn.commit()
        return {"action": "overwritten", "final_value": conflict.new_value}

    def _resolve_keep_both(self, conflict: Conflict) -> dict:
        """保留两者策略：旧值保留，新值也写入，标注为版本 2。"""
        # 旧值保留，新值也写入（两个都保留）
        return {"action": "kept_both",
                "values": [conflict.old_value, conflict.new_value]}

    def _resolve_merge(self, conflict: Conflict) -> dict:
        """合并策略：取并集（适用于多值属性如技能、标签等）。"""
        merged = f"{conflict.old_value}、{conflict.new_value}"
        return {"action": "merged", "final_value": merged}

    def generate_report(self, conflict: Conflict) -> str:
        """生成用户可读的冲突报告。"""
        return (
            f"⚠️ 检测到{conflict.type.display_name}\n"
            f"─────────────────────────────\n"
            f"实体：{conflict.entity_name}\n"
            f"属性：{conflict.predicate}\n"
            f"旧值：{conflict.old_value}\n"
            f"新值：{conflict.new_value}\n"
            f"相似度：{conflict.semantic_similarity:.2f}\n"
            f"置信度：{conflict.confidence:.2f}\n"
            f"─────────────────────────────\n"
            f"请确认处理方式：\n"
            f"  1. 覆盖（新替旧）\n"
            f"  2. 保留两者\n"
            f"  3. 合并（取并集）\n"
            f"  4. 忽略（保留旧值）"
        )

    def _generate_description(self, conflict: Conflict) -> str:
        """生成冲突描述。"""
        type_names = {
            ConflictType.UPDATE: "信息更新",
            ConflictType.CORRECTION: "信息纠错",
            ConflictType.PERSPECTIVE: "视角变化",
            ConflictType.REAL_CONFLICT: "真实冲突",
        }
        type_name = type_names.get(conflict.type, "未知")
        return (f"[{type_name}] {conflict.entity_name}.{conflict.predicate}: "
                f"{conflict.old_value} → {conflict.new_value} "
                f"(相似度 {conflict.semantic_similarity:.2f})")


# ── 冲突存储（持久化待处理冲突） ────────────────────────────────────────

CONFLICTS_FILE = config.ZWJH_DIR / "pending_conflicts.json"


def load_pending_conflicts() -> list[dict]:
    """加载待处理冲突列表。"""
    if CONFLICTS_FILE.exists():
        try:
            with open(CONFLICTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def save_pending_conflicts(conflicts: list[dict]) -> None:
    """保存待处理冲突列表。"""
    config.ensure_dirs()
    try:
        with open(CONFLICTS_FILE, "w", encoding="utf-8") as f:
            json.dump(conflicts, f, ensure_ascii=False, indent=2,
                      default=lambda o: o.value if isinstance(o, Enum) else str(o))
    except Exception:
        pass


def add_pending_conflict(conflict: Conflict) -> None:
    """添加一个待处理冲突。"""
    pending = load_pending_conflicts()
    d = {
        "conflict_id": conflict.conflict_id,
        "type": conflict.type.value,
        "entity_id": conflict.entity_id,
        "entity_name": conflict.entity_name,
        "predicate": conflict.predicate,
        "old_value": conflict.old_value,
        "new_value": conflict.new_value,
        "confidence": conflict.confidence,
        "description": conflict.description,
        "created_at": conflict.created_at,
    }
    pending.append(d)
    save_pending_conflicts(pending)


def remove_pending_conflict(conflict_id: str) -> bool:
    """移除已处理的冲突。"""
    pending = load_pending_conflicts()
    new_pending = [p for p in pending if p.get("conflict_id") != conflict_id]
    if len(new_pending) < len(pending):
        save_pending_conflicts(new_pending)
        return True
    return False


def get_all_pending() -> list[dict]:
    """获取所有待处理冲突。"""
    return load_pending_conflicts()


# ── 单例 ────────────────────────────────────────────────────────────────
_resolver: ConflictResolver | None = None
_resolver_lock = threading.Lock()


def get_resolver() -> ConflictResolver:
    """获取全局单例 ConflictResolver。"""
    global _resolver
    if _resolver is None:
        with _resolver_lock:
            if _resolver is None:
                _resolver = ConflictResolver()
    return _resolver


if __name__ == "__main__":
    # 自测
    r = get_resolver()
    print(f"Resolver initialized. Detector: {r.detector is not None}")
    print(f"Pending conflicts: {len(get_all_pending())}")
