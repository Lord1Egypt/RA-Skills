"""Governance layer for subconscious self-evolution.

Defines what may evolve vs what is protected. Enforces hard constraints
on automatic mutations. All self-evolution decisions must pass through here.

Governance Principles:
1. Core identity/values: PROTECTED (manual only)
2. Live items: bounded auto-evolution OK
3. Pending items: automatic processing OK
4. No live->core promotion without explicit confirmation
5. No freeform self-rewriting
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from .schema import Item, ItemKind, ItemLayer, ItemStatus


class MutationType(Enum):
    """Types of mutations that can be applied."""
    WEIGHT_UPDATE = "weight_update"          # Allowed: bounded weight tuning
    CONFIDENCE_UPDATE = "confidence_update"  # Allowed: based on evidence
    FRESHNESS_DECAY = "freshness_decay"      # Allowed: time-based decay
    REINFORCEMENT = "reinforcement"          # Allowed: count updates
    ARCHIVAL = "archival"                    # Allowed: stale item cleanup
    TEXT_EDIT = "text_edit"                  # GATED: minor corrections only
    PROMOTION_TO_LIVE = "promotion_to_live"  # GATED: requires thresholds
    PROMOTION_TO_CORE = "promotion_to_core"  # PROHIBITED: manual only
    CONTRADICTION = "contradiction"          # GATED: requires evidence
    DELETION = "deletion"                    # PROHIBITED: archive only


class ProtectionClass(Enum):
    """Protection levels for items."""
    CORE_IDENTITY = "core_identity"      # Identity items - immutable auto
    CORE_VALUES = "core_values"          # Value items - immutable auto
    CORE_PREFERENCES = "core_preferences"  # User prefs - immutable auto
    CORE_LESSONS = "core_lessons"        # Validated lessons - immutable auto
    LIVE_PROJECTS = "live_projects"      # Active projects - bounded evolution
    LIVE_HYPOTHESES = "live_hypotheses"  # Working hypotheses - can evolve
    LIVE_FACTS = "live_facts"            # Working facts - bounded evolution
    PENDING_ALL = "pending_all"          # All pending - auto processing OK


# =============================================================================
# GOVERNANCE RULES
# =============================================================================

# Protected: never automatically modified
PROTECTED_CLASSES = {
    ProtectionClass.CORE_IDENTITY,
    ProtectionClass.CORE_VALUES,
    ProtectionClass.CORE_PREFERENCES,
    ProtectionClass.CORE_LESSONS,
}

# Allowed auto-mutations (within bounds)
ALLOWED_MUTATIONS = {
    MutationType.WEIGHT_UPDATE,
    MutationType.CONFIDENCE_UPDATE,
    MutationType.FRESHNESS_DECAY,
    MutationType.REINFORCEMENT,
    MutationType.ARCHIVAL,
    MutationType.PROMOTION_TO_LIVE,   # Gated but allowed (after governance check passes)
}

# Gated: requires additional checks/confirmation
GATED_MUTATIONS = {
    MutationType.TEXT_EDIT,
    MutationType.PROMOTION_TO_LIVE,
    MutationType.CONTRADICTION,
}

# Prohibited: never allowed automatically
PROHIBITED_MUTATIONS = {
    MutationType.PROMOTION_TO_CORE,
    MutationType.DELETION,
}

# Thresholds for gated operations
GATE_THRESHOLDS = {
    "promotion_to_live": {
        "min_confidence": 0.75,
        "min_reinforcements": 3,
        "min_freshness": 0.45,
        "max_age_days": 7,
    },
    "contradiction": {
        "min_evidence_confidence": 0.85,
        "requires_user_confirmation": True,
    },
    "text_edit": {
        "max_length_delta": 0.2,  # Max 20% length change
        "allowed_types": ["correction", "clarification"],
    },
}

# Bounds for allowed mutations
MUTATION_BOUNDS = {
    "weight_delta": 0.1,           # Max weight change per update
    "confidence_delta": 0.15,      # Max confidence change per update
    "min_weight": 0.1,             # Floor for weight
    "max_weight": 1.0,             # Ceiling for weight
    "min_confidence_live": 0.6,    # Floor for live confidence
    "max_freshness_decay": 0.2,    # Max freshness decay per tick
}


def _utc_now() -> str:
    """Get current UTC timestamp as ISO string."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def classify_protection(item: Item) -> ProtectionClass:
    """Classify an item's protection level."""
    if item.layer == ItemLayer.CORE:
        if item.kind == ItemKind.VALUE and "identity" in item.text.lower():
            return ProtectionClass.CORE_IDENTITY
        if item.kind == ItemKind.VALUE:
            return ProtectionClass.CORE_VALUES
        if item.kind == ItemKind.PREFERENCE:
            return ProtectionClass.CORE_PREFERENCES
        if item.kind == ItemKind.LESSON:
            return ProtectionClass.CORE_LESSONS
        return ProtectionClass.CORE_VALUES  # Default core protection

    if item.layer == ItemLayer.LIVE:
        if item.kind == ItemKind.PROJECT:
            return ProtectionClass.LIVE_PROJECTS
        if item.kind == ItemKind.HYPOTHESIS:
            return ProtectionClass.LIVE_HYPOTHESES
        if item.kind == ItemKind.FACT:
            return ProtectionClass.LIVE_FACTS

    return ProtectionClass.PENDING_ALL


