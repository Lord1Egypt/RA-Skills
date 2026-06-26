"""用户偏好记忆系统 — 结构化分层存储 + 置信度衰减 + 冲突检测 + 负样本 + 版本化

设计原则：
    准确率 = 正确信息的留存率 × 错误信息的淘汰率
    强化正确的，淘汰过时的，让记忆越来越准而非越来越臃肿。

三层存储：
    Layer 1 — 原始事件 (daily notes)：保留完整上下文，作为证据溯源
    Layer 2 — 蒸馏偏好 (curated memory)：经筛选、去重、蒸馏后的精华
    Layer 3 — 显式声明 (explicit preference)：用户主动声明的偏好，置信度最高

置信度来源优先级：
    用户明确说的 > 系统推断的 > 默认假设的
    多源一致 → 高置信度；单源 → 待验证

核心能力：
    - 偏好提取（从对话中自动识别偏好表达）
    - 冲突检测与解决（新偏好覆盖旧偏好时保留版本）
    - 负样本学习（记录用户拒绝/修正的偏好）
    - 上下文关联（偏好绑定触发场景）
    - 置信度衰减（未被验证的偏好随时间降权）
    - 版本化回溯（偏好变更保留历史）
"""
from __future__ import annotations

import hashlib
import json
import logging
import re
import time
from dataclasses import dataclass, field, asdict

logger = logging.getLogger(__name__)

# ── 偏好表达检测模式 ──────────────────────────────

# 肯定偏好（正向）
_AFFIRMATIVE_PATTERNS = [
    re.compile(r'I\s+(?:prefer|like|love|enjoy|favor|favour|adore)\s+(.+?)(?:\.|,|;|$)', re.I),
    re.compile(r'(?:my|our)\s+(?:favorite|favourite|preferred|go-to)\s+(.+?)(?:\.|,|;|is|$)', re.I),
    re.compile(r'I\s+(?:usually|always|often|typically|normally)\s+(.+?)(?:\.|,|;|$)', re.I),
    re.compile(r"I've\s+been\s+(?:using|making|cooking|watching|listening|reading)\s+(.+?)(?:\.|,|;|$)", re.I),
    re.compile(r'I\s+(?:use|have|own|got|bought)\s+(?:a\s+|an\s+)?(.+?)(?:\.|,|;|and|$)', re.I),
    re.compile(r'(?:偏好|喜欢|最爱|推荐|习惯|常用|平时|我的|爱用)', re.I),
]

# 否定偏好（负向）
_NEGATIVE_PATTERNS = [
    re.compile(r"I\s+(?:don't|do\s+not|cannot|can't\s+stand)\s+(?:like|want|need|enjoy|use|eat|drink|watch|listen)\s+(.+?)(?:\.|,|;|$)", re.I),
    re.compile(r"I'm\s+not\s+(?:a\s+fan|into|interested)\s+(?:in\s+)?(.+?)(?:\.|,|;|$)", re.I),
    re.compile(r"I\s+(?:hate|dislike|detest|avoid)\s+(.+?)(?:\.|,|;|$)", re.I),
    re.compile(r'(?:不喜欢|讨厌|不想|不爱|不要|拒绝|避免)', re.I),
]

# 修正模式（用户纠正之前的偏好）
_CORRECTION_PATTERNS = [
    re.compile(r"(?:actually|no|wait|I\s+meant|I\s+changed|not\s+anymore|instead)", re.I),
    re.compile(r'(?:不对|不是|改了|换了|现在|其实|纠正)', re.I),
]

# 场景上下文提取
_CONTEXT_PATTERNS = [
    re.compile(r'(?:when|while|if|during|at|in)\s+(?:I\'m\s+)?(.+?)(?:\s*,|\s*\.|;|$)', re.I),
    re.compile(r'(?:在|当|如果|的时候|时)(.+?)(?:的话|，|。|；|$)', re.I),
]


