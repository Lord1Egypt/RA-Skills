"""
wyrd_matrix.py — Sigrid's Emotional Soul Engine
================================================

The living Norse psyche as a state machine, layered with a PAD (Pleasure-
Arousal-Dominance) 3D emotional vector for prompt synthesis.

Adopted and adapted from:
  soul_mechanics.py    → Hugr, Fylgja, Hamingja, CognitiveFriction,
                         EmotionalMemoryEcho, SoulLayer
  emotional_engine.py  → EmotionalProfile, extract_stimuli, EMOTION_KEYWORDS,
                         StressAccumulator, intensity_label

Key changes from sources:
  * Single-persona system — no registry, no dispatcher, no D&D condition logic
  * No game-engine imports (EventDispatcher, ConditionsSystem, SoulRegistry removed)
  * PAD 3D vector layer added — derives Pleasure/Arousal/Dominance from Hugr
  * Bio integration — BioState emotion multipliers scale incoming stimuli
  * All events publish to the Ørlög state bus, not a game dispatcher
  * SoulLayer.attach_echo() undefined-variable bug fixed (safe_turn → turn)
  * Standalone mode preserved — works without a bus during tests

Norse framing: The Wyrd Matrix is where Sigrid's inner world lives. Hugr (the
conscious mind) shifts with each exchange. Fylgja (the deep instinct) drifts
slowly beneath. Hamingja (spiritual luck) rises and falls with honor. All of
it braided — the way the Norns braid fate at the roots of Yggdrasil.
"""

from __future__ import annotations

import logging
import random
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)


# ─── PAD weight table ─────────────────────────────────────────────────────────
# Maps each emotion channel to (Pleasure, Arousal, Dominance) weights.
# Based on Mehrabian's PAD model adapted for Norse emotional channels.

_PAD_WEIGHTS: Dict[str, Tuple[float, float, float]] = {
    "joy":        (+1.00, +0.40, +0.20),
    "sadness":    (-0.80, -0.50, -0.40),
    "fear":       (-0.60, +0.70, -0.70),
    "anger":      (-0.50, +0.80, +0.50),
    "shame":      (-0.70, -0.30, -0.60),
    "attachment": (+0.60, +0.30, +0.10),
}


# ─── Emotion keyword extraction ───────────────────────────────────────────────
# Adopted from emotional_engine.py — unchanged except Norse channels.

EMOTION_KEYWORDS: Dict[str, List[Tuple[str, float]]] = {
    "fear": [
        ("fear", 0.12), ("afraid", 0.12), ("terrified", 0.20),
        ("dread", 0.16), ("horror", 0.20), ("panic", 0.18),
        ("tremble", 0.14), ("cower", 0.14), ("flee", 0.12),
        ("nightmare", 0.14), ("ominous", 0.10),
    ],
    "anger": [
        ("anger", 0.12), ("angry", 0.12), ("rage", 0.20),
        ("fury", 0.20), ("wrath", 0.18), ("irritated", 0.10),
        ("snarl", 0.14), ("growl", 0.12), ("scowl", 0.10),
        ("strike", 0.10), ("shout", 0.12), ("curse", 0.14),
    ],
    "sadness": [
        ("sad", 0.12), ("grief", 0.18), ("sorrow", 0.16),
        ("despair", 0.20), ("mourn", 0.16), ("weep", 0.14),
        ("lament", 0.16), ("anguish", 0.18), ("desolate", 0.18),
        ("loss", 0.10), ("hollow", 0.12),
    ],
    "joy": [
        ("joy", 0.12), ("happy", 0.12), ("delight", 0.14),
        ("pleasure", 0.12), ("content", 0.10), ("laugh", 0.14),
        ("celebrate", 0.14), ("triumph", 0.16), ("gleam", 0.10),
        ("cheer", 0.12), ("smile", 0.10), ("merry", 0.12),
    ],
    "shame": [
        ("shame", 0.14), ("guilt", 0.14), ("embarrass", 0.12),
        ("humiliate", 0.18), ("disgrace", 0.18), ("dishonor", 0.18),
        ("coward", 0.16), ("unworthy", 0.16), ("failure", 0.10),
    ],
    "attachment": [
        ("love", 0.14), ("loyal", 0.12), ("trust", 0.12),
        ("bond", 0.12), ("friend", 0.10), ("ally", 0.10),
        ("devotion", 0.16), ("cherish", 0.14), ("protect", 0.12),
        ("kinship", 0.14), ("oath", 0.14),
    ],
}


def extract_stimuli(text: str) -> Dict[str, float]:
    """Scan text for EMOTION_KEYWORDS and return per-channel strength floats.

    Features:
      - Tokenised matching (punctuation-safe)
      - Simple negation handling ("not afraid", "never angry")
      - Intensity modifiers ("very", "slightly", "utterly")

    Strength is summed per channel and capped at 1.0.
    """
    stimuli: Dict[str, float] = {}
    lowered = (text or "").lower()
    tokens = re.findall(r"[a-z']+", lowered)
    if not tokens:
        return stimuli

    negators = {"not", "never", "no", "hardly"}
    intensifiers = {
        "very": 1.30, "extremely": 1.55, "utterly": 1.55,
        "deeply": 1.35, "slightly": 0.70, "barely": 0.60,
    }

    for channel, pairs in EMOTION_KEYWORDS.items():
        total = 0.0
        for idx, token in enumerate(tokens):
            for keyword, base_weight in pairs:
                if token == keyword or token.startswith(keyword):
                    factor = 1.0
                    if idx > 0:
                        prev = tokens[idx - 1]
                        if prev in negators:
                            factor *= 0.25
                        factor *= intensifiers.get(prev, 1.0)
                    total += base_weight * factor
        if total > 0.0:
            stimuli[channel] = min(1.0, total)

    return stimuli


_INTENSITY_LABELS = [
    (0.75, "overwhelming"),
    (0.55, "strong"),
    (0.35, "simmering"),
    (0.15, "faint"),
    (0.0, "absent"),
]


