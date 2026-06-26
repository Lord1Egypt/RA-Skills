from __future__ import annotations

from .common import *

def looks_like_host_prompt(text: str) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in HOST_PROMPT_MARKERS)


def sanitize_history_text(text: str) -> str:
    lines = [line for line in text.splitlines() if not looks_like_host_prompt(line)]
    return "\n".join(lines)


def extract_history_strings(node, inherited_role: str | None = None) -> list[str]:
    if isinstance(node, str):
        if inherited_role in ALLOWED_HISTORY_ROLES and not looks_like_host_prompt(node):
            return [node]
        return []

    if isinstance(node, list):
        values: list[str] = []
        for item in node:
            values.extend(extract_history_strings(item, inherited_role))
        return values

    if isinstance(node, dict):
        node_type = normalize_name(str(node.get("type") or ""))
        if node_type == "turn-context":
            return []

        role = str(node.get("role") or inherited_role or "").lower()
        if role in {"developer", "system", "tool"}:
            return []

        values: list[str] = []
        next_role = role if role in ALLOWED_HISTORY_ROLES else inherited_role
        for key, value in node.items():
            key_norm = normalize_name(str(key))
            if key_norm in HISTORY_SKIP_FIELDS or key_norm == "role":
                continue
            values.extend(extract_history_strings(value, next_role))
        return values

    return []


def empty_usage_record() -> dict[str, object]:
    return {
        "calls": 0,
        "recent_30d_calls": None,
        "recent_90d_calls": None,
        "active_days": None,
        "first_seen_at": None,
        "last_used_at": None,
        "executions": None,
        "script_failures": None,
        "repair_turns": None,
        "reference_loads": None,
        "false_triggers": None,
    }


def sum_optional(left: int | None, right: int | None) -> int | None:
    if left is None:
        return right
    if right is None:
        return left
    return left + right


def max_optional(left: int | None, right: int | None) -> int | None:
    if left is None:
        return right
    if right is None:
        return left
    return max(left, right)


def max_optional_float(left: float | None, right: float | None) -> float | None:
    if left is None:
        return right
    if right is None:
        return left
    return max(left, right)


def merge_dates(existing: str | None, incoming: str | None, pick: str) -> str | None:
    if existing is None:
        return incoming
    if incoming is None:
        return existing
    existing_date = parse_dateish(existing)
    incoming_date = parse_dateish(incoming)
    if existing_date is None:
        return incoming
    if incoming_date is None:
        return existing
    if pick == "min":
        return min(existing_date, incoming_date).isoformat()
    return max(existing_date, incoming_date).isoformat()


def usage_record_from_mapping(mapping: dict, hint_name: str | None = None) -> tuple[str, dict[str, object]] | None:
    identity = extract_record_identity(mapping, hint_name=hint_name)
    lookup_key = record_lookup_key(identity)
    if not lookup_key:
        return None

    lowered = lowered_mapping(mapping)
    calls = coerce_int(first_present(mapping, COUNT_KEYS, lowered))
    recent_30d_calls = coerce_int(first_present(mapping, RECENT_30D_KEYS, lowered))
    recent_90d_calls = coerce_int(first_present(mapping, RECENT_90D_KEYS, lowered))
    active_days = coerce_int(first_present(mapping, ACTIVE_DAYS_KEYS, lowered))
    first_seen_at = normalize_dateish(first_present(mapping, FIRST_SEEN_KEYS, lowered))
    last_used_at = normalize_dateish(first_present(mapping, LAST_USED_KEYS, lowered))
    executions = coerce_int(first_present(mapping, EXECUTION_COUNT_KEYS, lowered))
    script_failures = coerce_int(first_present(mapping, SCRIPT_FAILURE_KEYS, lowered))
    repair_turns = coerce_int(first_present(mapping, REPAIR_TURN_KEYS, lowered))
    reference_loads = coerce_int(first_present(mapping, REFERENCE_LOAD_KEYS, lowered))
    false_triggers = coerce_int(first_present(mapping, FALSE_TRIGGER_KEYS, lowered))

    if calls is None and recent_90d_calls is not None:
        calls = recent_90d_calls
    if calls is None and recent_30d_calls is not None:
        calls = recent_30d_calls

    has_any_field = any(
        value is not None
        for value in (
            calls,
            recent_30d_calls,
            recent_90d_calls,
            active_days,
            first_seen_at,
            last_used_at,
            executions,
            script_failures,
            repair_turns,
            reference_loads,
            false_triggers,
        )
    )
    if not has_any_field:
        return None

    return (
        lookup_key,
        {
            "calls": max(0, calls or 0),
            "recent_30d_calls": recent_30d_calls,
            "recent_90d_calls": recent_90d_calls,
            "active_days": active_days,
            "first_seen_at": first_seen_at,
            "last_used_at": last_used_at,
            "executions": executions,
            "script_failures": script_failures,
            "repair_turns": repair_turns,
            "reference_loads": reference_loads,
            "false_triggers": false_triggers,
        },
    )


