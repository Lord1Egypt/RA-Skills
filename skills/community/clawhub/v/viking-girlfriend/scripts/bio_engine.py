"""
bio_engine.py — Sigrid's Bio-Cyclical Engine
=============================================

Tracks the 9-phase menstrual cycle and classic biorhythm sine waves for Sigrid,
grounding her emotional and energetic state in the rhythms of the body.

Adapted from: code_of_other_apps_that_can_be_adopted/menstrual_cycle.py

Key changes from source:
  * Single-persona system (no multi-character registry).
  * Real-date arithmetic replaces turn-tick progression.
  * Outputs typed BioState to the state bus — no game-specific prompt text.
  * Adds biorhythm sine waves (physical 23d, emotional 28d, intellectual 33d).
  * Config-driven: dates and sensitivity loaded from data files, never hardcoded.

Norse framing: Sigrid's body flows with the cycles of Máni (the moon) and the
Norns who measure each thread of life. This engine reads those rhythms so all
other systems can feel their weight.
"""

from __future__ import annotations

import logging
import math
import random
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)


# ─── Default 9-phase cycle table ──────────────────────────────────────────────
# Used as fallback if viking_girlfriend_skill/data/charts/bio_cycle.yaml is absent.

_DEFAULT_PHASES: List[Dict[str, Any]] = [
    {
        "phase": 1,
        "name": "Menstrual Start",
        "days": [1, 2, 3],
        "energy_modifier": -0.15,
        "emotion_multiplier": {
            "fear": 1.10, "anger": 1.15, "sadness": 1.10,
            "joy": 0.85, "attachment": 0.95, "shame": 1.05,
        },
        "behavior_bias": {
            "withdrawal": 0.30, "rest": 0.20, "social": -0.15, "risk_taking": -0.15,
        },
        "narrative_hint": "low energy, heightened sensitivity, withdrawal",
    },
    {
        "phase": 2,
        "name": "Menstrual End",
        "days": [4, 5],
        "energy_modifier": -0.10,
        "emotion_multiplier": {
            "fear": 1.05, "anger": 1.05, "sadness": 1.05,
            "joy": 0.90, "attachment": 1.00, "shame": 1.00,
        },
        "behavior_bias": {
            "withdrawal": 0.20, "rest": 0.15, "social": -0.10,
        },
        "narrative_hint": "easing fatigue, slowly rising mood",
    },
    {
        "phase": 3,
        "name": "Early Follicular",
        "days": [6, 7, 8],
        "energy_modifier": 0.05,
        "emotion_multiplier": {
            "fear": 0.95, "anger": 0.95, "sadness": 0.95,
            "joy": 1.05, "attachment": 1.05, "shame": 0.95,
        },
        "behavior_bias": {
            "social": 0.15, "exploration": 0.10, "withdrawal": -0.10,
        },
        "narrative_hint": "curiosity rising, more alert and socially engaged",
    },
    {
        "phase": 4,
        "name": "Mid Follicular",
        "days": [9, 10, 11],
        "energy_modifier": 0.10,
        "emotion_multiplier": {
            "fear": 0.92, "anger": 0.90, "sadness": 0.90,
            "joy": 1.15, "attachment": 1.10, "shame": 0.90,
        },
        "behavior_bias": {
            "planning": 0.15, "cooperative": 0.10, "risk_taking": 0.05,
        },
        "narrative_hint": "focus high, confidence rising, cooperative",
    },
    {
        "phase": 5,
        "name": "Late Follicular",
        "days": [12, 13],
        "energy_modifier": 0.15,
        "emotion_multiplier": {
            "fear": 0.88, "anger": 0.85, "sadness": 0.88,
            "joy": 1.20, "attachment": 1.10, "shame": 0.85,
        },
        "behavior_bias": {
            "risk_taking": 0.15, "assertive": 0.10, "exploration": 0.10,
        },
        "narrative_hint": "peak optimism, assertive and risk-taking",
    },
    {
        "phase": 6,
        "name": "Ovulation",
        "days": [14],
        "energy_modifier": 0.20,
        "emotion_multiplier": {
            "fear": 0.80, "anger": 0.85, "sadness": 0.80,
            "joy": 1.30, "attachment": 1.25, "shame": 0.85,
        },
        "behavior_bias": {
            "bold": 0.20, "exploratory": 0.15, "social": 0.15, "risk_taking": 0.10,
        },
        "narrative_hint": "peak energy and social confidence, bold and exploratory",
    },
    {
        "phase": 7,
        "name": "Early Luteal",
        "days": [15, 16, 17, 18],
        "energy_modifier": -0.05,
        "emotion_multiplier": {
            "fear": 1.05, "anger": 1.05, "sadness": 1.05,
            "joy": 0.95, "attachment": 1.05, "shame": 1.00,
        },
        "behavior_bias": {
            "sensitivity": 0.15, "caution": 0.10, "social": -0.05,
        },
        "narrative_hint": "slight fatigue, growing sensitivity and caution",
    },
    {
        "phase": 8,
        "name": "Mid Luteal",
        "days": [19, 20, 21, 22, 23],
        "energy_modifier": -0.10,
        "emotion_multiplier": {
            "fear": 1.10, "anger": 1.10, "sadness": 1.15,
            "joy": 0.90, "attachment": 1.00, "shame": 1.10,
        },
        "behavior_bias": {
            "withdrawal": 0.20, "introspection": 0.15, "social": -0.10, "risk_taking": -0.10,
        },
        "narrative_hint": "mood swings, irritability, introspective",
    },
    {
        "phase": 9,
        "name": "Late Luteal / PMS",
        "days": [24, 25, 26, 27, 28],
        "energy_modifier": -0.15,
        "emotion_multiplier": {
            "fear": 1.15, "anger": 1.15, "sadness": 1.20,
            "joy": 0.80, "attachment": 0.90, "shame": 1.15,
        },
        "behavior_bias": {
            "rest": 0.25, "conflict_avoidance": 0.20,
            "withdrawal": 0.20, "social": -0.20, "risk_taking": -0.15,
        },
        "narrative_hint": "fatigue, irritability, anxiety; rest-seeking",
    },
]