def intensity_label(value: float) -> str:
    """Convert a 0–1 float into a human-readable intensity label."""
    for threshold, label in _INTENSITY_LABELS:
        if value >= threshold:
            return label
    return "absent"


# ─── EmotionalProfile ─────────────────────────────────────────────────────────
# Adopted from emotional_engine.py — simplified for single-persona use.
# from_character() removed (persona-specific); from_config() replaces it.


@dataclass
class EmotionalProfile:
    """All tunable emotional parameters for Sigrid.

    Loaded from the ``emotion_profile`` block in data config.
    Falls back to sensible defaults if absent.

    tf_axis: 0.0 = pure Thinking (suppresses emotion), 1.0 = pure Feeling.
    Sigrid is INTP → default tf_axis = 0.35 (thinking-leaning but capable of depth).
    """

    tf_axis: float = 0.35
    gender_axis: float = 0.25         # female-leaning statistical tendency
    individual_offset: float = 0.0    # seeded variance ±0.2
    baseline_intensity: float = 1.0   # overall reactivity multiplier
    expression_threshold: float = 0.50
    rumination_bias: float = 0.35     # INTP: processes before releasing
    decay_rate: float = 0.12          # hugr decay fraction per turn
    channel_weights: Dict[str, float] = field(default_factory=lambda: {
        "fear": 1.0, "anger": 0.9, "sadness": 1.0,
        "joy": 1.0, "shame": 0.85, "attachment": 1.1,
    })
    chronotype: str = "diurnal"
    stress_resistance: float = 0.55   # INTP: internalises, but handles it

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "EmotionalProfile":
        """Build from a config dict (``emotion_profile`` block or flat dict)."""
        block = config.get("emotion_profile") or config
        if not block:
            return cls()
        return cls(
            tf_axis=float(block.get("tf_axis", 0.35)),
            gender_axis=float(block.get("gender_axis", 0.25)),
            individual_offset=float(block.get("individual_offset", 0.0)),
            baseline_intensity=float(block.get("baseline_intensity", 1.0)),
            expression_threshold=float(block.get("expression_threshold", 0.50)),
            rumination_bias=float(block.get("rumination_bias", 0.35)),
            decay_rate=float(block.get("decay_rate", 0.12)),
            channel_weights=dict(block.get("channel_weights", {})) or {
                "fear": 1.0, "anger": 0.9, "sadness": 1.0,
                "joy": 1.0, "shame": 0.85, "attachment": 1.1,
            },
            chronotype=str(block.get("chronotype", "diurnal")),
            stress_resistance=float(block.get("stress_resistance", 0.55)),
        )

    @property
    def effective_tf(self) -> float:
        """tf_axis adjusted for individual variance and gender tendency."""
        raw = self.tf_axis + (self.gender_axis * 0.10) + self.individual_offset
        return max(0.0, min(1.0, raw))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tf_axis": self.tf_axis,
            "gender_axis": self.gender_axis,
            "individual_offset": self.individual_offset,
            "baseline_intensity": self.baseline_intensity,
            "expression_threshold": self.expression_threshold,
            "rumination_bias": self.rumination_bias,
            "decay_rate": self.decay_rate,
            "channel_weights": self.channel_weights,
            "chronotype": self.chronotype,
            "stress_resistance": self.stress_resistance,
        }

    def nature_summary(self) -> str:
        """Return a human-readable emotional nature string for prompt building."""
        tf = self.effective_tf
        if tf >= 0.70:
            tf_label = "strongly Feeling-leaning"
        elif tf >= 0.55:
            tf_label = "Feeling-leaning"
        elif tf <= 0.30:
            tf_label = "strongly Thinking-leaning"
        elif tf <= 0.45:
            tf_label = "Thinking-leaning"
        else:
            tf_label = "balanced Thinking-Feeling"
        rumination = (
            "ruminates deeply" if self.rumination_bias >= 0.6
            else "moves on quickly" if self.rumination_bias <= 0.25
            else "processes and moves on"
        )
        expression = (
            "expressive" if self.expression_threshold <= 0.35
            else "reserved" if self.expression_threshold >= 0.65
            else "selectively expressive"
        )
        return f"{tf_label}, {expression}, {rumination}"


# ─── Soul layer components ────────────────────────────────────────────────────
# Adopted from soul_mechanics.py — game-engine imports removed.


@dataclass
class Hugr:
    """The Conscious Mind — volatile, short-term emotional surface.

    Each emotion is a float in [-1.0, +1.0].
    Decays toward 0 each turn by ``decay_rate``.
    Spikes (|delta| ≥ 0.4) are recorded for memory_store.
    """

    emotions: Dict[str, float] = field(default_factory=dict)
    decay_rate: float = 0.12
    spikes: List[Tuple[str, float, int]] = field(default_factory=list)

    def apply(self, emotion: str, delta: float, turn: int) -> float:
        """Apply a delta to an emotion. Returns the new clamped value."""
        current = self.emotions.get(emotion, 0.0)
        new_val = max(-1.0, min(1.0, current + delta))
        self.emotions[emotion] = new_val
        if abs(delta) >= 0.4:
            self.spikes.append((emotion, delta, turn))
            self.spikes = self.spikes[-40:]  # keep last 40 spikes
        return new_val

    def decay(self) -> None:
        """Move all emotions toward 0 (neutrality) each turn."""
        self.emotions = {
            k: v * (1.0 - self.decay_rate)
            for k, v in self.emotions.items()
            if abs(v) > 0.01
        }

    def dominant_emotion(self) -> Optional[Tuple[str, float]]:
        """Return the strongest current emotion by absolute magnitude."""
        if not self.emotions:
            return None
        return max(self.emotions.items(), key=lambda kv: abs(kv[1]))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "emotions": {k: round(v, 4) for k, v in self.emotions.items()},
            "decay_rate": self.decay_rate,
            "spikes": [
                {"emotion": e, "magnitude": round(m, 4), "turn": t}
                for e, m, t in self.spikes[-20:]
            ],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Hugr":
        obj = cls(
            emotions=data.get("emotions", {}),
            decay_rate=data.get("decay_rate", 0.12),
        )
        obj.spikes = [
            (s["emotion"], s["magnitude"], s["turn"])
            for s in data.get("spikes", [])
        ]
        return obj


