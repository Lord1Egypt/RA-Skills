#!/usr/bin/env python3
import json
import subprocess
import sys

LAST_NOTIFICATION_FILE = "/home/ubuntu/.openclaw/workspace/data/last_notification.json"
ACCOUNT = "qq"


def run_cmd(args):
    return subprocess.run(args, capture_output=True, text=True)


def load_refs():
    try:
        with open(LAST_NOTIFICATION_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("还没有可用的最近通知记录。请先等下一次邮件通知发出后，再查看正文。")
        sys.exit(2)


def fetch_body_raw(folder: str, msg_id: str) -> tuple:
    """获取邮件原始输出。"""
    cmd = ["himalaya", "message", "read", "--account", ACCOUNT, "--folder", folder, msg_id]
    p = run_cmd(cmd)
    if p.returncode != 0:
        return None, (p.stdout or p.stderr).strip()
    return p.stdout, None


def extract_body_text(raw: str) -> str:
    """从原始输出中提取正文，优先尝试HTML转Markdown。"""
    import html2text

    lines = raw.splitlines()
    body_lines = []
    in_body = False
    for line in lines:
        if not in_body and line.strip() == "":
            in_body = True
            continue
        if in_body:
            body_lines.append(line)

    text = "\n".join(body_lines) if body_lines else "\n".join(lines[len(lines)//2:])

    # 尝试检测是否为HTML并转换
    if "<html" in text.lower() or "<body" in text.lower() or "<div" in text.lower():
        try:
            h2t = html2text.HTML2Text()
            h2t.ignore_links = False
            h2t.body_width = 0  # 不折行
            converted = h2t.handle(text)
            if converted.strip():
                return converted.strip()
        except Exception:
            pass

    return text.strip() if text.strip() else "(正文为空)"


def main():
    if len(sys.argv) < 2:
        print("用法: python3 scripts/show_body.py 01 03 07")
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
        raw_body, err = fetch_body_raw(item["folder"], item["id"])
        if err:
            fail.append(f"{idx:02d} 获取失败：{err}")
            continue

        body = extract_body_text(raw_body)
        ok.append({
            "idx": idx,
            "item": item,
            "body": body,
        })

    for entry in ok:
        item = entry["item"]
        print(f"\n{'='*60}")
        print(f"【{entry['idx']:02d}】{item['subject']}")
        print(f"发件人: {item['from']}  时间: {item['date']}")
        print(f"{'='*60}")
        print(entry["body"])

    if fail:
        print("\n失败：")
        for line in fail:
            print(line)


if __name__ == "__main__":
    main()
