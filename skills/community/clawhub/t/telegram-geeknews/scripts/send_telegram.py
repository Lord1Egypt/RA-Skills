#!/usr/bin/env python3
"""
GeekNews OSS Brief — 텔레그램 전송 스크립트

사용법:
    python3 send_telegram.py --message-file /tmp/geeknews_brief.md
    python3 send_telegram.py --message "직접 메시지 텍스트"

환경변수:
    TELEGRAM_BOT_TOKEN  — 텔레그램 봇 토큰 (필수)
    TELEGRAM_CHAT_ID    — 수신 채팅 ID (필수)
"""

import argparse
import os
import sys
import urllib.request
import urllib.parse
import json


def send_telegram(token: str, chat_id: str, message: str, parse_mode: str = "MarkdownV2") -> dict:
    """텔레그램 메시지 전송"""
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False,
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode())
            if result.get("ok"):
                print(f"✅ 전송 성공 (message_id: {result['result']['message_id']})")
            else:
                print(f"❌ 전송 실패: {result.get('description', 'unknown error')}")
            return result
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ HTTP 에러 {e.code}: {error_body}")
        
        # MarkdownV2 파싱 실패 시 일반 텍스트로 재시도
        if parse_mode == "MarkdownV2" and "can't parse" in error_body.lower():
            print("⚠️  MarkdownV2 파싱 실패, 일반 텍스트로 재시도...")
            return send_telegram(token, chat_id, message, parse_mode="")
        
        sys.exit(1)
    except Exception as e:
        print(f"❌ 전송 실패: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="GeekNews Brief 텔레그램 전송")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--message-file", help="전송할 메시지 파일 경로")
    group.add_argument("--message", help="전송할 메시지 텍스트")
    args = parser.parse_args()

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not token:
        print("❌ TELEGRAM_BOT_TOKEN 환경변수가 설정되지 않았습니다.")
        print("   references/telegram_setup.md 를 참조하세요.")
        sys.exit(1)
    if not chat_id:
        print("❌ TELEGRAM_CHAT_ID 환경변수가 설정되지 않았습니다.")
        print("   references/telegram_setup.md 를 참조하세요.")
        sys.exit(1)

    if args.message_file:
        with open(args.message_file, "r", encoding="utf-8") as f:
            message = f.read().strip()
    else:
        message = args.message

    if not message:
        print("❌ 전송할 메시지가 비어있습니다.")
        sys.exit(1)

    # 텔레그램 메시지 길이 제한 (4096자)
    if len(message) > 4096:
        print(f"⚠️  메시지 길이 {len(message)}자 → 4096자로 잘림")
        message = message[:4090] + "\n..."

    send_telegram(token, chat_id, message)


if __name__ == "__main__":
    main()
