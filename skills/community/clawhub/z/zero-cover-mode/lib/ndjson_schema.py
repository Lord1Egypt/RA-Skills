"""零稀泥模式 — ndjson schema 校验与追加 ndjson_schema.py

Usage:
    python ndjson_schema.py append <ndjson_path> '<json_record>'
    python ndjson_schema.py validate <ndjson_path>
    python ndjson_schema.py rotate <ndjson_path>
"""

import json, os, sys, re, logging, time
from datetime import datetime

from .config import NDJSON_MAX_LINES

log = logging.getLogger("ndjson")

# Pydantic 已替代手写 FixRecord.model_validate（FixRecord model_validate 执行完整校验）
from .contracts import FixRecord

REQUIRED = ["timestamp", "bug_id", "module", "bug_type", "fix_type", "blocking"]


def validate_row(row):
    """返回 (is_valid, [errors]) — 使用 Pydantic FixRecord 替代手写校验"""
    errors = []
    try:
        FixRecord(**row)
        return True, []
    except Exception as e:
        return False, [str(e)]


def _check_bug_id_dup(ndjson_path, bug_id):
    """检查 ndjson 中是否已存在相同 bug_id（直接扫描，无模块级缓存）

    P6-GLOBAL: 移除 _BUG_ID_CACHE 模块级状态，每次直接 O(n) 扫描。
    ndjson 通常 <1000 行，全量扫描耗时 <1ms。
    """
    if not bug_id or not os.path.exists(ndjson_path):
        return False
    try:
        with open(ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
            for line in f:
                try:
                    row = json.loads(line.strip())
                    if row.get("bug_id") == bug_id:
                        return True
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return False


def append_record(ndjson_path, record_dict, validate=True, strict=True, dedup_bug_id=True):
    """追加一条记录，含校验 + 自动轮转 + bug_id 去重。返回 (成功, 新行数)

    P2-REFACTOR: strict 默认改为 True。校验失败即拒绝写入，不再降级。
    调用方负责在调用前修正数据。降级写入（validate=False, strict=False）
    仅保留给 ndjson_migrate_v1_to_v2.py 等迁移脚本使用。
    """
    # P0-1: 去重检查
    if dedup_bug_id:
        bug_id = record_dict.get("bug_id")
        if bug_id and os.path.exists(ndjson_path):
            if _check_bug_id_dup(ndjson_path, bug_id):
                log.warning("重复 bug_id %s — 跳过写入（已存在）", bug_id)
                return False, 0

    if validate:
        valid, errs = validate_row(record_dict)
        if not valid:
            if strict:
                raise ValueError(f"验证失败，禁止写入: {'; '.join(errs)}")
            log.warning("校验失败 — %s", '; '.join(errs))
            log.warning("仍写入数据（标记 validated: false）")
            record_dict["validated"] = False
        else:
            record_dict["validated"] = True

    # 检查行数，自动轮转
    new_count = 1
    if os.path.exists(ndjson_path):
        with open(ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
            line_count = sum(1 for _ in f)
        if line_count >= NDJSON_MAX_LINES:
            return rotate_and_append(ndjson_path, record_dict)
        new_count = line_count + 1

    with open(ndjson_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record_dict, ensure_ascii=False) + "\n")
    return True, new_count


def rotate_and_append(ndjson_path, record_dict):
    """安全轮转 ndjson — 带轮转前备份（Phase 1 修复）"""
    from . import file_ops as _fo
    try:
        # 使用 file_ops 的安全轮转（先备份再 rename）
        rotated_path, backup_path = _fo.safe_rotate_with_backup(ndjson_path)
        log.info('ndjson rotated: %s -> %s (备份: %s)',
                 ndjson_path, rotated_path, backup_path)
    except (FileNotFoundError, RuntimeError) as e:
        log.warning('ndjson not found or rotation failed, skip rotation: %s', e)
        rotated_path = None
    except Exception as e:
        log.error('rotation 异常: %s — 尝试直接覆盖', e)
        rotated_path = None

    with open(ndjson_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(record_dict, ensure_ascii=False) + chr(10))
    return True, 1


def validate_file(ndjson_path):
    """验证整个 ndjson 文件，返回 (total, valid, invalid)"""
    if not os.path.exists(ndjson_path):
        return 0, 0, 0, 0
    total = 0
    valid = 0
    invalid = 0
    old_format = 0
    with open(ndjson_path, "r", encoding="utf-8-sig", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                invalid += 1
                continue
            ok, _ = validate_row(row)
            if ok:
                valid += 1
            else:
                invalid += 1
    return total, valid, invalid, old_format


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="ndjson schema 工具")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("append", help="追加记录")
    p.add_argument("ndjson_path", nargs="?", default="FIX_CLOSURE_LOG.ndjson")
    p.add_argument("json_record")

    p = sub.add_parser("validate", help="验证文件")
    p.add_argument("ndjson_path", nargs="?", default="FIX_CLOSURE_LOG.ndjson")

    p = sub.add_parser("rotate", help="轮转文件")
    p.add_argument("ndjson_path", nargs="?", default="FIX_CLOSURE_LOG.ndjson")

    args = parser.parse_args()

    try:
        if args.command == "append":
            record = json.loads(args.json_record)
            ok, line_count = append_record(args.ndjson_path, record, strict=True)
            print(f"OK: appended to {args.ndjson_path} (now {line_count} lines)")
        elif args.command == "validate":
            total, valid, invalid, old_format = validate_file(args.ndjson_path)
            print(f"统计: {total} 行 / {valid} 有效 / {invalid} 无效")
        elif args.command == "rotate":
            week = datetime.now().strftime("W%W")
            rotated = f"{args.ndjson_path}.{week}.ndjson"
            os.replace(args.ndjson_path, rotated)
            open(args.ndjson_path, "w", encoding="utf-8").close()
            print(f"OK: rotated to {rotated}")
    except Exception as e:
        log.error("执行失败: %s", e)
        sys.exit(1)
