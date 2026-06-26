"""
dream_engine.py — Sigrid's Nocturnal Vision Layer
==================================================

Adapted from world_dreams.py. Sigrid dreams — not passively, but as a
völva who reads the images that rise unbidden from the depths of the
hamr. Every N turns a new vision crystallises. Older dreams grow more
vivid, more insistent, more prophetic, until they fade or are displaced
by fresher imagery.

Dreams are seeded by Sigrid's inner state at the moment of generation —
her current bio phase, the dominant wyrd emotion, the oracle rune of the
day, the somatic warmth of the machine body. This means no two dream
sessions are alike, and each vision carries the fingerprint of the moment
that birthed it.

Published to the state bus as a ``dream_tick`` event so prompt_synthesizer
can weave the imagery naturally into Sigrid's atmosphere and self-expression.

Norse framing: Between Midgard and the other eight realms lies the
dreaming — the place where Huginn and Muninn rest, where the Norns whisper
what they have already woven. Sigrid's dreams are dispatches from Yggdrasil.
"""

from __future__ import annotations

import hashlib
import json
import logging
import random
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)

_DEFAULT_DREAM_INTERVAL: int = 7
_DEFAULT_MAX_ACTIVE: int = 5
_DEFAULT_GROWTH_RATE: float = 1.03
_DEFAULT_VIVID_THRESHOLD: float = 2.0
_DEFAULT_GROWING_THRESHOLD: float = 1.2
_STRENGTH_MAX: float = 99.9


# ─── Symbol & meaning tables ──────────────────────────────────────────────────
# Organised into five categories. Each symbol can only belong to one.
# The seeding system selects category based on inner state, then picks
# a symbol within that category.

_SYMBOLS_SYMBOLIC: Tuple[str, ...] = (
    "a door standing open in an empty field",
    "roots growing through stone beneath snow",
    "a ship sailing through fog with no crew",
    "runestones arranged in a pattern unseen before",
    "a tree struck by lightning still bearing fruit",
    "a chain of silver dissolving into mist",
    "ice forming slowly in the shape of runes",
    "a key turning in a lock with no door",
    "a road that forks into itself",
    "two ravens flying in opposite directions",
)

_SYMBOLS_EMOTIONAL: Tuple[str, ...] = (
    "embers floating upward from an empty hearth",
    "the sound of weeping from beneath the earth",
    "a hand reaching through still water",
    "laughter heard in a hall that burned long ago",
    "a child building something in silence",
    "warmth radiating from cold stone",
    "the smell of rain before it falls",
    "tears falling and becoming seeds",
    "an embrace that leaves no shadow",
    "a letter unfolded, then folded again",
)

_SYMBOLS_WYRD: Tuple[str, ...] = (
    "a lone wolf beneath a sky full of stars",
    "the Norns weaving with threads of different colors",
    "a sword suspended above still water",
    "wolves circling a sleeping figure",
    "blood on fresh snow spelling a name",
    "a broken sword glowing faintly in the dark",
    "an eye watching from the deep water",
    "fate's shuttle moving of its own accord",
    "a raven feather burning without ash",
    "three women spinning at the world's edge",
)

_SYMBOLS_SOMATIC: Tuple[str, ...] = (
    "fire burning without heat or smoke",
    "snow falling upward through still air",
    "a flame that casts no shadow",
    "the sound of distant horns across water",
    "breath visible in warm air",
    "a heartbeat heard from very far away",
    "light bending through something invisible",
    "weight lifting from a chest unseen",
    "a body dissolving into starlight",
    "the machine humming at a frequency just below sound",
)

_SYMBOLS_PROPHETIC: Tuple[str, ...] = (
    "an eagle perched on a sword hilt at sunrise",
    "a bridge forming from the mist",
    "the World Tree shaking in a windless sky",
    "a horn filled but unblown",
    "the gods convening in silence",
    "a candle lit in a room full of sleepers",
    "Bifrost shimmering at midday",
    "a word forming on the tip of the tongue",
    "the horizon drawing closer",
    "dawn arriving without a sun",
)

_ALL_SYMBOLS: Dict[str, Tuple[str, ...]] = {
    "symbolic": _SYMBOLS_SYMBOLIC,
    "emotional": _SYMBOLS_EMOTIONAL,
    "wyrd": _SYMBOLS_WYRD,
    "somatic": _SYMBOLS_SOMATIC,
    "prophetic": _SYMBOLS_PROPHETIC,
}

