#!/usr/bin/env python3
"""
Skill-D webhook.py：监听 Gitea push webhook，
检测到 confirmed_issue.md 新增时，打印触发信号供 OpenClaw 识别。

启动方式（后台常驻）：
    nohup python3 scripts/webhook.py \
      > ~/.config/skill-d-create-issues/webhook.log 2>&1 &

Gitea 每个受管仓库 Settings → Webhooks → Add Webhook:
  URL: http://<server-ip>:<WEBHOOK_PORT>/gitea-webhook
  Content-Type: application/json
  Trigger: Push Events
  Secret: （与 WEBHOOK_SECRET 一致，留空则不验签）

收到触发后，本服务将在 stdout 打印如下格式的 JSON 触发信号：
  SKILL_D_TRIGGER: {"repo": "owner/repo", "meeting_dir": "2026-04-22-1500"}

OpenClaw 通过读取 webhook.log 或直接接管 stdout 来检测触发信号。
"""

import os
import sys
import json
import hashlib
import hmac
from datetime import datetime

import pytz
from flask import Flask, request, abort
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.config/skill-d-create-issues/.env"))

WEBHOOK_PORT   = int(os.getenv("WEBHOOK_PORT", "8765"))
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "").encode()
TZ             = pytz.timezone("Asia/Shanghai")

app = Flask(__name__)


def verify_signature(payload_bytes: bytes, signature_header: str) -> bool:
    """验证 Gitea HMAC-SHA256 签名（WEBHOOK_SECRET 为空时跳过验证）。"""
    if not WEBHOOK_SECRET:
        return True
    if not signature_header:
        return False
    # Gitea 格式：sha256=<hex>
    prefix = "sha256="
    if not signature_header.startswith(prefix):
        return False
    expected = hmac.new(WEBHOOK_SECRET, payload_bytes, hashlib.sha256).hexdigest()
    received = signature_header[len(prefix):]
    return hmac.compare_digest(expected, received)


def extract_triggers(payload: dict) -> list[dict]:
    """
    从 push payload 中提取所有 confirmed_issue.md 新增事件。
    返回 [{"repo": "owner/repo", "meeting_dir": "YYYY-MM-DD-HHMM"}]
    """
    triggers = []

    repo_full_name = payload.get("repository", {}).get("full_name", "")
    commits = payload.get("commits", [])

    for commit in commits:
        for added_file in commit.get("added", []):
            # 匹配 meetings/<dir>/confirmed_issue.md
            parts = added_file.split("/")
            if (
                len(parts) == 3
                and parts[0] == "meetings"
                and parts[2] == "confirmed_issue.md"
                and parts[1] != "archive"
            ):
                meeting_dir = parts[1]
                triggers.append({
                    "repo":        repo_full_name,
                    "meeting_dir": meeting_dir,
                })

    return triggers


@app.route("/gitea-webhook", methods=["POST"])
def gitea_webhook():
    payload_bytes = request.get_data()

    # 签名验证
    sig = request.headers.get("X-Gitea-Signature", "")
    if not verify_signature(payload_bytes, sig):
        abort(403)

    # 只处理 push 事件
    event = request.headers.get("X-Gitea-Event", "")
    if event != "push":
        return "ignored", 200

    try:
        payload = json.loads(payload_bytes)
    except Exception:
        abort(400)

    triggers = extract_triggers(payload)

    for trigger in triggers:
        # 输出触发信号（OpenClaw 通过日志或 stdout 检测）
        signal = {
            "ts":          datetime.now(TZ).isoformat(),
            "event":       "confirmed_issue_detected",
            "repo":        trigger["repo"],
            "meeting_dir": trigger["meeting_dir"],
        }
        line = f"SKILL_D_TRIGGER: {json.dumps(signal, ensure_ascii=False)}"
        print(line, flush=True)
        sys.stdout.flush()

    return "ok", 200


@app.route("/health", methods=["GET"])
def health():
    return json.dumps({"status": "ok", "port": WEBHOOK_PORT}), 200


if __name__ == "__main__":
    print(
        f"[Skill-D webhook] 启动中，监听端口 {WEBHOOK_PORT}...",
        flush=True,
    )
    print(
        f"[Skill-D webhook] 签名验证：{'已启用' if WEBHOOK_SECRET else '未启用（WEBHOOK_SECRET 为空）'}",
        flush=True,
    )
    app.run(host="0.0.0.0", port=WEBHOOK_PORT, debug=False)
