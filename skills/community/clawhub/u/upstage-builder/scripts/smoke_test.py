"""Smoke-test Upstage chat and embeddings access.

Usage:
  python skills/upstage-builder/scripts/smoke_test.py
"""

from __future__ import annotations

import os

from openai import OpenAI


def fail(message: str, code: int = 1) -> None:
    print(f"FAIL: {message}")
    raise SystemExit(code)


api_key = os.environ.get("UPSTAGE_API_KEY")
if not api_key:
    fail("UPSTAGE_API_KEY is not set")

client = OpenAI(api_key=api_key, base_url="https://api.upstage.ai/v1")

print("[1/2] Chat completion test...")
chat = client.chat.completions.create(
    model="solar-mini",
    messages=[{"role": "user", "content": "Reply with exactly: OK"}],
    max_tokens=10,
)
reply = (chat.choices[0].message.content or "").strip()
print(f"chat_reply={reply!r}")
if reply != "OK":
    fail(f"unexpected chat reply: {reply!r}")

print("[2/2] Embeddings test...")
emb = client.embeddings.create(model="embedding-query", input="solar energy")
vector = emb.data[0].embedding
print(f"embedding_dims={len(vector)}")
if len(vector) != 4096:
    fail(f"unexpected embedding dimension: {len(vector)}")

print("PASS")
