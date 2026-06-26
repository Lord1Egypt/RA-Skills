import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
GROUPS_FILE = BASE_DIR / "assets" / "groups.json"
HISTORY_FILE = BASE_DIR / "assets" / "post_history.json"
CONTENT_DIR = BASE_DIR / "assets" / "content"
SENDER_SCRIPT = Path(r"C:\Users\Lenovo\.openclaw\workspace\skills\wechat-desktop-sender\scripts\wechat_send.py")

ACTION_TO_FILE = {
    "morning_question": CONTENT_DIR / "questions.json",
    "afternoon_followup": CONTENT_DIR / "followups.json",
    "evening_case": CONTENT_DIR / "cases.json",
}


def parse_args():
    parser = argparse.ArgumentParser(description="微信群运营 MVP")
    parser.add_argument("--action", required=True, choices=list(ACTION_TO_FILE.keys()))
    parser.add_argument("--group", help="只发给指定群")
    parser.add_argument("--dry-run", action="store_true", help="只预演，不实际发送")
    return parser.parse_args()


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def get_enabled_groups(group_name=None):
    data = load_json(GROUPS_FILE)
    groups = [g for g in data.get("groups", []) if g.get("enabled")]
    if group_name:
        groups = [g for g in groups if g.get("name") == group_name]
    return groups


def select_content(action, group, history):
    items = load_json(ACTION_TO_FILE[action])
    used_ids = {
        p["content_id"]
        for p in history.get("posts", [])
        if p.get("group") == group["name"] and p.get("action") == action
    }

    topics = set(group.get("topics", []))
    topic_matched = [x for x in items if not topics or x.get("topic") in topics]
    candidates = [x for x in topic_matched if x.get("id") not in used_ids]

    if not candidates:
        candidates = topic_matched or items

    if not candidates:
        raise RuntimeError(f"没有可用内容: {action}")

    return candidates[0]


def build_message(action, content):
    if action == "evening_case":
        title = content.get("title", "今晚案例")
        return f"今晚丢个案例给大家。\n\n【{title}】\n{content.get('text', '').strip()}"
    if action == "afternoon_followup":
        return f"下午接着聊一句：\n\n{content.get('text', '').strip()}"
    return f"今天抛个问题：\n\n{content.get('text', '').strip()}"


def send_to_group(group_name, message, dry_run=False):
    cmd = [
        sys.executable,
        str(SENDER_SCRIPT),
        "--to",
        group_name,
        "--message",
        message,
        "--verify-title",
    ]
    if dry_run:
        return {"cmd": cmd, "stdout": "DRY_RUN", "returncode": 0}

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return {
        "cmd": cmd,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


def main():
    args = parse_args()
    groups = get_enabled_groups(args.group)
    if not groups:
        raise RuntimeError("没有可发送的目标群")

    history = load_json(HISTORY_FILE)
    now = datetime.now().isoformat(timespec="seconds")

    results = []
    for group in groups:
        content = select_content(args.action, group, history)
        message = build_message(args.action, content)
        send_result = send_to_group(group["name"], message, args.dry_run)

        record = {
            "time": now,
            "group": group["name"],
            "action": args.action,
            "content_id": content.get("id"),
            "content_topic": content.get("topic"),
            "message": message,
            "dry_run": args.dry_run,
            "returncode": send_result.get("returncode"),
        }
        history.setdefault("posts", []).append(record)
        results.append(record)

    save_json(HISTORY_FILE, history)
    output = json.dumps({"results": results}, ensure_ascii=False, indent=2)
    try:
        print(output)
    except UnicodeEncodeError:
        sys.stdout.buffer.write(output.encode("utf-8", errors="replace"))
        sys.stdout.buffer.write(b"\n")


if __name__ == "__main__":
    main()
