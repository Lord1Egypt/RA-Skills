#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 本地用量统计（只读）。

数据来源：~/.workbuddy-ai/workbuddy.db
  - sessions      会话元信息（标题 / 模型 / 时间）
  - session_usage 每会话 token 用量（used / size）与积分明细（credit_json）

为了不在客户端运行时干扰数据库（WAL 模式），先把 db / -wal / -shm 复制到临时目录再只读打开。

用法：
  python usage_report.py                # 输出摘要 + 生成 HTML 看板
  python usage_report.py --json         # 只输出 JSON
  python usage_report.py -o out.html    # 指定 HTML 输出路径
"""

import argparse
import json
import os
import shutil
import sqlite3
import sys
import tempfile
import time
from datetime import datetime, timedelta

HOME = os.path.expanduser("~")
DATA_DIR = os.environ.get("WB_DATA_DIR") or os.path.join(HOME, ".workbuddy-ai")
DB_NAME = "workbuddy.db"


# ---------------------------------------------------------------- 数据读取
def open_readonly_snapshot():
    """复制数据库快照并只读打开，避免锁库。"""
    src = os.path.join(DATA_DIR, DB_NAME)
    if not os.path.exists(src):
        raise SystemExit(f"找不到数据库：{src}")

    tmpdir = tempfile.mkdtemp(prefix="wb-usage-")
    dst = os.path.join(tmpdir, DB_NAME)
    shutil.copy2(src, dst)
    for suffix in ("-wal", "-shm"):
        p = src + suffix
        if os.path.exists(p):
            try:
                shutil.copy2(p, dst + suffix)
            except OSError:
                pass
    return sqlite3.connect(dst), tmpdir


def ts_to_dt(value):
    """兼容秒 / 毫秒时间戳。"""
    if value is None:
        return None
    v = float(value)
    if v > 1e11:  # 毫秒
        v /= 1000.0
    return datetime.fromtimestamp(v)


def table_columns(conn, table):
    try:
        return [d[0] for d in conn.execute(f"select * from {table} limit 1").description]
    except sqlite3.Error:
        return []


def load_sessions(conn):
    cols = table_columns(conn, "sessions")
    if not cols:
        return {}
    wanted = [c for c in ("id", "title", "custom_title", "model", "created_at",
                          "updated_at", "last_activity_at", "context_window",
                          "deleted_at", "cwd") if c in cols]
    sql = "select " + ", ".join(wanted) + " from sessions"
    out = {}
    for row in conn.execute(sql):
        rec = dict(zip(wanted, row))
        out[rec["id"]] = rec
    return out


def load_usage(conn):
    cols = table_columns(conn, "session_usage")
    if not cols:
        return []
    out = []
    for row in conn.execute(
        "select session_id, used, size, updated_at, credit_json from session_usage"
    ):
        sid, used, size, updated_at, credit_json = row
        credits = 0.0
        requests = 0
        if credit_json:
            try:
                detail = json.loads(credit_json)
                if isinstance(detail, dict):
                    requests = len(detail)
                    for v in detail.values():
                        if isinstance(v, (int, float)):
                            credits += float(v)
                elif isinstance(detail, list):
                    requests = len(detail)
            except (ValueError, TypeError):
                pass
        out.append({
            "session_id": sid,
            "used": int(used or 0),
            "size": int(size or 0),
            "updated_at": updated_at,
            "credits": round(credits, 2),
            "requests": requests,
        })
    return out


# ---------------------------------------------------------------- 聚合
def build_report():
    conn, tmpdir = open_readonly_snapshot()
    try:
        sessions = load_sessions(conn)
        usage = load_usage(conn)
    finally:
        conn.close()
        shutil.rmtree(tmpdir, ignore_errors=True)

    rows = []
    for u in usage:
        s = sessions.get(u["session_id"], {})
        created = ts_to_dt(s.get("created_at")) or ts_to_dt(u["updated_at"])
        last = ts_to_dt(u["updated_at"]) or created
        used, size = u["used"], u["size"]
        rows.append({
            "session_id": u["session_id"],
            "short_id": u["session_id"][:8],
            "title": (s.get("custom_title") or s.get("title") or "(未命名会话)")[:40],
            "model": s.get("model") or "unknown",
            "date": created.strftime("%Y-%m-%d") if created else "unknown",
            "created": created.isoformat(timespec="seconds") if created else None,
            "last_active": last.isoformat(timespec="seconds") if last else None,
            "used": used,
            "size": size,
            "percent": round(used / size * 100, 1) if size else 0.0,
            "credits": u["credits"],
            "requests": u["requests"],
            "deleted": bool(s.get("deleted_at")),
        })
    rows.sort(key=lambda r: r["last_active"] or "", reverse=True)

    total_tokens = sum(r["used"] for r in rows)
    total_credits = round(sum(r["credits"] for r in rows), 2)
    total_requests = sum(r["requests"] for r in rows)

    by_day = {}
    for r in rows:
        d = by_day.setdefault(r["date"], {"date": r["date"], "tokens": 0,
                                          "credits": 0.0, "sessions": 0})
        d["tokens"] += r["used"]
        d["credits"] = round(d["credits"] + r["credits"], 2)
        d["sessions"] += 1

    by_model = {}
    for r in rows:
        m = by_model.setdefault(r["model"], {"model": r["model"], "tokens": 0,
                                             "credits": 0.0, "sessions": 0})
        m["tokens"] += r["used"]
        m["credits"] = round(m["credits"] + r["credits"], 2)
        m["sessions"] += 1

    today = datetime.now().strftime("%Y-%m-%d")
    week_ago = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "data_dir": DATA_DIR,
        "totals": {
            "tokens": total_tokens,
            "credits": total_credits,
            "sessions": len(rows),
            "requests": total_requests,
            "avg_tokens": int(total_tokens / len(rows)) if rows else 0,
            "today_tokens": sum(r["used"] for r in rows if r["date"] == today),
            "week_tokens": sum(r["used"] for r in rows if r["date"] >= week_ago),
        },
        "sessions": rows,
        "by_day": sorted(by_day.values(), key=lambda x: x["date"]),
        "by_model": sorted(by_model.values(), key=lambda x: -x["tokens"]),
    }


# ---------------------------------------------------------------- 输出
def fmt_num(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def print_summary(rep):
    t = rep["totals"]
    print(f"数据来源：{rep['data_dir']}  (生成于 {rep['generated_at']})")
    print("-" * 56)
    print(f"累计 Token   : {t['tokens']:,}  ({fmt_num(t['tokens'])})")
    print(f"累计积分     : {t['credits']:,.2f}")
    print(f"会话数 / 请求: {t['sessions']} / {t['requests']}")
    print(f"今日 / 近7天 : {t['today_tokens']:,} / {t['week_tokens']:,} tokens")
    print("-" * 56)
    print(f"{'会话':<30}{'模型':<20}{'Token':>10}{'上下文':>8}{'积分':>9}")
    for r in rep["sessions"]:
        print(f"{r['title'][:28]:<30}{r['model'][:18]:<20}"
              f"{r['used']:>10,}{r['percent']:>7.1f}%{r['credits']:>9.2f}")


HTML_TMPL = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>WorkBuddy 用量看板</title>
<style>
  *{box-sizing:border-box;margin:0;padding:0}
  body{
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;
    background:#0d1117;color:#e6edf3;padding:28px 32px 48px;line-height:1.5;
  }
  .wrap{max-width:1180px;margin:0 auto}
  header{display:flex;align-items:flex-end;justify-content:space-between;
    border-bottom:1px solid #21262d;padding-bottom:16px;margin-bottom:24px;flex-wrap:wrap;gap:8px}
  h1{font-size:21px;font-weight:600;letter-spacing:.2px}
  .sub{font-size:12px;color:#8b949e;margin-top:4px}
  .badge{font-size:11px;padding:3px 9px;border-radius:999px;border:1px solid #30363d;
    color:#8b949e;background:#161b22}
  .cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin-bottom:26px}
  .card{background:#161b22;border:1px solid #21262d;border-radius:10px;padding:16px 18px}
  .card .k{font-size:12px;color:#8b949e;margin-bottom:8px}
  .card .v{font-size:26px;font-weight:600;font-variant-numeric:tabular-nums;letter-spacing:-.5px}
  .card .u{font-size:12px;color:#6e7681;margin-left:4px;font-weight:400}
  h2{font-size:14px;font-weight:600;color:#c9d1d9;margin:26px 0 12px}
  .panel{background:#161b22;border:1px solid #21262d;border-radius:10px;padding:18px}
  .bars{display:flex;align-items:flex-end;gap:10px;height:180px;padding-top:8px}
  .bar-col{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:6px;min-width:0}
  .bar{width:100%;max-width:54px;border-radius:4px 4px 0 0;
    background:linear-gradient(180deg,#3b82f6,#1d4ed8);transition:filter .15s}
  .bar:hover{filter:brightness(1.25)}
  .bar-lb{font-size:10px;color:#6e7681;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:100%}
  .bar-v{font-size:10px;color:#8b949e;font-variant-numeric:tabular-nums}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th{text-align:left;font-size:11px;font-weight:500;color:#8b949e;text-transform:uppercase;
    letter-spacing:.6px;padding:8px 10px;border-bottom:1px solid #21262d;white-space:nowrap}
  td{padding:11px 10px;border-bottom:1px solid #1b2129;vertical-align:middle}
  tr:last-child td{border-bottom:none}
  tr:hover td{background:#1a2029}
  .num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
  .mono{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;font-size:11px;color:#8b949e}
  .tag{display:inline-block;font-size:11px;padding:2px 7px;border-radius:5px;
    background:#1f2937;color:#93c5fd;border:1px solid #263449}
  .pbar{height:5px;background:#21262d;border-radius:3px;overflow:hidden;min-width:80px}
  .pbar i{display:block;height:100%;background:linear-gradient(90deg,#2563eb,#60a5fa);border-radius:3px}
  .pbar.warn i{background:linear-gradient(90deg,#b45309,#f59e0b)}
  .pbar.danger i{background:linear-gradient(90deg,#b91c1c,#ef4444)}
  .flex-cell{display:flex;align-items:center;gap:8px}
  .pct{font-size:11px;color:#8b949e;min-width:42px;text-align:right;font-variant-numeric:tabular-nums}
  footer{margin-top:30px;font-size:11px;color:#6e7681;line-height:1.8;border-top:1px solid #21262d;padding-top:14px}
  .empty{color:#6e7681;font-size:13px;padding:20px 0;text-align:center}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <div>
      <h1>WorkBuddy 用量看板</h1>
      <div class="sub">数据来源：本地数据库 session_usage · 生成于 __GEN__</div>
    </div>
    <div class="badge">离线统计 · 非官方账单</div>
  </header>

  <div class="cards">
    <div class="card"><div class="k">累计 Token</div>
      <div class="v">__T_TOKENS__<span class="u">tokens</span></div></div>
    <div class="card"><div class="k">累计积分消耗</div>
      <div class="v">__T_CREDITS__<span class="u">credits</span></div></div>
    <div class="card"><div class="k">今日 Token</div>
      <div class="v">__T_TODAY__<span class="u">tokens</span></div></div>
    <div class="card"><div class="k">会话数 / 请求数</div>
      <div class="v">__T_SESS__<span class="u">/ __T_REQ__</span></div></div>
  </div>

  <h2>每日 Token 消耗</h2>
  <div class="panel"><div class="bars">__BARS__</div></div>

  <h2>按模型分布</h2>
  <div class="panel">
    <table>
      <thead><tr><th>模型</th><th class="num">Token</th><th class="num">占比</th>
        <th class="num">积分</th><th class="num">会话</th></tr></thead>
      <tbody>__MODEL_ROWS__</tbody>
    </table>
  </div>

  <h2>会话明细</h2>
  <div class="panel">
    <table>
      <thead><tr><th>会话</th><th>模型</th><th>日期</th><th class="num">Token</th>
        <th>上下文占用</th><th class="num">积分</th><th class="num">请求</th></tr></thead>
      <tbody>__SESSION_ROWS__</tbody>
    </table>
  </div>

  <footer>
    统计口径：Token 取本地 <span class="mono">session_usage.used</span>（该会话累计用量），
    上下文占用 = used / size；积分取 <span class="mono">credit_json</span> 中各请求积分之和。<br>
    本页仅读取本机数据，不联网、不上传。数值可能与官方计费口径存在差异，仅供参考。
  </footer>
</div>
</body>
</html>
"""


