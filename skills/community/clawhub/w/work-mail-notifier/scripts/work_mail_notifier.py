#!/usr/bin/env python3
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Shanghai")
ACCOUNT = "qq"
FOLDERS = [
    "其他文件夹/Sent",
    "其他文件夹/CodeReview",
    "其他文件夹/Eservice",
    "其他文件夹/cmadmin",
    "其他文件夹/Redmine",
    "其他文件夹/zhangjiongjie@sagereal.com",
    "其他文件夹/Jenkins",
    "其他文件夹/Jira",
    "其他文件夹/TCLJira",
]
PAGE_SIZE = 100
STATE_PATH = "/home/ubuntu/.openclaw/workspace/data/work_mail_notifier_state.json"
LAST_NOTIFICATION_FILE = "/home/ubuntu/.openclaw/workspace/data/last_notification.json"
# 上次通知中与 anchor 时间相同的所有邮件 ID，用于去重
ANCHOR_IDS_PATH = "/home/ubuntu/.openclaw/workspace/data/work_mail_anchor_ids.json"

ROW_RE = re.compile(r"^\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$")
DATE_FMT_OUT = "%m-%d %H:%M"


def classify_item(item):
    subject_raw = item["subject"]
    subject = subject_raw.lower()
    if any(k in subject for k in ["告警", "delay warning", "warning", "block"]):
        return "告警/风险"
    if any(k in subject_raw for k in ["Fail", "FAIL"]) or "fail" in subject or "失败" in subject or "异常" in subject:
        return "失败/异常"
    return "普通"


def run_cmd(args):
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def parse_dt(s: str):
    s = s.strip()
    if not s:
        return None
    for fmt in ["%Y-%m-%d %H:%M%z", "%Y-%m-%d %H:%M:%S%z"]:
        try:
            return datetime.strptime(s, fmt).astimezone(TZ)
        except ValueError:
            pass
    return None


def list_folder_page(folder: str, page: int):
    cmd = [
        "himalaya", "envelope", "list",
        "--account", ACCOUNT,
        "--folder", folder,
        "--page", str(page),
        "--page-size", str(PAGE_SIZE),
    ]
    code, out, err = run_cmd(cmd)
    if code != 0:
        if "out of bounds" in err:
            return []
        raise RuntimeError(f"list failed for {folder} page {page}: {err.strip() or out.strip()}")

    items = []
    for line in out.splitlines():
        line = line.rstrip()
        if not line.startswith("|"):
            continue
        if "| ID" in line or set(line.replace("|", "").strip()) == {"-"}:
            continue
        m = ROW_RE.match(line)
        if not m:
            continue
        msg_id, flags, subject, sender, date_str = [x.strip() for x in m.groups()]
        if not msg_id.isdigit():
            continue
        dt = parse_dt(date_str)
        if dt is None:
            continue
        items.append({
            "id": msg_id,
            "flags": flags,
            "subject": subject,
            "from": sender,
            "date": dt,
            "folder": folder,
        })
    return items