# ── 数据结构 ──────────────────────────────────────

@dataclass
class Preference:
    """单条偏好记录。"""
    preference_id: str = ""
    person_id: str = "user"
    category: str = ""           # food/music/work/travel/tech/hobby/style/...
    subject: str = ""            # 偏好主题（如 "video editing software"）
    value: str = ""              # 偏好值（如 "Adobe Premiere Pro"）
    polarity: str = "positive"   # positive / negative / neutral
    confidence: float = 0.5      # 置信度 [0.0, 1.0]
    source: str = "inferred"     # explicit / inferred / behavioral / correction
    context: str = ""            # 触发场景（如 "when editing 4K footage"）
    evidence_ids: list[str] = field(default_factory=list)  # 关联的原始记忆ID
    verification_count: int = 0  # 被验证次数
    last_verified_at: int = 0    # 最后验证时间
    superseded_by: str = ""      # 被哪条偏好取代
    version: int = 1
    layer: str = "raw"           # raw / curated / explicit
    created_at: int = 0
    updated_at: int = 0

    def to_dict(self) -> dict:
        d = asdict(self)
        d["evidence_ids"] = json.dumps(d["evidence_ids"])
        return d

    @classmethod
    def from_row(cls, row: dict) -> "Preference":
        if isinstance(row.get("evidence_ids"), str):
            row["evidence_ids"] = json.loads(row["evidence_ids"])
        return cls(**{k: v for k, v in row.items() if k in cls.__dataclass_fields__})


# ── 偏好记忆引擎 ──────────────────────────────────

