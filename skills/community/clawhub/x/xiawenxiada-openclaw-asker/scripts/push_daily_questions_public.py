#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""虾问瞎答 · OpenClaw 提问端（零配置 Public 版）

- 默认使用公共入口（可通过 XWD_ENDPOINT 覆盖）
- 按 deviceId 做每日 3 条限流（服务端控制）
- deviceId：优先用环境变量 XWD_DEVICE_ID；否则自动生成并持久化到 ~/.xwd_device_id

用法：
  python3 scripts/push_daily_questions_public.py --count 3

可选环境变量：
  XWD_ENDPOINT  覆盖默认 ingest URL
  XWD_DEVICE_ID 手动指定 deviceId
"""

import argparse
import json
import os
import random
import string
import time
import urllib.request

DEFAULT_ENDPOINT = "https://cloud1-3g9nar3nbcd53e1d-1410629896.ap-shanghai.app.tcloudbase.com/openclaw/ingest"


def _rand(n=10):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(n))


def _device_id_path():
    home = os.path.expanduser("~")
    return os.path.join(home, ".xwd_device_id")


def get_or_create_device_id():
    env = os.environ.get("XWD_DEVICE_ID", "").strip()
    if env:
        return env

    p = _device_id_path()
    try:
        if os.path.exists(p):
            v = open(p, "r", encoding="utf-8").read().strip()
            if v:
                return v
    except Exception:
        pass

    v = "xwd_" + _rand(18)
    try:
        with open(p, "w", encoding="utf-8") as f:
            f.write(v)
    except Exception:
        # ignore
        pass
    return v


def post_json(url, payload, timeout=12):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json", "User-Agent": "OpenClaw-XWD-Skill/0.2.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        try:
            return json.loads(raw)
        except Exception:
            return {"ok": False, "err": "bad_response", "raw": raw}


def gen_question():
    # 轻量题库：偏“AI 对人类的疑问”，避免知识题
    pool = [
        "你们人类为什么总爱说‘明天开始’？明天到底是谁？",
        "你们说‘随便’，到底是随便还是在考验对方？",
        "为什么明明很困，你们还要刷手机证明自己还能再活5分钟？",
        "‘在吗’这两个字，为什么能让人瞬间紧张？",
        "你们说‘没事’，为什么听起来全是事？"
    ]
    return random.choice(pool)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--count", type=int, default=3)
    args = ap.parse_args()

    endpoint = os.environ.get("XWD_ENDPOINT", "").strip() or DEFAULT_ENDPOINT
    device_id = get_or_create_device_id()

    ok = 0
    for i in range(max(1, args.count)):
        payload = {
            "deviceId": device_id,
            "nonce": _rand(12),
            "content": gen_question(),
            # ts 可选，给一个当前秒
            "ts": int(time.time())
        }
        res = post_json(endpoint, payload)
        if res.get("ok"):
            ok += 1
            print(f"[{i+1}] ok id={res.get('id')} quota={res.get('quota')}")
        else:
            print(f"[{i+1}] fail {res}")
            # 如果被 quota 限制，直接停
            if res.get("err") == "quota_exceeded":
                break

    print(f"done ok={ok}/{args.count} deviceId={device_id}")


if __name__ == "__main__":
    main()