def load_anchor_ids():
    """加载上次通知中与 anchor 时间相同的邮件 ID 集合。"""
    try:
        with open(ANCHOR_IDS_PATH, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception:
        return set()


def fetch_all_since(start_dt: datetime, end_dt: datetime, exclude_ids: set):
    """Fetch all emails with send time in [start_dt, end_dt) across all folders.
    排除 exclude_ids 中的 ID（与 anchor 时间相同且已在上次通知中出现）。"""
    all_items = []
    seen = set()
    for folder in FOLDERS:
        page = 1
        while True:
            rows = list_folder_page(folder, page)
            if not rows:
                break
            stop_folder = False
            for item in rows:
                key = (folder, item["id"])
                if key in seen:
                    continue
                seen.add(key)
                # 排除：时间 == anchor 且 ID 在 exclude_ids 中（上次已通知过的）
                if item["date"] == start_dt and item["id"] in exclude_ids:
                    continue
                if start_dt <= item["date"] < end_dt:
                    all_items.append(item)
                if item["date"] < start_dt:
                    stop_folder = True
            if stop_folder:
                break
            page += 1
    all_items.sort(key=lambda x: x["date"])
    return all_items


def load_state():
    try:
        with open(STATE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)
    with open(STATE_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def save_anchor_ids(anchor_time: datetime, items):
    """保存上次通知中时间等于 anchor_time 的所有邮件 ID。"""
    anchor_ids = {item["id"] for item in items if item["date"] == anchor_time}
    os.makedirs(os.path.dirname(ANCHOR_IDS_PATH), exist_ok=True)
    with open(ANCHOR_IDS_PATH, "w", encoding="utf-8") as f:
        json.dump(list(anchor_ids), f, ensure_ascii=False)


def save_notification_refs(items):
    os.makedirs(os.path.dirname(LAST_NOTIFICATION_FILE), exist_ok=True)
    groups = {"告警/风险": [], "失败/异常": [], "普通": []}
    for item in items:
        groups[classify_item(item)].append(item)

    ordered = []
    for group_name in ["告警/风险", "失败/异常", "普通"]:
        for item in groups[group_name]:
            ordered.append({
                "ref": f"{item['folder']}#{item['id']}",
                "folder": item["folder"],
                "id": item["id"],
                "from": item["from"],
                "subject": item["subject"],
                "date": item["date"].isoformat(),
                "group": group_name,
            })
    with open(LAST_NOTIFICATION_FILE, "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False, indent=2)


def format_message(items):
    lines = [f"新工作邮件通知（共{len(items)}封）"]
    groups = {"告警/风险": [], "失败/异常": [], "普通": []}
    for item in items:
        groups[classify_item(item)].append(item)

    idx = 1
    for group_name in ["告警/风险", "失败/异常", "普通"]:
        group_items = groups[group_name]
        if not group_items:
            continue
        lines.append(f"\n【{group_name}｜{len(group_items)}封】")
        for item in group_items:
            sender = item["from"].replace("|", "/").strip()
            subject = item["subject"].replace("|", "/").strip()
            time_s = item["date"].strftime(DATE_FMT_OUT)
            ref = f"{item['folder']}#{item['id']}"
            lines.append(f"{idx:02d} {sender}  {time_s}  {subject}")
            lines.append(f"   标识: {ref}")
            idx += 1
    return "\n".join(lines)


def main():
    now = datetime.now(TZ)
    state = load_state()

    # Anchor: 上次统计到的最晚邮件时间
    # 不存在 anchor 时，取今天 00:00 作为起点
    raw_anchor = state.get("last_anchor")
    if raw_anchor:
        start_dt = datetime.fromisoformat(raw_anchor).astimezone(TZ)
    else:
        start_dt = now.replace(hour=0, minute=0, second=0, microsecond=0)

    end_dt = now

    # 加载上次通知中与 anchor 时间相同的邮件 ID，用于去重
    exclude_ids = load_anchor_ids()

    items = fetch_all_since(start_dt, end_dt, exclude_ids)

    if not items:
        # 无新邮件，不更新 anchor（保持原值，避免邮件被漏掉）
        print("NO_REPLY")
        return

    # 更新 anchor 为本次最晚邮件时间，下次从此时刻继续往后找
    new_anchor = max(item["date"] for item in items)
    state["last_anchor"] = new_anchor.isoformat()
    state["last_count"] = len(items)
    save_state(state)
    # 保存本次通知中与新 anchor 时间相同的邮件 ID，供下次去重用
    save_anchor_ids(new_anchor, items)

    print(format_message(items))
    save_notification_refs(items)


if __name__ == "__main__":
    import time
    max_retries = 3
    for i in range(max_retries):
        try:
            main()
            break
        except Exception as e:
            if i == max_retries - 1:
                print(f"工作邮件通知任务失败：{e}", file=sys.stderr)
                sys.exit(1)
            time.sleep(2 ** i * 10)
