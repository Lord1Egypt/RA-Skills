"""Severity classification with dedup escalation.

🟡 Dr. Neuron fix: No blind addition.
- Same behavior multiple times → counts ONCE (dedup)
- Only DIFFERENT behaviors → escalate
- Cap: maximum one step above highest individual hit
"""

from sal.monitor.behaviors import BehaviorHit, Severity


def classify_hits(hits: list[BehaviorHit]) -> dict:
    """Classify a list of behavior hits into a final severity.

    Returns:
        Dict with:
            - severity: Final Severity level
            - unique_behaviors: Number of distinct behavior IDs
            - total_hits: Number of raw hits before dedup
            - escalated: Whether severity was escalated
            - hits: Deduplicated hit list
    """
    if not hits:
        return {
            "severity": Severity.LOW,
            "unique_behaviors": 0,
            "total_hits": 0,
            "escalated": False,
            "hits": [],
        }

    # Step 1: Dedup — same behavior_id → keep highest severity instance
    deduped: dict[str, BehaviorHit] = {}
    for hit in hits:
        existing = deduped.get(hit.behavior_id)
        if existing is None or hit.severity > existing.severity:
            deduped[hit.behavior_id] = hit

    unique_hits = list(deduped.values())
    distinct_ids = set(deduped.keys())

    # Step 2: Base severity = highest individual hit
    base_severity = max(h.severity for h in unique_hits)

    # Step 3: Escalate if 3+ DIFFERENT behaviors detected
    escalated = False
    final_severity = base_severity

    if len(distinct_ids) >= 3 and base_severity < Severity.CRITICAL:
        # Cap: maximum one step above highest hit
        final_severity = Severity(base_severity + 1)
        escalated = True

    # Step 4: LLM hits → floor at MEDIUM
    has_llm = any(h.source == "llm" for h in unique_hits)
    if has_llm and final_severity < Severity.MEDIUM:
        final_severity = Severity.MEDIUM

    return {
        "severity": final_severity,
        "unique_behaviors": len(distinct_ids),
        "total_hits": len(hits),
        "escalated": escalated,
        "hits": unique_hits,
    }


def needs_alert(severity: Severity) -> bool:
    """Whether this severity triggers a Telegram alert."""
    return severity >= Severity.HIGH


def needs_block(severity: Severity) -> bool:
    """Whether this severity triggers agent blocking."""
    return severity >= Severity.CRITICAL
