from __future__ import annotations

import json
import logging
import time
import hashlib
from dataclasses import fields
from typing import List, Dict, Optional

from .personality_analyzer import PersonalityProfile, TraitScore

logger = logging.getLogger(__name__)


class PersonalityMemory:
    """统一人格记忆构建 — 持久化 + 增量更新 + 隐私控制 + 蒸馏集成"""

    PRIVACY_LEVELS = {
        "public": ["cognitive_style", "decision_style", "humor_style", "circadian_preference"],
        "team": ["big_five_summary", "social_energy_pattern", "communication_style"],
        "private": ["narcissism_index", "control_tendency", "anxiety_level", "attachment_style"],
        "restricted": ["deep_trait_details", "raw_analysis_data"],
    }

    _PRIVACY_FIELD_MAP = {
        "public": {
            "cognitive_style", "reasoning_style", "decision_style",
            "humor_style", "circadian_preference",
        },
        "team": {
            "big_five", "social_energy_pattern",
        },
        "private": {
            "narcissism_score", "control_score", "anxiety_score",
            "attachment_style", "social_dominance", "intimacy_capacity",
        },
        "restricted": {
            "empathy_score", "total_messages_analyzed",
            "analysis_confidence", "data_sources",
        },
    }

    _ACCESS_HIERARCHY = ["public", "team", "private", "restricted"]

    _BIG_FIVE_CN = {
        "openness": "开放性",
        "conscientiousness": "尽责性",
        "extraversion": "外向性",
        "agreeableness": "宜人性",
        "neuroticism": "神经质",
    }

    _COGNITIVE_CN = {
        "abstract": "抽象思维",
        "concrete": "具体思维",
    }

    _REASONING_CN = {
        "logical": "逻辑推理",
        "intuitive": "直觉推理",
    }

    _CIRCADIAN_CN = {
        "morning": "晨间活跃",
        "evening": "晚间活跃",
        "bimodal": "双峰型",
    }

    _DECISION_CN = {
        "analytical": "分析型",
        "intuitive": "直觉型",
        "mixed": "混合型",
    }

    _HUMOR_CN = {
        "affiliative": "亲和型",
        "self-enhancing": "自嘲型",
        "aggressive": "攻击型",
        "self-defeating": "自贬型",
    }

    def __init__(self, store=None, memory_system=None):
        self.store = store
        self.memory_system = memory_system
        self._ensure_tables()

    def _ensure_tables(self):
        if not self.store:
            return
        try:
            self.store.conn.executescript("""
                CREATE TABLE IF NOT EXISTS personality_profiles (
                    profile_id TEXT PRIMARY KEY,
                    person_id TEXT NOT NULL,
                    version INTEGER DEFAULT 1,
                    big_five TEXT DEFAULT '{}',
                    cognitive_style TEXT DEFAULT '',
                    reasoning_style TEXT DEFAULT '',
                    attachment_style TEXT DEFAULT '',
                    social_dominance REAL DEFAULT 0.5,
                    intimacy_capacity REAL DEFAULT 0.5,
                    social_energy_pattern TEXT DEFAULT '',
                    circadian_preference TEXT DEFAULT '',
                    decision_style TEXT DEFAULT '',
                    humor_style TEXT DEFAULT '',
                    narcissism_score REAL DEFAULT 0.3,
                    control_score REAL DEFAULT 0.3,
                    anxiety_score REAL DEFAULT 0.3,
                    empathy_score REAL DEFAULT 0.5,
                    total_messages_analyzed INTEGER DEFAULT 0,
                    analysis_confidence REAL DEFAULT 0.0,
                    data_sources TEXT DEFAULT '[]',
                    privacy_level TEXT DEFAULT 'team',
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL
                );

                CREATE TABLE IF NOT EXISTS personality_evidence (
                    evidence_id TEXT PRIMARY KEY,
                    profile_id TEXT NOT NULL,
                    trait_name TEXT NOT NULL,
                    source_type TEXT DEFAULT 'chat',
                    source_id TEXT DEFAULT '',
                    evidence_text TEXT DEFAULT '',
                    confidence REAL DEFAULT 0.5,
                    created_at INTEGER NOT NULL,
                    FOREIGN KEY (profile_id) REFERENCES personality_profiles(profile_id)
                );

                CREATE TABLE IF NOT EXISTS personality_versions (
                    version_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    snapshot TEXT NOT NULL,
                    change_reason TEXT DEFAULT '',
                    created_at INTEGER NOT NULL,
                    FOREIGN KEY (profile_id) REFERENCES personality_profiles(profile_id)
                );

                CREATE INDEX IF NOT EXISTS idx_pp_person ON personality_profiles(person_id);
                CREATE INDEX IF NOT EXISTS idx_pp_version ON personality_profiles(person_id, version);
                CREATE INDEX IF NOT EXISTS idx_pe_profile ON personality_evidence(profile_id);
                CREATE INDEX IF NOT EXISTS idx_pe_trait ON personality_evidence(profile_id, trait_name);
                CREATE INDEX IF NOT EXISTS idx_pv_profile ON personality_versions(profile_id);
            """)
            self.store.conn.commit()
        except Exception as e:
            logger.debug("personality_memory: ensure_tables: %s", e)

    def save_profile(self, profile, person_id: str = "main", privacy_level: str = "team") -> str:
        if not self.store:
            return ""

        data = self._profile_to_dict(profile)
        now = int(time.time())

        try:
            cursor = self.store.conn.execute(
                "SELECT profile_id, version FROM personality_profiles WHERE person_id = ? ORDER BY version DESC LIMIT 1",
                (person_id,),
            )
            existing = cursor.fetchone()

            if existing:
                existing_id = existing[0]
                existing_version = existing[1]
                self._save_version_snapshot(existing_id, existing_version, data, reason="incremental_update")
                new_version = existing_version + 1
                self.store.conn.execute(
                    """UPDATE personality_profiles SET
                        big_five = ?, cognitive_style = ?, reasoning_style = ?,
                        attachment_style = ?, social_dominance = ?, intimacy_capacity = ?,
                        social_energy_pattern = ?, circadian_preference = ?,
                        decision_style = ?, humor_style = ?,
                        narcissism_score = ?, control_score = ?, anxiety_score = ?, empathy_score = ?,
                        total_messages_analyzed = ?, analysis_confidence = ?,
                        data_sources = ?, privacy_level = ?, version = ?,
                        updated_at = ?
                    WHERE profile_id = ?""",
                    (
                        data["big_five"], data["cognitive_style"], data["reasoning_style"],
                        data["attachment_style"], data["social_dominance"], data["intimacy_capacity"],
                        data["social_energy_pattern"], data["circadian_preference"],
                        data["decision_style"], data["humor_style"],
                        data["narcissism_score"], data["control_score"], data["anxiety_score"], data["empathy_score"],
                        data["total_messages_analyzed"], data["analysis_confidence"],
                        data["data_sources"], privacy_level, new_version,
                        now, existing_id,
                    ),
                )
                self.store.conn.commit()
                profile_id = existing_id
            else:
                profile_id = self._generate_profile_id(person_id)
                self.store.conn.execute(
                    """INSERT INTO personality_profiles (
                        profile_id, person_id, version, big_five, cognitive_style, reasoning_style,
                        attachment_style, social_dominance, intimacy_capacity, social_energy_pattern,
                        circadian_preference, decision_style, humor_style,
                        narcissism_score, control_score, anxiety_score, empathy_score,
                        total_messages_analyzed, analysis_confidence, data_sources,
                        privacy_level, created_at, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        profile_id, person_id, 1,
                        data["big_five"], data["cognitive_style"], data["reasoning_style"],
                        data["attachment_style"], data["social_dominance"], data["intimacy_capacity"],
                        data["social_energy_pattern"], data["circadian_preference"],
                        data["decision_style"], data["humor_style"],
                        data["narcissism_score"], data["control_score"], data["anxiety_score"], data["empathy_score"],
                        data["total_messages_analyzed"], data["analysis_confidence"],
                        data["data_sources"], privacy_level, now, now,
                    ),
                )
                self.store.conn.commit()

            self._save_evidence(profile_id, profile)

            if self.memory_system:
                self.distill_to_memory(profile, person_id)

            return profile_id
        except Exception as e:
            logger.debug("personality_memory: save_profile: %s", e)
            return ""

    def load_profile(self, person_id: str = "main") -> Optional[dict]:
        if not self.store:
            return None
        try:
            cursor = self.store.conn.execute(
                "SELECT * FROM personality_profiles WHERE person_id = ? ORDER BY version DESC LIMIT 1",
                (person_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            columns = [desc[0] for desc in cursor.description]
            result = dict(zip(columns, row))
            if "big_five" in result and isinstance(result["big_five"], str):
                result["big_five"] = json.loads(result["big_five"])
            if "data_sources" in result and isinstance(result["data_sources"], str):
                result["data_sources"] = json.loads(result["data_sources"])
            return result
        except Exception as e:
            logger.debug("personality_memory: load_profile: %s", e)
            return None

    def load_profile_version(self, person_id: str, version: int) -> Optional[dict]:
        if not self.store:
            return None
        try:
            cursor = self.store.conn.execute(
                "SELECT profile_id FROM personality_profiles WHERE person_id = ? LIMIT 1",
                (person_id,),
            )
            row = cursor.fetchone()
            if not row:
                return None
            profile_id = row[0]

            cursor = self.store.conn.execute(
                "SELECT snapshot, change_reason, created_at FROM personality_versions WHERE profile_id = ? AND version = ?",
                (profile_id, version),
            )
            row = cursor.fetchone()
            if not row:
                return None

            result = json.loads(row[0])
            result["change_reason"] = row[1]
            result["snapshot_created_at"] = row[2]
            return result
        except Exception as e:
            logger.debug("personality_memory: load_profile_version: %s", e)
            return None

    def list_versions(self, person_id: str = "main") -> list[dict]:
        if not self.store:
            return []
        try:
            cursor = self.store.conn.execute(
                "SELECT profile_id FROM personality_profiles WHERE person_id = ? LIMIT 1",
                (person_id,),
            )
            row = cursor.fetchone()
            if not row:
                return []
            profile_id = row[0]

            cursor = self.store.conn.execute(
                "SELECT version_id, version, change_reason, created_at FROM personality_versions WHERE profile_id = ? ORDER BY version ASC",
                (profile_id,),
            )
            rows = cursor.fetchall()
            return [
                {"version_id": r[0], "version": r[1], "change_reason": r[2], "created_at": r[3]}
                for r in rows
            ]
        except Exception as e:
            logger.debug("personality_memory: list_versions: %s", e)
            return []

    def get_evidence(self, profile_id: str, trait_name: str = None) -> list[dict]:
        if not self.store:
            return []
        try:
            if trait_name:
                cursor = self.store.conn.execute(
                    "SELECT evidence_id, trait_name, source_type, source_id, evidence_text, confidence, created_at FROM personality_evidence WHERE profile_id = ? AND trait_name = ?",
                    (profile_id, trait_name),
                )
            else:
                cursor = self.store.conn.execute(
                    "SELECT evidence_id, trait_name, source_type, source_id, evidence_text, confidence, created_at FROM personality_evidence WHERE profile_id = ?",
                    (profile_id,),
                )
            rows = cursor.fetchall()
            return [
                {
                    "evidence_id": r[0], "trait_name": r[1], "source_type": r[2],
                    "source_id": r[3], "evidence_text": r[4], "confidence": r[5],
                    "created_at": r[6],
                }
                for r in rows
            ]
        except Exception as e:
            logger.debug("personality_memory: get_evidence: %s", e)
            return []

    def get_filtered_profile(self, person_id: str, access_level: str = "team") -> dict:
        profile = self.load_profile(person_id)
        if not profile:
            return {}

        allowed_fields = set()
        try:
            hierarchy_idx = self._ACCESS_HIERARCHY.index(access_level)
        except ValueError:
            hierarchy_idx = 1

        for level in self._ACCESS_HIERARCHY[:hierarchy_idx + 1]:
            allowed_fields.update(self._PRIVACY_FIELD_MAP.get(level, set()))

        allowed_fields.update({
            "profile_id", "person_id", "version",
            "created_at", "updated_at", "privacy_level",
        })

        filtered = {}
        for key, value in profile.items():
            if key in allowed_fields:
                filtered[key] = value

        return filtered

    def delete_profile(self, person_id: str) -> bool:
        if not self.store:
            return False
        try:
            cursor = self.store.conn.execute(
                "SELECT profile_id FROM personality_profiles WHERE person_id = ?",
                (person_id,),
            )
            rows = cursor.fetchall()
            if not rows:
                return False

            for row in rows:
                profile_id = row[0]
                self.store.conn.execute(
                    "DELETE FROM personality_evidence WHERE profile_id = ?",
                    (profile_id,),
                )
                self.store.conn.execute(
                    "DELETE FROM personality_versions WHERE profile_id = ?",
                    (profile_id,),
                )

            self.store.conn.execute(
                "DELETE FROM personality_profiles WHERE person_id = ?",
                (person_id,),
            )
            self.store.conn.commit()
            return True
        except Exception as e:
            logger.debug("personality_memory: delete_profile: %s", e)
            return False

    def distill_to_memory(self, profile, person_id: str = "main") -> list[str]:
        if not self.memory_system:
            return []

        memory_ids = []

        summary = self._generate_personality_summary(profile)
        if summary:
            result = self.memory_system.remember(
                content=summary,
                importance="high",
                topics=["personality", "profile"],
                nature="personality_summary",
            )
            if result.get("written") and result.get("memory_id"):
                memory_ids.append(result["memory_id"])

        for attr_name, cn_name in self._BIG_FIVE_CN.items():
            trait = getattr(profile, attr_name, None)
            if isinstance(trait, TraitScore) and trait.confidence > 0:
                level = "高" if trait.score > 0.6 else ("中" if trait.score >= 0.4 else "低")
                content = f"{cn_name}: {level}({trait.score:.2f}), 置信度: {trait.confidence:.2f}"
                result = self.memory_system.remember(
                    content=content,
                    importance="medium",
                    topics=["personality", "big_five", attr_name],
                    nature="personality_trait",
                )
                if result.get("written") and result.get("memory_id"):
                    memory_ids.append(result["memory_id"])

        style_entries = [
            ("cognitive_style", "认知风格", self._COGNITIVE_CN),
            ("reasoning_style", "推理风格", self._REASONING_CN),
            ("circadian_preference", "昼夜节律", self._CIRCADIAN_CN),
            ("decision_style", "决策风格", self._DECISION_CN),
            ("humor_style", "幽默风格", self._HUMOR_CN),
        ]
        for attr_name, cn_name, cn_map in style_entries:
            val = getattr(profile, attr_name, "")
            if val:
                cn_val = cn_map.get(val, val)
                content = f"{cn_name}: {cn_val}"
                result = self.memory_system.remember(
                    content=content,
                    importance="medium",
                    topics=["personality", "style", attr_name],
                    nature="personality_style",
                )
                if result.get("written") and result.get("memory_id"):
                    memory_ids.append(result["memory_id"])

        return memory_ids

    def _generate_profile_id(self, person_id: str) -> str:
        raw = f"personality_{person_id}_{time.time()}"
        return "PERS_" + hashlib.sha256(raw.encode()).hexdigest()[:12]

    def _profile_to_dict(self, profile) -> dict:
        big_five = {}
        for attr in ("openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"):
            trait = getattr(profile, attr, None)
            if isinstance(trait, TraitScore):
                big_five[attr] = {
                    "score": trait.score,
                    "confidence": trait.confidence,
                    "evidence_count": trait.evidence_count,
                }

        return {
            "big_five": json.dumps(big_five, ensure_ascii=False),
            "cognitive_style": profile.cognitive_style,
            "reasoning_style": profile.reasoning_style,
            "attachment_style": profile.attachment_style,
            "social_dominance": profile.social_dominance.score,
            "intimacy_capacity": profile.intimacy_capacity.score,
            "social_energy_pattern": profile.social_energy_pattern,
            "circadian_preference": profile.circadian_preference,
            "decision_style": profile.decision_style,
            "humor_style": profile.humor_style,
            "narcissism_score": profile.narcissism_index.score,
            "control_score": profile.control_tendency.score,
            "anxiety_score": profile.anxiety_level.score,
            "empathy_score": profile.empathy_capacity.score,
            "total_messages_analyzed": profile.total_messages_analyzed,
            "analysis_confidence": profile.analysis_confidence,
            "data_sources": json.dumps(profile.data_sources, ensure_ascii=False),
            "created_at": profile.created_at or int(time.time()),
            "updated_at": profile.updated_at or int(time.time()),
        }

    def _save_version_snapshot(self, profile_id: str, version: int, data: dict, reason: str = ""):
        if not self.store:
            return
        try:
            now = int(time.time())
            snapshot_json = json.dumps(data, ensure_ascii=False)
            self.store.conn.execute(
                "INSERT INTO personality_versions (profile_id, version, snapshot, change_reason, created_at) VALUES (?, ?, ?, ?, ?)",
                (profile_id, version, snapshot_json, reason, now),
            )
            self.store.conn.commit()
        except Exception as e:
            logger.debug("personality_memory: _save_version_snapshot: %s", e)

    def _save_evidence(self, profile_id: str, profile):
        if not self.store:
            return
        try:
            now = int(time.time())
            trait_fields = [
                ("openness", profile.openness),
                ("conscientiousness", profile.conscientiousness),
                ("extraversion", profile.extraversion),
                ("agreeableness", profile.agreeableness),
                ("neuroticism", profile.neuroticism),
                ("social_dominance", profile.social_dominance),
                ("intimacy_capacity", profile.intimacy_capacity),
                ("narcissism_index", profile.narcissism_index),
                ("control_tendency", profile.control_tendency),
                ("anxiety_level", profile.anxiety_level),
                ("empathy_capacity", profile.empathy_capacity),
            ]

            for trait_name, trait in trait_fields:
                if not isinstance(trait, TraitScore):
                    continue
                for i, source_id in enumerate(trait.source_ids):
                    evidence_id = f"EVID_{profile_id[:8]}_{trait_name}_{i}"
                    self.store.conn.execute(
                        "INSERT OR IGNORE INTO personality_evidence (evidence_id, profile_id, trait_name, source_type, source_id, confidence, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (evidence_id, profile_id, trait_name, "chat", source_id, trait.confidence, now),
                    )
            self.store.conn.commit()
        except Exception as e:
            logger.debug("personality_memory: _save_evidence: %s", e)

    @staticmethod
    def _generate_personality_summary(profile) -> str:
        parts = []

        big_five_parts = []
        for attr, cn_name in PersonalityMemory._BIG_FIVE_CN.items():
            trait = getattr(profile, attr, None)
            if isinstance(trait, TraitScore):
                level = "高" if trait.score > 0.6 else ("中" if trait.score >= 0.4 else "低")
                big_five_parts.append(f"{cn_name}{level}({trait.score:.2f})")
        if big_five_parts:
            parts.append("人格画像: " + ", ".join(big_five_parts))

        cognitive = getattr(profile, "cognitive_style", "")
        reasoning = getattr(profile, "reasoning_style", "")
        style_parts = []
        if cognitive:
            style_parts.append(PersonalityMemory._COGNITIVE_CN.get(cognitive, cognitive))
        if reasoning:
            style_parts.append(PersonalityMemory._REASONING_CN.get(reasoning, reasoning))
        if style_parts:
            parts.append("认知风格: " + ", ".join(style_parts))

        social_energy = getattr(profile, "social_energy_pattern", "")
        intimacy = getattr(profile, "intimacy_capacity", None)
        social_parts = []
        if isinstance(intimacy, TraitScore):
            social_parts.append("高亲密度" if intimacy.score > 0.5 else "低亲密度")
        if social_energy:
            social_parts.append(social_energy)
        if social_parts:
            parts.append("社交模式: " + ", ".join(social_parts))

        circadian = getattr(profile, "circadian_preference", "")
        if circadian:
            parts.append(PersonalityMemory._CIRCADIAN_CN.get(circadian, circadian))

        decision = getattr(profile, "decision_style", "")
        if decision:
            parts.append("决策风格: " + PersonalityMemory._DECISION_CN.get(decision, decision))

        humor = getattr(profile, "humor_style", "")
        if humor:
            parts.append("幽默风格: " + PersonalityMemory._HUMOR_CN.get(humor, humor))

        return ". ".join(parts) + "." if parts else ""
