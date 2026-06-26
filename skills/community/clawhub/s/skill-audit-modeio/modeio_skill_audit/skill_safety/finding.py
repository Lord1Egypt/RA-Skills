from __future__ import annotations

from typing import Optional, Sequence, Set, Tuple

from .common import truncate_snippet
from .constants import LAYER_EVASION, REQUIRED_LAYERS
from .models import Finding, LayerState


def initial_layer_state() -> LayerState:
    return {
        layer: {
            "executed": False,
            "finding_count": 0,
        }
        for layer in REQUIRED_LAYERS + (LAYER_EVASION,)
    }


def mark_layer_executed(layer_state: LayerState, layer: str) -> None:
    if layer not in layer_state:
        layer_state[layer] = {"executed": False, "finding_count": 0}
    layer_state[layer]["executed"] = True


def add_finding(
    findings: list[Finding],
    dedupe: Set[Tuple[str, str, int, str]],
    layer_state: LayerState,
    *,
    layer: str,
    rule_id: str,
    category: str,
    severity: str,
    confidence: str,
    file_path: str,
    line: int,
    snippet: str,
    why: str,
    fix: str,
    tags: Optional[Sequence[str]] = None,
    exploitability: float = 0.80,
    reach: float = 0.80,
) -> None:
    dedupe_key = (rule_id, file_path, int(line), snippet.strip())
    if dedupe_key in dedupe:
        return
    dedupe.add(dedupe_key)
    mark_layer_executed(layer_state, layer)
    layer_state[layer]["finding_count"] += 1

    findings.append(
        {
            "layer": layer,
            "rule_id": rule_id,
            "category": category,
            "severity": severity,
            "confidence": confidence,
            "exploitability": round(float(exploitability), 2),
            "reach": round(float(reach), 2),
            "file": file_path,
            "line": int(line),
            "snippet": truncate_snippet(snippet),
            "why": why,
            "fix": fix,
            "tags": list(tags or []),
        }
    )
