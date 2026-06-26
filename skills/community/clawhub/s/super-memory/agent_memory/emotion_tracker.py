from __future__ import annotations
"""
emotion_tracker.py - Emotional Trajectory Tracker

Tracks emotional evolution across conversations and time.
Provides:
  - Emotional trajectory (time series of valence/arousal/dominance)
  - Emotional state transitions (shift detection)
  - Emotional stability metrics
  - Dominant emotion trends
  - Empathic response suggestions based on emotional state
"""

import time
import math
import logging
from typing import Dict, List, Optional, Tuple
from .emotion import PLUTCHIK_PRIMARY, EmotionAnalyzer

logger = logging.getLogger(__name__)


class EmotionalState:
    """Snapshot of emotional state at a point in time."""

    __slots__ = (
        "timestamp", "valence", "arousal", "dominance",
        "primary_emotions", "compound_emotions", "significance", "nuance",
    )

    def __init__(self, emotion_result: dict, timestamp: float = None):
        self.timestamp = timestamp or time.time()
        self.valence = emotion_result.get("valence", 0.0)
        self.arousal = emotion_result.get("arousal", 0.2)
        self.dominance = emotion_result.get("dominance", 0.5)
        self.primary_emotions = emotion_result.get("primary_emotions", {})
        self.compound_emotions = emotion_result.get("compound_emotions", [])
        self.significance = emotion_result.get("significance", "notable")
        self.nuance = emotion_result.get("nuance", "literal")

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "valence": self.valence,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "primary_emotions": self.primary_emotions,
            "compound_emotions": self.compound_emotions,
            "significance": self.significance,
            "nuance": self.nuance,
        }


