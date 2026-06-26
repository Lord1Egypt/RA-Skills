#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
summarize_weibo_hot.py - Read hot.json, summarize via @steipete/summarize CLI,
produce Markdown digest, enqueue for Obsidian writing.

Called by skill_runner.py, which optionally loads env.ps1 first.
Environment variables such as SUMMARIZE_BIN may come from env.ps1 or existing process env.

Exit codes:  0 = Success,  1 = Error
"""

import hashlib, json, msvcrt, os, subprocess, sys, traceback, io
from datetime import datetime, timezone, timedelta

# Force UTF-8 output (fixes garbled Chinese in NSSM/PowerShell)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

STATE_DIR       = r"C:\Users\Intel\.openclaw\state\weibo_hot"
HOT_JSON        = os.path.join(STATE_DIR, "hot.json")
SUMMARY_MD      = os.path.join(STATE_DIR, "summary_latest.md")
QUEUE_JSONL     = os.path.join(STATE_DIR, "queue.jsonl")
LAST_SUMMARIZE  = os.path.join(STATE_DIR, "last_summarize.txt")
SUMMARIZE_INPUT = os.path.join(STATE_DIR, "summarize_input.txt")

TOP_N            = 20
# Default to npm path. skill_runner.py may set SUMMARIZE_BIN from env.ps1 before this script runs.
SUMMARIZE_BIN    = os.environ.get("SUMMARIZE_BIN", r"C:\Users\Intel\AppData\Roaming\npm\summarize.CMD")
SUMMARIZE_TIMEOUT = 180
CST = timezone(timedelta(hours=8))


def read_hot_json():
    if not os.path.isfile(HOT_JSON):
        raise FileNotFoundError(f"hot.json not found at {HOT_JSON}")
    with open(HOT_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    if not data.get("items"):
        raise ValueError("hot.json has no items")
    return data


def build_input_text(items):
    lines = ["\u5fae\u535a\u70ed\u641c\u699c\u5b9e\u65f6\u6570\u636e", "=" * 40, ""]
    for it in items[:TOP_N]:
        cat = f" [{it.get('category','')}]" if it.get("category") else ""
        lines.append(f"{it['rank']}. {it['title']} (\u70ed\u5ea6: {it.get('hot',0):,}){cat}")
    return "\n".join(lines)


def call_summarize(input_file):
    cmd = [SUMMARIZE_BIN, input_file,
           "--lang", "zh", "--length", "medium",
           "--plain", "--no-cache", "--timeout", "2m", "--retries", "1"]
    print(f"[summarize] Running: {' '.join(cmd)}")
    print(f"[summarize] SUMMARIZE_BIN = {SUMMARIZE_BIN}")
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=SUMMARIZE_TIMEOUT, encoding="utf-8", errors="replace")
        if r.returncode == 0 and r.stdout.strip():
            return r.stdout.strip()
        print(f"[summarize] CLI failed (code {r.returncode}): {(r.stderr or '')[:300]}", file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("[summarize] CLI timed out", file=sys.stderr)
    except FileNotFoundError:
        print(f"[summarize] CLI not found: {SUMMARIZE_BIN}", file=sys.stderr)
    except Exception as e:
        print(f"[summarize] CLI error: {e}", file=sys.stderr)
    return None


def fmt(score):
    if score is None: return "\u2014"
    try:
        n = int(score)
        return f"{n/10000:.1f}\u4e07" if n >= 10000 else str(n)
    except (ValueError, TypeError): return str(score)


def themes(items):
    out, seen = [], set()
    for t in [i["title"] for i in items[:TOP_N]][:8]:
        k = t[:4]
        if k not in seen: seen.add(k); out.append(t)
        if len(out) >= 5: break
    return out


def build_markdown(data, summary):
    items = data["items"]
    ts = data.get("fetched_at", "unknown")
    try: dt = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M")
    except Exception: dt = ts

    L = [f"# \u5fae\u535a\u70ed\u641c \u2014 {dt} (CST)", "",
         f"## Top {min(TOP_N, len(items))} \u70ed\u641c\u699c", "",
         "| \u6392\u540d | \u8bdd\u9898 | \u70ed\u5ea6 |", "|------|------|------|"]
    for i in items[:TOP_N]:
        L.append(f"| {i['rank']} | {i['title']} | {fmt(i.get('hot'))} |")
    L.append("")

    th = themes(items)
    if th:
        L.extend(["## \u70ed\u70b9\u4e3b\u9898 Key Themes", ""])
        L.extend(f"- {t}" for t in th)
        L.append("")

    L.extend(["## \u70ed\u641c\u6458\u8981 Summary", ""])
    if summary:
        L.append(summary)
    else:
        L.append("*(\u6458\u8981\u751f\u6210\u5931\u8d25)*\n")
        L.extend(f"- **{i['title']}** (\u70ed\u5ea6: {fmt(i.get('hot'))})" for i in items[:10])
    L.append("")

    h = hashlib.sha256(json.dumps([i["title"] for i in items], ensure_ascii=False).encode()).hexdigest()[:12]
    L.extend(["---", f"<!-- weibo-hot-digest sha:{h} ts:{ts} -->", ""])
    return "\n".join(L)


def safe_replace(src, dst):
    if os.path.exists(dst):
        bak = dst + ".bak"
        try:
            if os.path.exists(bak): os.remove(bak)
            os.rename(dst, bak)
        except OSError: os.remove(dst)
    os.rename(src, dst)


def write_atomic(path, content):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f: f.write(content)
    safe_replace(tmp, path)


def enqueue(record):
    line = json.dumps(record, ensure_ascii=False) + "\n"
    with open(QUEUE_JSONL, "a", encoding="utf-8") as f:
        fd = f.fileno()
        msvcrt.locking(fd, msvcrt.LK_LOCK, 1)
        try: f.write(line); f.flush()
        finally:
            try: msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            except OSError: pass


def main():
    os.makedirs(STATE_DIR, exist_ok=True)
    print("[summarize] Reading hot.json...")
    data = read_hot_json()
    items = data["items"]
    ts = data.get("fetched_at", "")
    print(f"[summarize] {len(items)} items.")

    txt = build_input_text(items)
    with open(SUMMARIZE_INPUT, "w", encoding="utf-8") as f: f.write(txt)
    print(f"[summarize] Input: {len(txt)} chars")

    summary = call_summarize(SUMMARIZE_INPUT)
    md = build_markdown(data, summary)
    write_atomic(SUMMARY_MD, md)
    print(f"[summarize] Written: {SUMMARY_MD}")

    now = datetime.now(CST).isoformat()
    write_atomic(LAST_SUMMARIZE, now)

    h = hashlib.sha256(md.encode()).hexdigest()[:12]
    try: dt = datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M")
    except Exception: dt = ts

    enqueue({"id": h, "ts": now, "type": "weibo_hot",
             "md_path": SUMMARY_MD,
             "title": f"\u5fae\u535a\u70ed\u641c \u2014 {dt} (CST)"})
    print(f"[summarize] Enqueued id={h}")
    print("\n" + "=" * 60 + "\n" + md + "=" * 60)


if __name__ == "__main__":
    try: main()
    except Exception as e:
        print(f"[error] {e}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr); sys.exit(1)
