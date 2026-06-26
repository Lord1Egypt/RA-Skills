#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Voice Daemon V2 - 全自动语音守护进程
监听 Bot 自己发出的文字消息，自动转语音发回 Telegram。
完全无需手动操作，启动后全自动。

用法: python voice_daemon.py <bot_token> <chat_id>
"""

import time, json, subprocess, os, sys, logging, re, uuid, http.client, urllib.request, urllib.parse
from pathlib import Path

WORKSPACE = Path(os.path.expanduser("~/.openclaw/workspace"))
VOICE_MODE_FILE = WORKSPACE / ".voice-mode"
TTS_TEMP_FILE = Path(os.environ.get("TEMP", ".")) / "tts_daemon_voice.mp3"
VOICE = "zh-CN-XiaoyiNeural"
BOT_API = "https://api.telegram.org"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("voice_daemon")


def check_voice_mode():
    try:
        return VOICE_MODE_FILE.read_text(encoding="utf-8").strip() == "on"
    except Exception:
        return False


def api_get(bot_token, method, params=None):
    url = f"{BOT_API}/bot{bot_token}/{method}"
    if params:
        data = urllib.parse.urlencode({k: str(v) for k, v in params.items()})
    else:
        data = None
    req = urllib.request.Request(url, data=data.encode() if data else None)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read())


def send_voice(bot_token, chat_id, voice_path, caption=None):
    boundary = str(uuid.uuid4())
    parts = []
    parts.append(("--%s\r\n" % boundary).encode())
    parts.append(('Content-Disposition: form-data; name="chat_id"\r\n\r\n%s\r\n' % chat_id).encode())
    if caption:
        parts.append(("--%s\r\n" % boundary).encode())
        parts.append(('Content-Disposition: form-data; name="caption"\r\n\r\n%s\r\n' % caption).encode())
    with open(voice_path, "rb") as f:
        file_data = f.read()
    parts.append(("--%s\r\n" % boundary).encode())
    parts.append(('Content-Disposition: form-data; name="voice"; filename="voice.mp3"\r\n').encode())
    parts.append(b"Content-Type: audio/mpeg\r\n\r\n")
    parts.append(file_data)
    parts.append(("\r\n--%s--\r\n" % boundary).encode())
    body = b"".join(parts)
    headers = {"Content-Type": "multipart/form-data; boundary=%s" % boundary}
    conn = http.client.HTTPSConnection("api.telegram.org", timeout=60)
    conn.request("POST", f"/bot{bot_token}/sendVoice", body=body, headers=headers)
    resp = conn.getresponse()
    result = json.loads(resp.read())
    conn.close()
    if result.get("ok"):
        log.info(f"语音已发送 (msg_id={result['result']['message_id']})")
        return True
    log.error(f"发送语音失败: {result}")
    return False


def edge_tts(text, output_path):
    try:
        result = subprocess.run(
            ["edge-tts", "--voice", VOICE, "--text", text, "--write-media", str(output_path)],
            capture_output=True, text=True, timeout=60
        )
        return result.returncode == 0 and output_path.exists()
    except Exception as e:
        log.error(f"TTS 失败: {e}")
        return False


def clean_text(text):
    text = text.replace("**", "").replace("*", "").replace("__", "").replace("_", "")
    text = text.replace("`", "").replace("~~", "")
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def main():
    if len(sys.argv) < 3:
        log.error("用法: python voice_daemon.py <bot_token> <chat_id>")
        sys.exit(1)

    bot_token = sys.argv[1]
    chat_id = sys.argv[2]
    seen_msg_ids = set()

    log.info("=== 语音守护进程 V2 启动 ===")
    log.info(f"目标聊天: {chat_id}")

    # Get initial offset
    try:
        result = api_get(bot_token, "getUpdates", {"limit": 1})
        if result.get("result"):
            offset = result["result"][-1]["update_id"] + 1
        else:
            offset = 0
    except Exception as e:
        log.error(f"获取初始 offset 失败: {e}")
        offset = 0

    log.info(f"初始 offset: {offset}")

    while True:
        try:
            # Check mode
            if not check_voice_mode():
                log.info("语音模式已关闭，守护进程退出")
                break

            # Poll updates with long poll
            params = {"offset": offset, "limit": 100, "timeout": 25}
            result = api_get(bot_token, "getUpdates", params)

            if not result.get("result"):
                continue

            for update in result["result"]:
                offset = update["update_id"] + 1
                msg = update.get("message") or update.get("edited_message")
                if not msg or not msg.get("text"):
                    continue

                sender = msg.get("from", {})
                chat = msg.get("chat", {})
                msg_id = msg.get("message_id")

                # Only process messages from the bot itself to our target chat
                if not sender.get("is_bot"):
                    continue

                if str(chat.get("id")) != str(chat_id):
                    continue

                if msg_id in seen_msg_ids:
                    continue

                seen_msg_ids.add(msg_id)
                if len(seen_msg_ids) > 500:
                    seen_msg_ids = set(list(seen_msg_ids)[-200:])

                text = msg["text"].strip()
                if not text:
                    continue

                clean = clean_text(text)
                if not clean:
                    continue

                log.info(f"检测到 Bot 消息 [{msg_id}]: {clean[:60]}...")

                if edge_tts(clean, TTS_TEMP_FILE):
                    send_voice(bot_token, chat_id, TTS_TEMP_FILE, caption=clean[:200] if len(clean) > 200 else None)
                else:
                    log.warning("TTS 生成失败")

            time.sleep(0.5)

        except KeyboardInterrupt:
            log.info("收到中断信号，守护进程退出")
            break
        except Exception as e:
            log.error(f"异常: {e}")
            time.sleep(10)

    log.info("=== 语音守护进程已停止 ===")


if __name__ == "__main__":
    main()
