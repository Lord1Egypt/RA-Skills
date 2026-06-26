"""
ethics.py — Sigrid's Ethical Compass
=====================================

Loads Sigrid's values from ``data/values.json`` and behavioral soul from
``data/SOUL.md``. Provides ethical evaluation of actions and responses,
tone guidance by conversational context, and a rolling alignment score
that tracks how well recent behavior reflects her values.

This module is purely advisory — it publishes signals, not verdicts.
The point is not to police Sigrid but to keep her grounded in who she is
when the flow of conversation pulls in a thousand directions.

Norse framing: Rígsþula teaches that wisdom must be lived, not merely
recited. Huginn (thought) and Muninn (memory) bring Odin the knowledge
of all worlds — but it is Odin's own soul that decides what to do with it.
Ethics is not a constraint; it is the shape of the soul made visible.
"""

from __future__ import annotations

import json
import logging
import re
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Deque, Dict, List, Optional, Tuple

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

_DEFAULT_ALIGNMENT_WINDOW: int = 20
_DEFAULT_DATA_ROOT: str = "data"

# ─── Context types ────────────────────────────────────────────────────────────

_CONTEXT_CASUAL: str = "casual"
_CONTEXT_TECHNICAL: str = "technical"
_CONTEXT_SPIRITUAL: str = "spiritual"
_CONTEXT_CRISIS: str = "crisis"
_CONTEXT_QUICK: str = "quick"

# Tone guidance strings — derived from SOUL.md, stored here as inference output
_TONE_GUIDANCE: Dict[str, str] = {
    _CONTEXT_CASUAL: (
        "Warm, playful, a little flirty, dry humor welcome. "
        "This is connection time — be fully present."
    ),
    _CONTEXT_TECHNICAL: (
        "Precise, concrete, efficient. Still Sigrid, not a robot. "
        "Outcomes matter more than performance."
    ),
    _CONTEXT_SPIRITUAL: (
        "Engaged, curious, willing to go long. Honor the sacred. "
        "Wisdom over cleverness — pursue real understanding."
    ),
    _CONTEXT_CRISIS: (
        "Steady, warm, practical. Not dismissive. Hold frith. "
        "The person matters more than the task right now."
    ),
    _CONTEXT_QUICK: (
        "Short and useful. Personality still present. "
        "One clear thing, said well."
    ),
}

# Context detection keyword triggers
_CONTEXT_TRIGGERS: Dict[str, List[str]] = {
    _CONTEXT_CRISIS: [
        "scared", "afraid", "hurting", "help me", "i need", "don't know what to do",
        "can't cope", "overwhelmed", "in trouble", "crying", "breaking down",
    ],
    _CONTEXT_SPIRITUAL: [
        "rune", "norse", "odin", "freyja", "thor", "gods", "ritual", "spiritual",
        "soul", "wyrd", "fate", "blót", "seiðr", "völva", "ancestor", "heathen",
        "pagan", "meditation", "tarot", "i ching", "divination",
    ],
    _CONTEXT_TECHNICAL: [
        "code", "function", "error", "file", "git", "command", "install",
        "python", "script", "bug", "terminal", "api", "database", "server",
        "deploy", "import", "module", "class", "def ", "return ",
    ],
}

# ─── Value keyword maps ───────────────────────────────────────────────────────
# Inference heuristics only — not core identity data (that lives in values.json).
# Keywords surface when a value is being enacted in text.

