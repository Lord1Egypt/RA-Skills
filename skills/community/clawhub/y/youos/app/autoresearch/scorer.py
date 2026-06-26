"""Scorecard comparison for YouOS Autoresearch."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.evaluation.service import EvalSuiteResult

_DEFAULT_WEIGHTS = {"pass_rate": 0.5, "avg_keyword_hit": 0.3, "avg_confidence": 0.2}
_cached_weights: dict[str, float] | None = None


def load_composite_weights(configs_dir: Path | None = None) -> dict[str, float]:
    """Load composite weights from configs/autoresearch.yaml.

    When ``configs_dir`` is given, the file is read fresh (no caching). The
    autoresearch optimizer rewrites these weights mid-run and re-scores; caching
    a stale copy would make every composite-weight mutation silently ineffective
    (it would score identically and always revert). The cache is only used for
    the default-config path where the file does not change during a process.
    """
    global _cached_weights
    use_cache = configs_dir is None
    if use_cache and _cached_weights is not None:
        return _cached_weights

    if configs_dir is None:
        configs_dir = Path(__file__).resolve().parents[2] / "configs"

    config_path = configs_dir / "autoresearch.yaml"
    if config_path.exists():
        import yaml

        try:
            data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            weights = data.get("composite_weights", {})
            result = {
                "pass_rate": float(weights.get("pass_rate", _DEFAULT_WEIGHTS["pass_rate"])),
                "avg_keyword_hit": float(weights.get("avg_keyword_hit", _DEFAULT_WEIGHTS["avg_keyword_hit"])),
                "avg_confidence": float(weights.get("avg_confidence", _DEFAULT_WEIGHTS["avg_confidence"])),
            }
            if use_cache:
                _cached_weights = result
            return result
        except Exception:
            pass

    if use_cache:
        _cached_weights = dict(_DEFAULT_WEIGHTS)
        return _cached_weights
    return dict(_DEFAULT_WEIGHTS)


def reset_weight_cache() -> None:
    """Clear cached weights (for testing)."""
    global _cached_weights
    _cached_weights = None


def draft_quality_weighting_enabled(configs_dir: Path | None = None) -> bool:
    """Whether to weight eval cases by real-world draft quality (default off)."""
    if configs_dir is None:
        configs_dir = Path(__file__).resolve().parents[2] / "configs"
    config_path = configs_dir / "autoresearch.yaml"
    if config_path.exists():
        import yaml

        try:
            data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            return bool(data.get("draft_quality_weighting", False))
        except Exception:
            return False
    return False


def draft_quality_case_weights(summary: dict, *, k: float = 2.0, max_weight: float = 3.0) -> dict[str, float]:
    """Per-sender_type eval-case weights from a ``summarize_draft_events`` summary.

    Cohorts whose real drafts get edited more (higher avg edit distance) are
    weighted higher, so the optimizer is pushed toward configs that help where
    drafting actually struggles. Benchmark cases carry the sender_type as their
    ``category`` (the join key). ``edit_distance`` is in [0, 1]; weight =
    clamp(1 + k·edit_distance, 1, max_weight). Cohorts with no edit-distance
    data are absent (treated as weight 1.0 by the scorer); an empty/dataless
    summary yields ``{}`` → uniform weighting (no behavior change).
    """
    if not isinstance(summary, dict):
        return {}
    outcome = summary.get("outcome", {})
    by_sender = outcome.get("avg_edit_distance_by_sender_type", {}) if isinstance(outcome, dict) else {}
    weights: dict[str, float] = {}
    for sender, info in (by_sender or {}).items():
        ed = info.get("avg_edit_distance") if isinstance(info, dict) else None
        if ed is None:
            continue
        weights[str(sender)] = max(1.0, min(max_weight, 1.0 + k * float(ed)))
    return weights


@dataclass
class Scorecard:
    config_tag: str
    pass_rate: float  # passed / total
    warn_rate: float
    fail_rate: float
    avg_keyword_hit: float
    avg_confidence: float
    composite: float  # weighted: 0.5*pass_rate + 0.3*avg_keyword_hit + 0.2*avg_confidence

    def summary(self) -> str:
        return f"pass={self.pass_rate:.0%} kw={self.avg_keyword_hit:.0%} conf={self.avg_confidence:.0%} composite={self.composite:.2f}"


def scorecard_from_eval_result(
    result: EvalSuiteResult,
    configs_dir: Path | None = None,
    *,
    case_weights: dict[str, float] | None = None,
) -> Scorecard:
    """Score an eval suite result.

    ``case_weights`` (sender_type → weight, from ``draft_quality_case_weights``)
    importance-weights the composite inputs (pass_rate / keyword / confidence)
    by ``CaseResult.category``, so the objective emphasizes the cohorts where
    real-world drafting is weakest. Cases whose category isn't in the map get
    weight 1.0; ``None`` or all-1.0 weights reduce to the equal-average
    behavior. Weighting must be applied identically to baseline and candidate
    so their composites stay comparable.
    """
    total = result.total_cases
    if total == 0:
        return Scorecard(
            config_tag=result.config_tag,
            pass_rate=0.0,
            warn_rate=0.0,
            fail_rate=0.0,
            avg_keyword_hit=0.0,
            avg_confidence=0.0,
            composite=0.0,
        )

    # warn/fail rates are display-only (not in the composite) → left unweighted.
    warn_rate = result.warned / total
    fail_rate = result.failed / total

    crs = result.case_results
    if case_weights:
        ws = [max(0.0, float(case_weights.get(cr.category, 1.0))) for cr in crs]
        wsum = sum(ws) or float(len(crs))
        pass_rate = sum(w * (1.0 if cr.pass_fail == "pass" else 0.0) for w, cr in zip(ws, crs, strict=False)) / wsum
        avg_kw = sum(w * cr.scores.get("keyword_hit_rate", 0.0) for w, cr in zip(ws, crs, strict=False)) / wsum
        avg_conf = sum(w * cr.scores.get("confidence_score", 0.0) for w, cr in zip(ws, crs, strict=False)) / wsum
    else:
        pass_rate = result.passed / total
        avg_kw = sum(cr.scores.get("keyword_hit_rate", 0.0) for cr in crs) / total
        avg_conf = sum(cr.scores.get("confidence_score", 0.0) for cr in crs) / total

    weights = load_composite_weights(configs_dir)
    composite = weights["pass_rate"] * pass_rate + weights["avg_keyword_hit"] * avg_kw + weights["avg_confidence"] * avg_conf

    return Scorecard(
        config_tag=result.config_tag,
        pass_rate=round(pass_rate, 4),
        warn_rate=round(warn_rate, 4),
        fail_rate=round(fail_rate, 4),
        avg_keyword_hit=round(avg_kw, 4),
        avg_confidence=round(avg_conf, 4),
        composite=round(composite, 4),
    )


def compare_scorecards(baseline: Scorecard, candidate: Scorecard) -> str:
    """Compare two scorecards.

    Returns:
        "improved"  — composite >= baseline + 0.02
        "regressed" — composite < baseline - 0.01
        "neutral"   — otherwise
    """
    diff = candidate.composite - baseline.composite
    if diff >= 0.02:
        return "improved"
    if diff < -0.01:
        return "regressed"
    return "neutral"
