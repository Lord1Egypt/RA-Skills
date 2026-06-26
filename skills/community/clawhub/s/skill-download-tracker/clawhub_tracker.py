#!/usr/bin/env python3
"""ClawHub 下载量检测 + 报告 + 飞书通知

用法:
  python3 clawhub_tracker.py              # 采集一次 + 推送飞书
  python3 clawhub_tracker.py report daily # 日度报告
  python3 clawhub_tracker.py report weekly# 周度报告
  python3 clawhub_tracker.py report monthly# 月度报告
"""

import csv
import json
import os
import shutil
import subprocess
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime, date, timedelta

# clawhub 可执行文件路径（launchd/cron 环境 PATH 可能不完整）
CLAWHUB_BIN = shutil.which("clawhub") or "/opt/homebrew/bin/clawhub"

DATA_DIR = os.path.expanduser("~/.openclaw/workspace/data/clawhub-tracker")
SKILLS_CSV = os.path.join(DATA_DIR, "skills.csv")
CHECKLOG_CSV = os.path.join(DATA_DIR, "checklog.csv")
REPORT_DIR = os.path.join(DATA_DIR, "reports")
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# 从环境变量或 .env 文件读取飞书凭证（不硬编码）
_env_path = os.path.join(DATA_DIR, ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if "=" in _line and not _line.startswith("#"):
                _k, _, _v = _line.partition("=")
                os.environ.setdefault(_k.strip(), _v.strip())

APP_ID = os.environ.get("CLAWHUB_FEISHU_APP_ID", "")
APP_SECRET = os.environ.get("CLAWHUB_FEISHU_APP_SECRET", "")
USER_OPEN_ID = os.environ.get("CLAWHUB_FEISHU_USER_OPEN_ID", "")


LOG_FILE = os.path.join(DATA_DIR, "tracker.log")

def log(msg):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {msg}\n")


# ── 飞书推送 ──────────────────────────────────────────────

def get_token():
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data, headers={"Content-Type": "application/json"}, method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode()).get("tenant_access_token", "")
    except Exception as e:
        log(f"token fetch failed: {e}")
        return ""


def send_feishu(text):
    token = get_token()
    if not token:
        log("token is empty")
        return False
    payload = json.dumps({
        "receive_id": USER_OPEN_ID,
        "msg_type": "text",
        "content": json.dumps({"text": text}),
    }).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id",
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = json.loads(r.read().decode())
            ok = resp.get("code") == 0
            if not ok:
                log(f"feishu send failed: {resp}")
            return ok
    except Exception as e:
        log(f"feishu send error: {e}")
        return False


# ── CSV 读写 ──────────────────────────────────────────────

def load_skills():
    if not os.path.exists(SKILLS_CSV):
        return []
    with open(SKILLS_CSV, newline="") as f:
        return [row for row in csv.DictReader(f)]


def append_checklog(ts, slug, downloads, delta):
    exists = os.path.exists(CHECKLOG_CSV)
    with open(CHECKLOG_CSV, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["timestamp", "slug", "downloads", "delta"])
        w.writerow([ts, slug, downloads, delta])


def get_last(slug):
    if not os.path.exists(CHECKLOG_CSV):
        return None
    last = None
    with open(CHECKLOG_CSV, newline="") as f:
        for row in csv.DictReader(f):
            if row["slug"] == slug:
                last = int(row["downloads"])
    return last


def read_checklog(path=None):
    """Read checklog, return records grouped by slug."""
    path = path or CHECKLOG_CSV
    if not os.path.exists(path):
        return {}
    by_slug = defaultdict(list)
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            slug = row["slug"].strip()
            by_slug[slug].append({
                "ts": row["timestamp"].strip(),
                "dl": int(row["downloads"]),
                "delta": int(row["delta"]),
            })
    return dict(by_slug)


# ── 数据采集 ──────────────────────────────────────────────

import re

def _valid_slug(slug):
    """校验 slug 格式，防止命令注入"""
    return bool(re.match(r'^[a-z0-9][a-z0-9._-]*$', slug))

def fetch(slug):
    if not _valid_slug(slug):
        log(f"invalid slug: {slug}")
        return None
    try:
        r = subprocess.run(
            [CLAWHUB_BIN, "inspect", slug, "--json"],
            capture_output=True, text=True, timeout=15,
        )
        if r.returncode != 0:
            log(f"clawhub inspect {slug} failed: {r.stderr}")
            return None
        stdout = r.stdout.strip()
        # 防御：丢弃 stderr 混入的非 JSON 前缀行
        while stdout and not stdout.startswith("{"):
            stdout = stdout.split("\n", 1)[1] if "\n" in stdout else stdout.lstrip()
        if not stdout:
            log(f"clawhub inspect {slug}: empty stdout")
            return None
        return json.loads(stdout).get("skill", {}).get("stats", {}).get("downloads")
    except Exception as e:
        log(f"fetch {slug} error: {e}")
        return None


# ── 报告生成 ──────────────────────────────────────────────

def _filter_by_date(data, date_start, date_end):
    """Filter checklog records within date range."""
    d_start = date.fromisoformat(date_start) if isinstance(date_start, str) else date_start
    d_end = date.fromisoformat(date_end) if isinstance(date_end, str) else date_end
    filtered = {}
    for slug, records in data.items():
        rows = []
        for r in records:
            ts_str = r["ts"].strip()
            if len(ts_str) < 10:
                continue
            try:
                ts_date = date.fromisoformat(ts_str[:10])
            except (ValueError, TypeError):
                continue
            if d_start <= ts_date <= d_end:
                rows.append(r)
        if rows:
            filtered[slug] = rows
    return filtered


