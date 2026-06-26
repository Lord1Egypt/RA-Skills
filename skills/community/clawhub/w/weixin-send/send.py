#!/usr/bin/env python3
"""
主动向微信 ClawBot 发送文本消息（独立于插件通道）
通过 ilinkai.weixin.qq.com API 直接发送，不依赖 OpenClaw 插件。
"""

import json
import sys
import os
import random
import string
import base64
import urllib.request
import urllib.error
from pathlib import Path

ACCOUNTS_DIR = Path.home() / ".openclaw" / "openclaw-weixin" / "accounts"


def find_account(account_id: str = None) -> tuple:
    """加载账号信息，返回 (账号数据, 账号ID)"""
    if account_id:
        acct_file = ACCOUNTS_DIR / f"{account_id}.json"
        if acct_file.exists():
            return json.loads(acct_file.read_text()), account_id
    if ACCOUNTS_DIR.exists():
        for f in sorted(ACCOUNTS_DIR.glob("*-im-bot.json")):
            return json.loads(f.read_text()), f.stem
    raise FileNotFoundError("未找到微信 bot 账号，请先运行 openclaw channels login")


def find_context_token(account_id: str, to_user: str) -> str:
    ctx_file = ACCOUNTS_DIR / f"{account_id}.context-tokens.json"
    if ctx_file.exists():
        tokens = json.loads(ctx_file.read_text())
        return tokens.get(to_user, "")
    return ""


def generate_client_id() -> str:
    chars = string.ascii_lowercase + string.digits
    return f"openclaw-weixin-{''.join(random.choices(chars, k=21))}"


def random_wechat_uin() -> str:
    return base64.b64encode(str(random.randint(0, 2**32 - 1)).encode()).decode()


def send_text(to_user: str, text: str, account_id: str = None) -> dict:
    """发送文本消息到微信用户"""
    acct, acct_id = find_account(account_id)
    token = acct["token"]
    base_url = acct.get("baseUrl", "https://ilinkai.weixin.qq.com")
    ctx_token = find_context_token(acct_id, to_user)

    body = json.dumps({
        "msg": {
            "from_user_id": "",
            "to_user_id": to_user,
            "client_id": generate_client_id(),
            "message_type": 2,
            "message_state": 2,
            "item_list": [{"type": 1, "text_item": {"text": text}}],
            "context_token": ctx_token,
        }
    }).encode()

    url = f"{base_url.rstrip('/')}/ilink/bot/sendmessage"
    req = urllib.request.Request(
        url, data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "AuthorizationType": "ilink_bot_token",
            "X-WECHAT-UIN": random_wechat_uin(),
        },
        method="POST",
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return {"ok": True, "status": resp.status}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": e.read().decode()}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def list_accounts() -> list:
    accounts = []
    if ACCOUNTS_DIR.exists():
        for f in sorted(ACCOUNTS_DIR.glob("*-im-bot.json")):
            data = json.loads(f.read_text())
            accounts.append({
                "accountId": f.stem,
                "userId": data.get("userId", ""),
                "baseUrl": data.get("baseUrl", ""),
            })
    return accounts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="主动向微信 ClawBot 发送文本消息")
    sub = parser.add_subparsers(dest="cmd")

    send_p = sub.add_parser("send", help="发送文本消息")
    send_p.add_argument("to", help="接收者 user_id (xxx@im.wechat)")
    send_p.add_argument("text", help="消息内容")
    send_p.add_argument("--account", "-a", help="账号 ID（默认自动选择）")

    sub.add_parser("list", help="列出可用账号")

    args = parser.parse_args()

    if args.cmd == "send":
        result = send_text(args.to, args.text, args.account)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0 if result["ok"] else 1)
    elif args.cmd == "list":
        for a in list_accounts():
            print(f"  {a['accountId']} -> {a['userId']}")
    else:
        parser.print_help()
