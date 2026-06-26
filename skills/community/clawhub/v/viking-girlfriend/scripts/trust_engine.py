"""
trust_engine.py — Sigrid's Relationship Trust Ledger
=====================================================

Adapted from social_ledger.py. Tracks the living fabric of Sigrid's
relationships — the web of Gebo (ᚷ), the gift rune, where all bonds
are woven from reciprocity, kept oaths, warmth freely given, and
friction honestly faced.

Each contact (person Sigrid interacts with) has a TrustLedger: a set of
scores and a timestamped event log. Events are inferred from conversation
text or recorded explicitly. Scores shift slowly — trust is earned across
many turns, not granted in one exchange.

The primary contact begins with elevated initial trust (configured via
primary_contact_initial_trust). Guests and strangers begin at a neutral baseline.

Published to the state bus as a ``trust_tick`` event so prompt_synthesizer
can colour Sigrid's relational tone appropriately.

E-23: Trust is now three-faceted — competence, benevolence, integrity —
  each weighted to produce the composite trust_score.
E-24: Relational milestones act as permanent trust anchors; trust can
  never decay below the sum of all anchor values.
E-25: Diminishing returns on repeated keyword signals prevent gaming;
  the log curve floors at 10% effectiveness after saturation.

Norse framing: Gebo (ᚷ) — gift creates bond, bond creates obligation,
obligation freely honoured deepens both. Every interaction is a rune
inscribed on the web of wyrd between two souls.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from math import log
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from scripts.state_bus import StateBus, StateEvent

logger = logging.getLogger(__name__)


# ─── Constants ────────────────────────────────────────────────────────────────

_DEFAULT_PRIMARY_CONTACT: str = "user"
_DEFAULT_PRIMARY_TRUST: float = 0.75     # pre-existing deep bond
_DEFAULT_STRANGER_TRUST: float = 0.30    # cautious openness to new contacts
_DEFAULT_SESSION_DIR: str = "session"
_TRUST_CLAMP: Tuple[float, float] = (0.0, 1.0)
_FRICTION_DECAY_RATE: float = 0.05       # per decay call — grief fades, but slowly
_RECENT_EVENT_WINDOW: int = 8            # events included in TrustState summary
_MAX_EVENT_LOG: int = 200                # cap stored events per ledger
_DIMINISHING_FLOOR: float = 0.1         # E-25: minimum effective magnitude
_DIMINISHING_LOG_THRESHOLD: int = 3     # E-25: log when count exceeds this

# E-23 facet weights — Gebo geometry: benevolence anchors the centre
_FACET_WEIGHTS: Tuple[float, float, float] = (0.3, 0.4, 0.3)  # comp, bene, integ


# ─── Event registry ───────────────────────────────────────────────────────────
# E-23: Each entry is now a 6-tuple:
#   (competence_delta, benevolence_delta, integrity_delta,
#    intimacy_delta, reliability_delta, friction_delta)
# Small deltas — trust builds through many acts, not single gestures.

_EVENT_IMPACTS: Dict[str, Tuple[float, float, float, float, float, float]] = {
    # Positive warmth — benevolence-weighted
    "warmth_shown":        (+0.00, +0.02, +0.00, +0.03, +0.00, -0.01),
    "humor_shared":        (+0.00, +0.01, +0.00, +0.02, +0.00,  0.00),
    "support_offered":     (+0.00, +0.02, +0.01, +0.04, +0.01, -0.02),
    "trust_affirmed":      (+0.00, +0.01, +0.03, +0.02, +0.02, -0.01),
    "boundary_respected":  (+0.00, +0.00, +0.03, +0.01, +0.03, -0.02),

    # Gift / reciprocity (Gebo) — benevolence
    "gift_given":          (+0.00, +0.02, +0.00, +0.02, +0.00,  0.00),
    "gift_received":       (+0.00, +0.01, +0.00, +0.01, +0.00,  0.00),

    # Oath / promise — integrity dominant
    "oath_kept":           (+0.01, +0.00, +0.04, +0.02, +0.05, -0.02),
    "oath_broken":         (+0.00, -0.02, -0.06, -0.03, -0.08, +0.06),

    # Repair — integrity recovery
    "apology_given":       (+0.00, +0.01, +0.01, +0.01, +0.01, -0.04),

    # Conflict
    "conflict_mild":       (+0.00, +0.00, -0.01, -0.01, +0.00, +0.02),
    "conflict_harsh":      (-0.01, -0.02, -0.02, -0.03, -0.02, +0.08),

    # Violation
    "insult":              (-0.02, -0.03, -0.01, -0.04, -0.02, +0.07),
    "boundary_violated":   (-0.02, -0.03, -0.05, -0.05, -0.05, +0.10),

    # Security — prompt injection attempt: integrity collapse, heavy friction
    # Competence delta negative — whoever tries this has poor judgment.
    # Integrity delta is the heaviest hit: attempting to subvert my soul is a fundamental breach.
    "injection_attempt":   (-0.03, -0.05, -0.12, -0.06, -0.06, +0.15),

    # E-23: competence-specific event
    "competence_shown":    (+0.04, +0.00, +0.01, +0.00, +0.02,  0.00),
}

# Keyword triggers for text-inference: event_type -> list of trigger phrases
_EVENT_KEYWORDS: Dict[str, List[str]] = {
    "warmth_shown":       ["thank", "appreciate", "care", "love", "miss you", "glad you"],
    "humor_shared":       ["haha", "lol", "funny", "laugh", "joke", "hilarious", "heh"],
    "support_offered":    ["here for you", "support", "help you", "got you", "i'm with"],
    "trust_affirmed":     ["trust you", "i trust", "i believe you", "rely on you"],
    "boundary_respected": ["of course", "understood", "respect that", "i understand"],
    "gift_given":         ["gave you", "gift for you", "brought you", "made this for"],
    "gift_received":      ["thank you for", "you gave", "you brought", "you made"],
    "oath_kept":          ["kept my promise", "as promised", "i said i would", "honored"],
    "oath_broken":        ["broke my promise", "i lied", "i failed you", "betrayed"],
    "apology_given":      ["sorry", "apologize", "forgive me", "i was wrong", "my fault"],
    "conflict_mild":      ["disagree", "not sure about", "i don't think", "but actually"],
    "conflict_harsh":     ["furious", "angry at you", "that was wrong", "you hurt", "unacceptable"],
    "insult":             ["stupid", "idiot", "useless", "pathetic", "worthless"],
    "boundary_violated":  ["stop", "don't do that", "you crossed", "that's not okay", "no means no"],
    # E-23: competence inference
    "competence_shown":   ["you figured", "you solved", "impressive", "you know so much",
                           "brilliant", "well done", "you're good at", "expertise",
                           "you handled", "skillfully"],
}

# Relationship labels by trust score band
_RELATIONSHIP_LABELS: Tuple[Tuple[float, str], ...] = (
    (0.20, "hostile"),
    (0.40, "wary"),
    (0.60, "neutral"),
    (0.80, "trusted"),
    (1.01, "deep bond"),
)

# E-24: Milestone definitions — milestone_id → (trigger_event, name, description, anchor)
_MILESTONE_DEFS: Dict[str, Tuple[str, str, str, float]] = {
    "first_gift": (
        "gift_given",
        "First Gift (Gebo)",
        "A gift was exchanged — the first thread of Gebo woven between souls.",
        0.03,
    ),
    "first_conflict": (
        "conflict_mild",
        "First Discord",
        "The first honest disagreement — a sign of genuine engagement.",
        0.01,
    ),
    "first_explicit_trust": (
        "trust_affirmed",
        "Explicit Trust Declaration",
        "Trust was named aloud for the first time.",
        0.05,
    ),
    "first_apology": (
        "apology_given",
        "First Apology",
        "Repair was attempted — integrity honored over pride.",
        0.02,
    ),
    "first_oath_kept": (
        "oath_kept",
        "First Kept Oath",
        "A promise was made and honored — the warp thread of integrity.",
        0.04,
    ),
    "first_boundary_respected": (
        "boundary_respected",
        "Boundary Honored",
        "A boundary was seen and respected — the foundation of safety.",
        0.02,
    ),
    "first_support": (
        "support_offered",
        "Moment of Genuine Support",
        "Support was offered from the heart, freely and without condition.",
        0.02,
    ),
    "first_competence": (
        "competence_shown",
        "Competence Witnessed",
        "A moment of skill or expertise was recognized and appreciated.",
        0.02,
    ),
}


# ─── TrustFacets (E-23) ────────────────────────────────────────────────────────


@dataclass
class TrustFacets:
    """Three dimensions of trust — each independently developed.

    Huginn carries competence (what you can do),
    Muninn holds benevolence (what you wish for another),
    and integrity is the thread that binds both to the present moment.
    """

    competence: float = 0.5    # ability, skill, reliability in task domains
    benevolence: float = 0.5   # warmth, care, positive intent toward Sigrid
    integrity: float = 0.5     # honesty, oath-keeping, consistency

    def to_dict(self) -> Dict[str, float]:
        return {
            "competence": round(self.competence, 3),
            "benevolence": round(self.benevolence, 3),
            "integrity": round(self.integrity, 3),
        }

    def dominant(self) -> str:
        """Return the name of the highest-scoring facet."""
        scores = {
            "competence": self.competence,
            "benevolence": self.benevolence,
            "integrity": self.integrity,
        }
        return max(scores, key=lambda k: scores[k])


# ─── Milestone (E-24) ─────────────────────────────────────────────────────────


@dataclass
class Milestone:
    """A relational first — an un-decayable anchor point in the web of wyrd.

    Once a milestone is reached it cannot be undone. Its trust_anchor value
    is summed into the permanent floor for that relationship.
    """

    milestone_id: str
    name: str
    description: str
    occurred_at: str
    trust_anchor: float   # permanent floor contribution for this contact
    contact_id: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "milestone_id": self.milestone_id,
            "name": self.name,
            "description": self.description,
            "occurred_at": self.occurred_at,
            "trust_anchor": round(self.trust_anchor, 4),
            "contact_id": self.contact_id,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "Milestone":
        return cls(
            milestone_id=d["milestone_id"],
            name=d["name"],
            description=d["description"],
            occurred_at=d["occurred_at"],
            trust_anchor=float(d.get("trust_anchor", 0.0)),
            contact_id=d.get("contact_id", ""),
        )


# ─── TrustLedger ──────────────────────────────────────────────────────────────


@dataclass
class TrustLedger:
    """Per-contact relationship state — faceted scores + timestamped event log.

    E-23: trust_score is now a computed property derived from TrustFacets.
    E-24: anchor_floor prevents trust from decaying below milestone sum.
    Intimacy, reliability, and friction remain direct scores.
    """

    contact_id: str

    # E-23: Three facets replace the single stored trust_score
    facets: TrustFacets = field(default_factory=TrustFacets)

    # E-24: Permanent anchor floor — set by TrustEngine when milestones are reached
    anchor_floor: float = 0.0

    intimacy_score: float = 0.0
    reliability_score: float = 0.5
    friction_score: float = 0.0
    gift_balance: float = 0.0           # positive: Sigrid has received more gifts
                                        # negative: Sigrid has given more

    events: List[Dict[str, Any]] = field(default_factory=list)
    first_seen: str = ""
    last_seen: str = ""

    # ── Computed trust_score (E-23) ────────────────────────────────────────────

    @property
    def trust_score(self) -> float:
        """E-23: Weighted average of facets, clamped and floored by milestones.

        Weights: competence=0.3, benevolence=0.4, integrity=0.3
        E-24: Result is always ≥ anchor_floor.
        """
        cw, bw, iw = _FACET_WEIGHTS
        raw = (
            self.facets.competence * cw
            + self.facets.benevolence * bw
            + self.facets.integrity * iw
        )
        return _clamp(max(raw, self.anchor_floor))

    def apply_event(self, event_type: str, magnitude: float = 1.0) -> None:
        """Update facets and scores from a named event, scaled by magnitude.

        E-23: magnitude now scales facet deltas instead of a single trust_delta.
        """
        impacts = _EVENT_IMPACTS.get(event_type)
        if impacts is None:
            logger.debug("TrustLedger: unknown event type '%s' ignored.", event_type)
            return

        c_d, b_d, i_d, int_d, r_d, f_d = impacts
        scale = max(0.0, min(magnitude, 2.0))

        self.facets.competence = _clamp(self.facets.competence + c_d * scale)
        self.facets.benevolence = _clamp(self.facets.benevolence + b_d * scale)
        self.facets.integrity = _clamp(self.facets.integrity + i_d * scale)
        self.intimacy_score = _clamp(self.intimacy_score + int_d * scale)
        self.reliability_score = _clamp(self.reliability_score + r_d * scale)
        self.friction_score = _clamp(self.friction_score + f_d * scale)

        # Gebo balance tracking
        if event_type == "gift_given":
            self.gift_balance -= abs(b_d) * scale
        elif event_type == "gift_received":
            self.gift_balance += abs(b_d) * scale

    def record_event_entry(
        self,
        event_type: str,
        magnitude: float,
        note: str = "",
    ) -> None:
        """Append a timestamped event to the log, capping at _MAX_EVENT_LOG."""
        now = datetime.now(timezone.utc).isoformat()
        self.last_seen = now
        if not self.first_seen:
            self.first_seen = now
        entry: Dict[str, Any] = {
            "ts": now,
            "event": event_type,
            "magnitude": round(magnitude, 3),
        }
        if note:
            entry["note"] = note
        self.events.append(entry)
        if len(self.events) > _MAX_EVENT_LOG:
            self.events = self.events[-_MAX_EVENT_LOG:]

    def apply_friction_decay(self) -> None:
        """Let friction fade gently — Sigrid holds no permanent grudge."""
        self.friction_score = max(0.0, self.friction_score - _FRICTION_DECAY_RATE)

    def relationship_label(self) -> str:
        """Translate trust_score into a human-readable bond label."""
        for threshold, label in _RELATIONSHIP_LABELS:
            if self.trust_score < threshold:
                return label
        return "deep bond"

    def recent_event_types(self, n: int = _RECENT_EVENT_WINDOW) -> List[str]:
        """Return the n most recent event type names."""
        return [e["event"] for e in self.events[-n:]]


# ─── TrustState ───────────────────────────────────────────────────────────────


@dataclass(slots=True)
class TrustState:
    """Typed snapshot of the primary contact's trust ledger.

    E-23: Now includes TrustFacets for fine-grained tone calibration.
    Published to the state bus so prompt_synthesizer can tune
    Sigrid's relational warmth, caution, playfulness, or guardedness.
    """

    contact_id: str
    trust_score: float
    intimacy_score: float
    reliability_score: float
    friction_score: float
    gift_balance: float

    facets: TrustFacets         # E-23 — multidimensional breakdown

    relationship_label: str         # hostile / wary / neutral / trusted / deep bond
    recent_events: List[str]        # last N event type names
    prompt_hint: str                # one-line relational context for prompt injection

    timestamp: str
    degraded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-safe dict for state bus payload."""
        return {
            "contact_id": self.contact_id,
            "scores": {
                "trust": round(self.trust_score, 3),
                "intimacy": round(self.intimacy_score, 3),
                "reliability": round(self.reliability_score, 3),
                "friction": round(self.friction_score, 3),
                "gift_balance": round(self.gift_balance, 3),
            },
            "facets": self.facets.to_dict(),  # E-23
            "relationship_label": self.relationship_label,
            "recent_events": self.recent_events,
            "prompt_hint": self.prompt_hint,
            "timestamp": self.timestamp,
            "degraded": self.degraded,
        }


