"""零稀泥模式 — ndjson 迁移脚本 ndjson_migrate_v1_to_v2.py

修复 FIX_CLOSURE_LOG.ndjson 中旧格式记录的兼容性问题。

迁移内容:
- bug_types (array) -> bug_type (string) + bug_type_secondary
- 缺失 bug_type -> 从 details/root_cause 推理
- 缺失 blocking -> false
- 微秒时间戳 -> 截断到秒
- fix_type "comprehensive" -> "permanent" + legacy_fix_type

Usage:
    python lib/ndjson_migrate_v1_to_v2.py <ndjson_path> [--in-place]
"""

import json, sys, os, re, logging
from datetime import datetime

from . import setup_logging as _setup_log
_setup_log(logging.WARNING)

log = logging.getLogger("migrate")


def infer_bug_type(row):
    """从其他字段推理 bug_type"""
    details = (row.get("details", "") or "") + (row.get("root_cause", "") or "")
    d = details.lower()
    if "config" in d or "hardcode" in d or "path" in d:
        return "config_error"
    if "type" in d or "mismatch" in d or "key" in d:
        return "type_mismatch"
    if "logic" in d or "break" in d or "flow" in d or "ignore" in d:
        return "logic_error"
    if "encoding" in d or "corrupt" in d:
        return "data_corruption"
    if "leak" in d or "source" in d:
        return "resource_leak"
    if "edge" in d or "ipv6" in d or "boundary" in d:
        return "edge_case"
    if "syntax" in d or "parse" in d:
        return "syntax_error"
    if "perform" in d or "cache" in d:
        return "performance"
    if "dead" in d or "orphan" in d or "clean" in d:
        return "dead_code"
    return "unknown"


def migrate_record(row):
    """迁移单条记录格式"""
    migrated = False
    result = dict(row)

    # 1. bug_types (array) -> bug_type (string)
    if "bug_types" in result and isinstance(result["bug_types"], list):
        bts = result["bug_types"]
        if bts:
            result["bug_type"] = bts[0]
            if len(bts) > 1:
                result["bug_type_secondary"] = bts[1:]
        result.pop("bug_types", None)
        migrated = True

    # 2-3. 缺失 bug_type
    if not result.get("bug_type") or result.get("bug_type") is None:
        result["bug_type"] = infer_bug_type(result)
        migrated = True

    # 4. 缺失 blocking
    if "blocking" not in result:
        result["blocking"] = False
        migrated = True

    # 5. 微秒时间戳 -> 截断
    ts = result.get("timestamp", "")
    if isinstance(ts, str) and "." in ts:
        try:
            dt = datetime.fromisoformat(ts)
            result["timestamp"] = dt.strftime("%Y-%m-%dT%H:%M:%S") + "+08:00"
            migrated = True
        except ValueError:
            pass

    # 6. fix_type "comprehensive"
    if result.get("fix_type") == "comprehensive":
        result["fix_type"] = "permanent"
        result["legacy_fix_type"] = "comprehensive"
        migrated = True

    if migrated:
        result["migrated"] = True
    return result


# P2-4: 有序输出字段，便于人工阅读 ndjson
_FIELD_ORDER = ["timestamp", "bug_id", "module", "bug_type", "root_cause",
               "fix_type", "test_count", "regression_pass", "regression_fail",
               "blocking", "details", "vcs_hash", "test_skipped",
               "migrated", "legacy_fix_type", "bug_type_secondary",
               "validated"]


def _ordered_dumps(record):
    """按 FIELD_ORDER 排序输出，剩余字段追加"""
    ordered = {}
    for field in _FIELD_ORDER:
        if field in record:
            ordered[field] = record[field]
    # 追加不在 FIELD_ORDER 中的字段
    for k, v in record.items():
        if k not in _FIELD_ORDER:
            ordered[k] = v
    return json.dumps(ordered, ensure_ascii=False)


def migrate_file(input_path, in_place=False):
    """迁移文件"""
    if not os.path.exists(input_path):
        log.error("文件不存在: %s", input_path)
        return False

    output_path = input_path + ".v2"

    with open(input_path, "r", encoding="utf-8-sig", errors="replace") as f:
        lines = [l.strip() for l in f if l.strip()]

    migrated = []
    total = len(lines)
    fix_count = 0
    stats = {"missing_bug_type": 0, "array_bug_type": 0,
             "missing_blocking": 0, "microsecond_ts": 0,
             "comprehensive_fix": 0}

    for i, line in enumerate(lines):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            log.warning("第 %d 行 JSON 损坏，保留原样", i + 1)
            migrated.append(line)
            continue

        before = dict(row)
        after = migrate_record(row)
        if after.get("migrated"):
            fix_count += 1
            if "bug_type" not in before or before.get("bug_type") is None:
                stats["missing_bug_type"] += 1
            if "bug_types" in before:
                stats["array_bug_type"] += 1
            if "blocking" not in before:
                stats["missing_blocking"] += 1
            ts = before.get("timestamp", "")
            if isinstance(ts, str) and "." in ts:
                stats["microsecond_ts"] += 1
            if before.get("fix_type") == "comprehensive":
                stats["comprehensive_fix"] += 1
        migrated.append(_ordered_dumps(after))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(migrated) + "\n")

    print(f"迁移完成:")
    print(f"  总记录: {total}")
    print(f"  已迁移: {fix_count}")
    for k, v in stats.items():
        print(f"    {k}: {v}")

    if in_place:
        os.replace(output_path, input_path)
        print(f"  原地替换: {input_path}")
    else:
        print(f"  输出: {output_path}")
    return True


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ndjson v1->v2 迁移")
    parser.add_argument("ndjson_path", help="ndjson 文件路径")
    parser.add_argument("--in-place", action="store_true",
                        help="原地替换文件")
    args = parser.parse_args()

    success = migrate_file(args.ndjson_path, in_place=args.in_place)
    sys.exit(0 if success else 1)
