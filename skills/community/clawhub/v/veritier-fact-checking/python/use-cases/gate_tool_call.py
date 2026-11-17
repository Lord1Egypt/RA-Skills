#!/usr/bin/env python3
"""
Gate a Tool Call - Veritier Use Case (Python)
=============================================
Attest before the agent runs a command. Only proceed on decision=allow.
HTTP 200 with decision=block means refuse the action (success, not an error).

Usage:
  python gate_tool_call.py

With a vt_test_ key this uses mock_decision (no live lookup). Production keys
run package_exists against npm/PyPI.

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

command = "npm install lodash"
payload = {
    "action_id": "agent_npm_install",
    "text": command,
    "procedure": "package_exists",
    "on_null": "block",
}
if API_KEY.startswith("vt_test_"):
    payload["mock_decision"] = "allow"

response = httpx.post(
    f"{API_URL}/v1/attest_action",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json=payload,
    timeout=120.0,
)

if response.status_code != 200:
    print(f"Attest failed ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
decision = data.get("decision")
cred = data.get("credential") or {}

print(f"command:  {command}")
print(f"decision: {decision}")
print(f"workpaper: {cred.get('verify_url')}")

if decision != "allow":
    print("Refusing to run the command. The gate fired.")
    sys.exit(2)

print("Allowed. In a real agent you would now execute the command.")
print("Informational verify credentials are not a gate - use attest_action.")