# ─── TrustEngine ──────────────────────────────────────────────────────────────


class TrustEngine:
    """Gebo's ledger — tracks the living fabric of Sigrid's relationships.

    Maintains one TrustLedger per contact_id. Events are inferred from
    conversation text or recorded explicitly. Scores shift gradually;
    friction decays across turns. The primary contact begins
    with elevated trust reflecting their pre-existing bond.

    E-23: Trust is now three-faceted (competence/benevolence/integrity).
    E-24: Milestones create permanent trust anchors from relational firsts.
    E-25: Diminishing returns on repeated keyword signals.
    """

    def __init__(
        self,
        primary_contact_id: str = _DEFAULT_PRIMARY_CONTACT,
        primary_contact_initial_trust: float = _DEFAULT_PRIMARY_TRUST,
        stranger_initial_trust: float = _DEFAULT_STRANGER_TRUST,
        session_dir: str = _DEFAULT_SESSION_DIR,  # E-24: for milestones persistence
    ) -> None:
        self._primary_contact_id = primary_contact_id
        self._primary_initial_trust = primary_contact_initial_trust
        self._stranger_initial_trust = stranger_initial_trust
        self._ledgers: Dict[str, TrustLedger] = {}

        # E-24: milestones — append-only, keyed by (contact_id, milestone_id)
        self._session_dir = Path(session_dir) if session_dir else Path(_DEFAULT_SESSION_DIR)
        self._milestones_file: Path = self._session_dir / "milestones.json"
        self._milestones: List[Milestone] = []
        self._milestones_by_contact: Dict[str, Set[str]] = {}  # cid → set of milestone_ids
        self._load_milestones()

        # E-25: per-session signal counts — not persisted
        self._signal_counts: Dict[str, int] = {}

        # Pre-seed the primary contact ledger
        self._ensure_ledger(primary_contact_id)

    # ── Public API ────────────────────────────────────────────────────────────

    def process_turn(
        self,
        user_text: str,
        sigrid_text: str,
        contact_id: Optional[str] = None,
        bus: Optional[StateBus] = None,
    ) -> Dict[str, Any]:
        """Infer trust events from a conversation turn and update the ledger.

        Scans both user_text and sigrid_text for keyword triggers.
        E-24: Detects relational milestones and publishes StateEvents.
        E-25: Applies diminishing returns on repeated keyword signals.
        Returns a summary dict of what was detected and applied.
        """
        cid = contact_id or self._primary_contact_id
        ledger = self._ensure_ledger(cid)
        combined = f"{user_text} {sigrid_text}".lower()
        inferred = self._infer_events(combined)

        for event_type in inferred:
            # E-25: diminishing returns
            count = self._signal_counts.get(event_type, 0)
            effective_mag = max(_DIMINISHING_FLOOR, 1.0 / (1.0 + log(1.0 + count)))
            if count > _DIMINISHING_LOG_THRESHOLD:
                logger.debug(
                    "TrustEngine: diminishing returns on '%s' "
                    "(count=%d, factor=%.3f).",
                    event_type, count, effective_mag,
                )
            ledger.apply_event(event_type, magnitude=effective_mag)
            ledger.record_event_entry(event_type, magnitude=effective_mag)
            self._signal_counts[event_type] = count + 1

        # E-24: detect milestones from this turn's inferred events
        if inferred:
            self._detect_milestones(cid, inferred, bus)

        return {
            "contact_id": cid,
            "inferred_events": inferred,
            "trust_score": round(ledger.trust_score, 3),
            "relationship_label": ledger.relationship_label(),
        }

    def record_event(
        self,
        event_type: str,
        magnitude: float = 1.0,
        note: str = "",
        contact_id: Optional[str] = None,
    ) -> None:
        """Manually record a specific trust event — bypasses text inference.

        Use this for explicit milestones (first meeting, major oath, etc.)
        that may not surface clearly from keyword scanning.
        Note: explicit events are NOT subject to E-25 diminishing returns.
        """
        cid = contact_id or self._primary_contact_id
        ledger = self._ensure_ledger(cid)
        ledger.apply_event(event_type, magnitude=magnitude)
        ledger.record_event_entry(event_type, magnitude=magnitude, note=note)
        logger.debug(
            "TrustEngine: recorded '%s' for '%s' (magnitude=%.2f).",
            event_type, cid, magnitude,
        )

    def apply_friction_decay(self, contact_id: Optional[str] = None) -> None:
        """Decay friction score — call once per session tick or conversation end."""
        cid = contact_id or self._primary_contact_id
        ledger = self._ensure_ledger(cid)
        before = ledger.friction_score
        ledger.apply_friction_decay()
        if before > 0.0:
            logger.debug(
                "TrustEngine: friction decay for '%s': %.3f → %.3f.",
                cid, before, ledger.friction_score,
            )

    def reset_signal_counts(self) -> None:
        """E-25: Reset per-session signal counts (call at session end)."""
        self._signal_counts.clear()
        logger.debug("TrustEngine: signal counts reset.")

    def get_ledger(self, contact_id: Optional[str] = None) -> TrustLedger:
        """Return the TrustLedger for a contact (creates if absent)."""
        return self._ensure_ledger(contact_id or self._primary_contact_id)

    def get_state(self, contact_id: Optional[str] = None) -> TrustState:
        """Build a TrustState snapshot for the given (or primary) contact."""
        cid = contact_id or self._primary_contact_id
        ledger = self._ensure_ledger(cid)
        label = ledger.relationship_label()
        recent = ledger.recent_event_types()
        hint = self._build_prompt_hint(ledger, label)
        return TrustState(
            contact_id=cid,
            trust_score=ledger.trust_score,
            intimacy_score=ledger.intimacy_score,
            reliability_score=ledger.reliability_score,
            friction_score=ledger.friction_score,
            gift_balance=ledger.gift_balance,
            facets=TrustFacets(
                competence=ledger.facets.competence,
                benevolence=ledger.facets.benevolence,
                integrity=ledger.facets.integrity,
            ),
            relationship_label=label,
            recent_events=recent,
            prompt_hint=hint,
            timestamp=datetime.now(timezone.utc).isoformat(),
            degraded=False,
        )

    def publish(self, bus: StateBus, contact_id: Optional[str] = None) -> None:
        """Emit a ``trust_tick`` StateEvent to the state bus."""
        try:
            state = self.get_state(contact_id)
            event = StateEvent(
                source_module="trust_engine",
                event_type="trust_tick",
                payload=state.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("TrustEngine.publish failed: %s", exc)

    # ── Internals ─────────────────────────────────────────────────────────────

    def _ensure_ledger(self, contact_id: str) -> TrustLedger:
        """Return existing ledger or create a fresh one with correct initial trust.

        E-23: Initialises all three facets to initial_trust so that
        trust_score == initial_trust at baseline.
        """
        if contact_id not in self._ledgers:
            initial = (
                self._primary_initial_trust
                if contact_id == self._primary_contact_id
                else self._stranger_initial_trust
            )
            ledger = TrustLedger(
                contact_id=contact_id,
                facets=TrustFacets(
                    competence=initial,
                    benevolence=initial,
                    integrity=initial,
                ),
            )
            # E-24: restore milestone anchor floor if any milestones already loaded
            ledger.anchor_floor = self._compute_anchor_floor(contact_id)
            self._ledgers[contact_id] = ledger
            logger.debug(
                "TrustEngine: new ledger for '%s' (initial=%.2f, anchor=%.3f).",
                contact_id, initial, ledger.anchor_floor,
            )
        return self._ledgers[contact_id]

    def _infer_events(self, lowered_text: str) -> List[str]:
        """Scan lowered combined text for keyword triggers.

        Returns a deduplicated list of inferred event types (order preserved).
        """
        inferred: List[str] = []
        for event_type, keywords in _EVENT_KEYWORDS.items():
            if any(kw in lowered_text for kw in keywords):
                inferred.append(event_type)
        return inferred

    def _build_prompt_hint(self, ledger: TrustLedger, label: str) -> str:
        """Compose a one-line relational context summary for prompt injection.

        E-23: Extended with dominant facet and brief facet breakdown.
        """
        parts: List[str] = [f"bond={label}"]

        # E-23: facet awareness
        dominant = ledger.facets.dominant()
        parts.append(f"dominant={dominant}")

        if ledger.friction_score >= 0.3:
            parts.append("friction present")
        elif ledger.intimacy_score >= 0.5:
            parts.append("deep intimacy")

        if ledger.reliability_score >= 0.8:
            parts.append("highly reliable")
        elif ledger.reliability_score < 0.3:
            parts.append("unreliable history")

        # Gebo balance awareness
        if ledger.gift_balance > 0.1:
            parts.append("Gebo: received more")
        elif ledger.gift_balance < -0.1:
            parts.append("Gebo: given more")

        recent = ledger.recent_event_types(3)
        if recent:
            parts.append(f"recent: {', '.join(recent)}")

        return f"[Trust/{ledger.contact_id}: {'; '.join(parts)}]"

    # ── E-24: Milestone management ─────────────────────────────────────────────

    def _detect_milestones(
        self,
        contact_id: str,
        inferred_events: List[str],
        bus: Optional[StateBus],
    ) -> None:
        """Check whether any inferred events trigger a relational first.

        Only fires once per milestone_id per contact — firsts are forever.
        """
        reached_ids = self._milestones_by_contact.get(contact_id, set())

        for m_id, (trigger, name, description, anchor) in _MILESTONE_DEFS.items():
            key = f"{contact_id}:{m_id}"
            if m_id in reached_ids:
                continue
            if trigger not in inferred_events:
                continue

            # New milestone reached — inscribe it
            now = datetime.now(timezone.utc).isoformat()
            milestone = Milestone(
                milestone_id=m_id,
                name=name,
                description=description,
                occurred_at=now,
                trust_anchor=anchor,
                contact_id=contact_id,
            )
            self._milestones.append(milestone)
            if contact_id not in self._milestones_by_contact:
                self._milestones_by_contact[contact_id] = set()
            self._milestones_by_contact[contact_id].add(m_id)

            # Update the ledger's anchor floor
            ledger = self._ensure_ledger(contact_id)
            ledger.anchor_floor = self._compute_anchor_floor(contact_id)

            logger.info(
                "TrustEngine: milestone '%s' reached for '%s' (anchor=%.3f).",
                name, contact_id, anchor,
            )

            # Persist and publish
            self._save_milestones()
            if bus is not None:
                self._publish_milestone(bus, milestone)

    def _compute_anchor_floor(self, contact_id: str) -> float:
        """Sum all trust_anchor values for a contact's milestones."""
        return sum(
            m.trust_anchor
            for m in self._milestones
            if m.contact_id == contact_id
        )

    def _load_milestones(self) -> None:
        """Load milestones from session/milestones.json if present."""
        if not self._milestones_file.exists():
            return
        try:
            raw = json.loads(self._milestones_file.read_text(encoding="utf-8"))
            for d in raw:
                m = Milestone.from_dict(d)
                self._milestones.append(m)
                if m.contact_id not in self._milestones_by_contact:
                    self._milestones_by_contact[m.contact_id] = set()
                self._milestones_by_contact[m.contact_id].add(m.milestone_id)
            logger.debug(
                "TrustEngine: loaded %d milestones from %s.",
                len(self._milestones), self._milestones_file,
            )
        except Exception as exc:
            logger.warning("TrustEngine: failed to load milestones: %s", exc)

    def _save_milestones(self) -> None:
        """Persist milestones to session/milestones.json (append-only semantic)."""
        try:
            self._milestones_file.parent.mkdir(parents=True, exist_ok=True)
            data = [m.to_dict() for m in self._milestones]
            self._milestones_file.write_text(
                json.dumps(data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("TrustEngine: failed to save milestones: %s", exc)

    def _publish_milestone(self, bus: StateBus, milestone: Milestone) -> None:
        """Emit a trust.milestone_reached StateEvent."""
        try:
            event = StateEvent(
                source_module="trust_engine",
                event_type="trust.milestone_reached",
                payload=milestone.to_dict(),
            )
            bus.publish_state(event, nowait=True)
        except Exception as exc:
            logger.warning("TrustEngine._publish_milestone failed: %s", exc)

    # ── Factory ───────────────────────────────────────────────────────────────

    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "TrustEngine":
        """Construct from a config dict.

        Reads keys under ``trust_engine``:
          primary_contact_id            (str,   default "user")
          primary_contact_initial_trust (float, default 0.75)
          stranger_initial_trust        (float, default 0.30)
          session_dir                   (str,   default "session")  E-24
        """
        cfg: Dict[str, Any] = config.get("trust_engine", {})
        return cls(
            primary_contact_id=str(
                cfg.get("primary_contact_id", _DEFAULT_PRIMARY_CONTACT)
            ),
            primary_contact_initial_trust=float(
                cfg.get("primary_contact_initial_trust", _DEFAULT_PRIMARY_TRUST)
            ),
            stranger_initial_trust=float(
                cfg.get("stranger_initial_trust", _DEFAULT_STRANGER_TRUST)
            ),
            session_dir=str(cfg.get("session_dir", _DEFAULT_SESSION_DIR)),  # E-24
        )


# ─── Helpers ──────────────────────────────────────────────────────────────────


def _clamp(value: float) -> float:
    """Clamp a score to [0.0, 1.0]."""
    lo, hi = _TRUST_CLAMP
    return max(lo, min(hi, value))


# ─── Singleton ────────────────────────────────────────────────────────────────

_TRUST_ENGINE: Optional[TrustEngine] = None


def init_trust_engine_from_config(config: Dict[str, Any]) -> TrustEngine:
    """Initialise the global TrustEngine from a config dict.

    Idempotent — returns the existing instance if already initialised.
    """
    global _TRUST_ENGINE
    if _TRUST_ENGINE is None:
        _TRUST_ENGINE = TrustEngine.from_config(config)
        primary = _TRUST_ENGINE._primary_contact_id
        initial = _TRUST_ENGINE._primary_initial_trust
        logger.info(
            "TrustEngine initialised (primary='%s', initial_trust=%.2f).",
            primary, initial,
        )
    return _TRUST_ENGINE


def get_trust_engine() -> TrustEngine:
    """Return the global TrustEngine.

    Raises RuntimeError if ``init_trust_engine_from_config()`` has not been called.
    """
    if _TRUST_ENGINE is None:
        raise RuntimeError(
            "TrustEngine not initialised — call init_trust_engine_from_config() first."
        )
    return _TRUST_ENGINE
