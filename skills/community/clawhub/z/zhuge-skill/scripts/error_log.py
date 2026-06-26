"""
错误日志 — append-only JSONL

用法（from 其它脚本）：
    from scripts.error_log import log_error
    try:
        ...
    except Exception as e:
        log_error(category="fetch_data", exc=e, context={"match": match_name})
        raise  # 或继续降级流程

查看最近错误：
    python scripts/stats.py --errors
"""
import json
import os
import random
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG_PATH = ROOT / "data" / "errors.jsonl"


def _new_id() -> str:
    date = datetime.now(timezone.utc).strftime("%Y%m%d")
    suffix = "".join(random.choice("0123456789ABCDEF") for _ in range(3))
    return f"ERR-{date}-{suffix}"


def _infer_priority(exc: BaseException, category: str) -> str:
    """根据异常类型 + category 给一个默认 priority"""
    name = type(exc).__name__.lower()
    cat = category.lower()
    if any(k in name for k in ("timeout", "connection", "authentication")):
        return "high"
    if any(k in cat for k in ("loop", "backfill")):
        return "high"
    if any(k in name for k in ("value", "keyerror", "typeerror", "attribute")):
        return "medium"
    return "medium"


def log_error(category: str, exc: BaseException, context: dict | None = None,
              priority: str | None = None) -> str:
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "id": _new_id(),
        "logged": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "category": category,
        "exc_type": type(exc).__name__,
        "summary": str(exc)[:200],
        "priority": priority or _infer_priority(exc, category),
        "status": "pending",
        "context": context or {},
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return entry["id"]


def resolve_error(error_id: str, note: str = "") -> bool:
    """把某条错误标记为 resolved（改写整个文件）"""
    if not LOG_PATH.exists():
        return False
    updated = False
    out_lines = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            e = json.loads(line)
        except Exception:
            out_lines.append(line)
            continue
        if e.get("id") == error_id:
            e["status"] = "resolved"
            e["resolved_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
            if note:
                e["resolve_note"] = note
            updated = True
        out_lines.append(json.dumps(e, ensure_ascii=False))
    if updated:
        LOG_PATH.write_text("\n".join(out_lines) + "\n", encoding="utf-8")
    return updated


def load_errors(limit: int = 10) -> list[dict]:
    if not LOG_PATH.exists():
        return []
    lines = LOG_PATH.read_text(encoding="utf-8").splitlines()
    out = []
    for line in lines[-limit:]:
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


def summarize_recent(limit: int = 10, status: str | None = None) -> str:
    errors = load_errors(limit * 3)  # 多拿一些，按 status 过滤后再截断
    if status:
        errors = [e for e in errors if e.get("status") == status]
    errors = errors[-limit:]
    if not errors:
        return f"  暂无{status or ''}错误记录。\n"
    lines = [f"  最近 {len(errors)} 条错误（data/errors.jsonl）:\n"]
    for e in errors:
        ts = e.get("logged", "?")[:19]
        cat = e.get("category", "?")
        exc_type = e.get("exc_type", "?")
        summary = e.get("summary", "")[:100]
        prio = e.get("priority", "?")
        st = e.get("status", "pending")
        ctx_brief = ""
        ctx = e.get("context") or {}
        if ctx:
            ctx_brief = " " + " ".join(f"{k}={v}" for k, v in list(ctx.items())[:3])
        st_tag = f"[{st}]" if st != "pending" else ""
        lines.append(f"  · [{e.get('id','?')}] {ts}  {prio}/{cat}/{exc_type}{st_tag}{ctx_brief}")
        lines.append(f"    {summary}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--demo", action="store_true", help="写一条自测错误")
    p.add_argument("--resolve", metavar="ERR_ID", help="把指定 ID 标为 resolved")
    p.add_argument("--note", default="", help="搭配 --resolve 一起用，附带解决说明")
    p.add_argument("--status", default=None,
                   help="只看特定 status 的条目（pending / resolved）")
    p.add_argument("--limit", type=int, default=10)
    args = p.parse_args()

    if args.demo:
        try:
            raise RuntimeError("demo error — self-test")
        except Exception as e:
            eid = log_error("self_test", e, {"demo": True})
            print(f"logged {eid}")

    if args.resolve:
        ok = resolve_error(args.resolve, args.note)
        if ok:
            print(f"✓ {args.resolve} 已标记为 resolved")
        else:
            print(f"✗ 没找到 ID={args.resolve}")
        sys.exit(0 if ok else 1)

    print(summarize_recent(limit=args.limit, status=args.status))
