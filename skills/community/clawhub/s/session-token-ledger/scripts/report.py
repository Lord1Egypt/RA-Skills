#!/usr/bin/env python3
import argparse
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DB = ROOT / "assets" / "session_tokens.db"
INDEX = ROOT / "assets" / "index.json"


def q(conn, sql, params=()):
    conn.row_factory = sqlite3.Row
    cur = conn.execute(sql, params)
    return [dict(r) for r in cur.fetchall()]


def fmt_int(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)


def fmt_float(x, digits=2):
    try:
        return f"{float(x):.{digits}f}"
    except Exception:
        return str(x)


def load_index():
    return json.loads(INDEX.read_text())


def diagnose_overall(overall_row, daily_rows, bloated_rows, hog_rows):
    bullets = []
    if overall_row:
        ratio = overall_row.get("total_input_tokens", 0) / max(overall_row.get("total_output_tokens", 1), 1)
        if ratio >= 10:
            bullets.append("最大问题不是嘴太碎，而是上下文太肥。输入/输出比已经难看了，说明大把 token 都花在背历史，不是产出新东西。")
        total = overall_row.get("total_tokens", 0)
        if total >= 1000000:
            bullets.append("总 token 已经上百万，这不是一次聊天，这是把不同工地全塞进同一辆车里。该切 session 的时候没切。")
    if bloated_rows:
        bullets.append("最该先查的是 bloated sessions 和 top context hogs。先砍最胖的，不要平均用力，那是懒人的幻觉。")
    if hog_rows:
        top = hog_rows[0]
        share = top.get("input_share_of_total", 0)
        if share >= 0.9:
            bullets.append("最肥的 session 里，九成以上 token 都是输入上下文。这种局面下继续长聊，和背着冰箱跑步差不多愚蠢。")
    if daily_rows:
        row = daily_rows[0]
        day_ratio = row.get("input_output_ratio", 0)
        if day_ratio >= 10:
            bullets.append("按天看也虚胖。要省 token，优先做三件事：一题一 session、阶段完成就 reset、先要短结论再决定要不要展开。")
    if not bullets:
        bullets.append("账面还算正常，别没病找病。")
    return bullets


def diagnose_session(meta, eff_row, bloated_row, hog_row):
    bullets = []
    if eff_row:
        ratio = eff_row.get("input_output_ratio", 0)
        entries = eff_row.get("usage_entries", 0)
        if ratio >= 15:
            bullets.append("这条 session 典型是上下文肥胖，不是回答太长。输入/输出比高得像坏账。")
        if entries and entries >= 40:
            bullets.append("回合数太多。一个主题聊成连续剧，token 自然被上下文租金吃掉。")
    if hog_row:
        share = hog_row.get("input_share_of_total", 0)
        if share >= 0.9:
            bullets.append("这条 session 基本由输入主导。继续在这条线上追加问题，只会把旧包袱越背越重。")
    if bloated_row:
        tpe = bloated_row.get("tokens_per_usage_entry", 0)
        if tpe >= 3000:
            bullets.append("每个 usage entry 平均 token 偏高，说明每轮都在背厚上下文，不够利索。")
    if meta and meta.get("cacheRead", 0) > meta.get("total", 0):
        bullets.append("cache read 远高于本轮总 token，说明这不是新信息太多，而是旧上下文在反复回放。")
    if not bullets:
        bullets.append("这条 session 看着还行，别过度治疗。")
    bullets.append("最直接的处方：收尾后开新 session，别把下一个问题继续挂在这条老轨道上。")
    return bullets


