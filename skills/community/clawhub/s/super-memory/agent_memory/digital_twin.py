from __future__ import annotations
"""
digital_twin.py - 数字孪生基础模块 — EXPERIMENTAL, no usage examples or integration tests.

⚠️ DISCLAIMER: Digital twin profiling is an opt-in feature that generates
statistical summaries from memory data. It does NOT represent an authoritative
or factual assessment of any person. Results should be treated as approximate
references only, never as definitive personality judgments. Enable only with
explicit user consent via AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED=true.

v7.5: 从工具到存在的第一步
- 整合 5 个模块的人格数据 → 统一画像
- 认知模式分析
- 决策模式提取
- 人格画像持久化

v8.0: 个人风格 Agent
- 风格混合机制
- 角色隔离
- 外部风格导入
"""

import json
import hashlib
import logging
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Any
from datetime import datetime
from .role_template import RoleTemplate, merge_styles

logger = logging.getLogger(__name__)


@dataclass
class CognitiveStyle:
    """认知风格"""
    reflective_depth: float  # 反思深度 0-1
    intuition_bias: float    # 直觉倾向 0-1
    risk_tolerance: float    # 风险容忍度 0-1
    complexity_preference: float  # 复杂度偏好 0-1
    update_source: str
    updated_at: int = None


@dataclass
class DecisionPattern:
    """决策模式"""
    pattern_id: str
    pattern_type: str  # performance / usability / collective / individual
    context: str
    frequency: int
    confidence: float
    examples: List[str]
    updated_at: int = None


@dataclass
class PersonaProfile:
    """人格画像"""
    profile_id: str
    version: int
    cognitive_summary: str
    decision_summary: str
    emotion_summary: str
    knowledge_summary: str
    values_summary: str
    overall_confidence: float
    generated_at: int = None


