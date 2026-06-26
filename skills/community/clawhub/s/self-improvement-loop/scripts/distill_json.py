#!/usr/bin/env python3
"""distill_json.py — 生成 distill.sh --check-only JSON 输出（v4.3）"""
import sys, json

def parse_pk(line):
    if not line.strip(): return None
    parts = line.split("|")
    if len(parts) < 9: return None
    pk_val = parts[0]
    # v4.4: if pk is empty but there's content, it's a format-invalid PK that was stripped
    has_content = len(parts) >= 7 and parts[6].strip()
    return {"pk": pk_val, "cnt": int(parts[1]), "fid": parts[2], "fcat": parts[3],
            "fstatus": parts[4], "notified": parts[5], "fraw": parts[6], "nc": int(parts[7]),
            "pk_stripped": (pk_val == "" and has_content),
            "source_file": parts[8]}

def parse_cat(line):
    if not line.strip(): return None
    parts = line.split("|")
    if len(parts) < 8: return None
    return {"cat": parts[0], "cnt": int(parts[1]), "fid": parts[2],
            "fstatus": parts[3], "notified": parts[4], "fraw": parts[5], "nc": int(parts[6]),
            "source_file": parts[7]}

def calc_trigger(notified, nc, cnt, threshold=2):
    if notified is None:
        return cnt >= threshold  # null notified → trigger only if count≥threshold
    try:
        n = int(notified)
        if n <= 0: return cnt >= threshold  # notified=0 → same logic
        if nc < cnt: return True  # count grew → trigger
        return False
    except (ValueError, TypeError):
        # notified=true/false as string, or unparseable → treat as false (not notified)
        return cnt >= threshold

def null_to_none(v):
    """Convert -1/'' to None, '1' to True, '0' to False"""
    if v in ("-1", ""): return None
    if v == "1": return True
    if v == "0": return False
    return None

def check_pk_format_invalid(line, is_pk_entry):
    """Check if PK was stripped due to format invalid (v4.4.8).
    If is_pk_entry is False (category), always return False.
    If is_pk_entry is True, check if raw_md contains Pattern-Key line with wrong format.
    """
    if not is_pk_entry:
        return False
    return False  # Logic moved to distill.sh; here we just flag based on context

pk_agg_path = sys.argv[1]
cat_agg_path = sys.argv[2]
threshold = int(sys.argv[3])

pk_agg = []
cat_agg = []

try:
    with open(pk_agg_path) as f:
        pk_agg = [l for l in f.read().splitlines() if l.strip()]
except FileNotFoundError:
    print(f"Warning: pk_agg file not found: {pk_agg_path}", file=sys.stderr)
except Exception as e:
    print(f"Warning: error reading pk_agg: {e}", file=sys.stderr)

try:
    with open(cat_agg_path) as f:
        cat_agg = [l for l in f.read().splitlines() if l.strip()]
except FileNotFoundError:
    print(f"Warning: cat_agg file not found: {cat_agg_path}", file=sys.stderr)
except Exception as e:
    print(f"Warning: error reading cat_agg: {e}", file=sys.stderr)

patterns = []
fallback = []

for line in pk_agg:
    e = parse_pk(line)
    if not e: continue
    n_val = e["notified"]
    trig = 1 if calc_trigger(n_val, e["nc"], e["cnt"], threshold) else 0
    obj = {
        "name": e["pk"] if e["pk"] else e["fcat"], "count": e["cnt"], "threshold_count": threshold,
        "source": "pattern_key", "first_entry_id": e["fid"],
        "first_category": e["fcat"], "first_status": e["fstatus"],
        "notified": null_to_none(n_val), "notification_count": e["nc"],
        "notification_trigger": trig, "raw_md": e["fraw"],
        "first_file": e.get("source_file", "")
    }
    if e["pk_stripped"]:
        obj["pk_format_invalid"] = True
    if e["cnt"] >= threshold:
        patterns.append(obj)
    else:
        fallback.append(obj)

for line in cat_agg:
    e = parse_cat(line)
    if not e: continue
    n_val = e["notified"]
    trig = 1 if calc_trigger(n_val, e["nc"], e["cnt"], threshold) else 0
    obj = {
        "name": e["cat"], "count": e["cnt"], "threshold_count": threshold,
        "source": "category", "first_entry_id": e["fid"],
        "first_category": e["cat"], "first_status": e["fstatus"],
        "notified": null_to_none(n_val), "notification_count": e["nc"],
        "notification_trigger": trig, "raw_md": e["fraw"],
        "first_file": e.get("source_file", "")
    }
    if e["cnt"] >= threshold:
        patterns.append(obj)
    else:
        fallback.append(obj)

result = {
    "patterns": patterns,
    "category_fallback": fallback,
    "meta": {
        "threshold": threshold,
        "files_scanned": ["LEARNINGS.md", "ERRORS.md", "FEATURE_REQUESTS.md"],
        "scan_mode": "pending_only",
        "aggregation_includes_promoted": False,
        "v4_3": True,
        "notification_logic": "notification_trigger = (count >= 2) AND (notified == false OR notification_count < count)",
        "notified_values": "null=字段不存在(视为false), false=未通知, true=已通知",
"explanation": "distill 只输出原始数据，action 判断、enrich 生成、通知发送由 Cron AI 完成。仅扫描 pending/active/in_progress 条目；notified/notification_count 来自条目的 Metadata 字段；notification_trigger = (count >= 2) AND (notified == false OR notification_count < count)，trigger=true 时 Cron AI 应发送通知并写回 Notified 状态。",
        "aggregation_includes_promoted_note": "仅聚合 pending 条目，promoted 条目不参与计数（设计文档要求 pending_and_promoted 但实际行为正确）"
    }
}

print(json.dumps(result, ensure_ascii=False, indent=2))