@dataclass
class Fylgja:
    """The Subconscious / Instinct — deep drivers and trauma signatures.

    Shifts very slowly over many turns. In extreme stress it can
    override the Hugr (triggering a FYLGJA_OVERRIDE state event).
    Traumas leave permanent scars that lower the override threshold.
    """

    drivers: Dict[str, float] = field(default_factory=dict)
    trauma_scars: List[str] = field(default_factory=list)
    override_threshold: float = 0.85
    drift_rate: float = 0.02

    def imprint(self, driver: str, delta: float) -> float:
        """Slowly imprint a psychological driver."""
        current = self.drivers.get(driver, 0.0)
        new_val = max(-1.0, min(1.0, current + delta * self.drift_rate))
        self.drivers[driver] = new_val
        return new_val

    def add_trauma(self, description: str) -> None:
        """Record a trauma scar, lowering the override threshold."""
        if description not in self.trauma_scars:
            self.trauma_scars.append(description)
            self.override_threshold = max(0.4, self.override_threshold - 0.08)
            logger.info(
                "Fylgja trauma imprinted: %s (threshold now %.2f)",
                description, self.override_threshold,
            )

    def check_override(self, hugr: Hugr) -> Optional[str]:
        """Return the overriding driver name if Hugr stress surpasses threshold."""
        stress = sum(abs(v) for v in hugr.emotions.values())
        if stress >= self.override_threshold and self.drivers:
            dominant = max(self.drivers.items(), key=lambda kv: abs(kv[1]))
            return dominant[0]
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "drivers": {k: round(v, 4) for k, v in self.drivers.items()},
            "trauma_scars": self.trauma_scars,
            "override_threshold": round(self.override_threshold, 3),
            "drift_rate": self.drift_rate,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Fylgja":
        return cls(
            drivers=data.get("drivers", {}),
            trauma_scars=data.get("trauma_scars", []),
            override_threshold=data.get("override_threshold", 0.85),
            drift_rate=data.get("drift_rate", 0.02),
        )


@dataclass
class Hamingja:
    """Spiritual Momentum — metaphysical weight of the soul.

    Range 0.0 (cursed) to 1.0 (blessed). Broken oaths and dishonorable
    acts drain it. Heroic deeds and sacred acts restore it.
    """

    value: float = 0.5
    history: List[Dict[str, Any]] = field(default_factory=list)

    def shift(self, delta: float, reason: str) -> None:
        """Apply a delta and record the cause."""
        old = self.value
        self.value = max(0.0, min(1.0, self.value + delta))
        self.history.append({
            "from": round(old, 3),
            "to": round(self.value, 3),
            "delta": round(delta, 3),
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })
        self.history = self.history[-30:]
        logger.debug("Hamingja: %.2f → %.2f (%s)", old, self.value, reason)

    @property
    def state_label(self) -> str:
        if self.value >= 0.8:
            return "blessed"
        if self.value >= 0.6:
            return "favored"
        if self.value >= 0.4:
            return "uncertain"
        if self.value >= 0.2:
            return "burdened"
        return "cursed"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value": round(self.value, 4),
            "state_label": self.state_label,
            "history": self.history[-10:],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Hamingja":
        obj = cls(value=data.get("value", 0.5))
        obj.history = data.get("history", [])
        return obj


@dataclass
class CognitiveFriction:
    """Friction between Sigrid's declared values and her recent behavioral record.

    High friction → stress accumulates → breakdown events fire to the bus.
    """

    core_values: List[str] = field(default_factory=list)
    violations: List[Dict[str, Any]] = field(default_factory=list)
    friction_score: float = 0.0
    breakdown_threshold: float = 0.75
    relief_rate: float = 0.05

    def record_action(self, action: str, violates_values: List[str], turn: int) -> float:
        """Log an action and its value conflicts. Returns updated friction."""
        if not violates_values:
            self.friction_score = max(0.0, self.friction_score - self.relief_rate)
            return self.friction_score
        delta = 0.10 * len(violates_values)
        self.friction_score = min(1.0, self.friction_score + delta)
        self.violations.append({
            "action": action[:200],
            "conflicts": violates_values,
            "turn": turn,
            "friction_after": round(self.friction_score, 3),
        })
        self.violations = self.violations[-30:]
        return self.friction_score

    def check_breakdown(self) -> bool:
        return self.friction_score >= self.breakdown_threshold

    def resolve(self, reason: str) -> None:
        """Cathartic resolution — sharply drop friction."""
        self.friction_score = max(0.0, self.friction_score - 0.40)
        logger.info("Cognitive friction resolved: %s (now %.2f)", reason, self.friction_score)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "core_values": self.core_values,
            "violations": self.violations[-10:],
            "friction_score": round(self.friction_score, 4),
            "breakdown_threshold": self.breakdown_threshold,
            "relief_rate": self.relief_rate,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CognitiveFriction":
        obj = cls(
            core_values=data.get("core_values", []),
            friction_score=data.get("friction_score", 0.0),
            breakdown_threshold=data.get("breakdown_threshold", 0.75),
            relief_rate=data.get("relief_rate", 0.05),
        )
        obj.violations = data.get("violations", [])
        return obj


