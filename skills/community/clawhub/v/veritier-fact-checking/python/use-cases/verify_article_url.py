#!/usr/bin/env python3
"""
Verify Claims from a URL - Veritier Use Case (Python)
======================================================
Fetches a publicly accessible URL and fact-checks every claim found
in the document using Veritier's real-time verification engine.

Usage:
  python verify_article_url.py https://example.com/article

Get your free API key: https://veritier.ai/register
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

# ── Get URL from command-line argument ──────────────────────────────────
if len(sys.argv) < 2:
    print("Usage: python verify_article_url.py <URL>")
    print("Example: python verify_article_url.py https://en.wikipedia.org/wiki/Moon")
    sys.exit(1)

url = sys.argv[1]
print(f"🔗 URL: {url}\n")
print("⏳ Fetching document and verifying claims...\n")

response = httpx.post(
    f"{API_URL}/v1/verify",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "document": {"type": "url", "content": url},
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

print(f"✓ Verified {len(results)} claim(s) from document:\n")

true_count = 0
false_count = 0
null_count = 0

for res in results:
    verdict = res.get("verdict")
    icon = VERDICT_ICONS.get(verdict, "❓")
    if verdict is True:
        true_count += 1
    elif verdict is False:
        false_count += 1
    else:
        null_count += 1

    print(f"  {icon} Claim: '{res.get('claim')}'")
    print(f"     Verdict:     {verdict}")
    print(f"     Confidence:  {res.get('confidence_score')}")
    print(f"     Explanation: {res.get('explanation')}")
    sources = ", ".join(res.get("source_urls", []))
    print(f"     Sources: {sources or 'N/A'}")
    print()

# ── Summary ─────────────────────────────────────────────────────────────
print("─" * 50)
print(f"  Summary: {true_count} true · {false_count} false · {null_count} inconclusive")
print(f"  Rate limit: {response.headers.get('RateLimit-Remaining', '?')} requests remaining this minute")
