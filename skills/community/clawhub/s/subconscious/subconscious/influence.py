"""Convert retrieved items into compact bias hints for reply shaping.

Max 5 bias items per turn. Low-confidence items filtered out.
"""

from typing import Optional

from .schema import Item, ItemKind


def build_bias(items: list[Item], max_items: int = 5, min_confidence: float = 0.7) -> dict:
    """Build compact bias block from relevant items.

    Args:
        items: Retrieved relevant items
        max_items: Maximum bias items (default 5)
        min_confidence: Minimum confidence to surface

    Returns:
        Dict with bias categories
    """
    # Filter and sort
    qualified = [
        item for item in items
        if item.confidence >= min_confidence and item.status.value != "archived"
    ]

    # Take top N
    selected = qualified[:max_items]

    # Build bias categories
    attention = []
    interpretation = []
    action = []
    style = []

    for item in selected:
        text = _compact_text(item.text)

        if item.kind == ItemKind.VALUE:
            style.append(text)
        elif item.kind == ItemKind.PREFERENCE:
            interpretation.append(text)
        elif item.kind == ItemKind.LESSON:
            attention.append(text)
        elif item.kind == ItemKind.HYPOTHESIS:
            interpretation.append(f"[HYPOTHESIS] {text}")
        elif item.kind == ItemKind.PROJECT:
            attention.append(f"Active: {text}")
        elif item.kind == ItemKind.FACT:
            interpretation.append(text)
        elif item.kind == ItemKind.CONTEXT:
            attention.append(text)

    return {
        "subconscious_bias": {
            "attention": attention,
            "interpretation": interpretation,
            "action": action,
            "style": style,
            "_meta": {
                "item_count": len(selected),
                "avg_confidence": sum(i.confidence for i in selected) / len(selected) if selected else 0,
            },
        }
    }


def _compact_text(text: str, max_len: int = 300) -> str:
    """Compact text to max length."""
    if len(text) <= max_len:
        return text
    return text[:max_len - 3] + "..."


def format_for_prompt(bias: dict) -> str:
    """Format bias block as markdown for system prompt injection."""
    bias_data = bias.get("subconscious_bias", {})

    lines = ["## SUBCONSCIOUS"]

    # style → Identity: show each item on its own line for readability
    if bias_data.get("style"):
        for item in bias_data["style"]:
            lines.append(f"Identity: {item}")

    # interpretation → Context: show each item on its own line
    if bias_data.get("interpretation"):
        for item in bias_data["interpretation"]:
            lines.append(f"Context: {item}")

    # attention → Active: show each item on its own line
    if bias_data.get("attention"):
        for item in bias_data["attention"]:
            lines.append(f"Active: {item}")

    # action → Priority: show each item on its own line
    if bias_data.get("action"):
        for item in bias_data["action"]:
            lines.append(f"Priority: {item}")

    return "\n".join(lines)
