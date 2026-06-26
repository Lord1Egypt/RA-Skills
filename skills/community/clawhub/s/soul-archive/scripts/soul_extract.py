#!/usr/bin/env python3
"""
🧬 灵魂提取器（Soul Extractor）


- 移除 voice 维度
- 移除 relationships 维度（AI 对话中难以采集）
- 移除加密层（全部明文 JSON）
- 新增 workflow 维度（工具/技术栈/硬规则/输出格式偏好/反感的事）
- 新增 aspirations 维度（长期目标/正在做/想学/认知盲区）
- 7 维权重重新分配：identity 8 / personality 18 / language 20 /
  knowledge 14 / memory 18 / workflow 15 / aspirations 7
- P1-4: 写入前做相似度查重，>=0.85 则合并/置信度+1，避免重复条目

用法：
  python3 soul_extract.py --input "对话内容"
  python3 soul_extract.py --mode status

默认数据目录：~/.agent-commons/skills_data/soul-archive/
"""


# ── Windows console safety: force UTF-8 on stdout/stderr so Chinese / emoji
#    don't blow up under the default cp936 codec on Windows PowerShell / cmd.
#    No-op on POSIX terminals that are already UTF-8.
import sys as _sys
try:
    _sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    _sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
except Exception:
    pass

import json
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path

# ============================================================
# Default data structures
# ============================================================

DEFAULT_PROFILE = {
    "soul_version": "3.0",
    "created_at": None,
    "last_updated": None,
    "total_conversations": 0,
    "total_extractions": 0,
    "completeness_score": 0.0,
    "dimensions": {
        "identity": 0.0,
        "personality": 0.0,
        "language_style": 0.0,
        "knowledge": 0.0,
        "memory": 0.0,
        "workflow": 0.0,
        "aspirations": 0.0
    }
}

DEFAULT_BASIC_INFO = {
    "name": None, "nickname": None, "age": None, "birth_year": None,
    "gender": None, "location": None, "hometown": None,
    "occupation": None, "company": None, "education": None,
    "languages": [], "hobbies": [], "self_description": None, "life_motto": None,
    "daily_routine": None, "sleep_schedule": None,
    "food_preferences": [], "food_dislikes": [],
    "music_taste": [], "movie_taste": [], "book_taste": [],
    "travel_preferences": None, "pet_preference": None,
    "aesthetic_style": None, "spending_style": None,
    "online_personas": [], "favorite_apps": [], "social_platforms": [],
    "digital_habits": None, "tech_proficiency": None,
    "_meta": {}
}

DEFAULT_PERSONALITY = {
    "mbti": None,
    "big_five": {
        "openness": None, "conscientiousness": None,
        "extraversion": None, "agreeableness": None, "neuroticism": None
    },
    "traits": [], "values": [],
    "decision_style": None, "communication_preference": None,
    "strengths": [], "weaknesses": [],
    "risk_tolerance": None, "procrastination_level": None,
    "perfectionism_level": None, "planning_style": None,
    "learning_style": None, "work_style": None,
    "social_energy": None, "group_role": None,
    "trust_building": None, "conflict_approach": None,
    "stress_response": None, "motivation_drivers": [], "growth_areas": [],
    "_meta": {}
}

DEFAULT_LANGUAGE = {
    "catchphrases": [], "sentence_patterns": [],
    "preferred_words": [], "avoided_words": [],
    "emoji_usage": {"frequency": "unknown", "favorites": []},
    "punctuation_habits": {},
    "formality_level": None, "verbosity": None,
    "humor_style": None, "response_length_preference": None,
    "thinking_expression": None, "examples": [],
    "dialect_features": [], "filler_words": [],
    "persuasion_style": None, "storytelling_style": None,
    "question_style": None, "agreement_expressions": [],
    "disagreement_expressions": [],
    "greeting_style": None, "farewell_style": None,
    "typing_habits": None,
    "_meta": {}
}

DEFAULT_COMMUNICATION = {
    "directness": None, "logic_vs_emotion": None,
    "detail_level": None, "listening_style": None,
    "conflict_style": None, "encouragement_style": None,
    "criticism_style": None, "_meta": {}
}

DEFAULT_TOPICS = {"topics": [], "_meta": {}}

DEFAULT_KNOWLEDGE = {
    "domains": [], "skills": [], "expertise_level": {},
    "belief_frameworks": [],
    "_meta": {}
}

DEFAULT_EMOTIONAL_PATTERNS = {
    "triggers": {
        "joy": [], "anger": [], "sadness": [], "anxiety": [],
        "excitement": [], "nostalgia": [], "pride": [], "gratitude": [],
        "frustration": [], "curiosity": [], "peace": [], "guilt": []
    },
    "expression_style": None, "emotional_range": None,
    "emotional_awareness": None, "empathy_level": None,
    "coping_mechanisms": [], "comfort_activities": [],
    "celebration_style": None, "_meta": {}
}

# Workflow（procedural memory）
DEFAULT_WORKFLOW = {
    "tools": {
        "ide": [], "terminal": [], "ai_tools": [],
        "vcs": [], "doc_systems": [], "communication": []
    },
    "tech_stack": {
        "languages": [], "frameworks": [], "platforms": []
    },
    "hard_rules": [],
    "collab_conventions": [],
    "cli_habits": [],
    "output_preferences": {
        "preferred_format": None,
        "preferred_length": None,
        "preferred_tone": None,
        "structure_first": None
    },
    "pet_peeves": [],
    "_meta": {}
}