def _build_report_text(title, filtered_data, all_slugs=None):
    """Build report text from filtered data."""
    all_slugs = all_slugs or []
    lines = [title]
    lines.append("─" * 36)

    total_dl = 0
    total_delta = 0

    # 优先展示有数据的 slug，然后是 skills.csv 中无数据的
    shown = set()
    for slug in list(filtered_data.keys()) + all_slugs:
        if slug in shown:
            continue
        shown.add(slug)
        records = filtered_data.get(slug, [])
        if not records:
            lines.append(f"  {slug}: no data")
            continue

        first_dl = records[0]["dl"] - records[0]["delta"]  # 周期起始下载量
        last_dl = records[-1]["dl"]
        sum_delta = sum(r["delta"] for r in records)
        total_delta += sum_delta
        total_dl += last_dl

        # 找出增长最多和最多的时间点
        peak_delta = max(records, key=lambda r: r["delta"])
        peak_ts = peak_delta["ts"][:16]

        delta_tag = f"+{sum_delta}" if sum_delta >= 0 else str(sum_delta)
        lines.append(f"  {slug}: {first_dl} → {last_dl}（{delta_tag}）")
        lines.append(f"    samples: {len(records)} · peak: {peak_ts}（{'+' + str(peak_delta['delta']) if peak_delta['delta'] >= 0 else peak_delta['delta']}）")

    lines.append("─" * 36)
    sign = '+' if total_delta >= 0 else ''
    lines.append(f"total: {sign}{total_delta} new · {total_dl} current")
    return "\n".join(lines)


def generate_daily_report(days=1):
    """Daily report: last N days."""
    data = read_checklog()
    all_slugs = [s["slug"].strip() for s in load_skills()]
    today = date.today()
    start = today - timedelta(days=days - 1)
    filtered = _filter_by_date(data, start, today)
    title = f"📊 ClawHub Downloads · {days}d Report ({start} ~ {today})"
    return _build_report_text(title, filtered, all_slugs)


def generate_weekly_report():
    """Weekly report: last 7 days."""
    return generate_daily_report(days=7)


def generate_monthly_report():
    """Monthly report: current month."""
    data = read_checklog()
    all_slugs = [s["slug"].strip() for s in load_skills()]
    today = date.today()
    start = today.replace(day=1)
    filtered = _filter_by_date(data, start, today)
    title = f"📊 ClawHub Downloads · Monthly Report ({start} ~ {today})"
    return _build_report_text(title, filtered, all_slugs)


def cmd_report(period):
    """Report sub-command: daily / weekly / monthly."""
    if period == "daily":
        text = generate_daily_report(days=1)
    elif period == "weekly":
        text = generate_weekly_report()
    elif period == "monthly":
        text = generate_monthly_report()
    else:
        print(f"❌ Unknown report period: {period} (supported: daily / weekly / monthly)")
        return False

    print(text)

    # 存档
    now = datetime.now()
    period_file = os.path.join(REPORT_DIR, f"{now.strftime('%Y-%m')}.md")
    with open(period_file, "a") as f:
        f.write(text + "\n\n")

    # 飞书推送
    ok = send_feishu(text)
    if ok:
        log(f"{period} report push succeeded")
    else:
        log(f"{period} report push failed")
    return ok


# ── 主采集流程 ────────────────────────────────────────────

def cmd_collect():
    """Collect current download counts, save CSV, push Feishu."""
    skills = load_skills()
    if not skills:
        send_feishu("📊 ClawHub Downloads — no skills to monitor")
        sys.exit(1)

    now = datetime.now()
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    lines = []
    total_dl = 0
    failed = 0

    for skill in skills:
        slug = skill["slug"].strip()
        dl = fetch(slug)
        if dl is None:
            lines.append(f"  {slug}: ❌ fetch failed")
            log(f"{slug}: fetch failed")
            failed += 1
            continue
        last = get_last(slug)
        delta = dl - last if last is not None else 0
        append_checklog(ts, slug, dl, delta)
        total_dl += dl

        tag = ""
        if delta > 0:
            tag = f" ↑+{delta}"
        elif delta < 0:
            tag = f" ↓{delta}"
        lines.append(f"  {slug}: {dl} downloads{tag}")

    output = f"📊 ClawHub Downloads · {now.strftime('%m/%d %H:%M')}"
    output += f"\n{'─' * 28}"
    for l in lines:
        output += f"\n{l}"
    output += f"\n{'─' * 28}"
    output += f"\n{len(skills)} skills · {total_dl} total downloads"

    print(output)

    # 存档
    report_path = os.path.join(REPORT_DIR, f"{now.strftime('%Y-%m')}.md")
    with open(report_path, "a") as f:
        f.write(output + "\n\n")

    # 飞书推送
    feishu_ok = send_feishu(output)
    if feishu_ok:
        log(f"feishu push succeeded: {total_dl} total downloads")
    else:
        log("feishu push failed")
        print("❌ Feishu push failed")

    # 全部失败时返回非零退出码
    if failed == len(skills):
        sys.exit(2)


# ── 入口 ──────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "report":
        ok = cmd_report(args[1])
        if not ok:
            sys.exit(1)
    elif len(args) == 1 and args[0] == "report":
        print("用法: python3 clawhub_tracker.py report [daily|weekly|monthly]")
        sys.exit(1)
    else:
        cmd_collect()


if __name__ == "__main__":
    main()