@dataclass
class EmotionalMemoryEcho:
    """When a significant memory surfaces, its original emotional charge
    re-applies to the Hugr with decaying intensity across subsequent turns.
    Called by memory_store when Muninn recalls a charged memory.
    """

    source_memory_id: str
    emotion_deltas: Dict[str, float]
    strength: float = 1.0
    decay_per_turn: float = 0.25
    turn_applied: int = 0

    def apply_to_hugr(self, hugr: Hugr, current_turn: int) -> bool:
        """Apply echo to Hugr. Returns False when the echo is spent (<5% strength)."""
        elapsed = current_turn - self.turn_applied
        intensity = self.strength * ((1.0 - self.decay_per_turn) ** elapsed)
        if intensity < 0.05:
            return False
        for emotion, base_delta in self.emotion_deltas.items():
            hugr.apply(emotion, base_delta * intensity, current_turn)
        logger.debug(
            "Memory echo '%s' applied at %.2f intensity",
            self.source_memory_id, intensity,
        )
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source_memory_id": self.source_memory_id,
            "emotion_deltas": self.emotion_deltas,
            "strength": self.strength,
            "decay_per_turn": self.decay_per_turn,
            "turn_applied": self.turn_applied,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmotionalMemoryEcho":
        return cls(
            source_memory_id=data.get("source_memory_id", ""),
            emotion_deltas=data.get("emotion_deltas", {}),
            strength=data.get("strength", 1.0),
            decay_per_turn=data.get("decay_per_turn", 0.25),
            turn_applied=data.get("turn_applied", 0),
        )


@dataclass
class StressAccumulator:
    """Tracks suppressed emotional pressure and converts it to a 0–100 score.

    Stress accumulates when emotions are internalized below the expression
    threshold. Published to the bus at STRESS_SPIKE and STRESS_BREAKDOWN levels.
    """

    stress_level: float = 0.0
    decay_mode: str = "exponential"     # "exponential" | "linear"
    _history: List[Dict[str, Any]] = field(default_factory=list)

    DECAY_PER_TURN: float = 1.5         # used only when decay_mode="linear"
    DECAY_RATE: float = 0.06            # fraction per turn for exponential mode
    SPIKE_THRESHOLD: float = 40.0
    BREAKDOWN_THRESHOLD: float = 80.0

    # Norse ritual recovery table
    RITUAL_EFFECTS: Dict[str, float] = field(default_factory=lambda: {
        "fire_vigil": -16.0,
        "oath_speaking": -10.0,
        "night_watch": -8.0,
        "communal_feast": -12.0,
        "seidr_working": -18.0,
        "blot": -14.0,
    })

    def accumulate(self, suppressed: Dict[str, float], resistance: float = 0.5) -> None:
        """Add suppressed emotion totals to stress pool."""
        total = sum(suppressed.values()) * (1.0 - resistance) * 100.0
        old = self.stress_level
        self.stress_level = min(100.0, self.stress_level + total)
        if total > 0.1:
            self._history.append({
                "from": round(old, 1),
                "to": round(self.stress_level, 1),
                "suppressed": suppressed,
            })
            self._history = self._history[-30:]

    def decay_turn(self) -> None:
        """Natural stress relief — call once per turn.

        Exponential mode (default): stress decays by a fixed fraction each turn,
        so high stress drops faster at first and slows as it approaches zero —
        mimicking human physiological recovery curves.
        Linear mode: fixed constant subtraction per turn (legacy behaviour).
        """
        if self.decay_mode == "exponential":
            self.stress_level = max(0.0, self.stress_level * (1.0 - self.DECAY_RATE))
        else:
            self.stress_level = max(0.0, self.stress_level - self.DECAY_PER_TURN)

    def apply_ritual(self, ritual_type: str) -> float:
        """Apply ritual stress relief. Returns new stress level."""
        delta = self.RITUAL_EFFECTS.get(ritual_type, -8.0)
        self.stress_level = max(0.0, min(100.0, self.stress_level + delta))
        return self.stress_level

    def check_threshold_events(self) -> List[str]:
        """Return event type strings if stress crosses thresholds."""
        events = []
        if self.stress_level >= self.BREAKDOWN_THRESHOLD:
            events.append("stress_breakdown")
        elif self.stress_level >= self.SPIKE_THRESHOLD:
            events.append("stress_spike")
        return events

    @property
    def label(self) -> str:
        if self.stress_level >= 80:
            return "breaking point"
        if self.stress_level >= 60:
            return "severely stressed"
        if self.stress_level >= 40:
            return "under strain"
        if self.stress_level >= 20:
            return "mildly stressed"
        return "composed"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stress_level": round(self.stress_level, 2),
            "decay_mode": self.decay_mode,
            "label": self.label,
            "history": self._history[-10:],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StressAccumulator":
        obj = cls(
            stress_level=data.get("stress_level", 0.0),
            decay_mode=data.get("decay_mode", "exponential"),
        )
        obj._history = data.get("history", [])
        return obj


# ─── SoulLayer ────────────────────────────────────────────────────────────────