def merge_usage_record(store: dict[str, dict[str, object]], name: str, incoming: dict[str, object]) -> None:
    target = store.setdefault(name, empty_usage_record())
    target["calls"] = int(target.get("calls", 0)) + int(incoming.get("calls", 0) or 0)
    target["recent_30d_calls"] = sum_optional(
        coerce_int(target.get("recent_30d_calls")),
        coerce_int(incoming.get("recent_30d_calls")),
    )
    target["recent_90d_calls"] = sum_optional(
        coerce_int(target.get("recent_90d_calls")),
        coerce_int(incoming.get("recent_90d_calls")),
    )
    target["active_days"] = max_optional(
        coerce_int(target.get("active_days")),
        coerce_int(incoming.get("active_days")),
    )
    target["first_seen_at"] = merge_dates(
        target.get("first_seen_at"),  # type: ignore[arg-type]
        incoming.get("first_seen_at"),  # type: ignore[arg-type]
        "min",
    )
    target["last_used_at"] = merge_dates(
        target.get("last_used_at"),  # type: ignore[arg-type]
        incoming.get("last_used_at"),  # type: ignore[arg-type]
        "max",
    )
    for key in ("executions", "script_failures", "repair_turns", "reference_loads", "false_triggers"):
        target[key] = sum_optional(
            coerce_int(target.get(key)),
            coerce_int(incoming.get(key)),
        )


def consume_usage_node(
    node,
    usage: dict[str, dict[str, object]],
    hint_name: str | None = None,
    scalar_map: bool = False,
) -> None:
    if isinstance(node, list):
        for item in node:
            consume_usage_node(item, usage, hint_name=hint_name, scalar_map=scalar_map)
        return

    if isinstance(node, dict):
        record = usage_record_from_mapping(node, hint_name=hint_name if scalar_map else None)
        if record:
            name, payload = record
            merge_usage_record(usage, name, payload)
            return

        scalar_items = []
        for key, value in node.items():
            key_text = str(key)
            key_norm = normalize_name(key_text)
            if key_text in COLLECTION_KEYS or key_norm in COLLECTION_KEYS:
                scalar_items = []
                break
            count = coerce_int(value)
            if count is None:
                scalar_items = []
                break
            scalar_items.append((key_text, count))
        if scalar_items:
            for key_text, count in scalar_items:
                identity = {"name": normalize_name(key_text), "slug": "", "identifier": "", "source": "", "namespace": "", "path": ""}
                lookup_key = record_lookup_key(identity)
                if lookup_key:
                    merge_usage_record(usage, lookup_key, {"calls": count})
            return

        for key, value in node.items():
            key_text = str(key)
            key_norm = normalize_name(key_text)
            next_scalar_map = scalar_map or key_text in SCALAR_MAP_KEYS or key_norm in SCALAR_MAP_KEYS
            child_hint = hint_name
            if not next_scalar_map and isinstance(value, dict) and key_text not in COLLECTION_KEYS and key_norm not in COLLECTION_KEYS:
                nested_record = usage_record_from_mapping(value, hint_name=key_text)
                if nested_record:
                    name, payload = nested_record
                    merge_usage_record(usage, name, payload)
                    continue
            if next_scalar_map and key_text not in COLLECTION_KEYS and key_norm not in COLLECTION_KEYS:
                child_hint = key_text
            consume_usage_node(value, usage, hint_name=child_hint, scalar_map=next_scalar_map)
        return

    if scalar_map and hint_name is not None:
        count = coerce_int(node)
        if count is None:
            return
        identity = {"name": normalize_name(hint_name), "slug": "", "identifier": "", "source": "", "namespace": "", "path": ""}
        lookup_key = record_lookup_key(identity)
        if lookup_key:
            merge_usage_record(usage, lookup_key, {"calls": count})


def load_usage_csv(path: Path) -> dict[str, dict[str, object]]:
    usage: dict[str, dict[str, object]] = {}
    delimiter = "\t" if path.suffix.lower() == ".tsv" else ","
    with path.open("r", encoding="utf-8", errors="replace", newline="") as handle:
        reader = csv.DictReader(handle, delimiter=delimiter)
        for row in reader:
            record = usage_record_from_mapping(row)
            if record is None:
                continue
            name, payload = record
            merge_usage_record(usage, name, payload)
    return usage


def load_usage_json(path: Path) -> dict[str, dict[str, object]]:
    usage: dict[str, dict[str, object]] = {}
    payload = load_json_or_jsonl(path)
    consume_usage_node(payload, usage)
    return usage


def load_usage(paths: list[Path]) -> dict[str, dict[str, object]]:
    usage: dict[str, dict[str, object]] = {}
    for path in paths:
        if not path.exists():
            continue
        if path.suffix.lower() in {".csv", ".tsv"}:
            parsed = load_usage_csv(path)
        else:
            parsed = load_usage_json(path)
        for key, value in parsed.items():
            merge_usage_record(usage, key, value)
    return usage


def infer_usage_from_history(paths: list[Path], skill_names: list[str]) -> dict[str, dict[str, object]]:
    usage = {
        f"name:{name}": {"calls": 0, "history_mentions": 0, "suspected_invocations": 0}
        for name in skill_names
    }
    patterns = {}
    for name in skill_names:
        alias_pattern = re.escape(name).replace(r"\-", r"[-\s_]?")
        patterns[f"name:{name}"] = re.compile(
            rf"(?<![a-z0-9])\$?{alias_pattern}(?![a-z0-9])",
            re.IGNORECASE,
        )
    for path in paths:
        if not path.exists():
            continue
        if path.suffix.lower() in {".json", ".jsonl"}:
            try:
                payload = load_json_or_jsonl(path)
                text = "\n".join(extract_history_strings(payload)).lower()
            except json.JSONDecodeError:
                text = sanitize_history_text(read_text(path)).lower()
        else:
            text = sanitize_history_text(read_text(path)).lower()
        for name, pattern in patterns.items():
            mentions = len(pattern.findall(text))
            usage[name]["history_mentions"] = int(usage[name]["history_mentions"]) + mentions
            usage[name]["suspected_invocations"] = int(usage[name]["suspected_invocations"]) + mentions
    return usage