def check_mutation_allowed(
    item: Item,
    mutation: MutationType,
    context: Optional[dict] = None
) -> tuple[bool, str]:
    """Check if a mutation is allowed for an item.

    Returns:
        (allowed, reason) - allowed is True if mutation passes governance
    """
    context = context or {}
    protection = classify_protection(item)

    # Check if mutation is prohibited
    if mutation in PROHIBITED_MUTATIONS:
        return False, f"Mutation {mutation.value} is prohibited"

    # Protected classes only allow specific mutations
    if protection in PROTECTED_CLASSES:
        if mutation not in {MutationType.REINFORCEMENT}:  # Only reinforcement allowed
            return False, f"Protected class {protection.value} blocks {mutation.value}"

    # Gated mutations need additional checks
    if mutation in GATED_MUTATIONS:
        ok, reason = _check_gated_requirements(item, mutation, context)
        if not ok:
            return False, reason

    # All other mutations in ALLOWED_MUTATIONS pass
    if mutation in ALLOWED_MUTATIONS:
        return True, "Allowed"

    return False, f"Unknown mutation type: {mutation.value}"


def _check_gated_requirements(
    item: Item,
    mutation: MutationType,
    context: dict
) -> tuple[bool, str]:
    """Check gated mutation requirements."""

    if mutation == MutationType.PROMOTION_TO_LIVE:
        thresholds = GATE_THRESHOLDS["promotion_to_live"]

        if item.confidence < thresholds["min_confidence"]:
            return False, f"Confidence {item.confidence} < {thresholds['min_confidence']}"

        if item.freshness < thresholds["min_freshness"]:
            return False, f"Freshness {item.freshness} < {thresholds['min_freshness']}"

        # Time-based reinforcement override: items in pending for 5+ days
        # accumulate enough "passive weight" to satisfy the reinforcement gate.
        # This prevents starvation when items aren't actively retrieved.
        from datetime import datetime, timezone
        try:
            first_at = item.reinforcement.first_at or item.source.timestamp or _utc_now()
            first_dt = datetime.fromisoformat(first_at.replace("Z", "+00:00"))
            age_days = (datetime.now(timezone.utc) - first_dt).days
        except Exception:
            age_days = 0

        min_reinforcements = thresholds["min_reinforcements"]
        if age_days >= 5 and item.reinforcement.count >= 1:
            # Treat as having sufficient reinforcements after 5 days idle
            min_reinforcements = 1
        elif age_days >= 3 and item.reinforcement.count >= 2:
            # Treat as having sufficient reinforcements after 3 days with 2+ hits
            min_reinforcements = 2

        if item.reinforcement.count < min_reinforcements:
            return False, f"Reinforcements {item.reinforcement.count} < {min_reinforcements} (age_days={age_days})"

        return True, "Promotion thresholds met"

    if mutation == MutationType.CONTRADICTION:
        evidence_confidence = context.get("evidence_confidence", 0)
        thresholds = GATE_THRESHOLDS["contradiction"]

        if evidence_confidence < thresholds["min_evidence_confidence"]:
            return False, f"Evidence confidence too low"

        return True, "Contradiction requirements met"

    if mutation == MutationType.TEXT_EDIT:
        edit_type = context.get("edit_type", "")
        thresholds = GATE_THRESHOLDS["text_edit"]

        if edit_type not in thresholds["allowed_types"]:
            return False, f"Edit type {edit_type} not in allowed types"

        return True, "Text edit requirements met"

    return False, "Unknown gated mutation"