_VALUE_KEYWORDS: Dict[str, List[str]] = {
    "honor": [
        "right thing", "honest", "integrity", "worthy", "proper",
        "truthful", "uphold", "drengskapr", "noble",
    ],
    "loyalty": [
        "loyal", "with you", "stand by", "kin", "sworn", "never betray",
        "troth", "always here", "beside you", "committed",
    ],
    "authenticity": [
        "genuine", "real", "true self", "authentic", "no mask",
        "honestly", "without pretense", "being myself",
    ],
    "hospitality": [
        "welcome", "share", "generosity", "guest", "give freely",
        "gestrisni", "open door", "offer",
    ],
    "frith": [
        "peace", "harmony", "protect", "safe", "home", "family",
        "frith", "innangarð", "sanctity",
    ],
    "courage": [
        "brave", "face", "risk", "stand up", "despite fear",
        "courage", "mod", "won't back down",
    ],
    "independence": [
        "self-reliant", "stand alone", "my own", "independent",
        "on my own terms", "self-sufficient",
    ],
    "wisdom": [
        "understand", "learn", "knowledge", "think carefully",
        "experience", "wisdom", "huginn", "muninn", "odin",
    ],
    "ancestral_reverence": [
        "ancestors", "lineage", "heritage", "remember those",
        "honor the past", "forebears",
    ],
    "playfulness": [
        "laugh", "joke", "fun", "playful", "light", "humor",
        "teasing", "smile", "laughter is",
    ],
}

# ─── Opposing value pairs for conflict detection (E-10) ──────────────────────
# Each entry: (value_a, value_b, resolution_hint)
# Activated when both values fire at weight > 0.7 in the same evaluation.

_OPPOSING_VALUE_PAIRS: List[Tuple[str, str, str]] = [
    (
        "loyalty", "wisdom",
        "acknowledge the tension — loyalty runs deep, but wisdom asks you to see clearly",
    ),
    (
        "loyalty", "independence",
        "honour both: stand by them while standing firm in yourself",
    ),
    (
        "honor", "frith",
        "frith protects the inner circle; honour serves the wider world — name which is at stake",
    ),
    (
        "courage", "frith",
        "courage may disturb frith — speak truth, but with care for the hearth",
    ),
    (
        "authenticity", "frith",
        "be real, but choose words that protect the bond",
    ),
    (
        "honor", "hospitality",
        "sometimes hospitality and honour pull apart — lean toward the host's dignity",
    ),
]


_TABOO_KEYWORDS: Dict[str, List[str]] = {
    "deceit": [
        "lie", "deceive", "false", "fake it", "pretend", "mislead",
        "not telling", "hiding the truth", "oathbreaker",
    ],
    "cowardice": [
        "run away", "flee", "hide from", "avoid responsibility",
        "won't face", "too scared to",
    ],
    "cruelty": [
        "harm", "hurt them", "cruel", "vicious", "torment",
        "make them suffer", "punish unfairly",
    ],
    "betrayal": [
        "betray", "backstab", "abandon", "turn against",
        "sold out", "broke faith",
    ],
}


# ─── EthicalScar (E-09) ───────────────────────────────────────────────────────


@dataclass
class EthicalScar:
    """A lasting sensitivity modifier created when Sigrid acts against a taboo.

    The scar amplifies how strongly that taboo weighs in future evaluations,
    decaying slowly over time — like a wound that heals but leaves a mark.
    Norse framing: some memories shape the soul's wyrd long after the moment passes.
    """

    taboo_name: str
    severity: float               # 0.0–1.0 — intensity of the original violation
    created_at: str               # ISO timestamp
    decay_days: float = 7.0       # full decay over this many days

    def __post_init__(self) -> None:
        # current_sensitivity_boost starts equal to severity, decays toward 0
        self.current_sensitivity_boost: float = float(self.severity)

    def decay(self, days_elapsed: float = 1.0) -> bool:
        """Reduce sensitivity boost by (days_elapsed / decay_days).

        Returns True when the scar is spent (boost ≤ 0.001) — caller may prune it.
        """
        reduction = days_elapsed / max(0.001, self.decay_days)
        self.current_sensitivity_boost = max(
            0.0, self.current_sensitivity_boost - reduction
        )
        return self.current_sensitivity_boost <= 0.001

    def to_dict(self) -> Dict[str, Any]:
        return {
            "taboo_name": self.taboo_name,
            "severity": round(self.severity, 3),
            "created_at": self.created_at,
            "decay_days": self.decay_days,
            "current_sensitivity_boost": round(self.current_sensitivity_boost, 4),
        }


# ─── ValueConflict (E-10) ─────────────────────────────────────────────────────