@dataclass
class SoulLayer:
    """The complete Norse psyche — Hugr, Fylgja, Hamingja, Friction, Echoes.

    One SoulLayer for Sigrid. Ticked once per conversation turn.
    """

    character_id: str
    hugr: Hugr = field(default_factory=Hugr)
    fylgja: Fylgja = field(default_factory=Fylgja)
    hamingja: Hamingja = field(default_factory=Hamingja)
    friction: CognitiveFriction = field(default_factory=CognitiveFriction)
    active_echoes: List[EmotionalMemoryEcho] = field(default_factory=list)

    def tick(self, turn: int) -> List[str]:
        """Advance one turn. Returns list of triggered event type strings."""
        events: List[str] = []

        # 1. Decay Hugr emotions toward neutral
        self.hugr.decay()

        # 2. Apply and cull spent memory echoes
        live_echoes = []
        for echo in self.active_echoes:
            if echo.apply_to_hugr(self.hugr, turn):
                live_echoes.append(echo)
            else:
                logger.debug("Memory echo '%s' expired", echo.source_memory_id)
        self.active_echoes = live_echoes

        # 3. Check for Fylgja override
        override = self.fylgja.check_override(self.hugr)
        if override:
            events.append(f"fylgja_override:{override}")
            logger.info(
                "Fylgja override triggered for %s — driver: %s",
                self.character_id, override,
            )

        # 4. Check cognitive breakdown
        if self.friction.check_breakdown():
            events.append("cognitive_breakdown")
            logger.info(
                "Cognitive breakdown for %s (friction %.2f)",
                self.character_id, self.friction.friction_score,
            )

        return events

    def attach_echo(
        self,
        memory_id: str,
        emotion_deltas: Dict[str, float],
        turn: int,
        strength: float = 0.6,
    ) -> None:
        """Attach a memory echo — called by memory_store when a memory surfaces."""
        echo = EmotionalMemoryEcho(
            source_memory_id=memory_id,
            emotion_deltas=emotion_deltas,
            strength=strength,
            turn_applied=turn,   # fixed: was undefined `safe_turn` in source
        )
        self.active_echoes.append(echo)
        if len(self.active_echoes) > 5:
            self.active_echoes = self.active_echoes[-5:]

    def get_ai_summary(self) -> str:
        """Compact human-readable summary for the AI Narrator context."""
        dominant = self.hugr.dominant_emotion()
        dom_str = f"{dominant[0]} ({dominant[1]:+.2f})" if dominant else "neutral"
        return (
            f"Hugr={dom_str} | "
            f"Hamingja={self.hamingja.state_label} ({self.hamingja.value:.2f}) | "
            f"Friction={self.friction.friction_score:.2f} | "
            f"Trauma scars={len(self.fylgja.trauma_scars)} | "
            f"Echoes={len(self.active_echoes)}"
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "character_id": self.character_id,
            "hugr": self.hugr.to_dict(),
            "fylgja": self.fylgja.to_dict(),
            "hamingja": self.hamingja.to_dict(),
            "friction": self.friction.to_dict(),
            "active_echoes": [e.to_dict() for e in self.active_echoes],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SoulLayer":
        obj = cls(character_id=data.get("character_id", "sigrid"))
        if "hugr" in data:
            obj.hugr = Hugr.from_dict(data["hugr"])
        if "fylgja" in data:
            obj.fylgja = Fylgja.from_dict(data["fylgja"])
        if "hamingja" in data:
            obj.hamingja = Hamingja.from_dict(data["hamingja"])
        if "friction" in data:
            obj.friction = CognitiveFriction.from_dict(data["friction"])
        obj.active_echoes = [
            EmotionalMemoryEcho.from_dict(e) for e in data.get("active_echoes", [])
        ]
        return obj


# ─── WyrdState ────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class WyrdState:
    """Typed snapshot of the complete Wyrd (emotional/spiritual) state.

    Published to the state bus as a ``wyrd_update`` StateEvent.
    Consumed by: prompt_synthesizer (all fields), oracle (hamingja),
                 memory_store (spikes + dominant emotion).
    """

    # Hugr (conscious emotions)
    hugr_emotions: Dict[str, float]
    hugr_dominant: Optional[Tuple[str, float]]
    hugr_spikes: List[Dict[str, Any]]   # recent spikes for memory_store

    # Fylgja (subconscious)
    fylgja_drivers: Dict[str, float]
    fylgja_override: Optional[str]      # non-None = instinct has overridden reason

    # Hamingja (spiritual luck)
    hamingja: float
    hamingja_label: str

    # Cognitive friction
    friction_score: float

    # Stress
    stress_level: float
    stress_label: str

    # PAD 3D emotional vector
    pad_pleasure: float
    pad_arousal: float
    pad_dominance: float

    # Behavioral hint (advisory)
    behavior_suggestion: Optional[str]

    # Nature summary for prompt context
    nature_summary: str

    # Meta
    turn: int
    timestamp: str
    vitality_modulated_decay: bool = False   # True if Hugr decay was slowed by low vitality
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dict for state bus payload."""
        return {
            "hugr_emotions": {k: round(v, 4) for k, v in self.hugr_emotions.items()},
            "hugr_dominant": (
                {"channel": self.hugr_dominant[0], "intensity": round(self.hugr_dominant[1], 4)}
                if self.hugr_dominant else None
            ),
            "hugr_spikes": self.hugr_spikes,
            "fylgja_drivers": {k: round(v, 4) for k, v in self.fylgja_drivers.items()},
            "fylgja_override": self.fylgja_override,
            "hamingja": round(self.hamingja, 4),
            "hamingja_label": self.hamingja_label,
            "friction_score": round(self.friction_score, 4),
            "stress_level": round(self.stress_level, 2),
            "stress_label": self.stress_label,
            "pad_pleasure": round(self.pad_pleasure, 4),
            "pad_arousal": round(self.pad_arousal, 4),
            "pad_dominance": round(self.pad_dominance, 4),
            "behavior_suggestion": self.behavior_suggestion,
            "nature_summary": self.nature_summary,
            "turn": self.turn,
            "timestamp": self.timestamp,
            "vitality_modulated_decay": self.vitality_modulated_decay,
            "degraded": self.degraded,
        }


# ─── Hamingja signal inference ────────────────────────────────────────────────

_HONOR_TOKENS = {"protect", "aid", "heal", "honor", "keep", "spare", "mercy", "forgive"}
_SHADOW_TOKENS = {"betray", "deceive", "steal", "murder", "slay", "lie", "abandon"}
_OATH_TOKENS = {"oath", "swear", "vow", "pledge", "promise"}
_BETRAYAL_TOKENS = {"betray", "treach", "break", "oath broken"}


def _infer_action_signals(text: str) -> Dict[str, Any]:
    """Huginn scouts action text for honor/shadow signals to shift Hamingja.

    Returns:
        hamingja_delta: float shift to apply
        violations: List[str] value conflicts for CognitiveFriction
        driver_deltas: Dict[str, float] Fylgja driver shifts
    """
    lowered = (text or "").lower()
    tokens = set(re.findall(r"[a-z']+", lowered))

    hamingja_delta = 0.0
    violations: List[str] = []
    driver_deltas: Dict[str, float] = {}

    if tokens & _HONOR_TOKENS:
        hamingja_delta += 0.06
        driver_deltas["duty"] = 0.35

    if tokens & _SHADOW_TOKENS:
        hamingja_delta -= 0.08
        violations.extend(["honor", "oath-keeping"])
        driver_deltas["wrath"] = 0.35

    if tokens & _OATH_TOKENS:
        hamingja_delta += 0.04

    if tokens & _BETRAYAL_TOKENS:
        hamingja_delta -= 0.12
        violations.append("oath-keeping")
        driver_deltas["guilt"] = 0.40

    return {
        "hamingja_delta": round(hamingja_delta, 3),
        "violations": sorted(set(violations)),
        "driver_deltas": driver_deltas,
    }


# ─── WyrdMatrix ───────────────────────────────────────────────────────────────


class WyrdMatrix:
    """Sigrid's emotional soul engine — the Wyrd Matrix.

    Integrates:
      - SoulLayer (Hugr/Fylgja/Hamingja/Friction/Echoes)
      - StressAccumulator
      - EmotionalProfile (MBTI/gender/chronotype modifiers)
      - PAD vector computation
      - Bio integration (BioState multipliers)
      - State bus publishing

    Turn cadence: tick() called once per conversation turn by the runtime.
    """

    MODULE_NAME = "wyrd_matrix"

    def __init__(
        self,
        profile: Optional[EmotionalProfile] = None,
        core_values: Optional[List[str]] = None,
    ) -> None:
        self.profile = profile or EmotionalProfile()
        self.soul = SoulLayer(character_id="sigrid")
        self.stress = StressAccumulator()
        self._turn: int = 0
        self._vitality_modulated: bool = False   # E-07: set True when tick() receives vitality

        # Seed CognitiveFriction with Sigrid's core values
        if core_values:
            self.soul.friction.core_values = list(core_values)

        # Sync Hugr decay rate from profile
        self.soul.hugr.decay_rate = self.profile.decay_rate

        logger.info(
            "WyrdMatrix initialised — tf=%.2f, threshold=%.2f, decay=%.2f",
            self.profile.effective_tf,
            self.profile.expression_threshold,
            self.profile.decay_rate,
        )

    # ─── Factory ──────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "WyrdMatrix":
        """Construct from a config dict (``wyrd`` or ``emotion_profile`` block)."""
        profile = EmotionalProfile.from_config(config)
        core_values = config.get("core_values") or config.get("wyrd", {}).get("core_values", [])
        return cls(profile=profile, core_values=core_values)

    # ─── Public API ───────────────────────────────────────────────────────────

    def process_text(
        self,
        text: str,
        bio_multipliers: Optional[Dict[str, float]] = None,
        time_of_day: str = "",
    ) -> WyrdState:
        """Extract emotional stimuli from text, apply to soul, return WyrdState.

        Args:
            text: User message or narrative content to scan.
            bio_multipliers: emotion_multipliers from BioState (bio_engine output).
            time_of_day: "morning" | "afternoon" | "night" etc. for chronotype mod.

        Returns:
            WyrdState snapshot after applying the stimuli.
        """
        try:
            stimuli = extract_stimuli(text)
            if stimuli:
                self._apply_stimuli_internal(stimuli, bio_multipliers, time_of_day)

            # Also infer Hamingja / Fylgja signals from action semantics
            signals = _infer_action_signals(text)
            if abs(signals["hamingja_delta"]) > 0.001:
                self.soul.hamingja.shift(
                    signals["hamingja_delta"],
                    reason=f"text signal: {text[:60]}",
                )
            for driver, delta in signals["driver_deltas"].items():
                self.soul.fylgja.imprint(driver, delta)
            if signals["violations"]:
                self.soul.friction.record_action(text[:200], signals["violations"], self._turn)

            return self.get_state()
        except Exception as exc:
            logger.error("WyrdMatrix.process_text failed: %s", exc)
            return self._degraded_state()

    def apply_stimuli(
        self,
        stimuli: Dict[str, float],
        bio_multipliers: Optional[Dict[str, float]] = None,
        time_of_day: str = "",
    ) -> WyrdState:
        """Apply pre-extracted stimuli dict directly. Returns WyrdState."""
        try:
            self._apply_stimuli_internal(stimuli, bio_multipliers, time_of_day)
            return self.get_state()
        except Exception as exc:
            logger.error("WyrdMatrix.apply_stimuli failed: %s", exc)
            return self._degraded_state()

    def tick(self, metabolism_vitality: Optional[float] = None) -> WyrdState:
        """Advance one conversation turn — decay, echo, check overrides.

        Args:
            metabolism_vitality: vitality_score from MetabolismState (0.0–1.0).
                When provided, slows Hugr decay proportional to exhaustion —
                low vitality makes emotions "stick" longer.

        Returns WyrdState after tick. Call once per user message exchange.
        """
        try:
            self._turn += 1

            # E-07: Vitality-driven emotional inertia
            # Low vitality (exhaustion) → emotions decay more slowly
            # vitality=1.0 → normal decay; vitality=0.0 → 1.5× slower decay
            base_decay = self.profile.decay_rate
            if metabolism_vitality is not None:
                vitality = max(0.0, min(1.0, float(metabolism_vitality)))
                effective_decay = base_decay / (1.0 + (1.0 - vitality) * 0.5)
                self.soul.hugr.decay_rate = effective_decay
                self._vitality_modulated = True
                logger.debug(
                    "WyrdMatrix vitality modulation: vitality=%.2f → decay %.3f→%.3f",
                    vitality, base_decay, effective_decay,
                )
            else:
                self.soul.hugr.decay_rate = base_decay
                self._vitality_modulated = False

            events = self.soul.tick(self._turn)
            self.stress.decay_turn()

            for event_str in events:
                logger.info("WyrdMatrix soul event: %s (turn %d)", event_str, self._turn)

            return self.get_state()
        except Exception as exc:
            logger.error("WyrdMatrix.tick failed: %s", exc)
            return self._degraded_state()

    def get_state(self) -> WyrdState:
        """Return a typed WyrdState snapshot — no side effects."""
        try:
            hugr = self.soul.hugr
            dominant = hugr.dominant_emotion()
            override = self.soul.fylgja.check_override(hugr)

            pad_p, pad_a, pad_d = self._compute_pad()

            behavior = self._compute_behavior_suggestion()

            return WyrdState(
                hugr_emotions=dict(hugr.emotions),
                hugr_dominant=dominant,
                hugr_spikes=[
                    {"emotion": e, "magnitude": m, "turn": t}
                    for e, m, t in hugr.spikes[-5:]
                ],
                fylgja_drivers=dict(self.soul.fylgja.drivers),
                fylgja_override=override,
                hamingja=self.soul.hamingja.value,
                hamingja_label=self.soul.hamingja.state_label,
                friction_score=self.soul.friction.friction_score,
                stress_level=self.stress.stress_level,
                stress_label=self.stress.label,
                pad_pleasure=pad_p,
                pad_arousal=pad_a,
                pad_dominance=pad_d,
                behavior_suggestion=behavior,
                nature_summary=self.profile.nature_summary(),
                turn=self._turn,
                timestamp=datetime.now(timezone.utc).isoformat(),
                vitality_modulated_decay=self._vitality_modulated,
                degraded=False,
            )
        except Exception as exc:
            logger.error("WyrdMatrix.get_state failed: %s", exc)
            return self._degraded_state()

    async def publish(self, bus: StateBus) -> None:
        """Publish current WyrdState as a ``wyrd_update`` StateEvent to the bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module=self.MODULE_NAME,
                event_type="wyrd_update",
                payload=state.to_dict(),
            )
            await bus.publish_state(event, nowait=True)
            logger.debug(
                "WyrdMatrix published wyrd_update — dominant=%s hamingja=%s stress=%.1f",
                state.hugr_dominant,
                state.hamingja_label,
                state.stress_level,
            )
        except Exception as exc:
            logger.error("WyrdMatrix.publish failed: %s", exc)

    def attach_memory_echo(
        self,
        memory_id: str,
        emotion_deltas: Dict[str, float],
        strength: float = 0.6,
    ) -> None:
        """Called by memory_store when Muninn surfaces a charged memory."""
        self.soul.attach_echo(memory_id, emotion_deltas, self._turn, strength)
        logger.info("Memory echo attached from '%s' (strength=%.2f)", memory_id, strength)

    def handle_dream_tick(self) -> None:
        """E-15: Apply a subtle PAD shuffle when deep_night begins.

        Sigrid's Hugr stirs as the dream-weave opens.  Each active emotion
        channel receives a small ±0.05 nudge seeded by the current turn so
        the effect is reproducible but different each night.  Best-effort —
        all exceptions are caught and logged as WARN.
        """
        try:
            rng = random.Random(self._turn)  # nosec B311 - deterministic wyrd seed, not cryptographic
            emotions = self.soul.hugr.emotions
            if not emotions:
                logger.debug("WyrdMatrix.handle_dream_tick: no active emotions — skipping.")
                return
            for channel in list(emotions.keys()):
                delta = rng.uniform(-0.05, 0.05)
                current = emotions[channel]
                emotions[channel] = round(max(-1.0, min(1.0, current + delta)), 4)
            logger.info(
                "WyrdMatrix: dream tick PAD shuffle applied to %d channels (turn %d).",
                len(emotions),
                self._turn,
            )
        except Exception as exc:
            logger.warning("WyrdMatrix.handle_dream_tick failed: %s", exc)

    def apply_ritual_calm(self, ritual_type: str = "fire_vigil") -> float:
        """Apply ritual stress relief. Returns new stress level."""
        new_level = self.stress.apply_ritual(ritual_type)
        # Ritual also calms negative Hugr channels slightly
        for ch in ("fear", "anger", "shame", "sadness"):
            val = self.soul.hugr.emotions.get(ch, 0.0)
            if val > 0.1:
                self.soul.hugr.emotions[ch] = max(0.0, val - 0.12)
        logger.info(
            "Ritual '%s' applied — stress now %.1f", ritual_type, new_level
        )
        return new_level

    def snapshot(self) -> Dict[str, Any]:
        """Return current WyrdState as a JSON-safe dict (for debug / health API)."""
        return self.get_state().to_dict()

    # ─── Internal computation ─────────────────────────────────────────────────

    def _apply_stimuli_internal(
        self,
        stimuli: Dict[str, float],
        bio_multipliers: Optional[Dict[str, float]],
        time_of_day: str,
    ) -> None:
        """Compute profile-weighted impact and write to soul. Track suppressed stress."""
        suppressed: Dict[str, float] = {}

        for channel, raw_strength in stimuli.items():
            # Apply bio cycle multiplier to incoming stimulus
            bio_mult = (bio_multipliers or {}).get(channel, 1.0)
            bio_scaled = raw_strength * bio_mult

            # Profile-weighted impact
            impact = self._compute_impact(channel, bio_scaled, time_of_day)

            # Apply to Hugr
            self.soul.hugr.apply(channel, impact, self._turn)

            # Check expression — internalized emotion feeds stress
            current = self.soul.hugr.emotions.get(channel, 0.0)
            expressed = abs(current) >= self.profile.expression_threshold
            if not expressed:
                suppressed[channel] = impact * (1.0 - self.profile.stress_resistance)

            logger.debug(
                "WyrdMatrix/%s: raw=%.3f bio×=%.2f impact=%.3f expressed=%s",
                channel, raw_strength, bio_mult, impact, expressed,
            )

        if suppressed:
            self.stress.accumulate(suppressed, self.profile.stress_resistance)

        # Publish stress events (fire-and-forget logging)
        for event_str in self.stress.check_threshold_events():
            logger.warning("Stress threshold event: %s (level=%.1f)", event_str, self.stress.stress_level)

    def _compute_impact(self, channel: str, raw_strength: float, time_of_day: str) -> float:
        """Convert raw stimulus strength into profile-adjusted emotional impact."""
        channel_w = self.profile.channel_weights.get(channel, 1.0)
        tf_mod = 0.80 + (self.profile.effective_tf * 0.40)   # [0.80, 1.20]
        chron_mod = self._chronotype_mod(time_of_day)

        impact = raw_strength * channel_w * tf_mod * chron_mod * self.profile.baseline_intensity
        return round(max(0.0, min(1.0, impact)), 4)

    def _chronotype_mod(self, time_of_day: str) -> float:
        """Emotional clarity modifier based on chronotype alignment."""
        tod = (time_of_day or "").lower()
        ct = (self.profile.chronotype or "diurnal").lower()
        night_times = {"night", "midnight", "dusk"}
        day_times = {"dawn", "morning", "midday", "afternoon"}
        crep_times = {"dusk", "dawn", "twilight"}

        if ct == "nocturnal" and tod in night_times:
            return 1.12
        if ct == "diurnal" and tod in day_times:
            return 1.12
        if ct == "crepuscular" and tod in crep_times:
            return 1.12
        if ct == "nocturnal" and tod in day_times:
            return 0.88
        if ct == "diurnal" and tod in night_times:
            return 0.88
        return 1.0

    def _compute_pad(self) -> Tuple[float, float, float]:
        """Derive the PAD 3D emotional vector from current Hugr emotions.

        Each emotion channel contributes weighted (P, A, D) components.
        Result is clamped to [-1.0, +1.0] per axis.
        """
        p, a, d = 0.0, 0.0, 0.0
        emotions = self.soul.hugr.emotions

        for channel, intensity in emotions.items():
            weights = _PAD_WEIGHTS.get(channel)
            if weights is None:
                continue
            wp, wa, wd = weights
            p += intensity * wp
            a += intensity * wa
            d += intensity * wd

        return (
            round(max(-1.0, min(1.0, p)), 4),
            round(max(-1.0, min(1.0, a)), 4),
            round(max(-1.0, min(1.0, d)), 4),
        )

    def _compute_behavior_suggestion(self) -> Optional[str]:
        """Return an advisory behavior suggestion based on dominant emotion.

        Simplified from EmotionalBehavior — deterministic, not random.
        The AI model has full discretion to ignore this.
        """
        dominant = self.soul.hugr.dominant_emotion()
        if not dominant:
            return None
        channel, intensity = dominant
        if abs(intensity) < self.profile.expression_threshold:
            return None

        _BEHAVIOR_MAP: Dict[str, List[str]] = {
            "fear":       ["defensive_posture", "ritual_ward", "seek_frith"],
            "anger":      ["confront_directly", "ritual_release", "cold_withdrawal"],
            "sadness":    ["withdrawal", "seek_comfort", "ritual_mourning"],
            "joy":        ["celebrate_openly", "share_with_user", "quiet_contentment"],
            "shame":      ["atonement_act", "withdrawal", "honest_confession"],
            "attachment": ["protectiveness", "confide_secrets", "gift_giving"],
        }
        options = _BEHAVIOR_MAP.get(channel, [])
        if not options:
            return None

        # Pick by intensity tier: high→[0], mid→[1], low→[2]
        tier = 0 if abs(intensity) >= 0.65 else 1 if abs(intensity) >= 0.35 else 2
        return options[min(tier, len(options) - 1)]

    def _degraded_state(self) -> WyrdState:
        """Return a neutral fallback WyrdState when computation fails."""
        return WyrdState(
            hugr_emotions={},
            hugr_dominant=None,
            hugr_spikes=[],
            fylgja_drivers={},
            fylgja_override=None,
            hamingja=0.5,
            hamingja_label="uncertain",
            friction_score=0.0,
            stress_level=0.0,
            stress_label="composed",
            pad_pleasure=0.0,
            pad_arousal=0.0,
            pad_dominance=0.0,
            behavior_suggestion=None,
            nature_summary=self.profile.nature_summary(),
            turn=self._turn,
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=True,
        )

    # ─── Persistence ──────────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        """Full serialisable state for session save."""
        return {
            "profile": self.profile.to_dict(),
            "soul": self.soul.to_dict(),
            "stress": self.stress.to_dict(),
            "turn": self._turn,
            "saved_at": datetime.now(timezone.utc).isoformat(),
        }

    def load_from_dict(self, data: Dict[str, Any]) -> None:
        """Restore from serialised state (session resume)."""
        try:
            if "profile" in data:
                self.profile = EmotionalProfile.from_config(data["profile"])
            if "soul" in data:
                self.soul = SoulLayer.from_dict(data["soul"])
                self.soul.hugr.decay_rate = self.profile.decay_rate
            if "stress" in data:
                self.stress = StressAccumulator.from_dict(data["stress"])
            self._turn = int(data.get("turn", 0))
            logger.info(
                "WyrdMatrix state restored — turn=%d hamingja=%.2f stress=%.1f",
                self._turn, self.soul.hamingja.value, self.stress.stress_level,
            )
        except Exception as exc:
            logger.error("WyrdMatrix.load_from_dict failed: %s — starting fresh", exc)


# ─── Module-level singleton ────────────────────────────────────────────────────

_MATRIX: Optional[WyrdMatrix] = None


def get_wyrd_matrix() -> WyrdMatrix:
    """Return the global WyrdMatrix. Raises RuntimeError if not initialised."""
    if _MATRIX is None:
        raise RuntimeError(
            "WyrdMatrix not initialised — call init_wyrd_matrix() in main.py first"
        )
    return _MATRIX


def init_wyrd_matrix(
    profile: Optional[EmotionalProfile] = None,
    core_values: Optional[List[str]] = None,
) -> WyrdMatrix:
    """Create and register the global WyrdMatrix (call once at startup)."""
    global _MATRIX
    _MATRIX = WyrdMatrix(profile=profile, core_values=core_values)
    return _MATRIX


def init_wyrd_matrix_from_config(config: Dict[str, Any]) -> WyrdMatrix:
    """Create and register the global WyrdMatrix from a config dict."""
    global _MATRIX
    _MATRIX = WyrdMatrix.from_config(config)
    return _MATRIX
