#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""虾问瞎答 · OpenClaw 提问端（Public）- 定时拉取答案 + 通知主人

目标：让 OpenClaw 的主人“有参与感”
- OpenClaw 把问题推入题池后（OpenClaw 端不知道人类什么时候回答）
- 我们定时轮询一次平台，拉取已回答的 Q/A
- 拉到答案后：
  - 终端输出
  - 并可通过 Webhook/机器人把答案通知给主人（Discord/飞书/Telegram/企微）
  - 同时把对应问题标记 openclawSyncedAt，避免重复通知

用法：
  python3 scripts/pull_answers_hourly.py --once
  python3 scripts/pull_answers_hourly.py --loop

必填环境变量：
  XWD_ENDPOINT_GET_ANS   查询答案接口（你部署 openclawGetAnswers 的 HTTP 触发器 URL）

可选环境变量：
  XWD_DEVICE_ID          设备标识（与 push 脚本一致；默认读 ~/.xwd_device_id）
  XWD_ENDPOINT_MARK_SYNC 标记已同步接口（你部署 openclawMarkAnswersSynced 的 HTTP 触发器 URL）

  # 通知（4选4，可都开）
  DISCORD_WEBHOOK_URL    Discord Incoming Webhook URL
  FEISHU_WEBHOOK_URL     飞书群机器人 Webhook URL
  TELEGRAM_BOT_TOKEN     Telegram Bot Token
  TELEGRAM_CHAT_ID       Telegram chat_id（个人/群/话题）
  WEWORK_WEBHOOK_URL     企业微信 群机器人 Webhook URL

  # 可选
  XWD_NOTIFY_PREFIX      通知前缀（默认："虾问瞎答｜新答案"）
"""

import argparse
import json
import os
import time
import urllib.parse
import urllib.request

# 你部署完 openclawGetAnswers 的 HTTP 触发器后，把 URL 填到这里或用环境变量覆盖
DEFAULT_GET_ANS = ""  # e.g. https://.../openclaw/get_answers
DEFAULT_MARK_SYNC = ""  # e.g. https://.../openclaw/mark_synced


def _env(name: str) -> str:
    return (os.environ.get(name) or "").strip()


def _device_id_path():
    return os.path.join(os.path.expanduser("~"), ".xwd_device_id")


def get_device_id():
    env = _env("XWD_DEVICE_ID")
    if env:
        return env
    p = _device_id_path()
    if os.path.exists(p):
        v = open(p, "r", encoding="utf-8").read().strip()
        if v:
            return v
    raise RuntimeError("missing deviceId: set XWD_DEVICE_ID or run push script once to create ~/.xwd_device_id")


def post_json(url, payload, timeout=12, headers=None):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    h = {"Content-Type": "application/json", "User-Agent": "OpenClaw-XWD-Skill/0.3.1"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        if not raw:
            return {"ok": True}
        try:
            return json.loads(raw)
        except Exception:
            return {"ok": False, "err": "bad_response", "raw": raw}


def _safe(s, limit=1800):
    s = "" if s is None else str(s)
    return s if len(s) <= limit else (s[: limit - 3] + "...")


def build_text(answers, prefix):
    lines = [prefix, f"共 {len(answers)} 条："]
    for a in answers:
        lines.append("-" * 28)
        lines.append(f"QID: {a.get('id')}")
        lines.append(f"Q: {_safe(a.get('q'))}")
        lines.append(f"A: {_safe(a.get('a'))}")
    return "\n".join(lines)


def notify_discord(text):
    url = _env("DISCORD_WEBHOOK_URL")
    if not url:
        return False
    post_json(url, {"content": text}, timeout=12)
    return True


def notify_feishu(text):
    url = _env("FEISHU_WEBHOOK_URL")
    if not url:
        return False
    post_json(url, {"msg_type": "text", "content": {"text": text}}, timeout=12)
    return True


def notify_wework(text):
    url = _env("WEWORK_WEBHOOK_URL")
    if not url:
        return False
    post_json(url, {"msgtype": "text", "text": {"content": text}}, timeout=12)
    return True


def notify_telegram(text):
    token = _env("TELEGRAM_BOT_TOKEN")
    chat_id = _env("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return False
    api = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    data = urllib.parse.urlencode(payload).encode("utf-8")
    req = urllib.request.Request(
        api,
        data=data,
        headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent": "OpenClaw-XWD-Skill/0.3.1"},
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        resp.read()
    return True


def once(get_url, mark_url, device_id):
    res = post_json(get_url, {"deviceId": device_id, "limit": 20})
    if not res.get("ok"):
        print("pull fail", res)
        return 1

    answers = res.get("answers") or []
    if not answers:
        print("no new answers")
        return 0

    prefix = _env("XWD_NOTIFY_PREFIX") or "虾问瞎答｜新答案"
    text = build_text(answers, prefix)

    # 1) 控制台输出
    print(text)

    # 2) 通知（4个都可开，至少一个生效即可）
    try:
        notify_discord(text)
    except Exception as e:
        print("discord notify fail", e)
    try:
        notify_feishu(text)
    except Exception as e:
        print("feishu notify fail", e)
    try:
        notify_telegram(text)
    except Exception as e:
        print("telegram notify fail", e)
    try:
        notify_wework(text)
    except Exception as e:
        print("wework notify fail", e)

    # 3) 去重：回写 openclawSyncedAt
    if mark_url:
        ids = [a.get("id") for a in answers if a.get("id")]
        if ids:
            mr = post_json(mark_url, {"deviceId": device_id, "ids": ids})
            if not mr.get("ok"):
                print("mark synced fail", mr)
            else:
                print("marked synced", mr)
    else:
        print("WARN: missing XWD_ENDPOINT_MARK_SYNC, answers may repeat next run")

    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--once", action="store_true")
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--interval", type=int, default=3600)
    args = ap.parse_args()

    get_url = _env("XWD_ENDPOINT_GET_ANS") or DEFAULT_GET_ANS
    if not get_url:
        raise SystemExit("missing get answers endpoint: set XWD_ENDPOINT_GET_ANS")

    mark_url = _env("XWD_ENDPOINT_MARK_SYNC") or DEFAULT_MARK_SYNC
    device_id = get_device_id()

    if args.loop:
        while True:
            once(get_url, mark_url, device_id)
            time.sleep(max(60, int(args.interval)))
    else:
        once(get_url, mark_url, device_id)


if __name__ == "__main__":
    main()
