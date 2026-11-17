#!/usr/bin/env python3
"""CLI to maintain a stock's PostgreSQL-backed valuation-model tracking table.

Thin wrapper over ``tracking_store`` (alpha_data, shared/data schema §16). Each
stock's fields are its own modeling variables — the primary-anchor inputs
(远期净利 / 远期收入 / 中周期 ROE / 管线节点 …), main-line connection strength,
and the 2–5 quantifiable catalyst points from the up/down-revision conditions.
Every ``set`` appends a dated entry; same-day re-runs replace that date's row,
older dates are never rewritten (append-only history).

This script performs no analysis — field choice and values come from the agent
per SKILL.md §2.5; here we only validate + persist + print JSON summaries.

Commands:
  init   <ts_code> --name 贵州茅台 [--anchor PE]
  set    <ts_code> --field fy2026_np --value "96–100" [--label "2026E 归母净利"]
         [--group 盈利预测] [--unit 亿元] [--sort 10] [--date YYYY-MM-DD]
         [--note ...] [--source ...] [--confidence 高|中|低] [--name 贵州茅台]
  retire <ts_code> --field fy2026_np
  show   <ts_code> [--field fy2026_np] [--json]
  list

DB connection comes from db_core (ALPHA_PG_URL / default alpha_user@/alpha_data
over the /tmp socket). Tables self-create on first write (ensure_schema).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Make db_core / tracking_store importable in the canonical repo (before AND
# after sync) and in the installed skill — mirror tracking_store's bootstrap.
_SCRIPT_DIR = Path(__file__).resolve().parent
_BUNDLED_SHARED = _SCRIPT_DIR / "_shared"
_DEV_SHARED_ROOT = _SCRIPT_DIR.parents[2] / "shared"
_SHARED_PATHS = [
    str(p)
    for p in (_SCRIPT_DIR, _DEV_SHARED_ROOT / "data", _BUNDLED_SHARED, _DEV_SHARED_ROOT)
    if p.exists()
]
sys.path[:0] = [p for p in _SHARED_PATHS if p not in sys.path]

import tracking_store as ts  # noqa: E402  (also wires db_core onto sys.path)
from db_core import close_pool, get_connection  # noqa: E402


def _emit(payload: Dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2, default=str))


def cmd_init(args) -> int:
    with get_connection() as conn:
        ts.ensure_schema(conn)
        existed = ts.get_meta(conn, args.ts_code) is not None
        ts.upsert_meta(conn, args.ts_code, args.name, args.anchor or None)
    _emit({
        "action": "init",
        "ts_code": args.ts_code,
        "name": args.name,
        "anchor": args.anchor or None,
        "status": "updated" if existed else "created",
    })
    return 0


def cmd_set(args) -> int:
    # Validate before opening a transaction so bad input fails cleanly.
    ts.validate_field_id(args.field)
    entry_date = ts.validate_date(args.date)
    ts.validate_confidence(args.confidence)
    if not (args.value or "").strip():
        raise ts.TrackingError("--value 不能为空")

    with get_connection() as conn:
        ts.ensure_schema(conn)
        if ts.get_meta(conn, args.ts_code) is None:
            if not args.name:
                raise ts.TrackingError(
                    f"{args.ts_code} 尚未 init；先运行 init，或在 set 时带 --name 自动建表头"
                )
            ts.upsert_meta(conn, args.ts_code, args.name, args.anchor or None)
        elif args.name or args.anchor:
            ts.upsert_meta(conn, args.ts_code, args.name, args.anchor or None)

        created = ts.upsert_field(
            conn, args.ts_code, args.field,
            label=args.label, grp=args.group, unit=args.unit, sort_key=args.sort,
        )
        status = ts.append_history(
            conn, args.ts_code, args.field,
            value=args.value, asof=entry_date, note=args.note,
            source=args.source, confidence=args.confidence,
        )
    _emit({
        "action": "set",
        "ts_code": args.ts_code,
        "field": args.field,
        "date": entry_date,
        "value": args.value.strip(),
        "field_status": "created" if created else "updated",
        "history_status": status,
    })
    return 0


def cmd_retire(args) -> int:
    with get_connection() as conn:
        ts.ensure_schema(conn)
        ts.retire_field(conn, args.ts_code, args.field)
    _emit({"action": "retire", "ts_code": args.ts_code, "field": args.field, "status": "retired"})
    return 0


def cmd_show(args) -> int:
    with get_connection() as conn:
        ts.ensure_schema(conn)
        table = ts.load_table(conn, args.ts_code)
    if table is None:
        _emit({"action": "show", "ts_code": args.ts_code, "status": "empty", "note": "无跟踪字段"})
        return 0
    fields: List[dict] = table["fields"]
    if args.field:
        fields = [f for f in fields if f["id"] == args.field]
        if not fields:
            raise ts.TrackingError(f"字段 {args.field!r} 不存在于 {args.ts_code}")
        table = {**table, "fields": fields}
    if args.json:
        _emit(table)
        return 0
    head = (f"{table.get('name') or ''} {table['ts_code']} · 主锚 {table.get('anchor') or '—'} "
            f"· 更新 {table.get('updated') or '—'} · {len(table['fields'])} 字段")
    print(head)
    for f in table["fields"]:
        hist = f["history"]
        latest = hist[-1] if hist else {}
        unit = f" {f['unit']}" if f.get("unit") else ""
        flag = "" if f["status"] == "active" else "（已退役）"
        print(f"- [{f['group']}] {f['label']}{flag} ({f['id']}): "
              f"{latest.get('value', '—')}{unit} @ {latest.get('date', '—')} · {len(hist)} 条记录")
        if args.field:
            for e in reversed(hist):
                bits = [e.get("date", "—"), e.get("value", "—")]
                if e.get("note"):
                    bits.append(e["note"])
                if e.get("source"):
                    bits.append(f"来源:{e['source']}")
                if e.get("confidence"):
                    bits.append(f"置信:{e['confidence']}")
                print("    " + " | ".join(bits))
    return 0


def cmd_list(args) -> int:
    with get_connection() as conn:
        ts.ensure_schema(conn)
        stocks = ts.list_stocks(conn)
    if args.json:
        _emit({"action": "list", "stocks": stocks})
        return 0
    if not stocks:
        print("（暂无跟踪个股）")
        return 0
    for s in stocks:
        print(f"- {s.get('name') or ''} {s['ts_code']} · 主锚 {s.get('anchor') or '—'} · "
              f"{s['active_fields']}/{s['total_fields']} 活跃字段 · 更新 {s.get('updated') or '—'}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Maintain a stock's PG-backed valuation-tracking table (append-only).")
    sub = parser.add_subparsers(dest="command", required=True)

    def with_code(p):
        p.add_argument("ts_code", help="如 600519.SH")

    p_init = sub.add_parser("init", help="登记跟踪个股（表头：公司名 + 主锚），幂等")
    with_code(p_init)
    p_init.add_argument("--name", required=True, help="公司名")
    p_init.add_argument("--anchor", default="", help="主估值锚，如 PE / PS / rNPV")
    p_init.set_defaults(func=cmd_init)

    p_set = sub.add_parser("set", help="给字段追加一条带日期记录（同日覆盖，跨日追加）")
    with_code(p_set)
    p_set.add_argument("--field", required=True, help="字段 id：^[a-z][a-z0-9_]{0,39}$")
    p_set.add_argument("--value", required=True, help="值，允许区间/定性，如 96–100、强连接")
    p_set.add_argument("--label", default=None, help="字段中文名；新字段首次必填")
    p_set.add_argument("--group", default=None, help="分组，如 盈利预测/估值锚/主线/催化")
    p_set.add_argument("--unit", default=None, help="单位，如 亿元/%%/倍")
    p_set.add_argument("--sort", type=int, default=None, help="排序键（小在前）")
    p_set.add_argument("--date", default=None, help="记录日期 YYYY-MM-DD，默认今天")
    p_set.add_argument("--note", default=None, help="本次变化一句话说明")
    p_set.add_argument("--source", default=None, help="依据来源，如 业绩预告/调研纪要/年报")
    p_set.add_argument("--confidence", default=None, help="高/中/低")
    p_set.add_argument("--name", default=None, help="表头不存在时带上可自动建表头")
    p_set.add_argument("--anchor", default=None, help=argparse.SUPPRESS)
    p_set.set_defaults(func=cmd_set)

    p_retire = sub.add_parser("retire", help="退役字段（保留历史，渲染置灰）")
    with_code(p_retire)
    p_retire.add_argument("--field", required=True)
    p_retire.set_defaults(func=cmd_retire)

    p_show = sub.add_parser("show", help="查看个股跟踪表；--field 看单字段完整历史")
    with_code(p_show)
    p_show.add_argument("--field", default=None)
    p_show.add_argument("--json", action="store_true", help="输出完整 JSON")
    p_show.set_defaults(func=cmd_show)

    p_list = sub.add_parser("list", help="列出所有跟踪个股")
    p_list.add_argument("--json", action="store_true")
    p_list.set_defaults(func=cmd_list)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except ts.TrackingError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 — CLI boundary: report cleanly
        print(f"error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    finally:
        close_pool()


if __name__ == "__main__":
    if sys.platform == "win32":
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
