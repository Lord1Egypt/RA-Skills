from __future__ import annotations

from .common import *

def normalize_verdict(value) -> str:
    if value is None:
        return ""
    lowered = str(value).strip().lower()
    return VERDICT_ALIASES.get(lowered, lowered)


def pick_arm(entry: dict, keys: tuple[str, ...]) -> dict:
    lowered = lowered_mapping(entry)
    for key in keys:
        value = entry.get(key)
        if isinstance(value, dict):
            return value
    for key in keys:
        value = lowered.get(key.lower())
        if isinstance(value, dict):
            return value
    return {}


def flat_metric(entry: dict, keys: tuple[str, ...], coercer):
    value = first_present(entry, keys, lowered_mapping(entry))
    return coercer(value)


def ablation_items_from_node(node, items: list[dict]) -> None:
    if isinstance(node, list):
        for item in node:
            ablation_items_from_node(item, items)
        return
    if not isinstance(node, dict):
        return

    has_name = first_present(node, NAME_KEYS) is not None
    has_verdict = first_present(node, ("verdict", "结果", "结论")) is not None
    has_arms = pick_arm(node, WITH_SKILL_KEYS) or pick_arm(node, WITHOUT_SKILL_KEYS)
    has_flat_metrics = (
        first_present(node, FLAT_WITH_SCORE_KEYS + FLAT_WITHOUT_SCORE_KEYS) is not None
        or first_present(node, FLAT_WITH_PASS_KEYS + FLAT_WITHOUT_PASS_KEYS) is not None
    )
    if has_name and (has_verdict or has_arms or has_flat_metrics):
        items.append(node)
        return

    for value in node.values():
        ablation_items_from_node(value, items)


def load_ablation(paths: list[Path]) -> dict[str, dict[str, float]]:
    by_skill: dict[str, list[dict]] = {}
    for path in paths:
        if not path.exists():
            continue
        payload = load_json_or_jsonl(path)
        items: list[dict] = []
        ablation_items_from_node(payload, items)
        for item in items:
            if not isinstance(item, dict):
                continue
            identity = extract_record_identity(item)
            lookup_key = record_lookup_key(identity)
            if not lookup_key:
                continue
            by_skill.setdefault(lookup_key, []).append(item)

    summary: dict[str, dict[str, float]] = {}
    for name, items in by_skill.items():
        same_count = 0
        better_count = 0
        worse_count = 0
        deltas: list[float] = []
        for item in items:
            verdict = normalize_verdict(first_present(item, ("verdict", "结果", "结论")))
            with_arm = pick_arm(item, WITH_SKILL_KEYS)
            without_arm = pick_arm(item, WITHOUT_SKILL_KEYS)
            with_pass = coerce_bool(first_present(with_arm, ("pass", "passed", "success", "结果", "通过")))
            without_pass = coerce_bool(first_present(without_arm, ("pass", "passed", "success", "结果", "通过")))
            with_score = coerce_float(first_present(with_arm, ("score", "quality", "quality_score", "分数", "质量分")))
            without_score = coerce_float(first_present(without_arm, ("score", "quality", "quality_score", "分数", "质量分")))
            if with_pass is None:
                with_pass = flat_metric(item, FLAT_WITH_PASS_KEYS, coerce_bool)
            if without_pass is None:
                without_pass = flat_metric(item, FLAT_WITHOUT_PASS_KEYS, coerce_bool)
            if with_score is None:
                with_score = flat_metric(item, FLAT_WITH_SCORE_KEYS, coerce_float)
            if without_score is None:
                without_score = flat_metric(item, FLAT_WITHOUT_SCORE_KEYS, coerce_float)

            delta = None
            if with_score is not None and without_score is not None:
                delta = with_score - without_score
            elif with_pass is not None and without_pass is not None:
                delta = float(with_pass) - float(without_pass)
            if delta is not None:
                deltas.append(delta)

            if verdict == "same":
                same_count += 1
                continue
            if verdict == "better":
                better_count += 1
                continue
            if verdict == "worse":
                worse_count += 1
                continue

            if delta is None:
                if with_pass is not None and without_pass is not None and with_pass == without_pass:
                    same_count += 1
                continue

            if abs(delta) < 0.05:
                same_count += 1
            elif delta > 0:
                better_count += 1
            else:
                worse_count += 1

        total = len(items)
        summary[name] = {
            "cases": float(total),
            "consistency_rate": same_count / total if total else 0.0,
            "better_rate": better_count / total if total else 0.0,
            "worse_rate": worse_count / total if total else 0.0,
            "avg_delta": sum(deltas) / len(deltas) if deltas else 0.0,
        }
    return summary
