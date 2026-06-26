from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Optional, Callable

from ..self_model import SelfModel, ReasoningTrace
from ..metacognition import MetacognitiveEngine, MetaEvaluation
from ..motivation import MotivationEngine, InternalState
from ..narrative import NarrativeBuilder
from ..digital_twin import DigitalTwinProfiler

try:
    from ..personality_analyzer import PersonalityAnalyzer, PersonalityProfile, TraitScore
except ImportError:
    PersonalityAnalyzer = None
    PersonalityProfile = None
    TraitScore = None

from .cognitive_profile import CognitiveProfile

try:
    from ..personality_memory import PersonalityMemory
except ImportError:
    PersonalityMemory = None

try:
    from ..style_analyzer import StyleAnalyzer
except ImportError:
    StyleAnalyzer = None

try:
    from ..emotion_tracker import EmotionTracker, EmotionalState
except ImportError:
    EmotionTracker = None
    EmotionalState = None

try:
    from ..memory_decision import MemoryDecisionEngine, EvidenceItem
except ImportError:
    MemoryDecisionEngine = None
    EvidenceItem = None

logger = logging.getLogger(__name__)


@dataclass
class SelfProfile:
    personality: Optional[object] = None
    style: dict = field(default_factory=dict)
    emotion_pattern: dict = field(default_factory=dict)
    cognitive_style: Optional[CognitiveProfile] = None
    narrative: str = ""
    values: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        p = self.personality
        personality_dict = None
        if p is not None and TraitScore is not None:
            personality_dict = {
                "openness": {"score": p.openness.score, "confidence": p.openness.confidence},
                "conscientiousness": {"score": p.conscientiousness.score, "confidence": p.conscientiousness.confidence},
                "extraversion": {"score": p.extraversion.score, "confidence": p.extraversion.confidence},
                "agreeableness": {"score": p.agreeableness.score, "confidence": p.agreeableness.confidence},
                "neuroticism": {"score": p.neuroticism.score, "confidence": p.neuroticism.confidence},
                "cognitive_style": p.cognitive_style,
                "reasoning_style": p.reasoning_style,
                "decision_style": p.decision_style,
                "humor_style": p.humor_style,
                "attachment_style": p.attachment_style,
                "analysis_confidence": p.analysis_confidence,
            }
        elif p is not None:
            personality_dict = {"raw": str(p)}

        cs = self.cognitive_style
        cognitive_dict = None
        if cs is not None:
            cognitive_dict = {
                "reflective_depth": cs.reflective_depth,
                "intuition_bias": cs.intuition_bias,
                "risk_tolerance": cs.risk_tolerance,
                "complexity_preference": cs.complexity_preference,
                "cognitive_style": cs.cognitive_style,
                "reasoning_style": cs.reasoning_style,
                "decision_style": cs.decision_style,
                "risk_profile": cs.risk_profile,
                "update_source": cs.update_source,
            }

        return {
            "personality": personality_dict,
            "style": self.style,
            "emotion_pattern": self.emotion_pattern,
            "cognitive_style": cognitive_dict,
            "narrative": self.narrative,
            "values": self.values,
        }


