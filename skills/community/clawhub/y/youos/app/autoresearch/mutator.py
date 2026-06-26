"""Config mutation engine for YouOS Autoresearch."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass
class ConfigSurface:
    name: str  # e.g. "top_k_reply_pairs" or "drafting_prompt"
    config_file: str  # relative to configs_dir, e.g. "retrieval/defaults.yaml"
    yaml_key: str  # top-level key in the yaml file
    current_value: Any
    mutation_type: str  # "numeric_step" | "template_variant"
    step_size: float | None = None
    min_val: float | None = None
    max_val: float | None = None
    variants: list[Any] | None = None
    variant_index: int = 0  # for template_variant: which variant is current


# -- Numeric surface definitions ────────────────────────────────────

_NUMERIC_SURFACES: list[dict[str, Any]] = [
    {"name": "top_k_reply_pairs", "config_file": "retrieval/defaults.yaml", "yaml_key": "top_k_reply_pairs", "step_size": 1, "min_val": 3, "max_val": 10},
    {"name": "top_k_chunks", "config_file": "retrieval/defaults.yaml", "yaml_key": "top_k_chunks", "step_size": 1, "min_val": 1, "max_val": 6},
    {"name": "recency_boost_days", "config_file": "retrieval/defaults.yaml", "yaml_key": "recency_boost_days", "step_size": 30, "min_val": 30, "max_val": 365},
    {
        "name": "recency_boost_weight",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "recency_boost_weight",
        "step_size": 0.05,
        "min_val": 0.0,
        "max_val": 0.5,
    },
    {
        "name": "account_boost_weight",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "account_boost_weight",
        "step_size": 0.05,
        "min_val": 0.0,
        "max_val": 0.4,
    },
    # E16: semantic vs keyword balance
    {
        "name": "semantic_weight",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "semantic_weight",
        "step_size": 0.05,
        "min_val": 0.0,
        "max_val": 1.0,
    },
    # E16: exemplar display length tuning
    {
        "name": "exemplar_reply_chars",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "exemplar_reply_chars",
        "step_size": 100,
        "min_val": 200,
        "max_val": 1000,
    },
    {
        "name": "exemplar_inbound_chars",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "exemplar_inbound_chars",
        "step_size": 100,
        "min_val": 100,
        "max_val": 600,
    },
    # BM25 lexical-score saturation. Historically hardcoded
    # `min(raw_rank * 2.0, 10.0)` — strong matches above raw_rank=5 all
    # flattened to lexical_score=10 and lost their order. Surfacing the scale
    # and cap lets autoresearch's golden-eval-gated loop find the right
    # ramp/ceiling for this corpus instead of guessing.
    {
        "name": "lexical_scale",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "lexical_scale",
        "step_size": 0.5,
        "min_val": 0.5,
        "max_val": 4.0,
    },
    {
        "name": "lexical_cap",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "lexical_cap",
        "step_size": 2.0,
        "min_val": 6.0,
        "max_val": 20.0,
    },
    # Subject/title/topic/sender boosts. Each was already in scoring code
    # via RetrievalConfig but only `recency_boost_*` and `account_boost_*`
    # were exposed for autoresearch — every other lever stayed pinned at its
    # historical default. Opening them up to the same golden-eval-gated loop
    # lets the optimizer find the right balance for *this* corpus instead of
    # the original guesses.
    {
        "name": "subject_match_boost",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "subject_match_boost",
        "step_size": 0.05,
        "min_val": 0.0,
        "max_val": 0.5,
    },
    {
        "name": "topic_match_boost",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "topic_match_boost",
        "step_size": 0.05,
        "min_val": 0.0,
        "max_val": 0.5,
    },
    {
        "name": "sender_type_boost",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "sender_type_boost",
        "step_size": 0.05,
        "min_val": 0.0,
        "max_val": 0.5,
    },
    {
        "name": "sender_domain_boost",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "sender_domain_boost",
        "step_size": 0.05,
        "min_val": 0.0,
        "max_val": 0.4,
    },
    {
        "name": "field_match_bonus_per_token",
        "config_file": "retrieval/defaults.yaml",
        "yaml_key": "field_match_bonus_per_token",
        "step_size": 0.05,
        "min_val": 0.0,
        "max_val": 0.5,
    },
]

# E16: Per-mode avg_reply_words surfaces (nested in persona.yaml modes)
_MODE_AVG_WORDS_SURFACES: list[dict[str, Any]] = [
    {"name": f"mode_avg_words_{mode}", "sender_type": mode, "step_size": 10, "min_val": 20, "max_val": 200}
    for mode in ("external_client", "personal", "internal", "automated")
]

# Per-sender-type boost surfaces (nested under sender_type_boost_map)
_SENDER_TYPE_BOOST_SURFACES: list[dict[str, Any]] = [
    {"name": f"sender_type_boost_{st}", "sender_type": st, "step_size": 0.1, "min_val": 0.5, "max_val": 2.0}
    for st in ("external_client", "personal", "automated", "internal")
]

# -- Prompt variant definitions ─────────────────────────────────────

_DRAFTING_PROMPT_VARIANTS: list[str] = [
    # variant_a: current standard
    """\
