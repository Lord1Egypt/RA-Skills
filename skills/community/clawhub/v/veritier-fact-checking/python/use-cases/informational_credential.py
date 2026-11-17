#!/usr/bin/env python3
"""
Informational Claim Credential on Verify - Veritier Use Case (Python)
=====================================================================
Optional action_id on POST /v1/verify mints a signed workpaper. Verdicts stay
the same; verify is not fail-closed. Use attest_action to gate a tool call.

Usage:
  python informational_credential.py

Docs: https://veritier.ai/docs#attestation
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
    sys.exit(1)

body = {
    "text": "Water boils at 100 degrees Celsius at standard pressure.",
    "grounding_mode": "web",
    "action_id": "verify_workpaper_demo",
}
if API_KEY.startswith("vt_test_"):
    body["mock_verdict"] = True
    print("TEST MODE: mock_verdict=true plus action_id\n")

response = httpx.post(
    f"{API_URL}/v1/verify",
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
cred = data.get("credential") or {}
print(f"claims: {len(data.get('results', []))}")
print(f"informational credential: {cred.get('id')}")
print(f"verify_url: {cred.get('verify_url')}")
print("Verify is not fail-closed. Use attest_action to gate an action.")

if cred.get("id"):
    pub = httpx.get(f"{API_URL}/v1/credentials/{cred['id']}", timeout=15.0)
    print(f"\npublic GET decision: {pub.json().get('decision') if pub.status_code == 200 else pub.status_code}")

if data.get("warnings"):
    print(f"\nWarnings: {'; '.join(data['warnings'])}")
