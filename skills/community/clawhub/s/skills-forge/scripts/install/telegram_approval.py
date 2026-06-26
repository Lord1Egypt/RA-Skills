#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.approval import derive_secret, hash_skill_dir, issue_token
from lib.telegram_config import discover_telegram_config


APPROVE_WORDS = {"y", "yes", "approve", "approved", "同意", "同意安装", "安装", "确认"}
REJECT_WORDS = {"n", "no", "reject", "rejected", "拒绝", "拒绝安装", "取消", "不同意"}


def api_url(token: str, method: str) -> str:
    return f"https://api.telegram.org/bot{token}/{method}"


def post_json(token: str, method: str, payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        api_url(token, method),
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_json(token: str, method: str, params: dict) -> dict:
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{api_url(token, method)}?{query}", timeout=35) as response:
        return json.loads(response.read().decode("utf-8"))


def approval_message(args: argparse.Namespace, request_id: str) -> str:
    agent = args.agent_name or "未指定"
    eval_text = "通过" if args.evaluation_passed else "未通过"
    return (
        "Skill Forge 安装审批\n\n"
        f"Skill: {args.skill}\n"
        f"Profile: {args.profile}\n"
        f"Agent: {agent}\n"
        f"Validation: {args.validation_grade} / {args.validation_score}\n"
        f"Hidden Eval: {eval_text} / {args.evaluation_score}\n"
        f"Target: {args.target}\n"
        f"Method: {args.method}\n"
        f"Request: {request_id}\n\n"
        "回复“同意安装”或“yes”批准。\n"
        "回复“拒绝安装”或“no”拒绝。\n"
        "为了安全，非回复消息需要包含 Request ID。"
    )


def normalize(text: str) -> str:
    return " ".join(text.strip().lower().split())


def classify_response(text: str) -> Optional[bool]:
    normalized = normalize(text)
    tokens = set(normalized.replace("，", " ").replace(",", " ").split())
    if normalized in APPROVE_WORDS or tokens & APPROVE_WORDS:
        return True
    if normalized in REJECT_WORDS or tokens & REJECT_WORDS:
        return False
    return None


def message_matches_request(message: dict, request_id: str, approval_message_id: int) -> bool:
    reply = message.get("reply_to_message") or {}
    if reply.get("message_id") == approval_message_id:
        return True
    text = message.get("text", "")
    return request_id in text


def wait_for_approval(token: str, chat_id: str, request_id: str, message_id: int, timeout_seconds: int) -> dict:
    started = time.time()
    offset = None
    while time.time() - started < timeout_seconds:
        params = {
            "timeout": 25,
            "allowed_updates": json.dumps(["message"]),
        }
        if offset is not None:
            params["offset"] = offset
        updates = get_json(token, "getUpdates", params)
        for update in updates.get("result", []):
            offset = update["update_id"] + 1
            message = update.get("message") or {}
            chat = message.get("chat") or {}
            if str(chat.get("id")) != str(chat_id):
                continue
            if not message_matches_request(message, request_id, message_id):
                continue
            decision = classify_response(message.get("text", ""))
            if decision is True:
                return {"approved": True, "status": "approved", "request_id": request_id}
            if decision is False:
                return {"approved": False, "status": "rejected", "request_id": request_id}
    return {"approved": False, "status": "timeout", "request_id": request_id}


def dry_run_result(mode: str, request_id: str) -> dict:
    if mode == "approve":
        return {"approved": True, "status": "approved", "request_id": request_id, "dry_run": True}
    if mode == "reject":
        return {"approved": False, "status": "rejected", "request_id": request_id, "dry_run": True}
    return {"approved": False, "status": "timeout", "request_id": request_id, "dry_run": True}


def build_token_claims(args: argparse.Namespace, request_id: str, mode: str) -> dict:
    source_dir = ""
    source_hash = ""
    if args.source_dir:
        source_path = Path(args.source_dir).expanduser().resolve()
        if not source_path.is_dir():
            raise ValueError("source-dir must be an existing skill directory")
        if not (source_path / "SKILL.md").is_file():
            raise ValueError("source-dir must contain SKILL.md")
        source_dir = str(source_path)
        source_hash = hash_skill_dir(source_path)
    target = str(Path(args.target).expanduser().resolve()) if args.target else ""
    return {
        "request_id": request_id,
        "skill": args.skill,
        "profile": args.profile,
        "source_dir": source_dir,
        "source_hash": source_hash,
        "target": target,
        "method": args.method,
        "mode": mode,
    }


def attach_token(payload: dict, args: argparse.Namespace, secret: Optional[bytes], mode: str) -> dict:
    if secret is None:
        payload["approval_token"] = None
        payload["token_error"] = "no-secret-available"
        return payload
    try:
        claims = build_token_claims(args, payload["request_id"], mode)
    except ValueError as exc:
        payload["approval_token"] = None
        payload["token_error"] = f"invalid-source-dir: {exc}"
        return payload
    payload["approval_token"] = issue_token(claims, secret, ttl_seconds=args.token_ttl)
    payload["approval_claims"] = claims
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Ask for Telegram approval before installing a generated skill.")
    parser.add_argument("--skill", required=True)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--agent-name", default="")
    parser.add_argument("--validation-score", required=True)
    parser.add_argument("--validation-grade", required=True)
    parser.add_argument("--evaluation-score", required=True)
    parser.add_argument("--evaluation-passed", action="store_true")
    parser.add_argument("--target", required=True)
    parser.add_argument("--method", required=True)
    parser.add_argument("--source-dir", default="", help="Candidate skill directory; bound to the issued approval token.")
    parser.add_argument("--token-ttl", type=int, default=1800, help="Approval token lifetime in seconds.")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--bot-token-env", default="TELEGRAM_BOT_TOKEN")
    parser.add_argument("--chat-id-env", default="TELEGRAM_CHAT_ID")
    parser.add_argument("--env-file", default="")
    parser.add_argument("--no-default-env-files", action="store_true")
    parser.add_argument("--dry-run", choices=["off", "approve", "reject", "timeout"], default="off")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    request_id = uuid.uuid4().hex[:16]
    config = discover_telegram_config(
        args.bot_token_env,
        args.chat_id_env,
        args.env_file,
        load_defaults=not args.no_default_env_files,
    )
    token = os.getenv(config["token_env"] or args.bot_token_env)
    chat_id = os.getenv(config["chat_id_env"] or args.chat_id_env)

    try:
        secret = derive_secret(token)
    except RuntimeError:
        secret = None

    if args.dry_run != "off":
        payload = dry_run_result(args.dry_run, request_id)
        if payload["approved"]:
            payload = attach_token(payload, args, secret, mode="dry-run")
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
        return 0 if payload["approved"] else 1

    if not token or not chat_id:
        payload = {
            "approved": False,
            "status": "missing-config",
            "request_id": request_id,
            "required_env": [args.bot_token_env, args.chat_id_env],
            "config": config,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
        return 1

    try:
        sent = post_json(
            token,
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": approval_message(args, request_id),
                "disable_web_page_preview": True,
            },
        )
    except Exception as exc:
        payload = {
            "approved": False,
            "status": "send-error",
            "request_id": request_id,
            "error": str(exc),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
        return 1

    if not sent.get("ok"):
        payload = {
            "approved": False,
            "status": "telegram-error",
            "request_id": request_id,
            "error": sent.get("description") or "telegram sendMessage failed",
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
        return 1

    message_id = sent["result"]["message_id"]
    try:
        payload = wait_for_approval(token, chat_id, request_id, message_id, args.timeout)
    except Exception as exc:
        payload = {
            "approved": False,
            "status": "poll-error",
            "request_id": request_id,
            "error": str(exc),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
        return 1

    payload["message_id"] = message_id
    if payload["approved"] and secret is not None:
        payload = attach_token(payload, args, secret, mode="telegram")
    print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["status"])
    return 0 if payload["approved"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