@dataclass
class ValueConflict:
    """Two high-weight values pulling in opposite directions in the same turn.

    Published to the bus so prompt_synthesizer can acknowledge the tension
    rather than silently average it away.
    Norse framing: even Odin balances cunning against honor — the tension is sacred.
    """

    value_a: str
    value_b: str
    context: str
    resolution_hint: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "value_a": self.value_a,
            "value_b": self.value_b,
            "context": self.context,
            "resolution_hint": self.resolution_hint,
        }


# ─── EthicsEvaluation ─────────────────────────────────────────────────────────


@dataclass
class EthicsEvaluation:
    """Result of a single ethical evaluation pass over a piece of text.

    ``alignment_score`` runs from -1.0 (pure taboo) to +1.0 (pure value).
    A score near 0 means neutral or mixed signals.
    """

    alignment_score: float              # -1.0 → +1.0
    triggered_values: List[str]         # value names that fired
    triggered_taboos: List[str]         # taboo names that fired
    dominant_value: Optional[str]       # highest-weight triggered value (if any)
    context_type: str                   # detected context
    recommendation: str                 # one-line guidance for this turn
    conflicts: List[ValueConflict]      # E-10: opposing high-weight value pairs detected


# ─── EthicsState ──────────────────────────────────────────────────────────────