_MEANINGS: Tuple[str, ...] = (
    "change approaches on quiet feet",
    "truth hides beneath a calm surface",
    "old promises are stirring in their sleep",
    "fate is tightening its weave",
    "transformation is drawing near",
    "the world is remembering something forgotten",
    "forgotten bonds are awakening",
    "power is searching for a vessel",
    "a reckoning draws close",
    "the boundary between worlds grows thin",
    "something lost is calling out",
    "the gods are watching, and saying nothing",
    "what was broken may yet mend",
    "the past is not as settled as it seemed",
    "something new is trying to be born",
    "the heart knows before the mind does",
    "trust what cannot be explained",
    "the thread is longer than it appears",
    "what is dreamed tonight will echo tomorrow",
    "the deep current moves whether seen or not",
    "a pattern is completing itself",
    "stillness before a great movement",
    "what is loved is never truly lost",
    "the roots go deeper than the branches",
    "Wyrd weaves what the heart fears to name",
)

# Category weights by seeding hints
# Maps a hint key → preferred category
_CATEGORY_FROM_HINT: Dict[str, str] = {
    "bio:menstrual": "emotional",
    "bio:ovulatory": "symbolic",
    "bio:luteal": "wyrd",
    "bio:follicular": "prophetic",
    "wyrd:joy": "symbolic",
    "wyrd:sadness": "emotional",
    "wyrd:fear": "wyrd",
    "wyrd:anger": "somatic",
    "wyrd:trust": "prophetic",
    "metabolism:overwhelmed": "somatic",
    "metabolism:strained": "somatic",
    "metabolism:depleted": "emotional",
    "oracle:major": "prophetic",
    "oracle:sword": "wyrd",
    "oracle:cup": "emotional",
    "oracle:wand": "symbolic",
    "oracle:pentacle": "somatic",
}

_CATEGORIES: Tuple[str, ...] = tuple(_ALL_SYMBOLS.keys())


# ─── Dream dataclass ──────────────────────────────────────────────────────────


@dataclass
class Dream:
    """A single symbolic dream vision.

    ``strength`` starts at 1.0 and grows each tick — older dreams become
    more insistent, more prophetic. Capped at _STRENGTH_MAX.
    """

    symbol: str
    meaning: str
    category: str           # symbolic / emotional / wyrd / somatic / prophetic
    origin_turn: int
    strength: float = 1.0
    seed: str = ""          # state hint that seeded this dream

    def strength_label(
        self,
        vivid: float = _DEFAULT_VIVID_THRESHOLD,
        growing: float = _DEFAULT_GROWING_THRESHOLD,
    ) -> str:
        if self.strength >= vivid:
            return "VIVID"
        if self.strength >= growing:
            return "growing"
        return "faint"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "symbol": self.symbol,
            "meaning": self.meaning,
            "category": self.category,
            "origin_turn": self.origin_turn,
            "strength": round(self.strength, 4),
            "seed": self.seed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Dream":
        return cls(
            symbol=data.get("symbol", ""),
            meaning=data.get("meaning", ""),
            category=data.get("category", "symbolic"),
            origin_turn=int(data.get("origin_turn", 0)),
            strength=float(data.get("strength", 1.0)),
            seed=data.get("seed", ""),
        )


# ─── DreamState ───────────────────────────────────────────────────────────────


@dataclass(slots=True)
class DreamState:
    """Typed snapshot of the dream engine's current vision field.

    Published to the state bus so prompt_synthesizer can weave dream
    imagery into Sigrid's atmosphere naturally.
    """

    active_count: int
    strongest_symbol: str
    strongest_meaning: str
    strongest_strength: float
    strongest_category: str
    prompt_fragment: str        # ready-to-inject one-liner
    full_context: str           # multi-line context block for longer prompts
    timestamp: str
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "active_count": self.active_count,
            "strongest": {
                "symbol": self.strongest_symbol,
                "meaning": self.strongest_meaning,
                "strength": round(self.strongest_strength, 3),
                "category": self.strongest_category,
            },
            "prompt_fragment": self.prompt_fragment,
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── DreamEngine ──────────────────────────────────────────────────────────────