class EmotionalTrajectory:
    """Time series of emotional states with analysis methods."""

    def __init__(self, max_states: int = 200):
        self.states: List[EmotionalState] = []
        self.max_states = max_states

    def add(self, state: EmotionalState):
        self.states.append(state)
        if len(self.states) > self.max_states:
            self.states = self.states[-self.max_states:]

    def valence_series(self) -> List[Tuple[float, float]]:
        return [(s.timestamp, s.valence) for s in self.states]

    def arousal_series(self) -> List[Tuple[float, float]]:
        return [(s.timestamp, s.arousal) for s in self.states]

    def dominant_emotion_series(self) -> List[Tuple[float, str]]:
        result = []
        for s in self.states:
            if s.primary_emotions:
                top = max(s.primary_emotions, key=s.primary_emotions.get)
                result.append((s.timestamp, top))
            else:
                result.append((s.timestamp, "neutral"))
        return result

    def valence_trend(self, window: int = 10) -> str:
        if len(self.states) < 3:
            return "stable"
        recent = self.states[-window:]
        valences = [s.valence for s in recent]
        if len(valences) < 3:
            return "stable"

        first_half = sum(valences[: len(valences) // 2]) / (len(valences) // 2)
        second_half = sum(valences[len(valences) // 2 :]) / (len(valences) - len(valences) // 2)

        diff = second_half - first_half
        if diff > 0.15:
            return "improving"
        elif diff < -0.15:
            return "declining"
        return "stable"

    def emotional_stability(self, window: int = 20) -> float:
        if len(self.states) < 3:
            return 1.0
        recent = self.states[-window:]
        valences = [s.valence for s in recent]
        mean = sum(valences) / len(valences)
        variance = sum((v - mean) ** 2 for v in valences) / len(valences)
        std_dev = math.sqrt(variance)
        return round(max(0.0, 1.0 - std_dev * 2), 3)

    def emotional_volatility(self, window: int = 20) -> float:
        if len(self.states) < 3:
            return 0.0
        recent = self.states[-window:]
        shifts = 0
        for i in range(1, len(recent)):
            if abs(recent[i].valence - recent[i - 1].valence) > 0.3:
                shifts += 1
            if abs(recent[i].arousal - recent[i - 1].arousal) > 0.3:
                shifts += 1
        return round(shifts / max(1, 2 * (len(recent) - 1)), 3)

    def detect_transitions(self, threshold: float = 0.4) -> List[dict]:
        transitions = []
        for i in range(1, len(self.states)):
            prev = self.states[i - 1]
            curr = self.states[i]

            valence_shift = curr.valence - prev.valence
            arousal_shift = curr.arousal - prev.arousal

            if abs(valence_shift) > threshold or abs(arousal_shift) > threshold:
                prev_top = max(prev.primary_emotions, key=prev.primary_emotions.get) if prev.primary_emotions else "neutral"
                curr_top = max(curr.primary_emotions, key=curr.primary_emotions.get) if curr.primary_emotions else "neutral"

                transitions.append({
                    "timestamp": curr.timestamp,
                    "from_valence": prev.valence,
                    "to_valence": curr.valence,
                    "valence_shift": round(valence_shift, 3),
                    "arousal_shift": round(arousal_shift, 3),
                    "from_emotion": prev_top,
                    "to_emotion": curr_top,
                })

        return transitions

    def dominant_emotion_distribution(self, window: int = 50) -> Dict[str, float]:
        if not self.states:
            return {}
        recent = self.states[-window:]
        counts = {}
        for s in recent:
            if s.primary_emotions:
                top = max(s.primary_emotions, key=s.primary_emotions.get)
                counts[top] = counts.get(top, 0) + 1
            else:
                counts["neutral"] = counts.get("neutral", 0) + 1

        total = sum(counts.values())
        return {k: round(v / total, 3) for k, v in sorted(counts.items(), key=lambda x: x[1], reverse=True)}

    def summary(self) -> dict:
        if not self.states:
            return {"status": "no_data"}

        latest = self.states[-1]
        return {
            "current_valence": latest.valence,
            "current_arousal": latest.arousal,
            "current_dominance": latest.dominance,
            "current_emotion": EmotionAnalyzer.emotion_label(latest.primary_emotions),
            "valence_trend": self.valence_trend(),
            "stability": self.emotional_stability(),
            "volatility": self.emotional_volatility(),
            "emotion_distribution": self.dominant_emotion_distribution(),
            "total_states": len(self.states),
        }


class EmpathicResponseEngine:
    """Generates empathic response suggestions based on emotional state.

    ⚠️ 安全: 共情响应仅作为建议，不自动执行。
    响应模板包含"行动导向"元素，防止过度共情导致被动/回避行为。
    负面情感的响应始终包含"下一步行动"建议，而非仅表达同情。
    """

    RESPONSE_TEMPLATES = {
        "sadness": {
            "high": "I can see this is really difficult. Let me help you work through this step by step.",
            "medium": "I understand this is frustrating. Let's find a way forward together.",
            "low": "I hear you. Let me see what I can do to help.",
        },
        "anger": {
            "high": "I understand your frustration. Let's focus on resolving this immediately.",
            "medium": "That's definitely annoying. Let me help you fix this.",
            "low": "I get it. Let's address this together.",
        },
        "fear": {
            "high": "This looks serious. Let me help you assess the situation and find a safe path forward.",
            "medium": "I understand your concern. Let's work through this carefully.",
            "low": "Noted. Let me help you evaluate the risks.",
        },
        "joy": {
            "high": "That's excellent! Let's build on this momentum.",
            "medium": "Great progress! What's next?",
            "low": "Good to hear. Let's keep going.",
        },
        "trust": {
            "high": "Thank you for your confidence. I'll make sure this is handled well.",
            "medium": "Appreciated. Let me continue delivering reliable results.",
            "low": "Got it. I'll keep things on track.",
        },
        "surprise": {
            "high": "That's unexpected! Let me help you understand what happened.",
            "medium": "Interesting finding. Let's investigate further.",
            "low": "Noted. Let me look into this.",
        },
        "disgust": {
            "high": "I understand this is unacceptable. Let's find a better approach.",
            "medium": "That's not ideal. Let me suggest an alternative.",
            "low": "I see the issue. Let's improve this.",
        },
        "anticipation": {
            "high": "Exciting plans ahead! Let me help you prepare thoroughly.",
            "medium": "Looking forward to this. Let's plan the next steps.",
            "low": "Understood. Let me help you get ready.",
        },
    }

    CN_RESPONSE_TEMPLATES = {
        "sadness": {
            "high": "我理解这确实很困难。让我一步步帮你解决，先从最紧急的开始。",
            "medium": "我知道这很令人沮丧。让我们一起找到解决方案，先分析问题。",
            "low": "我听到了。让我看看能怎么帮你。",
        },
        "anger": {
            "high": "我理解你的愤怒。让我们立刻着手解决这个问题，不再拖延。",
            "medium": "确实很烦人。让我帮你修复，先定位根因。",
            "low": "我理解。让我们一起处理。",
        },
        "fear": {
            "high": "这看起来很严重。让我帮你评估风险并制定应对方案，确保安全。",
            "medium": "我理解你的担忧。让我们仔细分析，找到稳妥的解决路径。",
            "low": "注意到了。让我帮你评估风险。",
        },
        "joy": {
            "high": "太好了！让我们趁势而上，继续推进。",
            "medium": "进展不错！下一步是什么？",
            "low": "不错。继续前进。",
        },
        "trust": {
            "high": "感谢你的信任。我会确保做好，让我开始执行。",
            "medium": "感谢认可。让我继续交付可靠的结果。",
            "low": "收到。我会保持进度。",
        },
        "surprise": {
            "high": "真没想到！让我帮你搞清楚发生了什么，然后制定对策。",
            "medium": "有趣的发现。让我们进一步调查。",
            "low": "注意到了。让我看看。",
        },
        "disgust": {
            "high": "我理解这不可接受。让我们立刻找个更好的方案替代。",
            "medium": "确实不理想。让我建议一个替代方案。",
            "low": "我看到问题了。让我们改进。",
        },
        "anticipation": {
            "high": "前景令人期待！让我帮你做好充分准备，确保万无一失。",
            "medium": "期待中。让我们规划下一步。",
            "low": "了解了。让我帮你准备。",
        },
    }

    @classmethod
    def suggest_response(cls, state: EmotionalState, lang: str = "cn") -> Optional[str]:
        if not state.primary_emotions:
            return None

        top_emotion = max(state.primary_emotions, key=state.primary_emotions.get)
        top_score = state.primary_emotions[top_emotion]

        if top_score < 0.1:
            return None

        if top_score >= 0.6:
            intensity = "high"
        elif top_score >= 0.3:
            intensity = "medium"
        else:
            intensity = "low"

        templates = cls.CN_RESPONSE_TEMPLATES if lang == "cn" else cls.RESPONSE_TEMPLATES
        emotion_templates = templates.get(top_emotion, {})
        return emotion_templates.get(intensity)

    @classmethod
    def suggest_response_from_result(cls, emotion_result: dict, lang: str = "cn") -> Optional[str]:
        state = EmotionalState(emotion_result)
        return cls.suggest_response(state, lang)


class EmotionTracker:
    """
    Main interface for emotional trajectory tracking.

    Usage:
        tracker = EmotionTracker()

        # After each memory write
        tracker.record(emotion_result)

        # Get trajectory analysis
        trajectory = tracker.get_trajectory()
        print(trajectory.summary())

        # Get empathic response suggestion
        suggestion = tracker.suggest_response(emotion_result)
    """

    def __init__(self, max_states: int = 200):
        self._trajectory = EmotionalTrajectory(max_states)
        self._per_agent: Dict[str, EmotionalTrajectory] = {}

    def record(self, emotion_result: dict, agent_id: str = None, timestamp: float = None):
        state = EmotionalState(emotion_result, timestamp)
        self._trajectory.add(state)
        if agent_id:
            if agent_id not in self._per_agent:
                self._per_agent[agent_id] = EmotionalTrajectory(self._trajectory.max_states)
            self._per_agent[agent_id].add(state)

    def get_trajectory(self, agent_id: str = None) -> EmotionalTrajectory:
        if agent_id and agent_id in self._per_agent:
            return self._per_agent[agent_id]
        return self._trajectory

    def get_current_state(self, agent_id: str = None) -> Optional[EmotionalState]:
        traj = self.get_trajectory(agent_id)
        return traj.states[-1] if traj.states else None

    def suggest_response(self, emotion_result: dict, agent_id: str = None, lang: str = "cn") -> Optional[str]:
        return EmpathicResponseEngine.suggest_response_from_result(emotion_result, lang)

    def get_summary(self, agent_id: str = None) -> dict:
        return self.get_trajectory(agent_id).summary()

    def get_transitions(self, agent_id: str = None, threshold: float = 0.4) -> List[dict]:
        return self.get_trajectory(agent_id).detect_transitions(threshold)

    def emotion_resonance(self, emotion_result: dict, agent_id: str = None) -> float:
        current = self.get_current_state(agent_id)
        if not current:
            return 0.0
        return EmotionAnalyzer.emotion_resonance_score(
            current.primary_emotions,
            emotion_result.get("primary_emotions", {}),
        )
