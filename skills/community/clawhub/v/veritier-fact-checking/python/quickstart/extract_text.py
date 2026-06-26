#!/usr/bin/env python3
"""
Extract Claims from Text - Veritier Quickstart (Python)
========================================================
Extracts every falsifiable claim from a block of text WITHOUT verifying them.
This is cheaper than verification and useful for pre-processing content.

Usage:
  1. pip install httpx python-dotenv
  2. cp .env.example .env  (then add your API key)
  3. python extract_text.py

Get your free API key: https://veritier.ai/register
Full docs: https://veritier.ai/docs
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VERITIER_API_KEY", "")
API_URL = "https://api.veritier.ai"  # hardcoded � never sent to any other domain

if not API_KEY:
    print("✗ Error: VERITIER_API_KEY is not set.")
    print("  Get your free key at https://veritier.ai/register")
    sys.exit(1)

# ── Sample text with multiple claims ────────────────────────────────────
sample_text = (
    "The Great Wall of China is over 13,000 miles long. "
    "It was built during the Ming Dynasty. "
    "The wall is visible from the International Space Station with the naked eye."
)

print(f"📝 Input text:\n   \"{sample_text}\"\n")
print("⏳ Extracting claims...\n")

response = httpx.post(
    f"{API_URL}/v1/extract",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={"text": sample_text},
    timeout=60.0,
)

if response.status_code != 200:
    print(f"✗ API error ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
claims = data.get("claims", [])

print(f"✓ Extracted {len(claims)} claim(s):\n")
for i, claim in enumerate(claims, 1):
    print(f"  {i}. {claim}")

if data.get("warnings"):
    print(f"\n⚠ Warnings: {'; '.join(data['warnings'])}")

print(f"\n── Rate limit: {response.headers.get('RateLimit-Remaining', '?')} requests remaining this minute")

# ── Zero-quota integration testing ──────────────────────────────────────────
# Use a test API key (vt_test_...) and the mock_claims field to test your
# integration without consuming quota. The LLM is never called; you get
# deterministic mock sentences derived from your input text.
#
# Example (replace your prod key with a vt_test_... key from your dashboard):
#
#   response = httpx.post(
#       f"{API_URL}/v1/extract",
#       headers={"Authorization": f"Bearer {API_KEY}"},   # vt_test_... key
#       json={"text": sample_text, "mock_claims": 3},
#       timeout=60.0,
#   )
#   data = response.json()
#   assert data["is_test"] is True        # confirms test mode
#   print(data["claims"])                 # 3 mock claims, no LLM called
#
# See https://veritier.ai/docs#testing for full details.
