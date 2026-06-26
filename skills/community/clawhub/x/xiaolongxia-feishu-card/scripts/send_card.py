#!/usr/bin/env python3
"""
飞书互动卡片发送脚本（国际版 Feishu schema 2.0 兼容）

用法：
  python3 send_card.py --open-id ou_xxx --title "标题" --content "**内容**"
  python3 send_card.py --open-id ou_xxx --title "标题" --content "内容" --template green
  python3 send_card.py --chat-id oc_xxx --title "标题" --content "内容"  # 发群聊

注意：content 支持 Markdown（**加粗**、*斜体*、`代码`、换行用 \\n）
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error


APP_ID = "cli_a9f5877b3378dbd8"
OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")


def get_app_secret():
    try:
        with open(OPENCLAW_CONFIG) as f:
            config = json.load(f)
        return config["channels"]["feishu"]["appSecret"]
    except Exception as e:
        print(f"❌ 读取 app_secret 失败: {e}", file=sys.stderr)
        sys.exit(1)


def get_token(app_id, app_secret):
    data = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
    token = result.get("tenant_access_token")
    if not token:
        print(f"❌ 获取 token 失败: {result}", file=sys.stderr)
        sys.exit(1)
    return token


def send_card(token, receive_id, receive_id_type, title, content, template="blue"):
    card = {
        "schema": "2.0",
        "header": {
            "title": {"tag": "plain_text", "content": title},
            "template": template,
        },
        "body": {
            "elements": [
                {"tag": "markdown", "content": content}
            ]
        },
    }

    # 关键：双重 stringify
    payload = {
        "receive_id": receive_id,
        "msg_type": "interactive",
        "content": json.dumps(card),  # 第一次 stringify（card → string）
    }
    # 第二次 stringify 在 json.dumps(payload) 时自动发生（string → escaped string）

    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type}",
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"❌ HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    if result.get("code") == 0:
        print(f"✅ 卡片发送成功！message_id: {result['data']['message_id']}")
    else:
        print(f"❌ 发送失败: code={result.get('code')} msg={result.get('msg')}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="发送飞书互动卡片（schema 2.0）")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--open-id", help="接收者 open_id（个人 DM）")
    group.add_argument("--chat-id", help="群聊 chat_id")
    parser.add_argument("--title", required=True, help="卡片标题")
    parser.add_argument("--content", required=True, help="卡片正文（支持 Markdown）")
    parser.add_argument(
        "--template",
        default="blue",
        choices=["blue", "green", "red", "orange", "purple", "grey"],
        help="标题栏颜色（默认 blue）",
    )
    args = parser.parse_args()

    app_secret = get_app_secret()
    token = get_token(APP_ID, app_secret)

    if args.open_id:
        receive_id = args.open_id
        receive_id_type = "open_id"
    else:
        receive_id = args.chat_id
        receive_id_type = "chat_id"

    # 处理 \n 转义（shell 传入的字面 \n 转成真正换行）
    content = args.content.replace("\\n", "\n")

    send_card(token, receive_id, receive_id_type, args.title, content, args.template)


if __name__ == "__main__":
    main()
