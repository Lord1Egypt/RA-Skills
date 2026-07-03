#!/usr/bin/env python3
"""ClawHub 下载量检测 + 报告 + 飞书通知

用法:
  python3 clawhub_tracker.py                       # 采集一次 + 推送飞书
  python3 clawhub_tracker.py report daily          # 日度报告
  python3 clawhub_tracker.py report weekly         # 周度报告
  python3 clawhub_tracker.py report monthly        # 月度报告
  python3 clawhub_tracker.py add <slug> [note]     # 添加监控 skill
  python3 clawhub_tracker.py remove <slug>         # 移除监控 skill
  python3 clawhub_tracker.py list                  # 列出所有监控的 skill
"""

import csv
import fcntl
import json
import os
import re
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
LAST_STATE_FILE = os.path.join(DATA_DIR, "last_state.json")
LOCK_FILE = os.path.join(DATA_DIR, ".tracker.lock")
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


class FileLock:
    """文件锁：防止 launchd 高频触发时并发写 last_state.json / checklog.csv"""

    def __init__(self, path):
        self.path = path
        self.fd = None

    def __enter__(self):
        self.fd = open(self.path, "w")
        try:
            fcntl.flock(self.fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            log("another tracker instance is running, exiting")
            print("⚠️  Another tracker instance is running, skipping this run.")
            sys.exit(0)
        return self.fd

    def __exit__(self, *args):
        if self.fd:
            try:
                fcntl.flock(self.fd, fcntl.LOCK_UN)
                self.fd.close()
            except Exception:
                pass


# ── 飞书推送 ──────────────────────────────────────────────

def get_token():
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data, headers={"Content-Type": "application/json"}, method="POST",
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

def _valid_slug(slug):
    """校验 slug 格式，防止命令注入"""
    return bool(re.match(r'^[a-z0-9][a-z0-9._-]*$', slug))


def load_skills():
    if not os.path.exists(SKILLS_CSV):
        return []
    with open(SKILLS_CSV, newline="") as f:
        return [row for row in csv.DictReader(f)]


def load_last_state():
    """Load cached last state: {slug: {downloads, ts}}"""
    if not os.path.exists(LAST_STATE_FILE):
        return {}
    try:
        with open(LAST_STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_last_state(state):
    """Save last state snapshot (atomic write)."""
    try:
        tmp = LAST_STATE_FILE + ".tmp"
        with open(tmp, "w") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        os.replace(tmp, LAST_STATE_FILE)
    except Exception as e:
        log(f"save_last_state failed: {e}")


def append_checklog(ts, slug, downloads, delta):
    exists = os.path.exists(CHECKLOG_CSV)
    with open(CHECKLOG_CSV, "a", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["timestamp", "slug", "downloads", "delta"])
        w.writerow([ts, slug, downloads, delta])


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


def _get_last_from_checklog(slug):
    """Fallback: read last download count from checklog (for migration)."""
    if not os.path.exists(CHECKLOG_CSV):
        return None
    last = None
    with open(CHECKLOG_CSV, newline="") as f:
        for row in csv.DictReader(f):
            if row["slug"].strip() == slug:
                last = int(row["downloads"])
    return last


# ── 数据采集 ──────────────────────────────────────────────

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
    period_best_slug = None
    period_best_delta = 0

    shown = set()
    for slug in list(filtered_data.keys()) + all_slugs:
        if slug in shown:
            continue
        shown.add(slug)
        records = filtered_data.get(slug, [])
        if not records:
            continue

        first_dl = records[0]["dl"] - records[0]["delta"]
        last_dl = records[-1]["dl"]
        sum_delta = sum(r["delta"] for r in records)
        total_delta += sum_delta
        total_dl += last_dl

        peak_delta_record = max(records, key=lambda r: r["delta"])
        peak_ts = peak_delta_record["ts"][:16]

        delta_tag = f"+{sum_delta}" if sum_delta >= 0 else str(sum_delta)
        lines.append(f"  {slug}: {first_dl} → {last_dl}（{delta_tag}）")
        peak_delta_str = (
            f"+{peak_delta_record['delta']}" if peak_delta_record['delta'] >= 0
            else str(peak_delta_record['delta'])
        )
        lines.append(
            f"    samples:{len(records)} · peak:{peak_ts}（{peak_delta_str}）"
        )

        period_best = max(r["delta"] for r in records)
        if period_best > period_best_delta:
            period_best_delta = period_best
            period_best_slug = slug

    lines.append("─" * 36)
    sign = '+' if total_delta >= 0 else ''
    lines.append(f"total: {sign}{total_delta} new · {total_dl} current")

    if period_best_slug and period_best_delta > 0:
        lines.append(f"🏆 best: {period_best_slug} (+{period_best_delta})")

    return "\n".join(lines)


def generate_daily_report(days=1):
    """Daily report: last N days. Falls back to last_state.json when checklog is empty."""
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
    title = f"📊 ClawHub Downloads · Monthly ({start} ~ {today})"
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
        print(f"❌ Unknown period: {period} (supported: daily / weekly / monthly)")
        return False

    print(text)

    now = datetime.now()
    period_file = os.path.join(REPORT_DIR, f"{now.strftime('%Y-%m')}.md")
    with open(period_file, "a") as f:
        f.write(text + "\n\n")

    ok = send_feishu(text)
    if ok:
        log(f"{period} report push succeeded")
    else:
        log(f"{period} report push failed")
    return ok


# ── skills.csv 管理 ───────────────────────────────────────

def cmd_add(slug, note=""):
    """Add a skill to monitor. Creates skills.csv if missing."""
    if not _valid_slug(slug):
        print(f"❌ Invalid slug format: {slug}")
        print("   (slug must be lowercase, digits, dots, underscores, hyphens)")
        return False

    with FileLock(LOCK_FILE):
        skills = load_skills()
        existing_slugs = {s["slug"].strip() for s in skills}
        if slug in existing_slugs:
            print(f"⚠️  {slug} is already monitored")
            return True

        new_file = not os.path.exists(SKILLS_CSV)
        with open(SKILLS_CSV, "a", newline="") as f:
            w = csv.writer(f)
            if new_file:
                w.writerow(["slug", "note"])
            w.writerow([slug, note])
        print(f"✅ Added: {slug}" + (f" ({note})" if note else ""))
        return True


def cmd_remove(slug):
    """Remove a skill from monitor (preserves historical data)."""
    if not _valid_slug(slug):
        print(f"❌ Invalid slug format: {slug}")
        return False

    with FileLock(LOCK_FILE):
        skills = load_skills()
        if not skills:
            print("⚠️  No skills monitored")
            return True

        kept = [s for s in skills if s["slug"].strip() != slug]
        if len(kept) == len(skills):
            print(f"⚠️  {slug} not found in monitor list")
            return True

        # 写回（保留表头）
        tmp = SKILLS_CSV + ".tmp"
        with open(tmp, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["slug", "note"])
            w.writeheader()
            w.writerows(kept)
        os.replace(tmp, SKILLS_CSV)
        print(f"✅ Removed: {slug}  (historical data preserved in checklog.csv)")
        return True


def cmd_list():
    """List all monitored skills with their last known download count."""
    skills = load_skills()
    if not skills:
        print("⚠️  No skills monitored. Use: clawhub_tracker.py add <slug>")
        return True

    last_state = load_last_state()
    print(f"📋 Monitored skills ({len(skills)}):")
    print("─" * 50)
    for s in skills:
        slug = s["slug"].strip()
        note = s.get("note", "").strip()
        dl = last_state.get(slug, {}).get("downloads")
        dl_str = f"{dl} dl" if dl is not None else "(no data)"
        line = f"  {slug:30s}  {dl_str}"
        if note:
            line += f"  · {note}"
        print(line)
    return True


# ── 主采集流程（仅变化时写入）──────────────────────────────

def cmd_collect():
    """Collect current download counts — only writes checklog on delta != 0."""
    with FileLock(LOCK_FILE):
        skills = load_skills()
        if not skills:
            send_feishu("📊 ClawHub Downloads — no skills to monitor")
            sys.exit(1)

        now = datetime.now()
        ts = now.strftime("%Y-%m-%d %H:%M:%S")
        lines = []
        total_dl = 0
        failed = 0
        changed = 0

        last_state = load_last_state()

        for skill in skills:
            slug = skill["slug"].strip()
            dl = fetch(slug)
            if dl is None:
                lines.append(f"  {slug}: ❌ fetch failed")
                log(f"{slug}: fetch failed")
                failed += 1
                continue

            last = last_state.get(slug, {}).get("downloads")
            if last is None:
                last = _get_last_from_checklog(slug)

            delta = dl - last if last is not None else 0
            total_dl += dl

            tag = ""
            if delta > 0:
                tag = f" ↑+{delta}"
                changed += 1
                append_checklog(ts, slug, dl, delta)
                last_state[slug] = {"downloads": dl, "ts": ts}
            elif delta < 0:
                tag = f" ↓{delta}"
                changed += 1
                append_checklog(ts, slug, dl, delta)
                last_state[slug] = {"downloads": dl, "ts": ts}
            else:
                tag = " ·"

            lines.append(f"  {slug}: {dl} dl{tag}")

        save_last_state(last_state)

        output = f"📊 ClawHub · {now.strftime('%m/%d %H:%M')}"
        output += f"\n{'─' * 30}"
        for l in lines:
            output += f"\n{l}"
        output += f"\n{'─' * 30}"
        output += f"\n{len(skills)} skills · {total_dl} total · {changed} changed"

        print(output)

        report_path = os.path.join(REPORT_DIR, f"{now.strftime('%Y-%m')}.md")
        with open(report_path, "a") as f:
            f.write(output + "\n\n")

        feishu_ok = send_feishu(output)
        if feishu_ok:
            log(f"feishu push ok: {total_dl} total, {changed} changed")
        else:
            log("feishu push failed")
            print("❌ Feishu push failed")

        if failed == len(skills):
            sys.exit(2)


def get_last(slug):
    """Public: get last known download count for a slug (backward compat + test)."""
    return _get_last_from_checklog(slug)


# ── 入口 ──────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    if len(args) == 0:
        cmd_collect()
    elif args[0] == "report" and len(args) >= 2:
        ok = cmd_report(args[1])
        if not ok:
            sys.exit(1)
    elif args[0] == "report":
        print("用法: python3 clawhub_tracker.py report [daily|weekly|monthly]")
        sys.exit(1)
    elif args[0] == "add":
        if len(args) < 2:
            print("用法: python3 clawhub_tracker.py add <slug> [note]")
            sys.exit(1)
        slug = args[1]
        note = " ".join(args[2:]) if len(args) > 2 else ""
        if not cmd_add(slug, note):
            sys.exit(1)
    elif args[0] == "remove" and len(args) == 2:
        if not cmd_remove(args[1]):
            sys.exit(1)
    elif args[0] == "remove":
        print("用法: python3 clawhub_tracker.py remove <slug>")
        sys.exit(1)
    elif args[0] == "list":
        if not cmd_list():
            sys.exit(1)
    else:
        print(f"❌ Unknown command: {args[0]}")
        print("用法: clawhub_tracker.py [report daily|weekly|monthly] [add <slug>] [remove <slug>] [list]")
        sys.exit(1)


if __name__ == "__main__":
    main()