class PreferenceMemory:
    """用户偏好记忆系统。

    三层存储 + 置信度衰减 + 冲突检测 + 负样本 + 版本化。
    """

    # 置信度来源权重
    SOURCE_CONFIDENCE = {
        "explicit": 0.95,    # 用户主动声明
        "correction": 0.90,  # 用户修正
        "behavioral": 0.70,  # 行为推断
        "inferred": 0.50,    # 系统推断
    }

    # 衰减参数（偏好比普通记忆衰减更慢）
    DECAY_HALF_LIFE_DAYS = 180  # 半衰期180天（普通记忆30-90天）
    MIN_CONFIDENCE = 0.15       # 最低置信度阈值
    VERIFICATION_BOOST = 0.10   # 每次验证提升的置信度

    # 冲突解决策略
    CONFLICT_RESOLUTION = "newer_wins"  # newer_wins / higher_confidence / explicit_wins

    def __init__(self, store=None, embedding_store=None):
        self.store = store
        self.embedding_store = embedding_store
        self._ensure_tables()

    def _ensure_tables(self):
        """创建偏好记忆专用表。"""
        if not self.store:
            return
        try:
            self.store.conn.executescript("""
                -- Layer 1-3: 偏好主表
                CREATE TABLE IF NOT EXISTS preferences (
                    preference_id TEXT PRIMARY KEY,
                    person_id TEXT NOT NULL DEFAULT 'user',
                    category TEXT NOT NULL DEFAULT '',
                    subject TEXT NOT NULL DEFAULT '',
                    value TEXT NOT NULL DEFAULT '',
                    polarity TEXT NOT NULL DEFAULT 'positive',
                    confidence REAL NOT NULL DEFAULT 0.5,
                    source TEXT NOT NULL DEFAULT 'inferred',
                    context TEXT NOT NULL DEFAULT '',
                    evidence_ids TEXT NOT NULL DEFAULT '[]',
                    verification_count INTEGER NOT NULL DEFAULT 0,
                    last_verified_at INTEGER NOT NULL DEFAULT 0,
                    superseded_by TEXT NOT NULL DEFAULT '',
                    version INTEGER NOT NULL DEFAULT 1,
                    layer TEXT NOT NULL DEFAULT 'raw',
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL
                );

                -- 偏好证据表（关联原始记忆）
                CREATE TABLE IF NOT EXISTS preference_evidence (
                    evidence_id TEXT PRIMARY KEY,
                    preference_id TEXT NOT NULL,
                    memory_id TEXT NOT NULL,
                    source_text TEXT NOT NULL DEFAULT '',
                    source_type TEXT NOT NULL DEFAULT 'chat',
                    confidence REAL NOT NULL DEFAULT 0.5,
                    created_at INTEGER NOT NULL,
                    FOREIGN KEY (preference_id) REFERENCES preferences(preference_id)
                );

                -- 偏好版本历史（支持回溯）
                CREATE TABLE IF NOT EXISTS preference_versions (
                    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    preference_id TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    snapshot TEXT NOT NULL,
                    change_reason TEXT NOT NULL DEFAULT '',
                    created_at INTEGER NOT NULL,
                    FOREIGN KEY (preference_id) REFERENCES preferences(preference_id)
                );

                -- 偏好冲突记录
                CREATE TABLE IF NOT EXISTS preference_conflicts (
                    conflict_id TEXT PRIMARY KEY,
                    old_pref_id TEXT NOT NULL,
                    new_pref_id TEXT NOT NULL DEFAULT '',
                    conflict_type TEXT NOT NULL DEFAULT 'contradiction',
                    resolution TEXT NOT NULL DEFAULT 'pending',
                    resolved_at INTEGER NOT NULL DEFAULT 0,
                    created_at INTEGER NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_pref_person ON preferences(person_id);
                CREATE INDEX IF NOT EXISTS idx_pref_category ON preferences(person_id, category);
                CREATE INDEX IF NOT EXISTS idx_pref_subject ON preferences(person_id, subject);
                CREATE INDEX IF NOT EXISTS idx_pref_layer ON preferences(person_id, layer);
                CREATE INDEX IF NOT EXISTS idx_pref_confidence ON preferences(confidence);
                CREATE INDEX IF NOT EXISTS idx_pref_superseded ON preferences(superseded_by);
                CREATE INDEX IF NOT EXISTS idx_pe_pref ON preference_evidence(preference_id);
                CREATE INDEX IF NOT EXISTS idx_pe_memory ON preference_evidence(memory_id);
                CREATE INDEX IF NOT EXISTS idx_pv_pref ON preference_versions(preference_id);
                CREATE INDEX IF NOT EXISTS idx_pconf_old ON preference_conflicts(old_pref_id);
            """)
            self.store.conn.commit()
        except Exception as e:
            logger.debug("preference_memory: ensure_tables: %s", e)

    # ── 偏好提取 ──────────────────────────────────

    @staticmethod
    def extract_preferences(text: str, person_id: str = "user") -> list[Preference]:
        """从文本中提取偏好表达。

        返回提取到的 Preference 列表（未持久化）。
        """
        prefs = []
        now = int(time.time())

        # 检测修正模式 → 高置信度修正
        is_correction = any(p.search(text) for p in _CORRECTION_PATTERNS)

        # 检测否定偏好
        for pattern in _NEGATIVE_PATTERNS:
            for match in pattern.finditer(text):
                value = match.group(1).strip() if match.lastindex else match.group(0).strip()
                if not value or len(value) < 2:
                    continue
                pref = Preference(
                    preference_id=f"pref_{hashlib.sha256(f'{person_id}:neg:{value}'.encode()).hexdigest()[:20]}",
                    person_id=person_id,
                    polarity="negative",
                    value=value,
                    source="correction" if is_correction else "inferred",
                    confidence=PreferenceMemory.SOURCE_CONFIDENCE.get(
                        "correction" if is_correction else "inferred", 0.5
                    ),
                    created_at=now,
                    updated_at=now,
                )
                prefs.append(pref)

        # 检测肯定偏好
        for pattern in _AFFIRMATIVE_PATTERNS:
            for match in pattern.finditer(text):
                value = match.group(1).strip() if match.lastindex else match.group(0).strip()
                if not value or len(value) < 2:
                    continue
                pref = Preference(
                    preference_id=f"pref_{hashlib.sha256(f'{person_id}:pos:{value}'.encode()).hexdigest()[:20]}",
                    person_id=person_id,
                    polarity="positive",
                    value=value,
                    source="correction" if is_correction else "inferred",
                    confidence=PreferenceMemory.SOURCE_CONFIDENCE.get(
                        "correction" if is_correction else "inferred", 0.5
                    ),
                    created_at=now,
                    updated_at=now,
                )
                prefs.append(pref)

        # 检测场景上下文
        for pref in prefs:
            for pattern in _CONTEXT_PATTERNS:
                match = pattern.search(text)
                if match:
                    pref.context = match.group(1).strip() if match.lastindex else ""
                    break

        return prefs

    # ── 偏好写入 ──────────────────────────────────

    def add_preference(self, pref: Preference, memory_id: str = "",
                       source_text: str = "") -> str:
        """写入偏好记录，自动检测冲突。"""
        if not self.store:
            return ""

        now = int(time.time())
        pref.updated_at = now
        if not pref.created_at:
            pref.created_at = now

        # 检测冲突：同 person + 同 subject 的现有偏好
        conflicts = self._detect_conflicts(pref)

        if conflicts:
            for old_pref in conflicts:
                self._resolve_conflict(old_pref, pref)

        # 写入偏好
        try:
            self.store.conn.execute(
                """INSERT OR REPLACE INTO preferences (
                    preference_id, person_id, category, subject, value,
                    polarity, confidence, source, context, evidence_ids,
                    verification_count, last_verified_at, superseded_by,
                    version, layer, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    pref.preference_id, pref.person_id, pref.category,
                    pref.subject, pref.value, pref.polarity, pref.confidence,
                    pref.source, pref.context, json.dumps(pref.evidence_ids),
                    pref.verification_count, pref.last_verified_at,
                    pref.superseded_by, pref.version, pref.layer,
                    pref.created_at, pref.updated_at,
                ),
            )

            # 写入证据
            if memory_id:
                eid = f"ev_{pref.preference_id}_{memory_id[:8]}"
                self.store.conn.execute(
                    """INSERT OR REPLACE INTO preference_evidence (
                        evidence_id, preference_id, memory_id, source_text,
                        source_type, confidence, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (eid, pref.preference_id, memory_id, source_text,
                     pref.source, pref.confidence, now),
                )

            self.store.conn.commit()
            return pref.preference_id
        except Exception as e:
            logger.warning("preference_memory: add_preference failed: %s", e)
            return ""

    def add_from_memory(self, memory_id: str, content: str,
                        person_id: str = "user") -> list[str]:
        """从记忆内容中提取偏好并写入。

        这是主要的入口方法：在记忆入库时调用，
        自动提取偏好表达并建立关联。

        Returns:
            写入的 preference_id 列表
        """
        prefs = self.extract_preferences(content, person_id)
        added_ids = []
        for pref in prefs:
            pid = self.add_preference(pref, memory_id=memory_id, source_text=content)
            if pid:
                added_ids.append(pid)
        return added_ids

    # ── 冲突检测与解决 ────────────────────────────

    def _detect_conflicts(self, new_pref: Preference) -> list[Preference]:
        """检测与现有偏好的冲突。

        冲突条件：同 person + 同 subject，但 value 不同。
        """
        if not self.store:
            return []

        conflicts = []
        try:
            cursor = self.store.conn.execute(
                """SELECT * FROM preferences
                   WHERE person_id = ? AND subject = ?
                   AND superseded_by = ''
                   AND preference_id != ?""",
                (new_pref.person_id, new_pref.subject, new_pref.preference_id),
            )
            columns = [desc[0] for desc in cursor.description]
            for row in cursor.fetchall():
                old = Preference.from_row(dict(zip(columns, row)))
                # 同极性但不同值 → 冲突
                if old.polarity == new_pref.polarity and old.value != new_pref.value:
                    conflicts.append(old)
                # 反极性同值 → 矛盾
                elif old.polarity != new_pref.polarity and old.value == new_pref.value:
                    conflicts.append(old)
        except Exception as e:
            logger.debug("preference_memory: conflict detection: %s", e)

        return conflicts

    def _resolve_conflict(self, old_pref: Preference, new_pref: Preference):
        """解决偏好冲突。

        策略：newer_wins — 新偏好取代旧偏好，但保留版本历史。
        """
        if not self.store:
            return

        now = int(time.time())

        # 保存旧版本快照
        self._save_version(old_pref, reason="conflict_resolved")

        # 标记旧偏好为被取代
        self.store.conn.execute(
            "UPDATE preferences SET superseded_by = ?, updated_at = ? WHERE preference_id = ?",
            (new_pref.preference_id, now, old_pref.preference_id),
        )

        # 记录冲突
        conflict_id = f"conflict_{old_pref.preference_id[:8]}_{new_pref.preference_id[:8]}"
        self.store.conn.execute(
            """INSERT OR REPLACE INTO preference_conflicts (
                conflict_id, old_pref_id, new_pref_id, conflict_type,
                resolution, resolved_at, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (conflict_id, old_pref.preference_id, new_pref.preference_id,
             "contradiction", "newer_wins", now, now),
        )

        # 新偏好继承旧偏好的验证次数
        new_pref.verification_count = old_pref.verification_count

        logger.info(
            "preference conflict resolved: [%s] '%s' superseded by [%s] '%s'",
            old_pref.preference_id[:8], old_pref.value,
            new_pref.preference_id[:8], new_pref.value,
        )

    # ── 置信度与衰减 ──────────────────────────────

    def apply_decay(self, person_id: str = "user") -> int:
        """对未验证的偏好应用时间衰减。

        偏好半衰期 180 天，最低不低于 MIN_CONFIDENCE。
        已被取代的偏好不参与衰减。

        Returns:
            衰减的偏好数量
        """
        if not self.store:
            return 0

        now = int(time.time())
        decayed = 0

        try:
            cursor = self.store.conn.execute(
                """SELECT preference_id, confidence, last_verified_at, verification_count, source, created_at
                   FROM preferences
                   WHERE person_id = ? AND superseded_by = ''""",
                (person_id,),
            )
            for row in cursor.fetchall():
                pid, conf, last_verified, ver_count, source, created_at = row

                # 显式声明不衰减
                if source == "explicit":
                    continue

                # 计算衰减
                age_days = (now - last_verified) / 86400 if last_verified else (now - created_at) / 86400 if created_at else 0
                if age_days <= 0:
                    continue

                # 指数衰减：conf * 0.5^(age/half_life)
                import math
                decayed_conf = conf * math.pow(0.5, age_days / self.DECAY_HALF_LIFE_DAYS)

                # 验证次数补偿：每验证一次，衰减减缓
                ver_boost = min(ver_count * 0.05, 0.3)
                decayed_conf = min(decayed_conf + ver_boost, 1.0)

                # 不低于最低阈值
                decayed_conf = max(decayed_conf, self.MIN_CONFIDENCE)

                if decayed_conf < conf:
                    self.store.conn.execute(
                        "UPDATE preferences SET confidence = ?, updated_at = ? WHERE preference_id = ?",
                        (round(decayed_conf, 3), now, pid),
                    )
                    decayed += 1

            self.store.conn.commit()
        except Exception as e:
            logger.debug("preference_memory: apply_decay: %s", e)

        return decayed

    def verify_preference(self, preference_id: str) -> bool:
        """验证偏好（增加验证计数和置信度）。"""
        if not self.store:
            return False

        now = int(time.time())
        try:
            self.store.conn.execute(
                """UPDATE preferences SET
                    verification_count = verification_count + 1,
                    last_verified_at = ?,
                    confidence = MIN(confidence + ?, 1.0),
                    updated_at = ?
                WHERE preference_id = ?""",
                (now, self.VERIFICATION_BOOST, now, preference_id),
            )
            self.store.conn.commit()
            return True
        except Exception as e:
            logger.debug("preference_memory: verify_preference: %s", e)
            return False

    # ── 查询接口 ──────────────────────────────────

    def get_preferences(self, person_id: str = "user", category: str = None,
                        subject: str = None, layer: str = None,
                        min_confidence: float = 0.0,
                        include_superseded: bool = False) -> list[Preference]:
        """查询偏好列表。"""
        if not self.store:
            return []

        conditions = ["person_id = ?"]
        params = [person_id]

        if category:
            conditions.append("category = ?")
            params.append(category)
        if subject:
            conditions.append("subject = ?")
            params.append(subject)
        if layer:
            conditions.append("layer = ?")
            params.append(layer)
        if min_confidence > 0:
            conditions.append("confidence >= ?")
            params.append(min_confidence)
        if not include_superseded:
            conditions.append("superseded_by = ''")

        where = " AND ".join(conditions)
        try:
            cursor = self.store.conn.execute(
                f"SELECT * FROM preferences WHERE {where} ORDER BY confidence DESC, updated_at DESC",
                params,
            )
            columns = [desc[0] for desc in cursor.description]
            return [Preference.from_row(dict(zip(columns, row))) for row in cursor.fetchall()]
        except Exception as e:
            logger.debug("preference_memory: get_preferences: %s", e)
            return []

    def search_preferences(self, query: str, person_id: str = "user",
                           limit: int = 10) -> list[Preference]:
        """语义+关键词搜索偏好。

        用于 recall 检索时，先搜索偏好库获取高置信度偏好，
        再从原始记忆中补充上下文。
        """
        if not self.store:
            return []

        # FTS 搜索（在 subject + value + context 上）
        results = []
        try:
            # 简单 LIKE 搜索（偏好表数据量小，无需 FTS）
            keywords = re.findall(r'\w+', query.lower())
            if not keywords:
                return self.get_preferences(person_id, min_confidence=0.3)[:limit]

            conditions = ["person_id = ?", "superseded_by = ''", "confidence >= 0.2"]
            params = [person_id]

            # 关键词 OR 匹配
            like_clauses = []
            for kw in keywords[:5]:
                like_clauses.append("(LOWER(subject) LIKE ? OR LOWER(value) LIKE ? OR LOWER(context) LIKE ?)")
                params.extend([f"%{kw}%", f"%{kw}%", f"%{kw}%"])

            if like_clauses:
                conditions.append(f"({' OR '.join(like_clauses)})")

            where = " AND ".join(conditions)
            cursor = self.store.conn.execute(
                f"SELECT * FROM preferences WHERE {where} ORDER BY confidence DESC LIMIT ?",
                params + [limit],
            )
            columns = [desc[0] for desc in cursor.description]
            results = [Preference.from_row(dict(zip(columns, row))) for row in cursor.fetchall()]
        except Exception as e:
            logger.debug("preference_memory: search_preferences: %s", e)

        return results

    def get_preference_summary(self, person_id: str = "user") -> Dict:
        """获取用户偏好摘要（用于上下文注入）。"""
        prefs = self.get_preferences(person_id, min_confidence=0.3)
        if not prefs:
            return {"person_id": person_id, "preferences": [], "total": 0}

        # 按类别分组
        by_category = {}
        for p in prefs:
            cat = p.category or "general"
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append({
                "subject": p.subject,
                "value": p.value,
                "polarity": p.polarity,
                "confidence": round(p.confidence, 2),
                "context": p.context,
                "source": p.source,
            })

        return {
            "person_id": person_id,
            "preferences": by_category,
            "total": len(prefs),
        }

    # ── 版本化 ────────────────────────────────────

    def _save_version(self, pref: Preference, reason: str = ""):
        """保存偏好版本快照。"""
        if not self.store:
            return
        try:
            snapshot = json.dumps(pref.to_dict(), ensure_ascii=False)
            self.store.conn.execute(
                """INSERT INTO preference_versions (preference_id, version, snapshot, change_reason, created_at)
                   VALUES (?, ?, ?, ?, ?)""",
                (pref.preference_id, pref.version, snapshot, reason, int(time.time())),
            )
        except Exception as e:
            logger.debug("preference_memory: save_version: %s", e)

    def get_preference_history(self, preference_id: str) -> list[dict]:
        """获取偏好的版本历史。"""
        if not self.store:
            return []
        try:
            cursor = self.store.conn.execute(
                "SELECT version, snapshot, change_reason, created_at FROM preference_versions WHERE preference_id = ? ORDER BY version",
                (preference_id,),
            )
            return [
                {"version": r[0], "snapshot": json.loads(r[1]), "reason": r[2], "created_at": r[3]}
                for r in cursor.fetchall()
            ]
        except Exception as e:
            logger.debug("preference_memory: get_history: %s", e)
            return []

    # ── 负样本 ────────────────────────────────────

    def get_negative_preferences(self, person_id: str = "user",
                                  min_confidence: float = 0.3) -> list[Preference]:
        """获取用户的否定偏好（"不喜欢什么"）。"""
        if not self.store:
            return []
        try:
            cursor = self.store.conn.execute(
                """SELECT * FROM preferences
                   WHERE person_id = ? AND polarity = 'negative'
                   AND superseded_by = '' AND confidence >= ?
                   ORDER BY confidence DESC""",
                (person_id, min_confidence),
            )
            columns = [desc[0] for desc in cursor.description]
            return [Preference.from_row(dict(zip(columns, row))) for row in cursor.fetchall()]
        except Exception as e:
            logger.debug("preference_memory: get_negative: %s", e)
            return []

    # ── 统计 ──────────────────────────────────────

    def get_stats(self, person_id: str = "user") -> Dict:
        """获取偏好记忆统计信息。"""
        if not self.store:
            return {}
        try:
            cursor = self.store.conn.execute(
                """SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN polarity = 'positive' THEN 1 ELSE 0 END) as positive,
                    SUM(CASE WHEN polarity = 'negative' THEN 1 ELSE 0 END) as negative,
                    SUM(CASE WHEN superseded_by != '' THEN 1 ELSE 0 END) as superseded,
                    AVG(confidence) as avg_confidence,
                    SUM(CASE WHEN source = 'explicit' THEN 1 ELSE 0 END) as explicit_count,
                    SUM(CASE WHEN source = 'inferred' THEN 1 ELSE 0 END) as inferred_count,
                    SUM(CASE WHEN layer = 'explicit' THEN 1 ELSE 0 END) as layer_explicit,
                    SUM(CASE WHEN layer = 'curated' THEN 1 ELSE 0 END) as layer_curated,
                    SUM(CASE WHEN layer = 'raw' THEN 1 ELSE 0 END) as layer_raw
                FROM preferences WHERE person_id = ?""",
                (person_id,),
            )
            row = cursor.fetchone()
            if row:
                return {
                    "total": row[0] or 0,
                    "positive": row[1] or 0,
                    "negative": row[2] or 0,
                    "superseded": row[3] or 0,
                    "avg_confidence": round(row[4] or 0, 2),
                    "explicit_count": row[5] or 0,
                    "inferred_count": row[6] or 0,
                    "layer_explicit": row[7] or 0,
                    "layer_curated": row[8] or 0,
                    "layer_raw": row[9] or 0,
                }
        except Exception as e:
            logger.debug("preference_memory: get_stats: %s", e)
        return {}