def report_overall(conn):
    overall = q(conn, "SELECT * FROM overall_summary")
    daily = q(conn, "SELECT * FROM daily_efficiency ORDER BY date DESC")
    bloated = q(conn, "SELECT * FROM bloated_sessions LIMIT 5")
    hogs = q(conn, "SELECT * FROM top_context_hogs LIMIT 5")
    out = []
    out.append("# Token Ledger Report\n")
    if overall:
        row = overall[0]
        out.append("## 老芒诊断")
        for bullet in diagnose_overall(row, daily, bloated, hogs):
            out.append(f"- {bullet}")
        out.append("")
        out.append("## Overall")
        for k, v in row.items():
            if isinstance(v, int):
                v = fmt_int(v)
            out.append(f"- **{k}**: {v}")
        out.append("")
    if daily:
        out.append("## Daily efficiency")
        for row in daily[:7]:
            parts = []
            for k, v in row.items():
                if isinstance(v, int):
                    v = fmt_int(v)
                elif isinstance(v, float):
                    v = fmt_float(v)
                parts.append(f"{k}={v}")
            out.append(f"- {' | '.join(parts)}")
        out.append("")
    if bloated:
        out.append("## Bloated sessions")
        for row in bloated:
            sid = row.get("session_id") or row.get("sessionId") or "unknown"
            total = row.get("total_tokens") or row.get("total") or "?"
            ratio = row.get("input_output_ratio") or row.get("ratio") or "?"
            out.append(f"- `{sid}` total={fmt_int(total)} ratio={fmt_float(ratio)}")
        out.append("")
    if hogs:
        out.append("## Top context hogs")
        for row in hogs:
            sid = row.get("session_id") or row.get("sessionId") or "unknown"
            share = row.get("input_share_of_total") or row.get("input_share") or "?"
            total = row.get("total_tokens") or row.get("total") or "?"
            out.append(f"- `{sid}` input_share_of_total={fmt_float(share,4)} total={fmt_int(total)}")
        out.append("")
    return "\n".join(out).strip() + "\n"


def report_session(conn, session_id):
    idx = load_index()
    meta = idx.get("sessions", {}).get(session_id)
    eff = q(conn, "SELECT * FROM usage_efficiency WHERE session_id = ?", (session_id,))
    bloated = q(conn, "SELECT * FROM bloated_sessions WHERE session_id = ?", (session_id,))
    hog = q(conn, "SELECT * FROM top_context_hogs WHERE session_id = ?", (session_id,))
    out = []
    out.append(f"# Token Session Report\n\n## Session\n- **session_id**: `{session_id}`")
    if meta:
        pass
    out.append("")
    diag = diagnose_session(meta, eff[0] if eff else None, bloated[0] if bloated else None, hog[0] if hog else None)
    out.append("## 老芒诊断")
    for bullet in diag:
        out.append(f"- {bullet}")
    out.append("")
    if meta:
        meta_fields = [
            ("date", ["date"]),
            ("start_at", ["start_at", "startAt"]),
            ("end_at", ["end_at", "endAt"]),
            ("model", ["model"]),
            ("input_tokens", ["input_tokens", "input"]),
            ("output_tokens", ["output_tokens", "output"]),
            ("total_tokens", ["total_tokens", "total"]),
            ("cache_read_tokens", ["cache_read_tokens", "cacheRead"]),
            ("ledger_file", ["ledger_file", "ledgerFile"]),
        ]
        for label, keys in meta_fields:
            value = None
            for key in keys:
                if key in meta:
                    value = meta[key]
                    break
            if value is not None:
                if isinstance(value, int):
                    value = fmt_int(value)
                out.append(f"- **{label}**: {value}")
    out.append("")
    if eff:
        out.append("## Efficiency")
        for k, v in eff[0].items():
            if isinstance(v, int):
                v = fmt_int(v)
            elif isinstance(v, float):
                v = fmt_float(v, 4)
            out.append(f"- **{k}**: {v}")
        out.append("")
    if bloated:
        out.append("## Bloated-session flags")
        for k, v in bloated[0].items():
            if isinstance(v, int):
                v = fmt_int(v)
            elif isinstance(v, float):
                v = fmt_float(v, 4)
            out.append(f"- **{k}**: {v}")
        out.append("")
    if hog:
        out.append("## Context-hog flags")
        for k, v in hog[0].items():
            if isinstance(v, int):
                v = fmt_int(v)
            elif isinstance(v, float):
                v = fmt_float(v, 4)
            out.append(f"- **{k}**: {v}")
        out.append("")
    return "\n".join(out).strip() + "\n"


def default_output_path(session_id=None):
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    slug = f"session-{session_id}" if session_id else "overall"
    out_dir = ROOT.parent / ".generated" / "session-token-ledger-reports"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"token-report-{slug}-{stamp}.md"


def main():
    ap = argparse.ArgumentParser(description="Generate markdown token-ledger reports")
    ap.add_argument("--session", help="Specific session_id to inspect")
    ap.add_argument("--output", help="Write report to file instead of stdout")
    ap.add_argument("--save", action="store_true", help="Save report under reports/ with an automatic filename")
    args = ap.parse_args()

    conn = sqlite3.connect(DB)
    try:
        text = report_session(conn, args.session) if args.session else report_overall(conn)
    finally:
        conn.close()

    if args.save and not args.output:
        args.output = str(default_output_path(args.session))

    if args.output:
        Path(args.output).write_text(text)
        print(args.output)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