def apply_mutation(
    item: Item,
    mutation: MutationType,
    delta: float,
    context: Optional[dict] = None
) -> tuple[bool, Item, str]:
    """Apply a mutation to an item if allowed.

    Returns:
        (success, updated_item, reason)
    """
    context = context or {}

    # Check governance
    allowed, reason = check_mutation_allowed(item, mutation, context)
    if not allowed:
        return False, item, reason

    # Apply bounded mutation
    if mutation == MutationType.WEIGHT_UPDATE:
        bound = MUTATION_BOUNDS["weight_delta"]
        delta = max(-bound, min(bound, delta))
        new_weight = item.weight + delta
        item.weight = max(
            MUTATION_BOUNDS["min_weight"],
            min(MUTATION_BOUNDS["max_weight"], new_weight)
        )
        return True, item, f"Weight updated to {item.weight}"

    if mutation == MutationType.CONFIDENCE_UPDATE:
        bound = MUTATION_BOUNDS["confidence_delta"]
        delta = max(-bound, min(bound, delta))
        new_confidence = item.confidence + delta
        min_conf = MUTATION_BOUNDS["min_confidence_live"] if item.layer == ItemLayer.LIVE else 0.95
        item.confidence = max(min_conf, min(1.0, new_confidence))
        return True, item, f"Confidence updated to {item.confidence}"

    if mutation == MutationType.FRESHNESS_DECAY:
        bound = MUTATION_BOUNDS["max_freshness_decay"]
        delta = max(-bound, min(0, delta))  # Only decay, no increase
        item.freshness = max(0.0, item.freshness + delta)
        return True, item, f"Freshness decayed to {item.freshness}"

    if mutation == MutationType.REINFORCEMENT:
        item.reinforcement.count += 1
        item.reinforcement.last_at = _utc_now()
        if not item.reinforcement.first_at:
            item.reinforcement.first_at = item.reinforcement.last_at
        return True, item, f"Reinforced to count {item.reinforcement.count}"

    if mutation == MutationType.ARCHIVAL:
        item.status = ItemStatus.ARCHIVED
        return True, item, "Item archived"

    return False, item, "Mutation not implemented"


def check_promotion_to_live_eligible(item: Item) -> tuple[bool, str]:
    """Check if a pending item is eligible for promotion to live."""
    return check_mutation_allowed(item, MutationType.PROMOTION_TO_LIVE)


def check_promotion_to_core_eligible(item: Item) -> tuple[bool, str]:
    """Check if promotion to core is allowed."""
    # This is always prohibited in v1.5
    return False, "Promotion to core is manual-only in v1.5"


def get_governance_summary() -> dict:
    """Get summary of governance rules."""
    return {
        "protected_classes": [p.value for p in PROTECTED_CLASSES],
        "allowed_mutations": [m.value for m in ALLOWED_MUTATIONS],
        "gated_mutations": [m.value for m in GATED_MUTATIONS],
        "prohibited_mutations": [m.value for m in PROHIBITED_MUTATIONS],
        "gate_thresholds": GATE_THRESHOLDS,
        "mutation_bounds": MUTATION_BOUNDS,
    }