# Aspirations
DEFAULT_ASPIRATIONS = {
    "long_term_goals": [],
    "active_projects": [],
    "identity_aspirations": [],
    "skills_to_learn": [],
    "knowledge_gaps": [],
    "_meta": {}
}

DEFAULT_CONFIG = {
    "privacy_level": "standard",
    "auto_extract": True,
    "auto_reflect": True,
    "auto_context_inject": True,
    "extract_dimensions": {
        "identity": True,
        "personality": True,
        "language_style": True,
        "knowledge": True,
        "episodic_memory": True,
        "emotional_patterns": True,
        "workflow": True,
        "aspirations": True
    },
    "agent_self_improvement": {
        "enabled": True,
        "auto_reflect_on_completion": True,
        "auto_critique_on_correction": True,
        "pattern_extraction": True,
        "recall_on_task_start": True,
        "warn_on_failure_pattern_match": True,
        "auto_distill_threshold": 5
    },
    "deduplication": {
        "enabled": True,
        "similarity_threshold": 0.85
    },
    "sensitive_topics_filter": True,
    "require_confirmation_for": ["health", "finance", "intimate_relationships"],
    "data_retention_days": None
}


# ============================================================
# IO utilities (plaintext only)
# ============================================================

def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default=None):
    if path.exists():
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (UnicodeDecodeError, json.JSONDecodeError):
            pass
    return default if default is not None else {}


def save_json(path: Path, data: dict):
    ensure_dir(path.parent)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def append_jsonl(path: Path, record: dict):
    ensure_dir(path.parent)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(record, ensure_ascii=False) + '\n')


def read_jsonl(path: Path) -> list:
    if not path.exists():
        return []
    entries = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return entries


def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")


# ============================================================
# Similarity-based dedup
# ============================================================

