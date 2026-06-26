#!/usr/bin/env python3
"""
Feishu notification for Session Memory Extractor.
v1.0.3: Fix extraction count — was reading wrong key 'extractions' instead of 'results'
"""

import json, os, sys, argparse, subprocess

def format_feishu_report(report_path: str) -> str:
    """Format JSON report as a readable Feishu text message."""
    with open(report_path) as f:
        r = json.load(f)

    disk = r.get("disk_before", {})
    disk_after = r.get("disk_after", {})

    # Count entries by type — v1.0.3: JSON uses 'results', not 'extractions'
    results = r.get("results", r.get("extractions", []))
    entries_by_type = {"DECISION": 0, "PREFERENCE": 0, "FACT": 0, "TODO": 0}
    for ex in results:
        for entry in ex.get("entries", []):
            t = entry.get("type", "").strip("[] ")  # v1.0.3: strip brackets from type like "[FACT]"
            if t in entries_by_type:
                entries_by_type[t] += 1

    # Memory file short path
    memory_file = r.get("memory_file", "")
    memory_short = memory_file.replace(os.path.expanduser("~"), "~")

    # Type breakdown — v1.0.3: show count even if 0 (means AI decided nothing worth extracting)
    type_lines = ""
    total_labeled = sum(entries_by_type.values())
    for t, count in entries_by_type.items():
        type_lines += f"\n  • {t}: {count} 条"
    if total_labeled == 0 and r.get("total_entries_extracted", 0) > 0:
        type_lines = "\n  • (类型未标注)"

    # v1.0.3: show top 3 extraction snippets as preview
    preview_lines = ""
    snippet_count = 0
    for ex in results:
        for entry in ex.get("entries", []):
            if snippet_count >= 3:
                break
            content = entry.get("content", "")[:80]
            if content:
                preview_lines += f"\n  ▸ {content}"
                snippet_count += 1
        if snippet_count >= 3:
            break

    msg = f"""🧠 Session Memory Extractor | {r['agent']}

✅ 提炼完成

📊 处理摘要:
  • Session: {r['sessions_processed']} 个
  • 提炼: {r['total_entries_extracted']} 条
  • 释放: {r['total_bytes_freed_human']}
{type_lines if type_lines else "  （无提炼内容）"}
{preview_lines if preview_lines else ""}

💾 磁盘变化:
  • .jsonl: {disk.get('jsonl_count','?')} → {disk_after.get('jsonl_count','?')} 个
    {disk.get('jsonl_bytes','')} → {disk_after.get('jsonl_bytes','')}
  • .trajectory: {disk.get('trajectory_count','?')} → {disk_after.get('trajectory_count','?')} 个
    {disk.get('trajectory_bytes','')} → {disk_after.get('trajectory_bytes','')}

📝 提炼内容已写入:
{memory_short}

🔍 报告文件:
extract-report-{r['agent']}-{r['date']}.json"""

    return msg


def send_via_openclaw(message: str, target: str) -> dict:
    """Send message via OpenClaw's message tool (feishu DM)."""
    result = subprocess.run(
        [
            "openclaw", "message", "send",
            "--channel", "feishu",
            "--target", target,
            "--message", message,
        ],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode != 0:
        raise RuntimeError(f"openclaw message send failed: {result.stderr}")
    return {"status": "ok", "stdout": result.stdout}


def send_via_webhook(token: str, message: str) -> dict:
    """Send text message to Feishu via webhook bot."""
    import urllib.request, urllib.error
    url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{token}"
    payload = {"msg_type": "text", "content": {"text": message}}
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def main():
    parser = argparse.ArgumentParser(description="Send extraction report to Feishu")
    parser.add_argument("--report", required=True, help="Path to JSON report file")
    parser.add_argument("--target", default="",
                        help="Feishu user ID or chat ID (default: user DM)")
    args = parser.parse_args()

    report_path = args.report
    if not os.path.exists(report_path):
        print(f"ERROR: Report file not found: {report_path}", file=sys.stderr)
        sys.exit(1)

    message = format_feishu_report(report_path)
    print("Formatted message preview:")
    print(message)
    print()

    # Try OpenClaw message tool first
    feishu_token = os.environ.get("FEISHU_WEBHOOK_TOKEN", "")
    target = os.environ.get("NOTIFY_TARGET", args.target)

    if not target:
        print("ERROR: No Feishu target specified", file=sys.stderr)
        sys.exit(1)

    print(f"Sending to Feishu target: {target}...")

    try:
        result = send_via_openclaw(message, target)
        print(f"Success: {result}")
    except Exception as e:
        print(f"OpenClaw message failed: {e}")
        if feishu_token:
            try:
                result = send_via_webhook(feishu_token, message)
                print(f"Webhook fallback success: {result}")
            except Exception as e2:
                print(f"Webhook also failed: {e2}", file=sys.stderr)
                sys.exit(1)
        else:
            print("No FEISHU_WEBHOOK_TOKEN env var set, skipping send", file=sys.stderr)
            sys.exit(0)


if __name__ == "__main__":
    main()
