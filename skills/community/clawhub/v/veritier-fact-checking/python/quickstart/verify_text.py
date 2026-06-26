#!/usr/bin/env python3
"""
Verify Claims from Text - Veritier Quickstart (Python)
=======================================================
Extracts and fact-checks every claim in a block of text using live web evidence.

Usage:
  1. pip install httpx python-dotenv
  2. cp .env.example .env  (then add your API key)
  3. python verify_text.py

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

# ── Sample text with a mix of true and false claims ─────────────────────
sample_text = (
    "Python was created by Guido van Rossum and first released in 1991. "
    "The language is named after the British comedy group Monty Python. "
    "Python 3 was released in December 2010."
)

print(f"📝 Input text:\n   \"{sample_text}\"\n")
print("⏳ Verifying claims against live web evidence...\n")

response = httpx.post(
    f"{API_URL}/v1/verify",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "text": sample_text,
        "grounding_mode": "web",
    },
    timeout=120.0,
)

if response.status_code != 200:
    print(f"✗ API error ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
results = data.get("results", [])

VERDICT_ICONS = {True: "✅", False: "❌", None: "❓"}

print(f"✓ Verified {len(results)} claim(s):\n")
for res in results:
    verdict = res.get("verdict")
    icon = VERDICT_ICONS.get(verdict, "❓")
    print(f"  {icon} Claim: '{res.get('claim')}'")
    print(f"     Verdict:    {verdict}")
    print(f"     Confidence: {res.get('confidence_score')}")
    print(f"     Explanation: {res.get('explanation')}")
    sources = ", ".join(res.get("source_urls", []))
    print(f"     Sources: {sources or 'N/A'}")
    print()

if data.get("warnings"):
    print(f"⚠ Warnings: {'; '.join(data['warnings'])}")

print(f"── Rate limit: {response.headers.get('RateLimit-Remaining', '?')} requests remaining this minute")

# ── Zero-quota integration testing ──────────────────────────────────────────
# Use a test API key (vt_test_...) and the mock_verdict field to test your
# integration without consuming your monthly verification quota.
# Returns 3 deterministic ClaimResult objects; no LLM is called.
#
# mock_verdict=True  → all verdicts True  (happy-path / success handling)
# mock_verdict=False → all verdicts False (error-path / failure handling)
#
# Example (replace your prod key with a vt_test_... key from your dashboard):
#
#   response = httpx.post(
#       f"{API_URL}/v1/verify",
#       headers={"Authorization": f"Bearer {API_KEY}"},   # vt_test_... key
#       json={"text": sample_text, "mock_verdict": True},
#       timeout=60.0,
#   )
#   data = response.json()
#   assert data["is_test"] is True                         # confirms test mode
#   assert all(r["verdict"] is True for r in data["results"])
#
# See https://veritier.ai/docs#testing for full details.