def render_html(rep):
    t = rep["totals"]

    bars = []
    days = rep["by_day"][-14:]
    peak = max([d["tokens"] for d in days], default=0) or 1
    for d in days:
        h = max(2, int(d["tokens"] / peak * 150))
        bars.append(
            f'<div class="bar-col" title="{d["date"]}：{d["tokens"]:,} tokens / '
            f'{d["credits"]:.2f} 积分 / {d["sessions"]} 会话">'
            f'<div class="bar-v">{fmt_num(d["tokens"])}</div>'
            f'<div class="bar" style="height:{h}px"></div>'
            f'<div class="bar-lb">{d["date"][5:]}</div></div>'
        )
    if not bars:
        bars = ['<div class="empty">暂无数据</div>']

    total_tok = t["tokens"] or 1
    model_rows = []
    for m in rep["by_model"]:
        share = m["tokens"] / total_tok * 100
        model_rows.append(
            f'<tr><td><span class="tag">{m["model"]}</span></td>'
            f'<td class="num">{m["tokens"]:,}</td>'
            f'<td class="num">{share:.1f}%</td>'
            f'<td class="num">{m["credits"]:,.2f}</td>'
            f'<td class="num">{m["sessions"]}</td></tr>'
        )
    if not model_rows:
        model_rows = ['<tr><td colspan="5" class="empty">暂无数据</td></tr>']

    session_rows = []
    for r in rep["sessions"]:
        p = r["percent"]
        cls = "danger" if p >= 80 else ("warn" if p >= 50 else "")
        session_rows.append(
            f'<tr><td>{r["title"]}<div class="mono">{r["short_id"]}</div></td>'
            f'<td><span class="tag">{r["model"]}</span></td>'
            f'<td class="mono">{r["date"]}</td>'
            f'<td class="num">{r["used"]:,}</td>'
            f'<td><div class="flex-cell"><div class="pbar {cls}">'
            f'<i style="width:{min(p, 100):.1f}%"></i></div>'
            f'<span class="pct">{p:.1f}%</span></div></td>'
            f'<td class="num">{r["credits"]:,.2f}</td>'
            f'<td class="num">{r["requests"]}</td></tr>'
        )
    if not session_rows:
        session_rows = ['<tr><td colspan="7" class="empty">暂无数据</td></tr>']

    return (HTML_TMPL
            .replace("__GEN__", rep["generated_at"].replace("T", " "))
            .replace("__T_TOKENS__", f"{t['tokens']:,}")
            .replace("__T_CREDITS__", f"{t['credits']:,.2f}")
            .replace("__T_TODAY__", f"{t['today_tokens']:,}")
            .replace("__T_SESS__", str(t["sessions"]))
            .replace("__T_REQ__", str(t["requests"]))
            .replace("__BARS__", "".join(bars))
            .replace("__MODEL_ROWS__", "".join(model_rows))
            .replace("__SESSION_ROWS__", "".join(session_rows)))


def main():
    ap = argparse.ArgumentParser(description="WorkBuddy 本地用量统计")
    ap.add_argument("-o", "--output", default=None, help="HTML 输出路径")
    ap.add_argument("--json", action="store_true", help="只输出 JSON")
    args = ap.parse_args()

    rep = build_report()

    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return

    print_summary(rep)
    out = args.output or os.path.join(os.getcwd(), "wb-usage-dashboard.html")
    out = os.path.abspath(out)
    with open(out, "w", encoding="utf-8") as f:
        f.write(render_html(rep))
    print(f"\n看板已生成：{out}")


if __name__ == "__main__":
    main()