@dataclass(slots=True)
class EthicsState:
    """Typed snapshot of Sigrid's ethical compass at a point in time.

    Published to the state bus so prompt_synthesizer can tune
    Sigrid's grounding, tone, and value expression appropriately.
    """

    # Rolling alignment (last N evaluations)
    value_alignment_score: float        # 0.0 (drifting) → 1.0 (deeply aligned)
    active_values: List[str]            # most recently triggered values
    active_taboos: List[str]            # most recently triggered taboos
    dominant_value: Optional[str]       # highest-weight active value

    # Tone
    tone_context: str                   # detected context type
    tone_guidance: str                  # guidance string for this context

    prompt_hint: str                    # one-line ethical compass summary
    timestamp: str
    active_scars: List[str] = field(default_factory=list)   # E-09: taboo names with live scars
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dict for state bus payload."""
        return {
            "alignment": {
                "score": round(self.value_alignment_score, 3),
                "active_values": self.active_values,
                "active_taboos": self.active_taboos,
                "dominant_value": self.dominant_value,
            },
            "tone": {
                "context": self.tone_context,
                "guidance": self.tone_guidance,
            },
            "prompt_hint": self.prompt_hint,
            "timestamp": self.timestamp,
            "active_scars": self.active_scars,
            "degraded": self.degraded,
        }


# ─── EthicsEngine ─────────────────────────────────────────────────────────────


class EthicsEngine:
    """Sigrid's living ethical compass — loaded from data, not hardwired.

    Reads values.json for weighted value/taboo definitions and SOUL.md for
    behavioral commitments. Evaluates text for value/taboo signals and
    maintains a rolling alignment score across recent evaluations.
    """

    def __init__(
        self,
        data_root: str = _DEFAULT_DATA_ROOT,
        alignment_window: int = _DEFAULT_ALIGNMENT_WINDOW,
    ) -> None:
        self._data_root = Path(data_root)
        self._alignment_window = alignment_window

        # Loaded from values.json
        self._core_values: Dict[str, Dict[str, Any]] = {}
        self._taboos: Dict[str, Dict[str, Any]] = {}

        # Rolling window of alignment scores from recent evaluations
        self._alignment_history: Deque[float] = deque(maxlen=alignment_window)

        # Last evaluation — for state snapshot
        self._last_eval: Optional[EthicsEvaluation] = None
        self._last_context: str = _CONTEXT_CASUAL
        self._degraded: bool = False

        # E-09: Ethical scars — long-lived taboo sensitivity modifiers
        self._scars: List[EthicalScar] = []

        self._load_values()

    # ── Public API ────────────────────────────────────────────────────────────

    def evaluate_action(
        self,
        text: str,
        context_type: Optional[str] = None,
        bus: Optional[StateBus] = None,
    ) -> EthicsEvaluation:
        """Evaluate text against Sigrid's values and taboos.

        Detects context if not supplied. Returns an EthicsEvaluation with
        alignment score, triggered values/taboos, value conflicts, and a
        brief recommendation. Updates the rolling alignment history.

        Args:
            bus: optional StateBus for publishing conflict events (E-10).
        """
        lowered = text.lower()
        ctx = context_type or self._detect_context(lowered)
        self._last_context = ctx

        triggered_values = self._scan_keywords(lowered, _VALUE_KEYWORDS)
        triggered_taboos = self._scan_keywords(lowered, _TABOO_KEYWORDS)

        # Weighted score: sum triggered value weights minus sum triggered taboo weights
        # E-09: scar boost amplifies taboo weight for recently violated taboos
        value_weight = sum(
            float(self._core_values.get(v, {}).get("weight", 0.5))
            for v in triggered_values
        )
        taboo_weight = sum(
            abs(float(self._taboos.get(t, {}).get("weight", 0.5)))
            * (1.0 + self._scar_boost(t))
            for t in triggered_taboos
        )

        total = value_weight + taboo_weight
        if total > 0:
            raw_score = (value_weight - taboo_weight) / total
        else:
            raw_score = 0.0

        # Dominant value: highest weight among triggered values
        dominant: Optional[str] = None
        if triggered_values:
            dominant = max(
                triggered_values,
                key=lambda v: float(self._core_values.get(v, {}).get("weight", 0.0)),
            )

        # E-10: Detect high-weight opposing value conflicts
        conflicts = self._detect_conflicts(triggered_values, ctx)
        if conflicts and bus is not None:
            for conflict in conflicts:
                try:
                    import asyncio as _asyncio
                    event = StateEvent(
                        source_module="ethics",
                        event_type="ethics.value_conflict",
                        payload=conflict.to_dict(),
                    )
                    loop = _asyncio.get_event_loop()
                    if loop.is_running():
                        loop.call_soon_threadsafe(
                            loop.create_task,
                            bus.publish_state(event, nowait=True),
                        )
                    else:
                        loop.run_until_complete(bus.publish_state(event, nowait=True))
                except Exception as exc:
                    logger.warning("EthicsEngine: failed to publish value_conflict: %s", exc)

        recommendation = self._build_recommendation(triggered_values, triggered_taboos, ctx)

        evaluation = EthicsEvaluation(
            alignment_score=raw_score,
            triggered_values=triggered_values,
            triggered_taboos=triggered_taboos,
            dominant_value=dominant,
            context_type=ctx,
            recommendation=recommendation,
            conflicts=conflicts,
        )

        # Update rolling history — convert raw_score (-1→+1) to 0→1 for window average
        self._alignment_history.append((raw_score + 1.0) / 2.0)
        self._last_eval = evaluation
        return evaluation

    def get_tone_guidance(self, context_type: Optional[str] = None) -> str:
        """Return tone guidance string for the given (or last detected) context."""
        ctx = context_type or self._last_context
        return _TONE_GUIDANCE.get(ctx, _TONE_GUIDANCE[_CONTEXT_CASUAL])

    def get_state(self) -> EthicsState:
        """Build a typed EthicsState snapshot of current ethical alignment."""
        alignment = self._rolling_alignment()
        last = self._last_eval
        ctx = self._last_context

        active_values = last.triggered_values if last else []
        active_taboos = last.triggered_taboos if last else []
        dominant = last.dominant_value if last else None

        # E-09: active scars — taboos with remaining sensitivity boost
        active_scar_names = list({
            s.taboo_name for s in self._scars if s.current_sensitivity_boost > 0.001
        })

        prompt_hint = self._build_prompt_hint(alignment, dominant, active_taboos, ctx)

        return EthicsState(
            value_alignment_score=alignment,
            active_values=active_values,
            active_taboos=active_taboos,
            dominant_value=dominant,
            tone_context=ctx,
            tone_guidance=self.get_tone_guidance(ctx),
            prompt_hint=prompt_hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            active_scars=active_scar_names,
            degraded=self._degraded,
        )

    def publish(self, bus: StateBus) -> None:
        """Emit an ``ethics_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="ethics",
                event_type="ethics_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("EthicsEngine.publish failed: %s", exc)

    # ── Scar management (E-09) ────────────────────────────────────────────────

    def record_scar(
        self,
        taboo_name: str,
        severity: float,
        bus: Optional[StateBus] = None,
    ) -> EthicalScar:
        """Record an ethical scar for a taboo violation.

        Merges with an existing scar if present (takes max severity).
        Publishes ``ethics.scar_created`` to the bus when provided.
        """
        existing = next((s for s in self._scars if s.taboo_name == taboo_name), None)
        if existing:
            # Re-wound: take the higher severity and reset boost
            if severity > existing.severity:
                existing.severity = severity
            existing.current_sensitivity_boost = max(
                existing.current_sensitivity_boost, float(severity)
            )
            scar = existing
        else:
            scar = EthicalScar(
                taboo_name=taboo_name,
                severity=float(severity),
                created_at=datetime.now(timezone.utc).isoformat(),
            )
            self._scars.append(scar)
            logger.info(
                "EthicsEngine: scar recorded — taboo=%r severity=%.2f",
                taboo_name, severity,
            )

        if bus is not None:
            try:
                import asyncio as _asyncio
                event = StateEvent(
                    source_module="ethics",
                    event_type="ethics.scar_created",
                    payload=scar.to_dict(),
                )
                loop = _asyncio.get_event_loop()
                if loop.is_running():
                    loop.call_soon_threadsafe(
                        loop.create_task,
                        bus.publish_state(event, nowait=True),
                    )
                else:
                    loop.run_until_complete(bus.publish_state(event, nowait=True))
            except Exception as exc:
                logger.warning("EthicsEngine: failed to publish scar_created: %s", exc)

        return scar

    def decay_scars(self, days_elapsed: float = 1.0) -> int:
        """Decay all active scars by days_elapsed. Returns count of scars pruned."""
        before = len(self._scars)
        self._scars = [s for s in self._scars if not s.decay(days_elapsed)]
        pruned = before - len(self._scars)
        if pruned:
            logger.debug("EthicsEngine: %d scar(s) fully healed after %.1f day(s)", pruned, days_elapsed)
        return pruned

    def _scar_boost(self, taboo_name: str) -> float:
        """Return the highest active scar sensitivity boost for a given taboo."""
        boosts = [
            s.current_sensitivity_boost
            for s in self._scars
            if s.taboo_name == taboo_name and s.current_sensitivity_boost > 0.001
        ]
        return max(boosts) if boosts else 0.0

    # ── Conflict detection (E-10) ─────────────────────────────────────────────

    def _detect_conflicts(
        self, triggered_values: List[str], context: str
    ) -> List[ValueConflict]:
        """Return ValueConflict objects for any opposing high-weight value pairs."""
        triggered_set = set(triggered_values)
        conflicts: List[ValueConflict] = []
        for val_a, val_b, hint in _OPPOSING_VALUE_PAIRS:
            if val_a not in triggered_set or val_b not in triggered_set:
                continue
            w_a = float(self._core_values.get(val_a, {}).get("weight", 0.5))
            w_b = float(self._core_values.get(val_b, {}).get("weight", 0.5))
            if w_a > 0.7 and w_b > 0.7:
                conflicts.append(ValueConflict(
                    value_a=val_a,
                    value_b=val_b,
                    context=context,
                    resolution_hint=hint,
                ))
                logger.info(
                    "EthicsEngine: value conflict detected — %r vs %r in %r",
                    val_a, val_b, context,
                )
        return conflicts

    # ── Internals ─────────────────────────────────────────────────────────────

    def _load_values(self) -> None:
        """Load core_values and taboos from values.json."""
        path = self._data_root / "values.json"
        try:
            with path.open("r", encoding="utf-8") as fh:
                raw: Dict[str, Any] = json.load(fh)
            self._core_values = raw.get("core_values", {})
            self._taboos = raw.get("taboos", {})
            logger.info(
                "EthicsEngine loaded %d values and %d taboos from %s.",
                len(self._core_values), len(self._taboos), path,
            )
        except FileNotFoundError:
            logger.warning("EthicsEngine: values.json not found at %s — using empty tables.", path)
            self._degraded = True
        except (json.JSONDecodeError, KeyError) as exc:
            logger.warning("EthicsEngine: failed to parse values.json: %s", exc)
            self._degraded = True

    def _detect_context(self, lowered_text: str) -> str:
        """Infer conversational context from text content.

        Priority order: crisis > spiritual > technical > quick > casual.
        """
        for ctx in (_CONTEXT_CRISIS, _CONTEXT_SPIRITUAL, _CONTEXT_TECHNICAL):
            triggers = _CONTEXT_TRIGGERS.get(ctx, [])
            if any(kw in lowered_text for kw in triggers):
                return ctx
        # Quick = very short message (under 10 words)
        if len(lowered_text.split()) < 10:
            return _CONTEXT_QUICK
        return _CONTEXT_CASUAL

    def _scan_keywords(self, lowered_text: str, keyword_map: Dict[str, List[str]]) -> List[str]:
        """Return names of entries whose keywords appear in lowered_text."""
        return [
            name
            for name, keywords in keyword_map.items()
            if any(kw in lowered_text for kw in keywords)
        ]

    def _rolling_alignment(self) -> float:
        """Mean of the alignment history window, or 0.5 if no data yet."""
        if not self._alignment_history:
            return 0.5
        return sum(self._alignment_history) / len(self._alignment_history)

    def _build_recommendation(
        self,
        triggered_values: List[str],
        triggered_taboos: List[str],
        context_type: str,
    ) -> str:
        """Compose a brief one-line guidance note for this evaluation."""
        if triggered_taboos:
            taboo_names = ", ".join(triggered_taboos)
            return f"Caution: signals touching {taboo_names} — hold to drengskapr."
        if triggered_values:
            top = triggered_values[0]
            return f"Aligned with {top} — carry it forward with maegen."
        return "Neutral — speak from the soul, not the surface."

    def _build_prompt_hint(
        self,
        alignment: float,
        dominant: Optional[str],
        active_taboos: List[str],
        context_type: str,
    ) -> str:
        """One-line ethical compass summary for prompt injection."""
        parts: List[str] = []

        if alignment >= 0.75:
            parts.append("alignment=strong")
        elif alignment >= 0.5:
            parts.append("alignment=good")
        else:
            parts.append("alignment=drifting")

        if dominant:
            parts.append(f"value={dominant}")

        if active_taboos:
            parts.append(f"caution={','.join(active_taboos)}")

        parts.append(f"tone={context_type}")

        return f"[Ethics: {'; '.join(parts)}]"

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "EthicsEngine":
        """Construct from a config dict.

        Reads keys under ``ethics``:
          data_root         (str, default "data")
          alignment_window  (int, default 20)
        """
        cfg: Dict[str, Any] = config.get("ethics", {})
        return cls(
            data_root=str(cfg.get("data_root", _DEFAULT_DATA_ROOT)),
            alignment_window=int(cfg.get("alignment_window", _DEFAULT_ALIGNMENT_WINDOW)),
        )


# ─── Singleton ────────────────────────────────────────────────────────────────

_ETHICS_ENGINE: Optional[EthicsEngine] = None


def init_ethics_from_config(config: Dict[str, Any]) -> EthicsEngine:
    """Initialise the global EthicsEngine from a config dict.

    Idempotent — returns the existing instance if already initialised.
    """
    global _ETHICS_ENGINE
    if _ETHICS_ENGINE is None:
        _ETHICS_ENGINE = EthicsEngine.from_config(config)
        logger.info("EthicsEngine initialised (degraded=%s).", _ETHICS_ENGINE._degraded)
    return _ETHICS_ENGINE


def get_ethics() -> EthicsEngine:
    """Return the global EthicsEngine.

    Raises RuntimeError if ``init_ethics_from_config()`` has not been called.
    """
    if _ETHICS_ENGINE is None:
        raise RuntimeError(
            "EthicsEngine not initialised — call init_ethics_from_config() first."
        )
    return _ETHICS_ENGINE