class DigitalTwinProfiler:
    """数字孪生分析器"""
    
    def __init__(self, store, emotion_analyzer, self_model, motivation_engine, narrative_builder, quality_evaluator, llm_fn=None):
        self.store = store
        self.emotion = emotion_analyzer
        self.self_model = self_model
        self.motivation = motivation_engine
        self.narrative = narrative_builder
        self.quality = quality_evaluator
        self._llm_fn = llm_fn
        self._ensure_schema()
    
    def _ensure_schema(self):
        """确保数字孪生相关表存在"""
        try:
            self.store.register_schema("digital_twin", '''
                CREATE TABLE IF NOT EXISTS cognitive_style (
                    style_id TEXT PRIMARY KEY,
                    reflective_depth REAL DEFAULT 0.5,
                    intuition_bias REAL DEFAULT 0.5,
                    risk_tolerance REAL DEFAULT 0.5,
                    complexity_preference REAL DEFAULT 0.5,
                    update_source TEXT,
                    updated_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                );

                CREATE TABLE IF NOT EXISTS decision_pattern (
                    pattern_id TEXT PRIMARY KEY,
                    pattern_type TEXT NOT NULL,
                    context TEXT,
                    frequency INTEGER DEFAULT 0,
                    confidence REAL DEFAULT 0.5,
                    examples TEXT,
                    updated_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                );

                CREATE TABLE IF NOT EXISTS persona_profile (
                    profile_id TEXT PRIMARY KEY,
                    version INTEGER DEFAULT 1,
                    cognitive_summary TEXT,
                    decision_summary TEXT,
                    emotion_summary TEXT,
                    knowledge_summary TEXT,
                    values_summary TEXT,
                    overall_confidence REAL DEFAULT 0.5,
                    generated_at INTEGER NOT NULL DEFAULT (strftime('%s','now'))
                );
            ''')
        except Exception as e:
            logger.warning("digital_twin: %s", e)
    
    def build_unified_profile(self) -> Dict[str, Any]:
        """构建统一人格画像"""
        logger.info("开始构建统一人格画像...")
        
        profile = {
            "cognitive_style": self.extract_cognitive_style(),
            "decision_patterns": self.extract_decision_patterns(),
            "emotion_patterns": self.extract_emotion_patterns(),
            "knowledge_boundaries": self.extract_knowledge_boundaries(),
            "values": self.extract_values(),
        }
        
        # 持久化画像
        self._persist_profile(profile)
        
        logger.info("统一人格画像构建完成")
        return profile
    
    def extract_cognitive_style(self) -> Dict[str, float]:
        """提取认知风格"""
        # 从 self_model 提取反思深度
        traces = self.self_model.get_traces(limit=100)
        if not traces:
            return {
                "reflective_depth": 0.5,
                "intuition_bias": 0.5,
                "risk_tolerance": 0.5,
                "complexity_preference": 0.5
            }
        
        # 计算反思深度：步骤数 / 平均置信度
        reflective_depth = min(1.0, sum(len(trace.get('steps', [])) for trace in traces) / 100)
        
        # 计算直觉倾向：低置信度快速决策的比例
        intuition_bias = sum(1 for trace in traces if trace.get('confidence', 1.0) < 0.6) / len(traces)
        
        # 风险容忍度：基于决策模式
        risk_tolerance = self._calculate_risk_tolerance()
        
        # 复杂度偏好：基于记忆内容长度
        complexity_preference = self._calculate_complexity_preference()
        
        return {
            "reflective_depth": round(reflective_depth, 2),
            "intuition_bias": round(intuition_bias, 2),
            "risk_tolerance": round(risk_tolerance, 2),
            "complexity_preference": round(complexity_preference, 2)
        }
    
    def extract_decision_patterns(self) -> List[Dict[str, Any]]:
        """提取决策模式"""
        # 从因果链提取决策模式
        patterns = []
        
        # 性能优先 vs 易用优先
        performance_pattern = self._extract_performance_vs_usability()
        if performance_pattern:
            patterns.append(performance_pattern)
        
        # 集体决策 vs 个人决策
        collective_pattern = self._extract_collective_vs_individual()
        if collective_pattern:
            patterns.append(collective_pattern)
        
        # 持久化决策模式
        for pattern in patterns:
            self._persist_decision_pattern(pattern)
        
        return patterns
    
    def extract_emotion_patterns(self) -> Dict[str, Any]:
        """提取情感模式（v8.2: 含 Plutchik 8维 + dominance + compound）"""
        emotions = self._get_recent_emotions(limit=1000)
        if not emotions:
            return {
                "positive_bias": 0.5,
                "arousal_level": 0.5,
                "dominance_level": 0.5,
                "emotion_stability": 0.5,
                "dominant_emotions": {},
                "top_compound_emotions": [],
            }

        # ⚠️ 安全: positive_bias 向 0 回归 30%，防止持久负面偏见
        raw_positive_bias = sum(e.get('valence', 0) for e in emotions) / len(emotions)
        positive_bias = raw_positive_bias * 0.7
        arousal_level = sum(e.get('arousal', 0) for e in emotions) / len(emotions)
        dominance_level = sum(e.get('dominance', 0.5) for e in emotions) / len(emotions)

        valences = [e.get('valence', 0) for e in emotions]
        mean_valence = sum(valences) / len(valences)
        emotion_stability = 1.0 - (sum((v - mean_valence)**2 for v in valences) / len(valences))**0.5

        dominant_emotions = {}
        for e in emotions:
            pe = e.get('primary_emotions', '{}')
            if isinstance(pe, str):
                import json as _json
                try:
                    pe = _json.loads(pe)
                except (ValueError, TypeError):
                    pe = {}
            if isinstance(pe, dict):
                for emo, score in pe.items():
                    dominant_emotions[emo] = dominant_emotions.get(emo, 0) + score

        if dominant_emotions:
            total = sum(dominant_emotions.values())
            dominant_emotions = {k: round(v / total, 3) for k, v in sorted(dominant_emotions.items(), key=lambda x: x[1], reverse=True)[:5]}

        compound_counts = {}
        for e in emotions:
            ce = e.get('compound_emotions', '[]')
            if isinstance(ce, str):
                import json as _json
                try:
                    ce = _json.loads(ce)
                except (ValueError, TypeError):
                    ce = []
            if isinstance(ce, list):
                for item in ce:
                    if isinstance(item, dict) and 'name' in item:
                        name = item['name']
                        compound_counts[name] = compound_counts.get(name, 0) + 1

        top_compound = sorted(compound_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_compound_emotions = [{"name": n, "count": c} for n, c in top_compound]

        return {
            "positive_bias": round(positive_bias, 2),
            "arousal_level": round(arousal_level, 2),
            "dominance_level": round(dominance_level, 2),
            "emotion_stability": round(emotion_stability, 2),
            "dominant_emotions": dominant_emotions,
            "top_compound_emotions": top_compound_emotions,
        }
    
    def extract_knowledge_boundaries(self) -> Dict[str, Any]:
        """提取知识边界"""
        # 从主题分布提取
        topics = self._get_topic_distribution()
        
        # 深度领域：记忆数 > 10 的主题
        deep_topics = [t for t, count in topics.items() if count > 10]
        
        # 广度领域：记忆数 <= 10 的主题
        broad_topics = [t for t, count in topics.items() if count <= 10]
        
        return {
            "deep_topics": deep_topics,
            "broad_topics": broad_topics,
            "topic_diversity": len(topics)
        }
    
    def extract_values(self) -> Dict[str, float]:
        """提取价值观"""
        # 从 narrative 提取
        try:
            identity = self.narrative.build_identity_profile()
            values = identity.get('core_values', {})
            return values
        except Exception as e:
            logger.debug("extract_values failed: %s", e)
            return {
                "performance": 0.5,
                "usability": 0.5,
                "innovation": 0.5,
                "stability": 0.5
            }
    
    def _calculate_risk_tolerance(self, memories=None) -> float:
        """Compute risk tolerance from actual behavior patterns."""
        if not memories:
            try:
                rows = self.store.execute_sql(
                    "SELECT content FROM memories ORDER BY time_ts DESC LIMIT 500",
                    fetch=True,
                )
                memories = rows
            except Exception as e:
                logger.debug("_calculate_risk_tolerance query failed: %s", e)
                return 0.5
        if not memories:
            return 0.5
        # Count risk-related keywords in memories
        risk_seeking = sum(1 for m in memories if any(kw in (m.get("content","").lower())
                          for kw in ["尝试", "冒险", "挑战", "新", "try", "risk", "experiment", "bold"]))
        risk_averse = sum(1 for m in memories if any(kw in (m.get("content","").lower())
                          for kw in ["谨慎", "保守", "安全", "稳定", "careful", "safe", "stable", "conservative"]))
        total = risk_seeking + risk_averse
        if total == 0:
            return 0.5
        return risk_seeking / total
    
    def _calculate_complexity_preference(self) -> float:
        """计算复杂度偏好"""
        try:
            rows = self.store.execute_sql(
                "SELECT AVG(LENGTH(content)) as avg_length FROM memories",
                fetch=True,
            )
            avg_length = rows[0]['avg_length'] if rows else 0
            return min(1.0, avg_length / 500)
        except Exception as e:
            logger.debug("Complexity preference calculation failed: %s", e)
            return 0.5

    def _extract_performance_vs_usability(self) -> Dict[str, Any]:
        """提取性能优先 vs 易用优先模式"""
        # 基于记忆内容关键词
        performance_keywords = ['性能', '速度', '效率', '优化', 'benchmark']
        usability_keywords = ['易用', '简单', '直观', '用户', '界面']
        
        performance_count = self._count_keywords(performance_keywords)
        usability_count = self._count_keywords(usability_keywords)
        
        total = performance_count + usability_count
        if total == 0:
            return None
        
        pattern_type = 'performance' if performance_count > usability_count else 'usability'
        confidence = abs(performance_count - usability_count) / total
        
        return {
            "pattern_id": f"perf_vs_usability_{int(datetime.now().timestamp())}",
            "pattern_type": pattern_type,
            "context": "技术选型",
            "frequency": total,
            "confidence": round(confidence, 2),
            "examples": self._get_keyword_examples(performance_keywords + usability_keywords, limit=3)
        }
    
    def _extract_collective_vs_individual(self) -> Dict[str, Any]:
        """提取集体决策 vs 个人决策模式"""
        # 基于记忆内容关键词
        collective_keywords = ['团队', '大家', '集体', '讨论', '会议']
        individual_keywords = ['我', '个人', '自己', '决定', '选择']
        
        collective_count = self._count_keywords(collective_keywords)
        individual_count = self._count_keywords(individual_keywords)
        
        total = collective_count + individual_count
        if total == 0:
            return None
        
        pattern_type = 'collective' if collective_count > individual_count else 'individual'
        confidence = abs(collective_count - individual_count) / total
        
        return {
            "pattern_id": f"collective_vs_individual_{int(datetime.now().timestamp())}",
            "pattern_type": pattern_type,
            "context": "决策过程",
            "frequency": total,
            "confidence": round(confidence, 2),
            "examples": self._get_keyword_examples(collective_keywords + individual_keywords, limit=3)
        }
    
    def _get_recent_emotions(self, limit: int = 1000) -> List[Dict[str, Any]]:
        """获取最近的情感数据"""
        try:
            return self.store.execute_sql('''
                SELECT valence, arousal, dominance, significance, confidence,
                       primary_emotions, compound_emotions
                FROM memories
                WHERE valence IS NOT NULL
                ORDER BY time_ts DESC
                LIMIT ?
            ''', (limit,), fetch=True)
        except Exception as e:
            logger.debug("Recent emotions query failed: %s", e)
            return []

    def _get_topic_distribution(self) -> Dict[str, int]:
        """获取主题分布"""
        try:
            rows = self.store.execute_sql('''
                SELECT topic_code, COUNT(*) as count
                FROM memory_topics
                GROUP BY topic_code
            ''', fetch=True)
            return {row['topic_code']: row['count'] for row in rows}
        except Exception as e:
            logger.debug("digital_twin: %s", e)
            return {}

    def _count_keywords(self, keywords: List[str]) -> int:
        """统计关键词出现次数"""
        try:
            if not keywords:
                return 0
            conditions = " OR ".join(["content LIKE ?" for _ in keywords])
            params = [f"%{kw}%" for kw in keywords]
            rows = self.store.execute_sql(
                f"SELECT COUNT(*) as count FROM memories WHERE {conditions}",
                params,
                fetch=True,
            )
            return rows[0]["count"] if rows else 0
        except Exception as e:
            logger.debug("digital_twin: _count_keywords: %s", e)
            return 0

    def _get_keyword_examples(self, keywords: List[str], limit: int = 3) -> List[str]:
        """获取关键词示例"""
        try:
            rows = self.store.execute_sql('''
                SELECT content
                FROM memories
                WHERE content LIKE '%' || ? || '%'
                LIMIT ?
            ''', (keywords[0], limit), fetch=True)
            return [row['content'][:100] + '...' for row in rows]
        except Exception as e:
            logger.debug("Keyword examples query failed: %s", e)
            return []

    def _persist_decision_pattern(self, pattern: Dict[str, Any]):
        """持久化决策模式"""
        try:
            self.store.execute_sql('''
                INSERT OR REPLACE INTO decision_pattern
                (pattern_id, pattern_type, context, frequency, confidence, examples, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                pattern['pattern_id'],
                pattern['pattern_type'],
                pattern['context'],
                pattern['frequency'],
                pattern['confidence'],
                json.dumps(pattern['examples']),
                int(datetime.now().timestamp())
            ))
        except Exception as e:
            logger.warning("digital_twin: %s", e)

    def _persist_profile(self, profile: Dict[str, Any]):
        """持久化人格画像"""
        try:
            profile_id = hashlib.md5(str(profile).encode()).hexdigest()
            self.store.execute_sql('''
                INSERT OR REPLACE INTO persona_profile
                (profile_id, version, cognitive_summary, decision_summary,
                 emotion_summary, knowledge_summary, values_summary,
                 overall_confidence, generated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                profile_id,
                1,
                json.dumps(profile['cognitive_style']),
                json.dumps(profile['decision_patterns']),
                json.dumps(profile['emotion_patterns']),
                json.dumps(profile['knowledge_boundaries']),
                json.dumps(profile['values']),
                0.7,
                int(datetime.now().timestamp())
            ))
        except Exception as e:
            logger.warning("digital_twin: %s", e)
    
    def get_latest_profile(self) -> Optional[Dict[str, Any]]:
        """获取最新的人格画像"""
        try:
            rows = self.store.execute_sql('''
                SELECT * FROM persona_profile
                ORDER BY generated_at DESC
                LIMIT 1
            ''', fetch=True)
            if rows:
                row = rows[0]
                return {
                    "profile_id": row['profile_id'],
                    "cognitive_style": json.loads(row['cognitive_summary']),
                    "decision_patterns": json.loads(row['decision_summary']),
                    "emotion_patterns": json.loads(row['emotion_summary']),
                    "knowledge_boundaries": json.loads(row['knowledge_summary']),
                    "values": json.loads(row['values_summary']),
                    "overall_confidence": row['overall_confidence'],
                    "generated_at": row['generated_at']
                }
        except Exception as e:
            logger.warning("digital_twin: %s", e)
        return None
    
    def apply_role_style(self, role: RoleTemplate, weight: float = 0.4) -> Dict[str, Any]:
        """应用角色风格
        
        Args:
            role: 角色模板
            weight: 角色风格权重
        
        Returns:
            混合后的人格画像
        """
        # 获取核心人格
        core_profile = self.get_latest_profile()
        if not core_profile:
            core_profile = self.build_unified_profile()
        
        # 混合认知风格
        core_cognitive = core_profile.get("cognitive_style", {})
        role_cognitive = role.personality_traits
        merged_cognitive = merge_styles(core_cognitive, role_cognitive, weight)
        
        # 构建混合画像
        hybrid_profile = {
            "profile_id": f"hybrid_{hashlib.md5(str(role.name).encode()).hexdigest()}",
            "cognitive_style": merged_cognitive,
            "decision_patterns": core_profile.get("decision_patterns", []),
            "emotion_patterns": core_profile.get("emotion_patterns", {}),
            "knowledge_boundaries": core_profile.get("knowledge_boundaries", {}),
            "values": core_profile.get("values", {}),
            "role_info": {
                "name": role.name,
                "speaking_style": role.speaking_style,
                "emotional_tone": role.emotional_tone,
                "topic_preferences": role.topic_preferences
            },
            "overall_confidence": core_profile.get("overall_confidence", 0.7),
            "generated_at": int(datetime.now().timestamp())
        }
        
        return hybrid_profile
    
    def remember_with_role(self, content: str, role: RoleTemplate, importance: str = "medium") -> dict:
        """Write memory with role context — actually persists to the store.

        Args:
            content: 记忆内容
            role: 角色模板
            importance: 重要度

        Returns:
            记忆结果
        """
        role_prefix = f"[{role.name}] "
        full_content = role_prefix + content

        try:
            if self.store and hasattr(self.store, 'insert_memory'):
                result = self.store.insert_memory(full_content, importance=importance)
                return {
                    "written": True,
                    "memory_id": result if isinstance(result, str) else result.get("memory_id"),
                    "role": role.name,
                    "content": content,
                    "importance": importance,
                }
            elif self.store and hasattr(self.store, 'store'):
                result = self.store.store(
                    content=full_content,
                    importance=importance,
                    source=f"role:{role.name}",
                )
                return {
                    "written": True,
                    "memory_id": result if isinstance(result, str) else None,
                    "role": role.name,
                    "content": content,
                    "importance": importance,
                }
            else:
                return {"written": False, "reason": "no store available"}
        except Exception as e:
            logger.warning("digital_twin: remember_with_role failed: %s", e)
            return {"written": False, "reason": str(e)}
    
    def get_role_memories(self, role_name: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get memories associated with a role — actually queries the store.

        Args:
            role_name: 角色名称
            limit: 返回条数

        Returns:
            记忆列表
        """
        if not self.store:
            return []
        prefix = f"[{role_name}]"
        try:
            if hasattr(self.store, 'query'):
                results = self.store.query(limit=limit * 2)
                return [m for m in results if (m.get("content") or "").startswith(prefix)][:limit]
            elif hasattr(self.store, 'execute_sql'):
                rows = self.store.execute_sql(
                    "SELECT * FROM memories WHERE content LIKE ? ORDER BY time_ts DESC LIMIT ?",
                    (f"{prefix}%", limit),
                    fetch=True,
                )
                return rows
        except Exception as e:
            logger.warning("digital_twin: get_role_memories failed: %s", e)
        return []

    # ══════════════════════════════════════════════════════
    # v8.3: 用户画像与模拟
    # ══════════════════════════════════════════════════════

    def build_user_profile(self, person_id: str = None) -> dict:
        """
        构建用户画像。

        基于记忆数据提取用户的行为特征、偏好、沟通风格等。

        参数:
            person_id: 人物 ID（None=全部）

        返回: {
            "communication_style": dict,
            "topic_interests": dict,
            "activity_pattern": dict,
            "emotional_profile": dict,
            "interaction_preferences": dict,
        }
        """
        try:
            if person_id:
                rows = self.store.execute_sql(
                    "SELECT * FROM memories WHERE person_id = ? ORDER BY time_ts DESC LIMIT 500",
                    (person_id,),
                    fetch=True,
                )
            else:
                rows = self.store.execute_sql(
                    "SELECT * FROM memories ORDER BY time_ts DESC LIMIT 500",
                    fetch=True,
                )
        except Exception as e:
            logger.debug("build_user_profile query failed: %s", e)
            return {}

        if not rows:
            return {}

        memories = rows

        comm_style = self._analyze_communication_style(memories)
        topic_interests = self._analyze_topic_interests(memories)
        activity_pattern = self._analyze_activity_pattern(memories)
        emotional_profile = self._analyze_emotional_profile(memories)
        interaction_prefs = self._analyze_interaction_preferences(memories)

        return {
            "communication_style": comm_style,
            "topic_interests": topic_interests,
            "activity_pattern": activity_pattern,
            "emotional_profile": emotional_profile,
            "interaction_preferences": interaction_prefs,
            "sample_size": len(memories),
        }

    def _analyze_communication_style(self, memories: list) -> dict:
        """分析沟通风格"""
        avg_length = sum(len(m.get("content", "")) for m in memories) / max(1, len(memories))

        question_count = sum(1 for m in memories if "?" in m.get("content", "") or "？" in m.get("content", ""))
        imperative_count = sum(1 for m in memories if any(
            w in m.get("content", "")
            for w in ["请", "帮我", "做", "写", "创建", "实现", "配置"]
        ))

        style = "balanced"
        if avg_length > 200:
            style = "detailed"
        elif avg_length < 50:
            style = "concise"

        mode = "mixed"
        if question_count > len(memories) * 0.4:
            mode = "inquiring"
        elif imperative_count > len(memories) * 0.4:
            mode = "directive"

        return {
            "avg_message_length": round(avg_length, 1),
            "style": style,
            "mode": mode,
            "question_ratio": round(question_count / max(1, len(memories)), 2),
        }

    def _analyze_topic_interests(self, memories: list) -> dict:
        """分析主题兴趣"""
        topic_counts = {}
        for m in memories:
            for t in m.get("topics", []):
                code = t.get("code", t) if isinstance(t, dict) else t
                if code:
                    topic_counts[code] = topic_counts.get(code, 0) + 1

        sorted_topics = sorted(topic_counts.items(), key=lambda x: -x[1])
        return {
            "top_topics": sorted_topics[:10],
            "total_topics": len(topic_counts),
            "focus_ratio": round(sorted_topics[0][1] / max(1, len(memories)), 2) if sorted_topics else 0,
        }

    def _analyze_activity_pattern(self, memories: list) -> dict:
        """分析活动模式"""
        hour_counts = {}
        dow_counts = {}
        for m in memories:
            ts = m.get("time_ts", 0)
            if ts:
                dt = datetime.fromtimestamp(ts)
                hour = dt.hour
                dow = dt.weekday()
                hour_counts[hour] = hour_counts.get(hour, 0) + 1
                dow_counts[dow] = dow_counts.get(dow, 0) + 1

        peak_hour = max(hour_counts, key=hour_counts.get) if hour_counts else 12
        peak_dow = max(dow_counts, key=dow_counts.get) if dow_counts else 0
        dow_names = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]

        return {
            "peak_hour": peak_hour,
            "peak_day": dow_names[peak_dow] if peak_dow < len(dow_names) else "未知",
            "hour_distribution": dict(sorted(hour_counts.items())[:24]),
        }

    def _analyze_emotional_profile(self, memories: list) -> dict:
        """分析情感画像"""
        valences = [m.get("valence", 0) for m in memories if m.get("valence") is not None]
        if not valences:
            return {"average_valence": 0, "stability": 0.5}

        avg_valence = sum(valences) / len(valences)
        variance = sum((v - avg_valence) ** 2 for v in valences) / len(valences)
        stability = max(0, 1.0 - variance ** 0.5)

        return {
            "average_valence": round(avg_valence, 3),
            "stability": round(stability, 3),
            "tendency": "positive" if avg_valence > 0.1 else ("negative" if avg_valence < -0.1 else "neutral"),
        }

    def _analyze_interaction_preferences(self, memories: list) -> dict:
        """分析交互偏好"""
        nature_counts = {}
        for m in memories:
            nat = m.get("nature_id", "unknown")
            nature_counts[nat] = nature_counts.get(nat, 0) + 1

        importance_counts = {}
        for m in memories:
            imp = m.get("importance", "medium")
            importance_counts[imp] = importance_counts.get(imp, 0) + 1

        return {
            "nature_distribution": nature_counts,
            "importance_distribution": importance_counts,
        }

    def simulate_response(
        self,
        input_text: str,
        person_id: str = None,
        use_llm: bool = True,
    ) -> dict:
        """
        基于用户画像模拟可能的响应。

        参数:
            input_text: 输入文本
            person_id: 人物 ID
            use_llm: 是否使用 LLM

        返回: {
            "predicted_topics": [str],
            "predicted_emotion": dict,
            "predicted_importance": str,
            "simulated_response": str,
        }
        """
        profile = self.build_user_profile(person_id)

        predicted_topics = []
        topic_interests = profile.get("topic_interests", {})
        for topic, count in topic_interests.get("top_topics", [])[:3]:
            predicted_topics.append(topic)

        emotional = profile.get("emotional_profile", {})
        predicted_emotion = {
            "tendency": emotional.get("tendency", "neutral"),
            "stability": emotional.get("stability", 0.5),
        }

        comm = profile.get("communication_style", {})
        if comm.get("mode") == "inquiring":
            predicted_importance = "medium"
        elif comm.get("mode") == "directive":
            predicted_importance = "high"
        else:
            predicted_importance = "medium"

        simulated = ""
        if use_llm and hasattr(self, '_llm_fn') and self._llm_fn:
            simulated = self._simulate_with_llm(input_text, profile)
        else:
            simulated = self._simulate_rule_based(input_text, profile)

        return {
            "predicted_topics": predicted_topics,
            "predicted_emotion": predicted_emotion,
            "predicted_importance": predicted_importance,
            "simulated_response": simulated,
        }

    def _simulate_rule_based(self, input_text: str, profile: dict) -> str:
        """基于规则模拟响应（启发式推测，非精确预测）"""
        comm = profile.get("communication_style", {})
        style = comm.get("style", "balanced")
        mode = comm.get("mode", "mixed")

        if mode == "inquiring":
            return f"[启发式推测] 基于已有行为模式，用户可能追问细节，偏好{style}式回答"
        elif mode == "directive":
            return f"[启发式推测] 基于已有行为模式，用户可能给出明确指令，偏好{style}式执行"
        else:
            return f"[启发式推测] 基于已有行为模式，用户可能以{style}方式回应"

    def _simulate_with_llm(self, input_text: str, profile: dict) -> str:
        """用 LLM 模拟响应"""
        if not hasattr(self, '_llm_fn') or not self._llm_fn:
            return self._simulate_rule_based(input_text, profile)

        prompt = f"""基于以下用户画像，模拟用户对输入的可能反应。

用户画像: {json.dumps(profile, ensure_ascii=False, indent=2)[:500]}
输入: {input_text[:200]}

请用1-2句话描述用户可能的反应。"""

        try:
            return self._llm_fn(prompt)[:300]
        except Exception as e:
            logger.debug("LLM simulation failed: %s", e)
            return self._simulate_rule_based(input_text, profile)