Task: produce a draft in your style grounded in retrieved corpus evidence.

Inputs:
- user request
- retrieved chunks
- relevant reply-pair exemplars

Requirements:
- preserve intent and tone consistent with your style
- do not invent personal facts that are not retrieved
- prefer concise drafts unless the request demands detail
""",
    # variant_b: concise format
    """\
Task: draft a concise reply in your style using retrieved evidence.

Inputs: user request, retrieved chunks, reply-pair exemplars.

Rules:
- match your style and intent
- no invented facts
- keep it short
""",
    # variant_c: direct, skip pleasantries
    """\
Task: produce a draft in your style grounded in retrieved corpus evidence.

Inputs:
- user request
- retrieved chunks
- relevant reply-pair exemplars

Requirements:
- preserve intent and tone consistent with your style
- do not invent personal facts that are not retrieved
- prefer concise drafts unless the request demands detail
- be direct, skip pleasantries
""",
]


_COMPOSITE_WEIGHT_SURFACES: list[dict[str, Any]] = [
    {"name": f"composite_weight_{k}", "yaml_key": f"composite_weights.{k}", "step_size": 0.05, "min_val": 0.0, "max_val": 1.0}
    for k in ("pass_rate", "avg_keyword_hit", "avg_confidence")
]


def _normalize_composite_weights(data: dict[str, Any]) -> None:
    """Enforce sum == 1.0 for composite weights after mutation."""
    weights = data.get("composite_weights", {})
    if not weights:
        return
    total = sum(float(v) for v in weights.values())
    if total > 0:
        for k in weights:
            weights[k] = round(float(weights[k]) / total, 4)


def get_mutable_surfaces(configs_dir: Path, *, surface_filter: str | None = None) -> list[ConfigSurface]:
    """Load current config values and return mutable surfaces."""
    surfaces: list[ConfigSurface] = []

    if surface_filter is None or surface_filter == "retrieval":
        retrieval_path = configs_dir / "retrieval" / "defaults.yaml"
        retrieval_data = yaml.safe_load(retrieval_path.read_text(encoding="utf-8")) or {}

        for spec in _NUMERIC_SURFACES:
            current = retrieval_data.get(spec["yaml_key"])
            if current is None:
                continue
            # Coerce to match step type
            if isinstance(spec["step_size"], int):
                current = int(current)
            else:
                current = float(current)
            surfaces.append(
                ConfigSurface(
                    name=spec["name"],
                    config_file=spec["config_file"],
                    yaml_key=spec["yaml_key"],
                    current_value=current,
                    mutation_type="numeric_step",
                    step_size=spec["step_size"],
                    min_val=spec["min_val"],
                    max_val=spec["max_val"],
                )
            )

        # Sender-type boost map surfaces
        boost_map = retrieval_data.get("sender_type_boost_map", {})
        for spec in _SENDER_TYPE_BOOST_SURFACES:
            st = spec["sender_type"]
            current = float(boost_map.get(st, 1.0))
            surfaces.append(
                ConfigSurface(
                    name=spec["name"],
                    config_file="retrieval/defaults.yaml",
                    yaml_key=f"sender_type_boost_map.{st}",
                    current_value=current,
                    mutation_type="numeric_step",
                    step_size=spec["step_size"],
                    min_val=spec["min_val"],
                    max_val=spec["max_val"],
                )
            )

    # E16: per-mode avg_reply_words from persona.yaml
    if surface_filter is None or surface_filter == "persona":
        persona_path = configs_dir / "persona.yaml"
        if persona_path.exists():
            persona_data = yaml.safe_load(persona_path.read_text(encoding="utf-8")) or {}
            modes = persona_data.get("modes", {})
            for spec in _MODE_AVG_WORDS_SURFACES:
                mode = spec["sender_type"]
                mode_cfg = modes.get(mode, {})
                current_words = mode_cfg.get("avg_reply_words")
                if current_words is None:
                    continue
                surfaces.append(
                    ConfigSurface(
                        name=spec["name"],
                        config_file="persona.yaml",
                        yaml_key=f"modes.{mode}.avg_reply_words",
                        current_value=int(current_words),
                        mutation_type="numeric_step",
                        step_size=spec["step_size"],
                        min_val=spec["min_val"],
                        max_val=spec["max_val"],
                    )
                )

    if surface_filter is None or surface_filter == "autoresearch":
        autoresearch_path = configs_dir / "autoresearch.yaml"
        if autoresearch_path.exists():
            ar_data = yaml.safe_load(autoresearch_path.read_text(encoding="utf-8")) or {}
            weights = ar_data.get("composite_weights", {})
            for spec in _COMPOSITE_WEIGHT_SURFACES:
                key_parts = spec["yaml_key"].split(".")
                current = float(weights.get(key_parts[-1], 0.0))
                surfaces.append(
                    ConfigSurface(
                        name=spec["name"],
                        config_file="autoresearch.yaml",
                        yaml_key=spec["yaml_key"],
                        current_value=current,
                        mutation_type="numeric_step",
                        step_size=spec["step_size"],
                        min_val=spec["min_val"],
                        max_val=spec["max_val"],
                    )
                )

    if surface_filter is None or surface_filter == "prompt_drafting":
        prompts_path = configs_dir / "prompts.yaml"
        prompts_data = yaml.safe_load(prompts_path.read_text(encoding="utf-8")) or {}
        current_prompt = prompts_data.get("drafting_prompt", "")

        # Determine which variant index matches current
        variant_index = 0
        for i, variant in enumerate(_DRAFTING_PROMPT_VARIANTS):
            if variant.strip() == current_prompt.strip():
                variant_index = i
                break

        surfaces.append(
            ConfigSurface(
                name="drafting_prompt",
                config_file="prompts.yaml",
                yaml_key="drafting_prompt",
                current_value=current_prompt,
                mutation_type="template_variant",
                variants=_DRAFTING_PROMPT_VARIANTS,
                variant_index=variant_index,
            )
        )

    return surfaces


def apply_mutation(surface: ConfigSurface, configs_dir: Path) -> Any:
    """Apply one mutation step to the surface. Returns old value for revert."""
    old_value = surface.current_value
    file_path = configs_dir / surface.config_file
    raw = file_path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}

    if surface.mutation_type == "numeric_step":
        new_value = _next_numeric_value(surface)
        if new_value == old_value:
            return old_value  # at boundary, no mutation possible
        _set_nested(data, surface.yaml_key, new_value)
        surface.current_value = new_value
        # Normalize composite weights if this is an autoresearch weight
        if surface.config_file == "autoresearch.yaml" and "composite_weights" in surface.yaml_key:
            _normalize_composite_weights(data)
    elif surface.mutation_type == "template_variant":
        new_index = (surface.variant_index + 1) % len(surface.variants)
        new_value = surface.variants[new_index]
        data[surface.yaml_key] = new_value
        surface.current_value = new_value
        surface.variant_index = new_index
    else:
        raise ValueError(f"Unknown mutation type: {surface.mutation_type}")

    _write_yaml(file_path, data)
    return old_value


def revert_mutation(surface: ConfigSurface, old_value: Any, configs_dir: Path) -> None:
    """Revert a mutation by restoring the old value exactly."""
    file_path = configs_dir / surface.config_file
    raw = file_path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw) or {}
    _set_nested(data, surface.yaml_key, old_value)
    surface.current_value = old_value
    # For template variants, find the matching index
    if surface.mutation_type == "template_variant" and surface.variants:
        for i, v in enumerate(surface.variants):
            if v.strip() == str(old_value).strip():
                surface.variant_index = i
                break
    _write_yaml(file_path, data)


def describe_mutation(surface: ConfigSurface) -> str:
    """Describe what the next mutation would do."""
    if surface.mutation_type == "numeric_step":
        new_val = _next_numeric_value(surface)
        if new_val == surface.current_value:
            return f"{surface.name}: {surface.current_value} (at boundary, skip)"
        return f"{surface.name}: {surface.current_value} -> {new_val}"
    elif surface.mutation_type == "template_variant":
        new_index = (surface.variant_index + 1) % len(surface.variants)
        labels = ["variant_a", "variant_b", "variant_c"]
        old_label = labels[surface.variant_index] if surface.variant_index < len(labels) else f"variant_{surface.variant_index}"
        new_label = labels[new_index] if new_index < len(labels) else f"variant_{new_index}"
        return f"{surface.name}: {old_label} -> {new_label}"
    return f"{surface.name}: unknown mutation"


def _next_numeric_value(surface: ConfigSurface) -> Any:
    """Compute the next value for a numeric surface (increment by step)."""
    new_val = surface.current_value + surface.step_size
    if surface.max_val is not None and new_val > surface.max_val:
        # Try decrementing instead
        alt = surface.current_value - surface.step_size
        if surface.min_val is not None and alt < surface.min_val:
            return surface.current_value  # at boundary
        return alt
    return new_val


def _set_nested(data: dict[str, Any], key: str, value: Any) -> None:
    """Set a value in a dict, supporting dotted keys like 'sender_type_boost_map.internal'."""
    parts = key.split(".")
    if len(parts) == 1:
        data[key] = value
    else:
        obj = data
        for part in parts[:-1]:
            obj = obj.setdefault(part, {})
        obj[parts[-1]] = value


def _write_yaml(path: Path, data: dict[str, Any]) -> None:
    """Write YAML preserving block scalar style for multi-line strings."""
    path.write_text(
        yaml.dump(data, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120),
        encoding="utf-8",
    )
