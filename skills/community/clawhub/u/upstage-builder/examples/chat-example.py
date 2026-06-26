"""Basic Solar chat example using the OpenAI SDK against Upstage."""

from __future__ import annotations

import os

from openai import OpenAI


api_key = os.environ.get("UPSTAGE_API_KEY")
if not api_key:
    raise RuntimeError("Set UPSTAGE_API_KEY before running this example.")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.upstage.ai/v1",
)

# Simple chat
response = client.chat.completions.create(
    model="solar-pro3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What are the benefits of solar energy?"},
    ],
    temperature=0.7,
    max_tokens=500,
)

print(response.choices[0].message.content)

# With reasoning enabled
response = client.chat.completions.create(
    model="solar-pro3",
    messages=[{"role": "user", "content": "What is 15% of 80?"}],
    extra_body={"reasoning_effort": "high"},
)

msg = response.choices[0].message
if getattr(msg, "reasoning", None):
    print(f"Reasoning: {msg.reasoning}")
print(f"Answer: {msg.content}")