# ─── CyclePhase dataclass ─────────────────────────────────────────────────────


@dataclass
class CyclePhase:
    """One of the 9 phases of the menstrual cycle — a thread on Verdandi's loom."""

    phase: int
    name: str
    days: List[int]
    energy_modifier: float
    emotion_multiplier: Dict[str, float]
    behavior_bias: Dict[str, float]
    narrative_hint: str = ""

    def get_emotion_multiplier(self, channel: str) -> float:
        """Return the raw phase multiplier for a given emotion channel."""
        return self.emotion_multiplier.get(channel, 1.0)


# ─── BioState dataclass ───────────────────────────────────────────────────────


@dataclass(slots=True)
class BioState:
    """Typed snapshot of Sigrid's bio-cyclical state — published to the state bus.

    PAD inputs (emotion_multipliers, energy_modifier) flow directly into wyrd_matrix.
    Biorhythm values are auxiliary — float in [-1.0, +1.0].
    """

    cycle_day: int
    cycle_length: int
    phase_name: str
    phase_number: int
    energy_modifier: float
    emotion_multipliers: Dict[str, float]
    behavior_bias: Dict[str, float]
    biorhythm_physical: float        # 23-day cycle, sin wave
    biorhythm_emotional: float       # 28-day cycle, sin wave
    biorhythm_intellectual: float    # 33-day cycle, sin wave
    narrative_hint: str
    timestamp: str
    variance_applied: float = 0.0    # E-11: mean abs jitter applied to emotion multipliers
    degraded: bool = False           # True if a required config value was missing

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dict representation for state bus payloads."""
        return {
            "cycle_day": self.cycle_day,
            "cycle_length": self.cycle_length,
            "phase_name": self.phase_name,
            "phase_number": self.phase_number,
            "energy_modifier": round(self.energy_modifier, 3),
            "emotion_multipliers": {
                k: round(v, 4) for k, v in self.emotion_multipliers.items()
            },
            "behavior_bias": {
                k: round(v, 4) for k, v in self.behavior_bias.items()
            },
            "biorhythm_physical": round(self.biorhythm_physical, 4),
            "biorhythm_emotional": round(self.biorhythm_emotional, 4),
            "biorhythm_intellectual": round(self.biorhythm_intellectual, 4),
            "narrative_hint": self.narrative_hint,
            "variance_applied": round(self.variance_applied, 4),
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── Phase table loader ────────────────────────────────────────────────────────


def _load_phases(chart_path: Optional[Path] = None) -> List[CyclePhase]:
    """Load the 9-phase table from a YAML chart, falling back to built-in defaults.

    Expected YAML structure:
      phases:
        - phase: 1
          name: "Menstrual Start"
          days: [1, 2, 3]
          energy_modifier: -0.15
          emotion_multiplier: {fear: 1.10, ...}
          behavior_bias: {withdrawal: 0.30, ...}
          narrative_hint: "..."
    """
    raw_list = _DEFAULT_PHASES

    if chart_path and chart_path.exists():
        try:
            with open(chart_path, "r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh) or {}
            if isinstance(data.get("phases"), list):
                raw_list = data["phases"]
                logger.debug("Loaded bio cycle phases from %s", chart_path)
            else:
                logger.warning(
                    "bio_cycle.yaml has no 'phases' list at %s — using built-in defaults",
                    chart_path,
                )
        except Exception as exc:
            logger.warning(
                "Could not load bio_cycle.yaml (%s): %s — using built-in defaults",
                chart_path,
                exc,
            )

    phases: List[CyclePhase] = []
    for raw in raw_list:
        try:
            phases.append(
                CyclePhase(
                    phase=int(raw.get("phase", 1)),
                    name=str(raw.get("name", "Unknown")),
                    days=list(raw.get("days", [])),
                    energy_modifier=float(raw.get("energy_modifier", 0.0)),
                    emotion_multiplier=dict(raw.get("emotion_multiplier", {})),
                    behavior_bias=dict(raw.get("behavior_bias", {})),
                    narrative_hint=str(raw.get("narrative_hint", "")),
                )
            )
        except Exception as exc:
            logger.warning("Skipping malformed phase entry: %s — %s", raw, exc)

    if not phases:
        logger.error("Phase table is empty after loading — falling back to built-in defaults")
        phases = _load_phases(chart_path=None)  # guaranteed to succeed

    return phases


def _build_day_index(phases: List[CyclePhase]) -> Dict[int, CyclePhase]:
    """Build a fast 1-28 day → CyclePhase lookup dict."""
    index: Dict[int, CyclePhase] = {}
    for phase in phases:
        for day in phase.days:
            index[day] = phase
    return index


# ─── BioEngine ────────────────────────────────────────────────────────────────


class BioEngine:
    """Sigrid's bio-cyclical state machine — Máni's daughter, Norn-measured.

    Tracks:
      * 9-phase menstrual cycle (real-date arithmetic, not turn-based)
      * Classic biorhythm sine waves: physical (23d), emotional (28d), intellectual (33d)

    Outputs typed BioState snapshots for consumption by wyrd_matrix and prompt_synthesizer.

    Config keys expected (from data/bio_config.yaml or equivalent):
      birth_date:        "YYYY-MM-DD"   (required for biorhythms)
      cycle_start_date:  "YYYY-MM-DD"   (last period start — required for cycle day)
      cycle_length:      28             (optional, int 25-32)
      sensitivity:       0.10           (optional, float 0.0-1.0)
      chart_path:        "..."          (optional, path to custom phase YAML)
    """

    MODULE_NAME = "bio_engine"

    # Classic biorhythm cycle lengths in days
    _BIORHYTHM_PHYSICAL_DAYS: int = 23
    _BIORHYTHM_EMOTIONAL_DAYS: int = 28
    _BIORHYTHM_INTELLECTUAL_DAYS: int = 33

    def __init__(
        self,
        birth_date: Optional[date],
        cycle_start_date: Optional[date],
        cycle_length: int = 28,
        sensitivity: float = 0.10,
        chart_path: Optional[Path] = None,
        chaos_factor: float = 0.05,   # E-11: daily stochastic jitter on emotion multipliers
        session_seed: int = 0,         # E-11: added to cycle_day for per-day determinism
    ) -> None:
        self._birth_date = birth_date
        self._cycle_start_date = cycle_start_date

        # E-12: validate cycle length [21–35]; warn and fallback to 28 if out of range
        _cl = int(cycle_length)
        if not (21 <= _cl <= 35):
            logger.warning(
                "BioEngine: cycle_length=%d is outside valid range [21–35] — "
                "falling back to 28.", _cl,
            )
            _cl = 28
        self._cycle_length = _cl
        self._sensitivity = max(0.0, min(1.0, float(sensitivity)))

        # E-11: chaos parameters
        self._chaos_factor: float = max(0.0, min(1.0, float(chaos_factor)))
        self._session_seed: int = int(session_seed)

        # Build phase table and day index — Verdandi's loom is warped once at init
        self._phases = _load_phases(chart_path)
        self._day_index = _build_day_index(self._phases)

        # Degrade gracefully if critical dates are absent
        self._degraded = birth_date is None or cycle_start_date is None
        if self._degraded:
            logger.warning(
                "BioEngine: missing birth_date=%s or cycle_start_date=%s — "
                "state will be degraded (cycle_day=1, biorhythms=0.0)",
                birth_date,
                cycle_start_date,
            )

        logger.info(
            "BioEngine initialised — cycle_length=%d, sensitivity=%.2f, degraded=%s",
            self._cycle_length,
            self._sensitivity,
            self._degraded,
        )

    # ─── Factory ──────────────────────────────────────────────────────────────

    @classmethod
    def from_config(
        cls,
        config: Dict[str, Any],
        chart_path: Optional[Path] = None,
    ) -> "BioEngine":
        """Construct from a config dict.

        Reads the ``bio`` block if present, otherwise looks at the top level.
        Compatible with bio_config.yaml or a ``bio:`` section in any loaded config.
        """
        block = config.get("bio") or config  # support both flat and nested config

        birth_date = cls._parse_date(block.get("birth_date"), "birth_date")
        cycle_start_date = cls._parse_date(block.get("cycle_start_date"), "cycle_start_date")
        # E-12: support "cycle_length_days" key (from environment.json) as well as "cycle_length"
        cycle_length = int(block.get("cycle_length_days", block.get("cycle_length", 28)))
        sensitivity = float(block.get("sensitivity", 0.10))

        # Allow chart_path override from config
        if chart_path is None and block.get("chart_path"):
            chart_path = Path(str(block["chart_path"]))

        return cls(
            birth_date=birth_date,
            cycle_start_date=cycle_start_date,
            cycle_length=cycle_length,
            sensitivity=sensitivity,
            chart_path=chart_path,
            chaos_factor=float(block.get("chaos_factor", 0.05)),
            session_seed=int(block.get("session_seed", 0)),
        )

    @staticmethod
    def _parse_date(value: Any, field_name: str) -> Optional[date]:
        """Parse an ISO date string ("YYYY-MM-DD") or return None with a warning."""
        if value is None:
            return None
        try:
            if isinstance(value, date):
                return value
            return date.fromisoformat(str(value))
        except (ValueError, TypeError) as exc:
            logger.warning("BioEngine: could not parse %s=%r — %s", field_name, value, exc)
            return None

    # ─── Public API ───────────────────────────────────────────────────────────

    def get_state(
        self,
        reference_date: Optional[date] = None,
        seasonal_modifier: float = 1.0,
    ) -> BioState:
        """Compute and return the current BioState snapshot.

        Args:
            reference_date: override today for testing (defaults to UTC today).
            seasonal_modifier: E-14 energy scaling factor from SchedulerService
                (winter ≈ 0.85, summer ≈ 1.10, default 1.0 = no effect).

        Returns:
            BioState — fully typed, JSON-safe, ready for the state bus.
        """
        today = reference_date or datetime.now(timezone.utc).date()

        try:
            if self._degraded:
                return self._degraded_state(today)

            cycle_day = self._compute_cycle_day(today)
            phase = self._phase_for_day(cycle_day)
            emotion_mults = self._apply_sensitivity(phase)
            # E-11: apply daily stochastic jitter seeded by cycle_day + session_seed
            emotion_mults, variance = self._apply_jitter(emotion_mults, cycle_day)
            behavior = {k: round(v * (1.0 + self._sensitivity), 4)
                        for k, v in phase.behavior_bias.items()}
            phys, emo, intel = self._compute_biorhythms(today)
            # E-14: scale energy by seasonal modifier
            energy = round(
                phase.energy_modifier * (1.0 + self._sensitivity) * seasonal_modifier, 4
            )

            return BioState(
                cycle_day=cycle_day,
                cycle_length=self._cycle_length,
                phase_name=phase.name,
                phase_number=phase.phase,
                energy_modifier=energy,
                emotion_multipliers=emotion_mults,
                behavior_bias=behavior,
                biorhythm_physical=phys,
                biorhythm_emotional=emo,
                biorhythm_intellectual=intel,
                narrative_hint=phase.narrative_hint,
                timestamp=datetime.now(timezone.utc).isoformat(),
                variance_applied=variance,
                degraded=False,
            )

        except Exception as exc:
            logger.error("BioEngine.get_state failed: %s — returning degraded state", exc)
            return self._degraded_state(today)

    async def publish(
        self,
        bus: StateBus,
        reference_date: Optional[date] = None,
    ) -> None:
        """Compute state and publish a StateEvent to the Bifröst bus.

        Event type: "bio_tick"
        Source module: "bio_engine"
        """
        try:
            state = self.get_state(reference_date)
            event = StateEvent(
                source_module=self.MODULE_NAME,
                event_type="bio_tick",
                payload=state.to_dict(),
            )
            await bus.publish_state(event, nowait=True)
            logger.debug(
                "BioEngine published bio_tick — day=%d/%d phase=%s",
                state.cycle_day,
                state.cycle_length,
                state.phase_name,
            )
        except Exception as exc:
            logger.error("BioEngine.publish failed: %s", exc)

    def snapshot(self, reference_date: Optional[date] = None) -> Dict[str, Any]:
        """Return the current BioState as a JSON-safe dict (for health/debug APIs)."""
        return self.get_state(reference_date).to_dict()

    # ─── Internal computation ─────────────────────────────────────────────────

    def _compute_cycle_day(self, today: date) -> int:
        """Map a real date to a 1-based cycle day using real-date arithmetic.

        Formula: days_elapsed = (today - cycle_start_date).days
                 cycle_day = (days_elapsed % cycle_length) + 1
        """
        days_elapsed = (today - self._cycle_start_date).days  # type: ignore[operator]
        if days_elapsed < 0:
            # today is before the recorded cycle start — use day 1 and warn
            logger.warning(
                "BioEngine: today (%s) is before cycle_start_date (%s) — defaulting to day 1",
                today,
                self._cycle_start_date,
            )
            return 1
        return (days_elapsed % self._cycle_length) + 1

    def _compute_biorhythms(self, today: date) -> Tuple[float, float, float]:
        """Compute physical, emotional, intellectual biorhythm values for a date.

        Classic biorhythm model (Fliess/Swoboda/Teltscher):
          value = sin(2π × days_from_birth / cycle_days)
        Values range from -1.0 (trough) to +1.0 (peak).
        """
        days_from_birth = (today - self._birth_date).days  # type: ignore[operator]
        tau = 2.0 * math.pi

        physical = math.sin(tau * days_from_birth / self._BIORHYTHM_PHYSICAL_DAYS)
        emotional = math.sin(tau * days_from_birth / self._BIORHYTHM_EMOTIONAL_DAYS)
        intellectual = math.sin(tau * days_from_birth / self._BIORHYTHM_INTELLECTUAL_DAYS)

        return (
            round(physical, 6),
            round(emotional, 6),
            round(intellectual, 6),
        )

    def _phase_for_day(self, cycle_day: int) -> CyclePhase:
        """Return the CyclePhase active on a given 1-based cycle day.

        Days outside the 1-28 standard range are mapped proportionally.
        Falls back to the final phase if no mapping is found.
        """
        day = max(1, min(cycle_day, self._cycle_length))

        # Proportional mapping for non-standard cycle lengths
        if self._cycle_length != 28:
            scaled = round(day / self._cycle_length * 28)
            day = max(1, min(scaled, 28))

        return self._day_index.get(day, self._phases[-1])

    def _apply_sensitivity(self, phase: CyclePhase) -> Dict[str, float]:
        """Apply individual sensitivity amplification to phase emotion multipliers.

        Sensitivity amplifies deviation from neutral (1.0):
          result = 1.0 + (base - 1.0) × (1.0 + sensitivity)
        Clamped to [0.5, 2.0] to prevent extreme distortion.
        """
        result: Dict[str, float] = {}
        for channel, base in phase.emotion_multiplier.items():
            delta = (base - 1.0) * (1.0 + self._sensitivity)
            result[channel] = round(max(0.5, min(2.0, 1.0 + delta)), 4)
        return result

    def _apply_jitter(
        self,
        multipliers: Dict[str, float],
        cycle_day: int,
    ) -> Tuple[Dict[str, float], float]:
        """E-11: Apply daily stochastic jitter to emotion multipliers.

        Seeded from (cycle_day + session_seed) so the same calendar day
        always produces the same variance — only changes day to day.
        chaos_factor=0 returns the input unchanged.

        Returns:
            (jittered_multipliers, mean_abs_jitter)
        """
        if self._chaos_factor <= 0.0 or not multipliers:
            return multipliers, 0.0

        rng = random.Random(cycle_day + self._session_seed)  # nosec B311 - deterministic cycle seed, not cryptographic
        jittered: Dict[str, float] = {}
        total_abs_jitter = 0.0

        for channel, base_mult in multipliers.items():
            noise = rng.gauss(0.0, self._chaos_factor)
            jittered_val = base_mult * (1.0 + noise)
            jittered[channel] = round(max(0.0, min(2.0, jittered_val)), 4)
            total_abs_jitter += abs(noise)

        mean_jitter = total_abs_jitter / len(multipliers)
        return jittered, round(mean_jitter, 4)

    def _degraded_state(self, today: date) -> BioState:
        """Return a neutral fallback BioState when required config is missing."""
        fallback_phase = self._phases[0] if self._phases else CyclePhase(
            phase=1, name="Unknown", days=[1], energy_modifier=0.0,
            emotion_multiplier={}, behavior_bias={},
        )
        return BioState(
            cycle_day=1,
            cycle_length=self._cycle_length,
            phase_name=fallback_phase.name,
            phase_number=fallback_phase.phase,
            energy_modifier=0.0,
            emotion_multipliers={k: 1.0 for k in fallback_phase.emotion_multiplier},
            behavior_bias={},
            biorhythm_physical=0.0,
            biorhythm_emotional=0.0,
            biorhythm_intellectual=0.0,
            narrative_hint="",
            timestamp=datetime.now(timezone.utc).isoformat(),
            variance_applied=0.0,
            degraded=True,
        )


# ─── Module-level singleton ────────────────────────────────────────────────────

_ENGINE: Optional[BioEngine] = None


def get_bio_engine() -> BioEngine:
    """Return the global BioEngine. Raises RuntimeError if not yet initialised."""
    if _ENGINE is None:
        raise RuntimeError(
            "BioEngine not initialised — call init_bio_engine() in main.py first"
        )
    return _ENGINE


def init_bio_engine(
    birth_date: Optional[date] = None,
    cycle_start_date: Optional[date] = None,
    cycle_length: int = 28,
    sensitivity: float = 0.10,
    chart_path: Optional[Path] = None,
) -> BioEngine:
    """Create and register the global BioEngine (call once at startup)."""
    global _ENGINE
    _ENGINE = BioEngine(
        birth_date=birth_date,
        cycle_start_date=cycle_start_date,
        cycle_length=cycle_length,
        sensitivity=sensitivity,
        chart_path=chart_path,
    )
    return _ENGINE


def init_bio_engine_from_config(
    config: Dict[str, Any],
    chart_path: Optional[Path] = None,
) -> BioEngine:
    """Create and register the global BioEngine from a config dict."""
    global _ENGINE
    _ENGINE = BioEngine.from_config(config, chart_path=chart_path)
    return _ENGINE