def _similarity(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    a, b = str(a).strip(), str(b).strip()
    if a == b:
        return 1.0

    def _bigrams(s):
        s = s.lower()
        return set(s[i:i + 2] for i in range(len(s) - 1)) if len(s) >= 2 else {s}

    sa, sb = _bigrams(a), _bigrams(b)
    if not sa or not sb:
        return 0.0
    inter = len(sa & sb)
    union = len(sa | sb)
    return inter / union if union > 0 else 0.0


def _dedup_merge_list(existing: list, candidates: list, threshold: float = 0.85) -> tuple:
    if not candidates:
        return existing, 0
    out = list(existing)
    added = 0
    for cand in candidates:
        cand_str = str(cand)
        if any(str(e) == cand_str for e in out):
            continue
        if any(_similarity(str(e), cand_str) >= threshold for e in out):
            continue
        out.append(cand)
        added += 1
    return out, added


# ============================================================
# Soul Archive
# ============================================================

class SoulArchive:
    """7-axis archive: identity / personality / language / knowledge /
    memory / workflow / aspirations"""

    def __init__(self, soul_dir: str):
        self.root = Path(soul_dir)
        self.profile_path = self.root / "profile.json"
        self.config_path = self.root / "config.json"
        self.changelog_path = self.root / "soul_changelog.jsonl"

        self.paths = {
            "basic_info":  self.root / "identity" / "basic_info.json",
            "personality": self.root / "identity" / "personality.json",
            "language":    self.root / "style" / "language.json",
            "communication": self.root / "style" / "communication.json",
            "topics":      self.root / "memory" / "semantic" / "topics.json",
            "knowledge":   self.root / "memory" / "semantic" / "knowledge.json",
            "emotional":   self.root / "memory" / "emotional" / "patterns.json",
            "workflow":    self.root / "workflow" / "preferences.json",
            "aspirations": self.root / "aspirations.json",
        }

    def is_initialized(self) -> bool:
        return self.profile_path.exists()

    def load_profile(self) -> dict:
        return load_json(self.profile_path, DEFAULT_PROFILE.copy())

    def load_config(self) -> dict:
        return load_json(self.config_path, DEFAULT_CONFIG.copy())

    def _dedup_threshold(self) -> float:
        cfg = self.load_config().get("deduplication", {})
        if not cfg.get("enabled", True):
            return 1.01
        return float(cfg.get("similarity_threshold", 0.85))

    def load_all(self) -> dict:
        return {
            "profile":       self.load_profile(),
            "config":        self.load_config(),
            "basic_info":    load_json(self.paths["basic_info"],  DEFAULT_BASIC_INFO.copy()),
            "personality":   load_json(self.paths["personality"], DEFAULT_PERSONALITY.copy()),
            "language":      load_json(self.paths["language"],    DEFAULT_LANGUAGE.copy()),
            "communication": load_json(self.paths["communication"], DEFAULT_COMMUNICATION.copy()),
            "topics":        load_json(self.paths["topics"],      DEFAULT_TOPICS.copy()),
            "knowledge":     load_json(self.paths["knowledge"],   DEFAULT_KNOWLEDGE.copy()),
            "emotional":     load_json(self.paths["emotional"],   DEFAULT_EMOTIONAL_PATTERNS.copy()),
            "workflow":      load_json(self.paths["workflow"],    DEFAULT_WORKFLOW.copy()),
            "aspirations":   load_json(self.paths["aspirations"], DEFAULT_ASPIRATIONS.copy()),
        }

    def save_data(self, key: str, data: dict):
        if key == "profile":
            save_json(self.profile_path, data)
        elif key == "config":
            save_json(self.config_path, data)
        elif key in self.paths:
            save_json(self.paths[key], data)

    # --------------------------------------------------------
    # Save extraction
    # --------------------------------------------------------

    def save_extraction(self, extraction: dict):
        changes = []
        config = self.load_config()
        dims = config.get("extract_dimensions", {})
        thr = self._dedup_threshold()

        # 1. Identity
        if dims.get("identity", True) and extraction.get("basic_info"):
            current = load_json(self.paths["basic_info"], DEFAULT_BASIC_INFO.copy())
            updated = self._merge_identity(current, extraction["basic_info"], thr)
            if updated:
                save_json(self.paths["basic_info"], current)
                changes.append(f"identity: updated {', '.join(updated)}")

        # 2. Personality
        if dims.get("personality", True) and extraction.get("personality"):
            current = load_json(self.paths["personality"], DEFAULT_PERSONALITY.copy())
            updated = self._merge_personality(current, extraction["personality"], thr)
            if updated:
                save_json(self.paths["personality"], current)
                changes.append(f"personality: updated {', '.join(updated)}")

        # 3. Language
        if dims.get("language_style", True) and extraction.get("language"):
            current = load_json(self.paths["language"], DEFAULT_LANGUAGE.copy())
            updated = self._merge_language(current, extraction["language"], thr)
            if updated:
                save_json(self.paths["language"], current)
                changes.append(f"language: updated {', '.join(updated)}")

        # 4. Knowledge & Topics
        if dims.get("knowledge", True) and extraction.get("topics"):
            current = load_json(self.paths["topics"], DEFAULT_TOPICS.copy())
            n = self._merge_topics(current, extraction["topics"], thr)
            if n:
                save_json(self.paths["topics"], current)
                changes.append(f"topics: added/updated {n} topics")
        if dims.get("knowledge", True) and extraction.get("knowledge"):
            current = load_json(self.paths["knowledge"], DEFAULT_KNOWLEDGE.copy())
            updated = self._merge_knowledge(current, extraction["knowledge"], thr)
            if updated:
                save_json(self.paths["knowledge"], current)
                changes.append(f"knowledge: updated {', '.join(updated)}")

        # 5. Memory: episodic + emotional
        if dims.get("episodic_memory", True) and extraction.get("episodic"):
            today = datetime.now().strftime("%Y-%m-%d")
            ep_path = self.root / "memory" / "episodic" / f"{today}.jsonl"
            existing_today = read_jsonl(ep_path)
            existing_events = [e.get("event", "") for e in existing_today]
            added = 0
            for episode in extraction["episodic"]:
                ev = episode.get("event", "")
                if any(_similarity(ev, x) >= thr for x in existing_events if x):
                    continue
                episode["timestamp"] = now_iso()
                append_jsonl(ep_path, episode)
                existing_events.append(ev)
                added += 1
            if added:
                changes.append(f"episodic: added {added} episodes")

        if dims.get("emotional_patterns", True) and extraction.get("emotional"):
            current = load_json(self.paths["emotional"], DEFAULT_EMOTIONAL_PATTERNS.copy())
            updated = self._merge_emotional(current, extraction["emotional"], thr)
            if updated:
                save_json(self.paths["emotional"], current)
                changes.append(f"emotional: updated {', '.join(updated)}")

        # 6. Workflow ⭐
        if dims.get("workflow", True) and extraction.get("workflow"):
            current = load_json(self.paths["workflow"], DEFAULT_WORKFLOW.copy())
            updated = self._merge_workflow(current, extraction["workflow"], thr)
            if updated:
                save_json(self.paths["workflow"], current)
                changes.append(f"workflow: updated {', '.join(updated)}")

        # 7. Aspirations ⭐
        if dims.get("aspirations", True) and extraction.get("aspirations"):
            current = load_json(self.paths["aspirations"], DEFAULT_ASPIRATIONS.copy())
            updated = self._merge_aspirations(current, extraction["aspirations"], thr)
            if updated:
                save_json(self.paths["aspirations"], current)
                changes.append(f"aspirations: updated {', '.join(updated)}")

        # Update profile
        if changes:
            profile = self.load_profile()
            profile["last_updated"] = now_iso()
            profile["total_extractions"] = profile.get("total_extractions", 0) + 1
            profile["total_conversations"] = profile.get("total_conversations", 0) + 1
            dimensions = self._calc_dimension_scores()
            profile["dimensions"] = dimensions
            profile["completeness_score"] = self._calc_completeness_from_scores(dimensions)
            save_json(self.profile_path, profile)
            append_jsonl(self.changelog_path, {
                "timestamp": now_iso(),
                "extraction_id": profile["total_extractions"],
                "changes": changes,
                "summary": extraction.get("summary", ""),
                "completeness": profile["completeness_score"],
                "dimensions": dimensions   # 快照各维度分数
            })
        return changes

    # --------------------------------------------------------
    # Merge strategies
    # --------------------------------------------------------

    def _merge_identity(self, current: dict, new_data: dict, thr: float) -> list:
        updated = []
        meta = current.get("_meta", {})
        for key, value in new_data.items():
            if key.startswith("_") or value is None:
                continue
            if isinstance(value, dict) and "value" in value:
                new_conf = value.get("confidence", 0.5)
                old_conf = meta.get(key, {}).get("confidence", 0)
                if current.get(key) is None or new_conf > old_conf:
                    current[key] = value["value"]
                    meta[key] = {"confidence": new_conf, "updated": now_iso()}
                    updated.append(key)
            else:
                if isinstance(value, list) and isinstance(current.get(key), list):
                    merged, added = _dedup_merge_list(current[key], value, thr)
                    if added:
                        current[key] = merged
                        meta[key] = {"confidence": 0.7, "updated": now_iso()}
                        updated.append(f"{key}(+{added})")
                elif current.get(key) is None:
                    current[key] = value
                    meta[key] = {"confidence": 0.7, "updated": now_iso()}
                    updated.append(key)
        current["_meta"] = meta
        return updated

    def _merge_personality(self, current: dict, new_data: dict, thr: float) -> list:
        updated = []
        for key, value in new_data.items():
            if key.startswith("_") or value is None:
                continue
            if key in ("traits", "values", "motivation_drivers", "growth_areas",
                      "strengths", "weaknesses") and isinstance(value, list):
                merged, added = _dedup_merge_list(current.get(key, []), value, thr)
                if added:
                    current[key] = merged
                    updated.append(f"{key}(+{added})")
            elif key == "big_five" and isinstance(value, dict):
                bf = current.setdefault("big_five", {})
                for dim, score in value.items():
                    if score is not None and bf.get(dim) is None:
                        bf[dim] = score
                        updated.append(f"big_five.{dim}")
            elif current.get(key) is None:
                current[key] = value
                updated.append(key)
        return updated

    def _merge_language(self, current: dict, new_data: dict, thr: float) -> list:
        updated = []
        list_keys = ("catchphrases", "sentence_patterns", "preferred_words",
                    "avoided_words", "examples",
                    "filler_words", "dialect_features",
                    "agreement_expressions", "disagreement_expressions")
        for key, value in new_data.items():
            if key.startswith("_") or value is None:
                continue
            if key in list_keys and isinstance(value, list):
                merged, added = _dedup_merge_list(current.get(key, []), value, thr)
                if added:
                    current[key] = merged
                    updated.append(f"{key}(+{added})")
            elif key == "emoji_usage" and isinstance(value, dict):
                eu = current.setdefault("emoji_usage", {})
                if value.get("frequency"):
                    eu["frequency"] = value["frequency"]
                if value.get("favorites"):
                    merged, added = _dedup_merge_list(eu.get("favorites", []),
                                                       value["favorites"], thr)
                    if added:
                        eu["favorites"] = merged
                        updated.append("emoji_usage")
            elif current.get(key) is None:
                current[key] = value
                updated.append(key)
        return updated

    def _merge_topics(self, current: dict, new_topics: list, thr: float) -> int:
        existing = {t["name"]: t for t in current.get("topics", []) if t.get("name")}
        existing_names = list(existing.keys())
        count = 0
        for topic in new_topics:
            name = topic.get("name")
            if not name:
                continue
            match_name = None
            if name in existing:
                match_name = name
            else:
                for ex in existing_names:
                    if _similarity(ex, name) >= thr:
                        match_name = ex
                        break
            if match_name:
                et = existing[match_name]
                et["frequency"] = et.get("frequency", 0) + 1
                et["last_mentioned"] = datetime.now().strftime("%Y-%m-%d")
                if topic.get("key_opinions"):
                    merged, added = _dedup_merge_list(et.get("key_opinions", []),
                                                       topic["key_opinions"], thr)
                    if added:
                        et["key_opinions"] = merged
                if topic.get("sentiment"):
                    et["sentiment"] = topic["sentiment"]
                if topic.get("stance"):
                    et["stance"] = topic["stance"]
                count += 1
            else:
                topic.setdefault("frequency", 1)
                topic.setdefault("last_mentioned", datetime.now().strftime("%Y-%m-%d"))
                current.setdefault("topics", []).append(topic)
                existing[name] = topic
                existing_names.append(name)
                count += 1
        return count

    def _merge_knowledge(self, current: dict, new_data: dict, thr: float) -> list:
        updated = []
        for key in ("domains", "skills", "belief_frameworks"):
            value = new_data.get(key)
            if isinstance(value, list) and value:
                merged, added = _dedup_merge_list(current.get(key, []), value, thr)
                if added:
                    current[key] = merged
                    updated.append(f"{key}(+{added})")
        if isinstance(new_data.get("expertise_level"), dict):
            ex = current.setdefault("expertise_level", {})
            for k, v in new_data["expertise_level"].items():
                if k not in ex:
                    ex[k] = v
                    updated.append(f"expertise.{k}")
        return updated

    def _merge_emotional(self, current: dict, new_data: dict, thr: float) -> list:
        updated = []
        if new_data.get("triggers"):
            triggers = current.setdefault("triggers", {})
            for emotion, items in new_data["triggers"].items():
                if items:
                    merged, added = _dedup_merge_list(triggers.get(emotion, []), items, thr)
                    if added:
                        triggers[emotion] = merged
                        updated.append(f"triggers.{emotion}")
        for key in ("expression_style", "emotional_range", "emotional_awareness",
                    "empathy_level", "celebration_style"):
            if new_data.get(key) and current.get(key) is None:
                current[key] = new_data[key]
                updated.append(key)
        for list_key in ("coping_mechanisms", "comfort_activities"):
            if new_data.get(list_key):
                merged, added = _dedup_merge_list(current.get(list_key, []),
                                                   new_data[list_key], thr)
                if added:
                    current[list_key] = merged
                    updated.append(list_key)
        return updated

    def _merge_workflow(self, current: dict, new_data: dict, thr: float) -> list:
        """Merge workflow preferences"""
        updated = []
        # tools
        if isinstance(new_data.get("tools"), dict):
            tools = current.setdefault("tools", {})
            for cat, items in new_data["tools"].items():
                if isinstance(items, list) and items:
                    merged, added = _dedup_merge_list(tools.get(cat, []), items, thr)
                    if added:
                        tools[cat] = merged
                        updated.append(f"tools.{cat}(+{added})")
        # tech_stack
        if isinstance(new_data.get("tech_stack"), dict):
            stack = current.setdefault("tech_stack", {})
            for cat, items in new_data["tech_stack"].items():
                if isinstance(items, list) and items:
                    merged, added = _dedup_merge_list(stack.get(cat, []), items, thr)
                    if added:
                        stack[cat] = merged
                        updated.append(f"tech_stack.{cat}(+{added})")
        # list-typed
        for key in ("hard_rules", "collab_conventions", "cli_habits", "pet_peeves"):
            value = new_data.get(key)
            if isinstance(value, list) and value:
                merged, added = _dedup_merge_list(current.get(key, []), value, thr)
                if added:
                    current[key] = merged
                    updated.append(f"{key}(+{added})")
        # output_preferences
        if isinstance(new_data.get("output_preferences"), dict):
            op = current.setdefault("output_preferences", {})
            for k, v in new_data["output_preferences"].items():
                if v is not None and op.get(k) is None:
                    op[k] = v
                    updated.append(f"output_pref.{k}")
        return updated

    def _merge_aspirations(self, current: dict, new_data: dict, thr: float) -> list:
        """Merge aspirations"""
        updated = []
        for key in ("long_term_goals", "active_projects", "identity_aspirations",
                    "skills_to_learn", "knowledge_gaps"):
            value = new_data.get(key)
            if isinstance(value, list) and value:
                # active_projects 用 dict 类型，按 name 去重
                if key == "active_projects":
                    existing_names = {p.get("name") for p in current.get(key, [])
                                     if isinstance(p, dict)}
                    added_count = 0
                    for proj in value:
                        if isinstance(proj, dict):
                            name = proj.get("name")
                            if name and name not in existing_names:
                                current.setdefault(key, []).append(proj)
                                existing_names.add(name)
                                added_count += 1
                        else:
                            # 字符串形式：当作 name 处理
                            if proj not in existing_names:
                                current.setdefault(key, []).append({"name": proj})
                                existing_names.add(proj)
                                added_count += 1
                    if added_count:
                        updated.append(f"{key}(+{added_count})")
                else:
                    merged, added = _dedup_merge_list(current.get(key, []), value, thr)
                    if added:
                        current[key] = merged
                        updated.append(f"{key}(+{added})")
        return updated

    # --------------------------------------------------------
    # Completeness scoring (7-axis weights)
    # --------------------------------------------------------

    @staticmethod
    def _saturation(value: float, threshold: float) -> float:
        import math
        if value <= 0:
            return 0.0
        return min(1.0, math.log10(1 + value) / math.log10(1 + threshold))

    @staticmethod
    def _early_penalty(extractions: int) -> float:
        if extractions <= 0:
            return 0.0
        if extractions < 30:
            return 0.30
        if extractions < 100:
            return 0.45
        if extractions < 300:
            return 0.65
        if extractions < 1000:
            return 0.82
        if extractions < 3000:
            return 0.92
        return 1.0

    # 7-axis weights
    DIM_WEIGHTS = {
        "identity":       0.08,
        "personality":    0.18,
        "language_style": 0.20,
        "knowledge":      0.14,
        "memory":         0.18,   # episodic + emotional 合并
        "workflow":       0.15,   # ⭐ 新维度
        "aspirations":    0.07,   # ⭐ 新维度
    }

    def _calc_completeness_from_scores(self, scores: dict) -> float:
        raw_total = sum(scores.get(k, 0) * w for k, w in self.DIM_WEIGHTS.items())
        profile = self.load_profile()
        extractions = profile.get("total_extractions", 0)
        return round(raw_total * self._early_penalty(extractions), 3)

    def _calc_completeness(self) -> float:
        return self._calc_completeness_from_scores(self._calc_dimension_scores())

    def _calc_dimension_scores(self) -> dict:
        sat = self._saturation
        scores = {}

        # Identity
        bi = load_json(self.paths["basic_info"], {})
        core_fields = ["name", "occupation", "location"]
        filled = sum(1 for f in core_fields if bi.get(f))
        extra_fields = ["age", "gender", "education", "hometown", "hobbies"]
        filled += sum(0.5 for f in extra_fields if bi.get(f))
        lifestyle_fields = ["daily_routine", "sleep_schedule", "food_preferences",
                           "music_taste", "movie_taste", "book_taste",
                           "aesthetic_style", "spending_style"]
        filled += sum(0.3 for f in lifestyle_fields if bi.get(f))
        digital_fields = ["favorite_apps", "social_platforms", "tech_proficiency"]
        filled += sum(0.3 for f in digital_fields if bi.get(f))
        max_score = (len(core_fields) + len(extra_fields) * 0.5
                    + len(lifestyle_fields) * 0.3 + len(digital_fields) * 0.3)
        profile = self.load_profile()
        extractions = profile.get("total_extractions", 0)
        field_ratio = filled / max_score if max_score > 0 else 0
        scores["identity"] = round(min(0.85, field_ratio) * 0.3
                                    + sat(extractions, 5000) * 0.7 * 0.85, 2)

        # Personality
        ps = load_json(self.paths["personality"], {})
        trait_count = len(ps.get("traits", []))
        value_count = len(ps.get("values", []))
        bf_count = sum(1 for v in ps.get("big_five", {}).values() if v is not None)
        behavior_fields = ["risk_tolerance", "procrastination_level", "planning_style",
                          "learning_style", "work_style"]
        behavior_filled = sum(1 for f in behavior_fields if ps.get(f))
        social_fields = ["social_energy", "group_role", "conflict_approach"]
        social_filled = sum(1 for f in social_fields if ps.get(f))
        motivation_count = len(ps.get("motivation_drivers", []))
        scores["personality"] = round(
            sat(trait_count, 600000) * 0.30 +
            sat(value_count, 180000) * 0.10 +
            sat(motivation_count, 180000) * 0.55 +
            (bf_count / 5) * 0.02 +
            (behavior_filled / len(behavior_fields)) * 0.01 +
            (social_filled / len(social_fields)) * 0.01
        , 2)

        # Language
        lang = load_json(self.paths["language"], {})
        cp_count = len(lang.get("catchphrases", []))
        sp_count = len(lang.get("sentence_patterns", []))
        ex_count = len(lang.get("examples", []))
        deep_lang_fields = ["dialect_features", "filler_words",
                           "persuasion_style", "storytelling_style",
                           "agreement_expressions", "disagreement_expressions"]
        deep_filled = sum(1 for f in deep_lang_fields if lang.get(f))
        scores["language_style"] = round(
            sat(cp_count, 1200000) * 0.30 +
            sat(sp_count, 1000000) * 0.25 +
            sat(ex_count, 4000000) * 0.43 +
            (deep_filled / len(deep_lang_fields)) * 0.02
        , 2)

        # Knowledge: topics + belief_frameworks + skills
        topics = load_json(self.paths["topics"], {})
        topic_count = len(topics.get("topics", []))
        knowl = load_json(self.paths["knowledge"], {})
        belief_count = len(knowl.get("belief_frameworks", []))
        skills_count = len(knowl.get("skills", []))
        scores["knowledge"] = round(
            sat(topic_count, 2000000) * 0.7 +
            sat(belief_count, 100) * 0.2 +
            sat(skills_count, 1000) * 0.1
        , 2)

        # Memory: episodic + emotional triggers
        ep_dir = self.root / "memory" / "episodic"
        ep_count = 0
        if ep_dir.exists():
            for f in ep_dir.glob("*.jsonl"):
                with open(f, 'r', encoding='utf-8') as fh:
                    ep_count += sum(1 for _ in fh)
        emo = load_json(self.paths["emotional"], {})
        triggers = emo.get("triggers", {}) or {}
        emo_count = sum(len(v) for v in triggers.values() if isinstance(v, list))
        scores["memory"] = round(
            sat(ep_count, 6000000) * 0.75 +
            sat(emo_count, 500) * 0.25
        , 2)

        # Workflow ⭐
        wf = load_json(self.paths["workflow"], DEFAULT_WORKFLOW.copy())
        tools_count = sum(len(v) for v in (wf.get("tools") or {}).values()
                         if isinstance(v, list))
        stack_count = sum(len(v) for v in (wf.get("tech_stack") or {}).values()
                         if isinstance(v, list))
        rules_count = len(wf.get("hard_rules", []))
        peeves_count = len(wf.get("pet_peeves", []))
        cli_count = len(wf.get("cli_habits", []))
        op = wf.get("output_preferences") or {}
        op_filled = sum(1 for k in ("preferred_format", "preferred_length",
                                     "preferred_tone", "structure_first")
                       if op.get(k))
        scores["workflow"] = round(
            sat(tools_count, 200) * 0.25 +
            sat(stack_count, 200) * 0.20 +
            sat(rules_count, 100) * 0.25 +
            sat(peeves_count, 50) * 0.10 +
            sat(cli_count, 100) * 0.10 +
            (op_filled / 4) * 0.10
        , 2)

        # Aspirations ⭐
        asp = load_json(self.paths["aspirations"], DEFAULT_ASPIRATIONS.copy())
        goals_c = len(asp.get("long_term_goals", []))
        proj_c = len(asp.get("active_projects", []))
        idasp_c = len(asp.get("identity_aspirations", []))
        skills_c = len(asp.get("skills_to_learn", []))
        gaps_c = len(asp.get("knowledge_gaps", []))
        scores["aspirations"] = round(
            sat(goals_c, 50) * 0.30 +
            sat(proj_c, 100) * 0.30 +
            sat(idasp_c, 30) * 0.15 +
            sat(skills_c, 100) * 0.15 +
            sat(gaps_c, 100) * 0.10
        , 2)

        return scores

    def get_status_report(self) -> str:
        profile = self.load_profile()
        scores = self._calc_dimension_scores()
        completeness = self._calc_completeness()

        lines = [
            "🧬 灵魂存档状态报告 (7-axis)",
            "━━━━━━━━━━━━━━━━━━━━━━━━",
            f"总完整度: {completeness:.1%}",
            f"总提取次数: {profile.get('total_extractions', 0)}",
            f"最后更新: {profile.get('last_updated', '从未')}",
            "",
            "各维度完整度:",
        ]

        dim_names = {
            "identity":       ("👤 身份信息",  0.08),
            "personality":    ("💫 性格特征",  0.18),
            "language_style": ("🗣️ 语言风格",  0.20),
            "knowledge":      ("🧠 知识观点",  0.14),
            "memory":         ("📝 记忆/情感", 0.18),
            "workflow":       ("⚙️ 工作偏好",  0.15),
            "aspirations":    ("🎯 理想抱负",  0.07),
        }

        for key, (name, w) in dim_names.items():
            score = scores.get(key, 0)
            bar = "█" * int(score * 10) + "░" * (10 - int(score * 10))
            lines.append(f"  {name} ({int(w*100)}%): [{bar}] {score:.0%}")

        return "\n".join(lines)


# ============================================================
# ExtractionBuilder
# ============================================================

class ExtractionBuilder:

    def __init__(self):
        self.result = {
            "basic_info": {},
            "personality": {},
            "language": {},
            "topics": [],
            "knowledge": {},
            "episodic": [],
            "emotional": {},
            "workflow": {},
            "aspirations": {},
            "summary": ""
        }

    # ---- Identity ----
    def set_identity(self, **kwargs):
        self.result["basic_info"].update(kwargs)
        return self

    def set_lifestyle(self, **kwargs):
        self.result["basic_info"].update(kwargs)
        return self

    def add_food_preference(self, food: str):
        self.result.setdefault("basic_info", {}).setdefault("food_preferences", []).append(food)
        return self

    def add_music_taste(self, genre: str):
        self.result.setdefault("basic_info", {}).setdefault("music_taste", []).append(genre)
        return self

    def add_favorite_app(self, app: str):
        self.result.setdefault("basic_info", {}).setdefault("favorite_apps", []).append(app)
        return self

    # ---- Personality ----
    def set_personality(self, **kwargs):
        self.result["personality"].update(kwargs)
        return self

    def set_behavior(self, **kwargs):
        self.result["personality"].update(kwargs)
        return self

    def add_trait(self, trait: str):
        self.result.setdefault("personality", {}).setdefault("traits", []).append(trait)
        return self

    def add_value(self, value: str):
        self.result.setdefault("personality", {}).setdefault("values", []).append(value)
        return self

    def add_motivation(self, driver: str):
        self.result.setdefault("personality", {}).setdefault("motivation_drivers", []).append(driver)
        return self

    # ---- Language ----
    def set_language(self, **kwargs):
        self.result["language"].update(kwargs)
        return self

    def add_catchphrase(self, phrase: str):
        self.result.setdefault("language", {}).setdefault("catchphrases", []).append(phrase)
        return self

    def add_sentence_pattern(self, pattern: str):
        self.result.setdefault("language", {}).setdefault("sentence_patterns", []).append(pattern)
        return self

    def add_language_example(self, example: str):
        self.result.setdefault("language", {}).setdefault("examples", []).append(example)
        return self

    def add_filler_word(self, word: str):
        self.result.setdefault("language", {}).setdefault("filler_words", []).append(word)
        return self

    def add_dialect_feature(self, feature: str):
        self.result.setdefault("language", {}).setdefault("dialect_features", []).append(feature)
        return self

    def add_agreement_expression(self, expr: str):
        self.result.setdefault("language", {}).setdefault("agreement_expressions", []).append(expr)
        return self

    def add_disagreement_expression(self, expr: str):
        self.result.setdefault("language", {}).setdefault("disagreement_expressions", []).append(expr)
        return self

    # ---- Knowledge ----
    def add_topic(self, name: str, sentiment: str = None, stance: str = None, opinions: list = None):
        topic = {"name": name}
        if sentiment:
            topic["sentiment"] = sentiment
        if stance:
            topic["stance"] = stance
        if opinions:
            topic["key_opinions"] = opinions
        self.result["topics"].append(topic)
        return self

    def add_belief_framework(self, name: str):
        self.result.setdefault("knowledge", {}).setdefault("belief_frameworks", []).append(name)
        return self

    def add_skill(self, name: str):
        self.result.setdefault("knowledge", {}).setdefault("skills", []).append(name)
        return self

    def add_domain(self, name: str):
        self.result.setdefault("knowledge", {}).setdefault("domains", []).append(name)
        return self

    # ---- Memory ----
    def add_episode(self, event: str, emotion: str = None, context: str = None,
                    significance: str = "normal"):
        ep = {"event": event, "significance": significance}
        if emotion:
            ep["emotion"] = emotion
        if context:
            ep["context"] = context
        self.result["episodic"].append(ep)
        return self

    def add_emotional_trigger(self, emotion: str, trigger: str):
        self.result.setdefault("emotional", {}).setdefault("triggers", {})\
            .setdefault(emotion, []).append(trigger)
        return self

    def add_comfort_activity(self, activity: str):
        self.result.setdefault("emotional", {}).setdefault("comfort_activities", []).append(activity)
        return self

    # ---- Workflow ⭐ ----
    def add_tool(self, category: str, name: str):
        """category: ide/terminal/ai_tools/vcs/doc_systems/communication"""
        self.result.setdefault("workflow", {}).setdefault("tools", {})\
            .setdefault(category, []).append(name)
        return self

    def add_tech(self, category: str, name: str):
        """category: languages/frameworks/platforms"""
        self.result.setdefault("workflow", {}).setdefault("tech_stack", {})\
            .setdefault(category, []).append(name)
        return self

    def add_hard_rule(self, rule: str):
        self.result.setdefault("workflow", {}).setdefault("hard_rules", []).append(rule)
        return self

    def add_collab_convention(self, conv: str):
        self.result.setdefault("workflow", {}).setdefault("collab_conventions", []).append(conv)
        return self

    def add_cli_habit(self, habit: str):
        self.result.setdefault("workflow", {}).setdefault("cli_habits", []).append(habit)
        return self

    def add_pet_peeve(self, peeve: str):
        self.result.setdefault("workflow", {}).setdefault("pet_peeves", []).append(peeve)
        return self

    def set_output_preferences(self, **kwargs):
        self.result.setdefault("workflow", {}).setdefault("output_preferences", {}).update(kwargs)
        return self

    # ---- Aspirations ⭐ ----
    def add_long_term_goal(self, goal: str):
        self.result.setdefault("aspirations", {}).setdefault("long_term_goals", []).append(goal)
        return self

    def add_active_project(self, name: str, status: str = None, expectation: str = None):
        proj = {"name": name}
        if status:
            proj["status"] = status
        if expectation:
            proj["expectation"] = expectation
        self.result.setdefault("aspirations", {}).setdefault("active_projects", []).append(proj)
        return self

    def add_identity_aspiration(self, asp: str):
        self.result.setdefault("aspirations", {}).setdefault("identity_aspirations", []).append(asp)
        return self

    def add_skill_to_learn(self, skill: str):
        self.result.setdefault("aspirations", {}).setdefault("skills_to_learn", []).append(skill)
        return self

    def add_knowledge_gap(self, gap: str):
        self.result.setdefault("aspirations", {}).setdefault("knowledge_gaps", []).append(gap)
        return self

    # ---- Misc ----
    def set_summary(self, summary: str):
        self.result["summary"] = summary
        return self

    def build(self) -> dict:
        return self.result


# ============================================================
# CLI entry
# ============================================================

def main():
    from soul_paths import resolve_soul_dir
    default_soul_dir = str(resolve_soul_dir())
    parser = argparse.ArgumentParser(description="🧬 灵魂提取器")
    parser.add_argument("--soul-dir", default=default_soul_dir,
                        help=f"灵魂数据目录路径（默认: {default_soul_dir}）")
    parser.add_argument("--input", help="对话内容（纯文本，直接传入）")
    parser.add_argument("--mode", default="auto", choices=["auto", "manual", "status"],
                        help="模式")

    args = parser.parse_args()

    archive = SoulArchive(args.soul_dir)

    if args.mode == "status":
        if not archive.is_initialized():
            print("❌ 灵魂存档尚未初始化。请先运行 soul_init.py")
            sys.exit(1)
        print(archive.get_status_report())
        return

    if not args.input:
        print("请通过 --input 提供对话内容（纯文本）")
        sys.exit(1)

    if not archive.is_initialized():
        print("❌ 灵魂存档尚未初始化。请先运行 soul_init.py")
        sys.exit(1)

    print(f"📖 收到对话内容（{len(args.input)} 字符）")
    print(f"📂 灵魂存档路径：{args.soul_dir}")
    print()
    print("请使用 ExtractionBuilder 构建提取结果：")
    print("```python")
    print("from soul_extract import SoulArchive, ExtractionBuilder")
    print(f"archive = SoulArchive('{args.soul_dir}')")
    print("builder = ExtractionBuilder()")
    print("builder.set_identity(name='张三', occupation='程序员')")
    print("builder.add_catchphrase('你懂我意思吧')")
    print("builder.add_topic('人工智能', sentiment='positive', stance='乐观派')")
    print("builder.add_tool('ide', 'VS Code')                 # ⭐ workflow")
    print("builder.add_hard_rule('禁止 git rebase')           # ⭐ workflow")
    print("builder.add_pet_peeve('反感冗长解释')              # ⭐ workflow")
    print("builder.add_long_term_goal('做一个独立开发者')      # ⭐ aspirations")
    print("builder.add_knowledge_gap('Rust 异步编程')          # ⭐ aspirations")
    print("builder.set_summary('本次发现：用户是程序员，重视效率')")
    print("changes = archive.save_extraction(builder.build())")
    print("```")


if __name__ == "__main__":
    main()
