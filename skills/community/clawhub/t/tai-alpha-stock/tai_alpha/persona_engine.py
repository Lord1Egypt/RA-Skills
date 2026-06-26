"""Apply persona overlays to base score; optional ensemble."""

from __future__ import annotations

import math
from typing import Any

from tai_alpha.persona_registry import list_persona_ids, load_persona_by_id

_SIGNAL_ORDER = ["SELL", "AVOID", "HOLD", "BUY", "STRONG BUY"]


def _signal_rank(sig: str) -> int:
    try:
        return _SIGNAL_ORDER.index(sig)
    except ValueError:
        return 2


def _cap_signal(current: str, cap: str) -> str:
    if _signal_rank(current) > _signal_rank(cap):
        return cap
    return current


def apply_persona_overlay(
    base_score: dict[str, Any],
    data: dict[str, Any],
    persona_id: str,
) -> dict[str, Any]:
    """
    Return a new score dict with persona overlay applied (does not mutate inputs).
    """
    cfg = load_persona_by_id(persona_id)
    ov = cfg.get("overlay", {})
    out = dict(base_score)

    conv = float(out.get("conviction", 0))
    scale = float(ov.get("conviction_scale", 1.0))
    bias = int(ov.get("conviction_bias", 0))
    conv = conv * scale + float(bias)

    pe = float(data.get("pe", 999))
    if pe < 20 and ov.get("pe_bonus_weight"):
        conv += (float(ov["pe_bonus_weight"]) - 1.0) * 3.0
    rsi = float(data.get("rsi", 50))
    extra = float(ov.get("high_rsi_penalty_extra", 0))
    if rsi > 75 and extra:
        conv -= extra

    eg = float(data.get("eps_growth", 0))
    if eg > 0.2 and ov.get("eps_growth_weight"):
        conv += (float(ov["eps_growth_weight"]) - 1.0) * 5.0

    if str(data.get("macd")) == "bull" and ov.get("macd_bull_bonus"):
        conv += float(ov["macd_bull_bonus"])

    vix = float(data.get("vix", 20))
    if vix > 20 and ov.get("vix_weight"):
        conv -= (float(ov["vix_weight"]) - 1.0) * 2.0
    sm = float(data.get("spy_mom", 0))
    if sm > 5 and ov.get("spy_mom_weight"):
        conv += (float(ov["spy_mom_weight"]) - 1.0) * 2.0

    roe = float(data.get("roe", 0))
    if roe > 0.15 and ov.get("roe_weight"):
        conv += (float(ov["roe_weight"]) - 1.0) * 4.0
    debt = float(data.get("debt", 999))
    if debt > 40 and ov.get("debt_penalty_weight"):
        conv -= (float(ov["debt_penalty_weight"]) - 1.0) * 3.0

    dy = float(data.get("div_yield", 0))
    if dy > 0.03 and ov.get("div_yield_weight"):
        conv += (float(ov["div_yield_weight"]) - 1.0) * 4.0

    flags = data.get("risk_flags") or []
    if isinstance(flags, list) and ov.get("risk_flag_penalty_per"):
        conv -= len(flags) * float(ov["risk_flag_penalty_per"])

    if not math.isfinite(conv):
        conv = 0.0
    conv_i = int(min(100, max(0, round(conv))))
    if conv_i > 85:
        sig = "STRONG BUY"
    elif conv_i > 75:
        sig = "BUY"
    elif conv_i < 55:
        sig = "SELL"
    elif conv_i < 65:
        sig = "AVOID"
    else:
        sig = "HOLD"
    if ov.get("signal_cap_max"):
        sig = _cap_signal(sig, str(ov["signal_cap_max"]))
    out["conviction"] = conv_i
    out["signal"] = sig
    out["persona_id"] = cfg["id"]
    out["persona_display_name"] = cfg.get("display_name", cfg["id"])
    out["persona_display_name_zh"] = cfg.get("display_name_zh", "")
    return out


def apply_persona_ensemble(
    base_score: dict[str, Any],
    data: dict[str, Any],
    persona_ids: list[str] | None,
) -> dict[str, Any]:
    """
    If ``persona_ids`` is empty/None, return ``base_score`` unchanged.
    If one id, use ``apply_persona_overlay``.
    If multiple, weighted average conviction + majority signal.
    """
    if not persona_ids:
        return dict(base_score)
    ids = [p.strip() for p in persona_ids if p.strip()]
    if not ids:
        return dict(base_score)
    if len(ids) == 1:
        return apply_persona_overlay(base_score, data, ids[0])

    results: list[dict[str, Any]] = []
    weights: list[float] = []
    for pid in ids:
        one = apply_persona_overlay(base_score, data, pid)
        cfg = load_persona_by_id(pid)
        w = float(cfg.get("ensemble_weight", 1.0))
        results.append(one)
        weights.append(w)

    tw = sum(weights) or 1.0
    avg_conv = sum(float(r["conviction"]) * w for r, w in zip(results, weights)) / tw
    conv_i = int(min(100, max(0, round(avg_conv))))
    if conv_i > 85:
        best_sig = "STRONG BUY"
    elif conv_i > 75:
        best_sig = "BUY"
    elif conv_i < 55:
        best_sig = "SELL"
    elif conv_i < 65:
        best_sig = "AVOID"
    else:
        best_sig = "HOLD"

    merged = dict(base_score)
    merged["conviction"] = conv_i
    merged["signal"] = best_sig
    merged["persona_ensemble"] = [r.get("persona_id") for r in results]
    merged["persona_id"] = "ensemble"
    return merged


def resolve_persona_ids(persona: str | None, persona_all: bool) -> list[str]:
    """Return list of persona ids from CLI flags."""
    if persona_all:
        return list_persona_ids(enabled_only=True)
    if persona and persona.strip().lower() not in ("", "none", "off"):
        return [p.strip() for p in persona.split(",") if p.strip()]
    return []