class CognitionEngine:
    """
    READ-ONLY cognitive core.

    Consolidates all "self-awareness" modules into a unified interface
    that the Spirit (butler) accesses. Never writes to the memory store
    directly — only reads and analyzes.
    """

    def __init__(
        self,
        store=None,
        recall_engine=None,
        self_model: Optional[SelfModel] = None,
        metacognition: Optional[MetacognitiveEngine] = None,
        motivation: Optional[MotivationEngine] = None,
        narrative: Optional[NarrativeBuilder] = None,
        digital_twin: Optional[DigitalTwinProfiler] = None,
        personality_analyzer=None,
        personality_memory=None,
        style_analyzer=None,
        emotion_tracker=None,
        memory_decision=None,
        llm_fn: Optional[Callable] = None,
        embedding_store=None,
    ):
        self.store = store
        self.recall_engine = recall_engine
        self.llm_fn = llm_fn
        self.embedding_store = embedding_store

        self.self_model = self_model or (SelfModel(store) if store else None)
        self.metacognition = metacognition
        self.motivation = motivation
        self.narrative = narrative
        self.digital_twin = digital_twin
        self.personality_analyzer = personality_analyzer or (PersonalityAnalyzer() if PersonalityAnalyzer is not None else None)
        self.personality_memory = personality_memory
        self.style_analyzer = style_analyzer or (StyleAnalyzer() if StyleAnalyzer is not None else None)
        self.emotion_tracker = emotion_tracker or (EmotionTracker() if EmotionTracker is not None else None)
        self.memory_decision = memory_decision

    def build_self_profile(self) -> SelfProfile:
        """
        Build a comprehensive self-profile from all cognition modules.

        Aggregates personality, style, emotion trajectory, cognitive style,
        narrative summary, and value system into a single SelfProfile.

        Requires AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED=true for deep analysis.
        """
        # Security: require consent for personality aggregation
        import os as _os
        if _os.environ.get("AGENT_MEMORY_PERSONALITY_ANALYSIS_ENABLED", "").lower() not in ("1", "true", "yes"):
            return SelfProfile()

        profile = SelfProfile()

        profile.personality = self._collect_personality()

        profile.style = self._collect_style()

        profile.emotion_pattern = self._collect_emotion_pattern()

        profile.cognitive_style = self._collect_cognitive_style()

        profile.narrative = self._collect_narrative()

        profile.values = self._collect_values()

        return profile

    def reflect_on_recall(self, query: str, results: list[dict]) -> dict:
        """
        Metacognitive reflection after a recall operation.

        Evaluates result quality, generates reflection insights,
        and identifies gaps — without writing anything back.
        """
        if self.metacognition is None:
            return {"evaluation": {}, "reflection": None, "gaps": []}

        evaluation = self.metacognition.evaluate_result(query, results)

        reflection = None
        if evaluation.needs_reflection:
            reflection = self.metacognition.generate_reflection(query, evaluation, results)

        return {
            "evaluation": evaluation.to_dict(),
            "reflection": reflection,
            "gaps": evaluation.gap_analysis,
            "confidence": evaluation.overall_confidence,
        }

    def should_explore(self, topic: str) -> dict:
        """
        Curiosity-driven exploration decision.

        Combines motivation state, knowledge gaps, and metacognitive
        assessment to decide whether a topic is worth exploring.
        """
        result = {
            "topic": topic,
            "should_explore": False,
            "reason": "",
            "priority": 0.0,
            "curiosity_level": 0.0,
            "gap_detected": False,
        }

        if self.motivation is not None:
            state = self.motivation.state
            result["curiosity_level"] = state.curiosity

            if state.curiosity > 0.6:
                result["should_explore"] = True
                result["reason"] = f"好奇心较高（{state.curiosity:.2f}）"
                result["priority"] = min(1.0, state.curiosity)

            if state.boredom > 0.5:
                result["should_explore"] = True
                result["reason"] = (result["reason"] + "；无聊度较高" if result["reason"]
                                    else f"无聊度较高（{state.boredom:.2f}）")
                result["priority"] = min(1.0, result["priority"] + 0.2)

            if state.momentum < 0.3:
                result["should_explore"] = True
                result["reason"] = (result["reason"] + "；学习动量低，需换方向" if result["reason"]
                                    else "学习动量低，建议换方向探索")
                result["priority"] = min(1.0, result["priority"] + 0.1)

        if self.metacognition is not None:
            gaps = self.metacognition.detect_knowledge_gaps()
            matching = [g for g in gaps if topic in g.get("topic", "")]
            if matching:
                result["gap_detected"] = True
                result["should_explore"] = True
                gap = matching[0]
                result["reason"] = (result["reason"] + f"；知识盲区（{gap['gap_type']}）" if result["reason"]
                                    else f"知识盲区: {gap['gap_type']}")
                result["priority"] = min(1.0, result["priority"] + gap.get("priority", 0.3))

        if not result["reason"]:
            result["reason"] = "当前状态无需特别探索该主题"

        return result

    def analyze_personality(self, sessions: list, self_name: str = ""):
        if self.personality_analyzer is None or PersonalityProfile is None:
            return None
        profile = self.personality_analyzer.analyze(sessions, self_name)
        return profile

    def get_emotion_pattern(self) -> dict:
        """
        Emotion trajectory summary.

        Returns current state, trend, stability, volatility,
        and dominant emotion distribution.
        """
        if self.emotion_tracker is None:
            return {"status": "no_tracker"}

        trajectory = self.emotion_tracker.get_trajectory()
        summary = trajectory.summary()

        transitions = trajectory.detect_transitions()

        return {
            **summary,
            "recent_transitions": transitions[:5],
        }

    def get_decision_analysis(self, agent_id: str = "main",
                              query: str = "", top_k: int = 20) -> dict:
        """
        Decision pattern analysis based on historical memories.

        Returns coordinate analysis, lifecycle summary, emotional context,
        and a synthesized recommendation.
        """
        if self.memory_decision is None:
            return {"status": "no_decision_engine"}

        advice = self.memory_decision.analyze_pattern(
            agent_id=agent_id, query=query, top_k=top_k,
        )

        return {
            "recommendation": advice.recommendation,
            "confidence": advice.confidence,
            "evidence": advice.evidence,
            "alternatives": advice.alternatives,
            "risk_factors": advice.risk_factors,
            "coordinate_analysis": advice.coordinate_analysis,
            "lifecycle_summary": advice.lifecycle_summary,
            "emotional_context": advice.emotional_context,
        }

    def _collect_personality(self) -> Optional[object]:
        """Collect personality profile with degradation strategy."""
        if self.personality_memory is not None:
            try:
                profile = self.personality_memory.load_profile()
                if profile:
                    return self._dict_to_personality_profile(profile)
            except Exception as e:
                logger.debug("_collect_personality load_profile: %s", e)

        if PersonalityAnalyzer is not None:
            try:
                recent = self._get_recent_content(50)
                if recent:
                    from chat_parser import ChatParser
                    parser = ChatParser()
                    result = parser.parse("\n".join(recent), source_type="wechat_txt")
                    if result.sessions:
                        analyzer = PersonalityAnalyzer()
                        return analyzer.analyze(result.sessions)
            except Exception as e:
                logger.debug("_collect_personality PersonalityAnalyzer: %s", e)

        return self._infer_basic_personality()

    def _infer_basic_personality(self) -> Optional[object]:
        """Infer basic personality traits from linguistic patterns when no analyzer available."""
        recent = self._get_recent_content(30)
        if not recent:
            return None

        all_text = " ".join(recent)

        traits = {}

        unique_chars = len(set(all_text))
        total_chars = max(len(all_text), 1)
        traits["openness"] = min(1.0, (unique_chars / total_chars) * 5)

        list_markers = sum(1 for t in recent if any(m in t for m in ["1.", "2.", "首先", "其次", "第一", "第二", "步骤"]))
        traits["conscientiousness"] = min(1.0, list_markers / max(len(recent), 1) * 3)

        social_words = sum(1 for t in recent if any(w in t for w in ["我们", "一起", "大家", "分享", "讨论", "！"]))
        traits["extraversion"] = min(1.0, social_words / max(len(recent), 1) * 2)

        agree_words = sum(1 for t in recent if any(w in t for w in ["好的", "同意", "理解", "谢谢", "抱歉", "对"]))
        traits["agreeableness"] = min(1.0, agree_words / max(len(recent), 1) * 2)

        worry_words = sum(1 for t in recent if any(w in t for w in ["担心", "焦虑", "不确定", "可能", "也许", "但是"]))
        traits["neuroticism"] = min(1.0, worry_words / max(len(recent), 1) * 2)

        if TraitScore is not None:
            profile = type('BasicPersonalityProfile', (), {
                "openness": TraitScore("openness", traits["openness"], 0.3, 0, []),
                "conscientiousness": TraitScore("conscientiousness", traits["conscientiousness"], 0.3, 0, []),
                "extraversion": TraitScore("extraversion", traits["extraversion"], 0.3, 0, []),
                "agreeableness": TraitScore("agreeableness", traits["agreeableness"], 0.3, 0, []),
                "neuroticism": TraitScore("neuroticism", traits["neuroticism"], 0.3, 0, []),
            })()
        else:
            profile = type('BasicPersonalityProfile', (), traits)()

        return profile

    def _collect_style(self) -> dict:
        """Collect communication style with degradation strategy."""
        if self.style_analyzer is not None:
            try:
                recent = self._get_recent_content(50)
                if recent:
                    combined = "\n".join(recent)
                    result = self.style_analyzer.analyze(combined)
                    if result:
                        return result
            except Exception as e:
                logger.debug("_collect_style style_analyzer: %s", e)

        return self._infer_basic_style()

    def _infer_basic_style(self) -> dict:
        """Infer basic communication style from linguistic patterns."""
        recent = self._get_recent_content(30)
        if not recent:
            return {"style": "unknown", "confidence": 0.0}

        all_text = " ".join(recent)

        avg_len = sum(len(t) for t in recent) / max(len(recent), 1)
        verbosity = "concise" if avg_len < 20 else "moderate" if avg_len < 50 else "verbose"

        formal_markers = sum(1 for t in recent if any(w in t for w in ["因此", "然而", "此外", "综上", "鉴于"]))
        casual_markers = sum(1 for t in recent if any(w in t for w in ["哈哈", "嗯嗯", "哦", "啊", "呢", "嘛"]))
        formality = "formal" if formal_markers > casual_markers else "casual" if casual_markers > formal_markers * 2 else "mixed"

        questions = sum(1 for t in recent if "？" in t or "?" in t)
        imperatives = sum(1 for t in recent if any(w in t for w in ["请", "必须", "需要", "应该", "得"]))
        directness = "indirect" if questions > imperatives * 2 else "direct" if imperatives > questions else "balanced"

        return {
            "verbosity": verbosity,
            "formality": formality,
            "directness": directness,
            "avg_message_length": round(avg_len, 1),
            "confidence": 0.4,
            "source": "linguistic_heuristic",
        }

    def _collect_emotion_pattern(self) -> dict:
        """Collect emotion pattern with degradation strategy."""
        if self.digital_twin is not None:
            try:
                profile = self.digital_twin.build_unified_profile()
                if profile and "emotion" in profile:
                    return profile["emotion"]
            except Exception as e:
                logger.debug("_collect_emotion_pattern digital_twin: %s", e)

        if self.emotion_tracker is not None:
            try:
                recent = self._get_recent_content(30)
                if recent:
                    emotions = []
                    for text in recent:
                        result = self.emotion_tracker.analyze(text)
                        if result:
                            emotions.append(result)
                    if emotions:
                        return {"recent_emotions": emotions, "source": "emotion_tracker"}
            except Exception as e:
                logger.debug("_collect_emotion_pattern emotion_tracker: %s", e)

        return self._infer_basic_emotion()

    def _infer_basic_emotion(self) -> dict:
        """Infer basic emotion pattern from content when no emotion module available."""
        recent = self._get_recent_content(20)
        if not recent:
            return {"valence": 0.0, "source": "none"}

        positive_words = {"开心", "高兴", "好", "棒", "优秀", "成功", "喜欢", "爱", "感谢", "赞", "happy", "good", "great", "love", "thanks"}
        negative_words = {"难过", "伤心", "差", "糟", "失败", "讨厌", "恨", "烦", "焦虑", "担心", "sad", "bad", "hate", "angry", "worry"}

        pos_count = sum(1 for t in recent if any(w in t for w in positive_words))
        neg_count = sum(1 for t in recent if any(w in t for w in negative_words))
        total = max(pos_count + neg_count, 1)

        valence = (pos_count - neg_count) / total

        return {
            "valence": round(valence, 2),
            "positive_ratio": round(pos_count / max(len(recent), 1), 2),
            "negative_ratio": round(neg_count / max(len(recent), 1), 2),
            "source": "linguistic_heuristic",
            "confidence": 0.3,
        }

    def _get_recent_content(self, limit: int = 30) -> list[str]:
        """Get recent memory contents."""
        try:
            rows = self.store.conn.execute(
                "SELECT content FROM memories ORDER BY created_at DESC LIMIT ?",
                (limit,)
            ).fetchall()
            return [r[0] for r in rows if r[0]]
        except Exception as e:
            logger.debug("_get_recent_content: %s", e)
            return []

    def _collect_cognitive_style(self) -> Optional[CognitiveProfile]:
        dt_profile = None
        pa_profile = None

        if self.digital_twin is not None:
            try:
                cs_dict = self.digital_twin.extract_cognitive_style()
                dt_profile = CognitiveProfile.from_digital_twin(cs_dict)
            except Exception as e:
                logger.debug("cognition: cognitive style from digital_twin failed: %s", e)

        if self.personality_memory is not None:
            try:
                loaded = self.personality_memory.load_profile()
                if loaded:
                    cog = loaded.get("cognitive_style", "")
                    reas = loaded.get("reasoning_style", "")
                    if cog or reas:
                        pa_profile = CognitiveProfile.from_personality(cog, reas)
            except Exception as e:
                logger.debug("cognition: cognitive style from personality_memory failed: %s", e)

        if dt_profile and pa_profile:
            return dt_profile.merge(pa_profile, weight=0.3)
        if dt_profile:
            return dt_profile
        if pa_profile:
            return pa_profile
        return None

    def _collect_narrative(self) -> str:
        if self.narrative is not None:
            try:
                concept = self.narrative.update_self_concept()
                return concept.get("narrative_summary", "")
            except Exception as e:
                logger.debug("cognition: narrative collection failed: %s", e)
        return ""

    def _collect_values(self) -> dict:
        if self.narrative is not None:
            try:
                worldview = self.narrative.get_worldview()
                return {
                    "beliefs": worldview.get("beliefs", []),
                    "values": worldview.get("values", []),
                    "principles": worldview.get("principles", []),
                }
            except Exception as e:
                logger.debug("cognition: values collection failed: %s", e)
        return {}

    @staticmethod
    def _dict_to_personality_profile(data: dict):
        if PersonalityProfile is None or TraitScore is None:
            return data
        profile = PersonalityProfile()

        big_five = data.get("big_five", {})
        if isinstance(big_five, str):
            import json
            try:
                big_five = json.loads(big_five)
            except (ValueError, TypeError):
                big_five = {}

        for attr in ("openness", "conscientiousness", "extraversion",
                      "agreeableness", "neuroticism"):
            info = big_five.get(attr, {})
            if isinstance(info, dict):
                setattr(profile, attr, TraitScore(
                    name=attr,
                    score=info.get("score", 0.5),
                    confidence=info.get("confidence", 0.0),
                    evidence_count=info.get("evidence_count", 0),
                ))

        profile.cognitive_style = data.get("cognitive_style", "")
        profile.reasoning_style = data.get("reasoning_style", "")
        profile.attachment_style = data.get("attachment_style", "")
        profile.social_dominance = TraitScore(
            name="social_dominance",
            score=data.get("social_dominance", 0.5),
            confidence=0.0,
        )
        profile.intimacy_capacity = TraitScore(
            name="intimacy_capacity",
            score=data.get("intimacy_capacity", 0.5),
            confidence=0.0,
        )
        profile.social_energy_pattern = data.get("social_energy_pattern", "")
        profile.circadian_preference = data.get("circadian_preference", "")
        profile.decision_style = data.get("decision_style", "")
        profile.humor_style = data.get("humor_style", "")
        profile.narcissism_index = TraitScore(
            name="narcissism",
            score=data.get("narcissism_score", 0.3),
            confidence=0.0,
        )
        profile.control_tendency = TraitScore(
            name="control",
            score=data.get("control_score", 0.3),
            confidence=0.0,
        )
        profile.anxiety_level = TraitScore(
            name="anxiety",
            score=data.get("anxiety_score", 0.3),
            confidence=0.0,
        )
        profile.empathy_capacity = TraitScore(
            name="empathy",
            score=data.get("empathy_score", 0.5),
            confidence=0.0,
        )
        profile.total_messages_analyzed = data.get("total_messages_analyzed", 0)
        profile.analysis_confidence = data.get("analysis_confidence", 0.0)

        return profile
