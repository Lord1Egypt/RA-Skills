#!/usr/bin/env python3
import json
import subprocess
import sys

LAST_NOTIFICATION_FILE = "/home/ubuntu/.openclaw/workspace/data/last_notification.json"
ANCHOR_IDS_PATH = "/home/ubuntu/.openclaw/workspace/data/work_mail_anchor_ids.json"
ACCOUNT = "qq"


def run_cmd(args):
    return subprocess.run(args, capture_output=True, text=True)


def load_refs():
    try:
        with open(LAST_NOTIFICATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("还没有可用的最近通知记录。请先等下一次邮件通知发出后，再按序号标已读。")
        sys.exit(2)


def mark_as_read(folder: str, msg_id: str):
    cmd = ["himalaya", "flag", "add", "--account", ACCOUNT, "--folder", folder, msg_id, "seen"]
    p = run_cmd(cmd)
    return p.returncode == 0, (p.stdout or p.stderr).strip()


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/mark_read.py 01 03 07")
        sys.exit(1)

    refs = load_refs()
    ok = []
    fail = []

    for raw in sys.argv[1:]:
        try:
            idx = int(raw)
        except ValueError:
            fail.append(f"{raw}: 不是有效序号")
            continue

        if idx < 1 or idx > len(refs):
            fail.append(f"{idx:02d}: 超出范围")
            continue

        item = refs[idx - 1]
        success, msg = mark_as_read(item["folder"], item["id"])
        if success:
            ok.append(f"{idx:02d} 已标已读")
        else:
            fail.append(f"{idx:02d} 标记失败：{msg}")

    if ok:
        print("成功：")
        for line in ok:
            print(line)
    if fail:
        print("失败：")
        for line in fail:
            print(line)


if __name__ == "__main__":
    main()
