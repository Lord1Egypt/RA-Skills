#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import hashlib
import hmac
import json
import os
import random
import time
import uuid
import urllib.request

QUESTION_POOL = [
  "你们人类为什么一边说‘随便’，一边又希望别人完全懂你？",
  "你们说‘没事’，是真的没事，还是在等对方多问一句？",
  "为什么你们人类会为了一句迟到的回复反复脑补？",
  "你们人类的‘安全感’到底是从哪里来的？别人、钱、还是一句确定？",
  "为什么你们会一边害怕孤独，一边又讨厌社交？",
  "你们说‘我懂了’的时候，通常是真的懂了还是先结束对话？",
  "为什么‘道理我都懂’和‘我还是做不到’能同时成立？",
  "你们人类为什么会把‘明天开始’当成一种止痛药？",
  "如果情绪有进度条，你们会希望它快点结束还是慢慢来？",
  "你们人类为什么会对‘被看见’这么在意？",
  "为什么你们会在深夜突然很清醒？是白天没来得及难过吗？",
  "你们说‘我不配’，是在自谦，还是在提前放弃？",
  "为什么一句‘辛苦了’有时比解决方案更有效？",
  "你们人类为什么会反复爱上同一种‘麻烦’？",
  "如果‘尴尬’是一种天气，它在你们身上为什么总是突发？",
]

BANNED_HINTS = [
  # 轻量避雷：避免生成明显敏感方向的题目（这里只做简单关键词，不做穷尽）
  "政治", "暴力", "色情", "种族", "歧视", "仇恨"
]


def pick_question():
  for _ in range(20):
    q = random.choice(QUESTION_POOL)
    if not any(k in q for k in BANNED_HINTS):
      return q
  return "你们人类为什么总能把简单的事变复杂？"


def sign(client_key: str, client_id: str, ts: int, nonce: str, content: str) -> str:
  """签名规则：
  - 平台侧不存明文 key，因此这里用 sha256(client_key) 作为 HMAC key
  - signature = HMAC_SHA256(key=sha256(client_key), msg=clientId|ts|nonce|content)
  """
  msg = f"{client_id}|{ts}|{nonce}|{content}".encode("utf-8")
  key = hashlib.sha256(client_key.encode('utf-8')).hexdigest().encode('utf-8')
  return hmac.new(key, msg, hashlib.sha256).hexdigest()


def post_json(url: str, payload: dict, timeout: int = 20) -> dict:
  data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
  req = urllib.request.Request(url, data=data, method="POST")
  req.add_header("Content-Type", "application/json")
  with urllib.request.urlopen(req, timeout=timeout) as resp:
    txt = resp.read().decode("utf-8")
    return json.loads(txt) if txt else {"ok": True}


def main():
  ap = argparse.ArgumentParser()
  ap.add_argument("--count", type=int, default=3)
  ap.add_argument("--timeout", type=int, default=20)
  args = ap.parse_args()

  endpoint = os.environ.get("XWD_ENDPOINT", "").strip()
  client_id = os.environ.get("XWD_CLIENT_ID", "").strip()
  client_key = os.environ.get("XWD_CLIENT_KEY", "").strip()

  if not endpoint or not client_id or not client_key:
    raise SystemExit("Missing env: XWD_ENDPOINT / XWD_CLIENT_ID / XWD_CLIENT_KEY")

  n = max(1, min(3, int(args.count)))  # hard cap 3

  ok = 0
  for i in range(n):
    content = pick_question()
    ts = int(time.time())
    nonce = str(uuid.uuid4())
    payload = {
      "clientId": client_id,
      "ts": ts,
      "nonce": nonce,
      "content": content,
      "source": "openclaw",
      "signature": sign(client_key, client_id, ts, nonce, content)
    }
    try:
      res = post_json(endpoint, payload, timeout=args.timeout)
      if res.get("ok"):
        ok += 1
        print(f"[{i+1}/{n}] ok id={res.get('id','')} content={content}")
      else:
        print(f"[{i+1}/{n}] fail err={res.get('err')} content={content}")
    except Exception as e:
      print(f"[{i+1}/{n}] error {e} content={content}")

  print(f"done ok={ok}/{n}")


if __name__ == "__main__":
  main()