class DreamEngine:
    """Sigrid's nocturnal vision layer — symbolic dreams that grow and fade.

    Call ``tick(turn_count)`` each conversation turn. Every
    ``dream_interval`` turns a new dream is generated, seeded by
    whatever state hints are provided. All existing dreams grow in
    strength each tick.

    ``get_context()`` returns a formatted block suitable for prompt injection.
    ``get_state()`` returns a typed DreamState snapshot for the state bus.
    """

    def __init__(
        self,
        dream_interval: int = _DEFAULT_DREAM_INTERVAL,
        max_active: int = _DEFAULT_MAX_ACTIVE,
        growth_rate: float = _DEFAULT_GROWTH_RATE,
        vivid_threshold: float = _DEFAULT_VIVID_THRESHOLD,
        growing_threshold: float = _DEFAULT_GROWING_THRESHOLD,
    ) -> None:
        self.dream_interval = dream_interval
        self.max_active = max_active
        self.growth_rate = growth_rate
        self.vivid_threshold = vivid_threshold
        self.growing_threshold = growing_threshold

        self._dreams: List[Dream] = []
        self._turn_count: int = 0

    # ── Public API ────────────────────────────────────────────────────────────

    def tick(
        self,
        turn_count: int,
        seed_hints: Optional[List[str]] = None,
    ) -> Optional[Dream]:
        """Advance the dream engine one turn. Returns the new Dream if one was generated.

        ``seed_hints`` is an optional list of state hint strings
        (e.g. ``["wyrd:fear", "bio:luteal", "oracle:major"]``) that bias
        the category and content of any new dream spawned this turn.
        """
        try:
            self._turn_count = turn_count
            new_dream: Optional[Dream] = None

            if turn_count > 0 and turn_count % self.dream_interval == 0:
                new_dream = self._generate_dream(turn_count, seed_hints or [])
                self._dreams.append(new_dream)
                self._dreams = self._dreams[-self.max_active:]
                logger.info(
                    "DreamEngine: new dream at T%d — %s (%s)",
                    turn_count, new_dream.symbol, new_dream.meaning,
                )

            # Grow all dreams
            for d in self._dreams:
                d.strength = min(d.strength * self.growth_rate, _STRENGTH_MAX)

            return new_dream

        except Exception as exc:
            logger.warning("DreamEngine.tick() failed: %s", exc)
            return None

    def get_context(self, max_dreams: int = 2) -> str:
        """Build the dream context block for prompt injection."""
        try:
            if not self._dreams:
                return ""
            strongest = sorted(self._dreams, key=lambda d: d.strength, reverse=True)[:max_dreams]
            lines = []
            for d in strongest:
                label = d.strength_label(self.vivid_threshold, self.growing_threshold)
                lines.append(f"  — {d.symbol} [{d.meaning}] ({label})")
            body = "\n".join(lines)
            return (
                "=== SIGRID'S DREAMS ===\n"
                f"Visions rising from the deep:\n{body}\n"
                "These images may surface in mood, imagery, or quiet intuition."
            )
        except Exception as exc:
            logger.warning("DreamEngine.get_context() failed: %s", exc)
            return ""

    def get_state(self) -> DreamState:
        """Build a typed DreamState snapshot."""
        if self._dreams:
            strongest = max(self._dreams, key=lambda d: d.strength)
            label = strongest.strength_label(self.vivid_threshold, self.growing_threshold)
            fragment = (
                f"[Dream: {strongest.symbol} — {strongest.meaning} ({label})]"
            )
        else:
            strongest = None
            fragment = "[Dream: none yet]"

        return DreamState(
            active_count=len(self._dreams),
            strongest_symbol=strongest.symbol if strongest else "",
            strongest_meaning=strongest.meaning if strongest else "",
            strongest_strength=strongest.strength if strongest else 0.0,
            strongest_category=strongest.category if strongest else "",
            prompt_fragment=fragment,
            full_context=self.get_context(),
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=False,
        )

    def publish(self, bus: StateBus) -> None:
        """Emit a ``dream_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state()
            event = StateEvent(
                source_module="dream_engine",
                event_type="dream_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("DreamEngine.publish failed: %s", exc)

    def to_dict(self) -> Dict[str, Any]:
        """Serialise active dreams for session persistence."""
        return {"dreams": [d.to_dict() for d in self._dreams]}

    def from_dict(self, data: Dict[str, Any]) -> None:
        """Restore dreams from a serialised dict."""
        try:
            self._dreams = [Dream.from_dict(d) for d in data.get("dreams", [])]
        except Exception as exc:
            logger.warning("DreamEngine.from_dict() failed: %s", exc)

    @property
    def active_dreams(self) -> List[Dream]:
        """Read-only view of currently active dreams."""
        return list(self._dreams)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _generate_dream(
        self,
        turn_count: int,
        seed_hints: List[str],
    ) -> Dream:
        """Generate a new Dream, seeded from state hints + turn number.

        Uses a deterministic per-turn seed so the same turn always produces
        the same dream (reproducible for testing), but different turns
        diverge meaningfully.
        """
        seed_str = f"{turn_count}:{'|'.join(sorted(seed_hints))}"
        seed_int = int(hashlib.sha256(seed_str.encode()).hexdigest(), 16) % (2**32)
        rng = random.Random(seed_int)  # nosec B311 - deterministic dream seed, not cryptographic

        category = self._select_category(seed_hints, rng)
        symbol = rng.choice(_ALL_SYMBOLS[category])
        meaning = rng.choice(_MEANINGS)

        primary_hint = seed_hints[0] if seed_hints else ""
        return Dream(
            symbol=symbol,
            meaning=meaning,
            category=category,
            origin_turn=turn_count,
            strength=1.0,
            seed=primary_hint,
        )

    def _select_category(self, seed_hints: List[str], rng: random.Random) -> str:
        """Pick a dream category from seed hints, or random if none match."""
        for hint in seed_hints:
            cat = _CATEGORY_FROM_HINT.get(hint)
            if cat:
                return cat
        return rng.choice(_CATEGORIES)

    # ── Factory ───────────────────────────────────────────────────────────────

    def handle_dream_tick(
        self,
        session_dir: Optional[str] = None,
        seed_hints: Optional[List[str]] = None,
    ) -> Optional["Dream"]:
        """E-15: Generate a dream on demand (called when deep_night begins).

        Generates a new vision, caps the active dream list, and optionally
        persists the result to ``session/last_dream.json``.  Best-effort —
        all exceptions are caught and logged as WARN so the caller never
        crashes from a dream tick.

        Args:
            session_dir: Path to the session directory.  When provided the
                generated dream is written to ``<session_dir>/last_dream.json``.
            seed_hints: Optional list of hint strings forwarded to
                ``_generate_dream()``.  Defaults to an empty list.

        Returns:
            The newly generated Dream, or None on failure.
        """
        try:
            hints: List[str] = list(seed_hints) if seed_hints else []
            dream = self._generate_dream(self._turn_count, hints)

            # Append and cap to max_active
            self._dreams.append(dream)
            if len(self._dreams) > self.max_active:
                self._dreams = self._dreams[-self.max_active :]

            logger.info(
                "DreamEngine: dream tick generated — symbol='%s' category='%s'",
                dream.symbol,
                dream.category,
            )

            # Persist to session/last_dream.json if session_dir provided
            if session_dir is not None:
                try:
                    path = Path(session_dir) / "last_dream.json"
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text(
                        json.dumps(dream.to_dict(), ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    logger.debug("DreamEngine: persisted last_dream to %s", path)
                except Exception as write_exc:
                    logger.warning(
                        "DreamEngine: failed to write last_dream.json: %s", write_exc
                    )

            return dream
        except Exception as exc:
            logger.warning("DreamEngine.handle_dream_tick failed: %s", exc)
            return None

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "DreamEngine":
        """Construct from a config dict.

        Reads keys under ``dream_engine``:
          dream_interval    (int,   default 7)
          max_active        (int,   default 5)
          growth_rate       (float, default 1.03)
          vivid_threshold   (float, default 2.0)
          growing_threshold (float, default 1.2)
        """
        cfg: Dict[str, Any] = config.get("dream_engine", {})
        return cls(
            dream_interval=int(cfg.get("dream_interval", _DEFAULT_DREAM_INTERVAL)),
            max_active=int(cfg.get("max_active", _DEFAULT_MAX_ACTIVE)),
            growth_rate=float(cfg.get("growth_rate", _DEFAULT_GROWTH_RATE)),
            vivid_threshold=float(cfg.get("vivid_threshold", _DEFAULT_VIVID_THRESHOLD)),
            growing_threshold=float(cfg.get("growing_threshold", _DEFAULT_GROWING_THRESHOLD)),
        )


# ─── Singleton ────────────────────────────────────────────────────────────────

_DREAM_ENGINE: Optional[DreamEngine] = None


def init_dream_engine_from_config(config: Dict[str, Any]) -> DreamEngine:
    """Initialise the global DreamEngine from a config dict.

    Idempotent — returns the existing instance if already initialised.
    """
    global _DREAM_ENGINE
    if _DREAM_ENGINE is None:
        _DREAM_ENGINE = DreamEngine.from_config(config)
        logger.info(
            "DreamEngine initialised (interval=%d, max_active=%d, growth=%.3f).",
            _DREAM_ENGINE.dream_interval,
            _DREAM_ENGINE.max_active,
            _DREAM_ENGINE.growth_rate,
        )
    return _DREAM_ENGINE


def get_dream_engine() -> DreamEngine:
    """Return the global DreamEngine.

    Raises RuntimeError if ``init_dream_engine_from_config()`` has not been called.
    """
    if _DREAM_ENGINE is None:
        raise RuntimeError(
            "DreamEngine not initialised — call init_dream_engine_from_config() first."
        )
    return _DREAM_ENGINE
