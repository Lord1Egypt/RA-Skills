#!/usr/bin/env python3
"""
Hallucination Audit - Veritier Use Case (Python)
=================================================
Demonstrates how to use Veritier as a post-generation safety net
for LLM outputs. Feeds simulated AI-generated text through the
verification engine and highlights any false claims.

This is the #1 use case for AI developers: catch hallucinations
before they reach users.

Usage:
  python hallucination_audit.py

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

# ── Simulated LLM output (contains deliberate hallucinations) ──────────
llm_output = (
    "Albert Einstein won the Nobel Prize in Physics in 1921 for his "
    "discovery of the photoelectric effect. He was born in Munich, Germany "
    "on March 14, 1879. Einstein published his theory of general relativity "
    "in 1915, and he later became the second president of Israel in 1952."
)

print("🤖 Simulated LLM output:")
print(f"   \"{llm_output}\"\n")
print("⏳ Auditing for hallucinations...\n")

response = httpx.post(
    f"{API_URL}/v1/verify",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "text": llm_output,
        "grounding_mode": "web",
    },
    timeout=120.0,
)

if response.status_code != 200:
    print(f"✗ API error ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
results = data.get("results", [])

# ── Separate true claims from hallucinations ────────────────────────────
hallucinations = [r for r in results if r.get("verdict") is False]
verified = [r for r in results if r.get("verdict") is True]
inconclusive = [r for r in results if r.get("verdict") is None]

if hallucinations:
    print(f"🚨 HALLUCINATIONS DETECTED ({len(hallucinations)}):\n")
    for res in hallucinations:
        print(f"  ❌ \"{res.get('claim')}\"")
        print(f"     Why it's wrong: {res.get('explanation')}")
        sources = ", ".join(res.get("source_urls", []))
        print(f"     Evidence: {sources or 'N/A'}")
        print()
else:
    print("✅ No hallucinations detected.\n")

if verified:
    print(f"✅ Verified claims ({len(verified)}):")
    for res in verified:
        print(f"   ✓ \"{res.get('claim')}\"")
    print()

if inconclusive:
    print(f"❓ Inconclusive ({len(inconclusive)}):")
    for res in inconclusive:
        print(f"   ? \"{res.get('claim')}\"")
    print()

# ── Verdict ─────────────────────────────────────────────────────────────
total = len(results)
print("─" * 50)
if hallucinations:
    pct = len(hallucinations) / total * 100 if total else 0
    print(f"  ⚠ Audit result: {len(hallucinations)}/{total} claims are false ({pct:.0f}% hallucination rate)")
    print("  → This LLM output should NOT be published without correction.")
else:
    print("  ✓ Audit result: All claims verified. Safe to publish.")
