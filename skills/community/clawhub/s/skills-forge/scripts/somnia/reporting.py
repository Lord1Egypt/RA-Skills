#!/usr/bin/env python3
import argparse
import json
import os
import urllib.request

def build_markdown(report: dict) -> str:
    lines = [
        "# Skill Forge Nightly Review",
        "",
        f"- created_at: {report['created_at']}",
        f"- skills_checked: {report['summary']['skills_checked']}",
        f"- needs_attention: {report['summary']['needs_attention']}",
        f"- updates_proposed: {report['summary']['updates_proposed']}",
        "",
        "## Findings",
        "",
    ]
    for item in report["skills"]:
        status = "needs-attention" if item["issues"] else "ok"
        lines.extend(
            [
                f"### {item['skill']}",
                "",
                f"- status: {status}",
                f"- validation: {item['validation'].get('grade')} / {item['validation'].get('score')}",
                f"- hidden_eval: {item.get('evaluation_summary', {}).get('status', 'not-run')}",
                f"- replay: {item.get('replay_summary', {}).get('status', 'not-run')}",
                f"- feedback: total={item['feedback']['total']} negative={item['feedback']['negative']}",
                f"- issues: {', '.join(item['issues']) or 'none'}",
                f"- update_status: {item.get('update_status') or 'not-proposed'}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def send_telegram_report(markdown: str, args: argparse.Namespace) -> dict:
    token = os.getenv(args.telegram_bot_token_env)
    chat_id = os.getenv(args.telegram_chat_id_env)
    if not token or not chat_id:
        return {"sent": False, "status": "missing-config"}
    text = markdown
    if len(text) > 3900:
        text = text[:3800].rstrip() + "\n\n[truncated]"
    body = json.dumps({"chat_id": chat_id, "text": text, "disable_web_page_preview": True}).encode("utf-8")
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        return {"sent": False, "status": "send-error", "error": str(exc)}
    if not payload.get("ok"):
        return {"sent": False, "status": "telegram-error", "error": payload.get("description")}
    return {"sent": True, "status": "sent", "message_id": payload.get("result", {}).get("message_id")}

