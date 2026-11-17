#!/usr/bin/env python3
"""
Document Authenticity Scan - Veritier Quickstart (Python)
==========================================================
Runs an authenticity scan on a document URL, base64, or extracted_text.

Usage:
  1. pip install httpx python-dotenv
  2. cp .env.example .env  (then add your API key)
  3. python validate_document.py

REST fields: document_url, document_base64, or extracted_text (not "url").
MCP validate still uses the parameter name "url".

Get your free API key: https://veritier.ai/register
Full docs: https://veritier.ai/docs
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VERITIER_API_KEY", "")
API_URL = "https://api.veritier.ai"

if not API_KEY:
    print("Error: VERITIER_API_KEY is not set.")
    print("  Get your free key at https://veritier.ai/register")
    sys.exit(1)

# Prefer extracted_text for a fast demo. Swap in document_url for a live PDF.
body = {
    "extracted_text": "Certificate of completion issued to Jane Doe on 12 January 2024.",
}
if API_KEY.startswith("vt_test_"):
    body["mock_validation"] = True
    print("TEST MODE: mock_validation=true (no pipeline, no quota)\n")

print("Running authenticity scan...\n")

response = httpx.post(
    f"{API_URL}/v1/validate",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json=body,
    timeout=120.0,
)

if response.status_code != 200:
    print(f"API error ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
result = data.get("result") or data
print(f"verdict:          {result.get('verdict')}")
print(f"fraud_risk_score: {result.get('fraud_risk_score')}")
print(f"document_type:    {result.get('document_type')}")
if data.get("is_test"):
    print("is_test: true")

if data.get("warnings"):
    print(f"\nWarnings: {'; '.join(data['warnings'])}")

print(
    f"\nRate limit: {response.headers.get('RateLimit-Remaining', '?')} "
    "requests remaining this minute"
)
