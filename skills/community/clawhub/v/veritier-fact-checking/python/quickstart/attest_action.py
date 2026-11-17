#!/usr/bin/env python3
"""
Attest a Tool Call - Veritier Quickstart (Python)
=================================================
Fail-closed lookup against a named procedure. HTTP 200 with decision=block is
success (the interrupt fired), not an API error.

Does not replace extract, verify, or validate. Live web is not the default.
Named procedures: package_exists, citation_exists (CourtListener existence and
quoted passages in the matched opinion), filing_exists (SEC EDGAR),
statute_exists (Cornell LII U.S. Code / IRC), policy_ground.

Usage:
  1. pip install httpx python-dotenv
  2. cp .env.example .env  (then add your API key)
  3. python attest_action.py

With a vt_test_ key this script sends mock_decision=allow (no live lookup,
no quota). With a production key it runs package_exists against npm.

REST: procedure is required; provide text XOR document; policy_ground uses
grounding_references (not reference_text). MCP is a separate schema.

Get your free API key: https://veritier.ai/register
Full docs: https://veritier.ai/docs#attestation
OpenAPI: https://api.veritier.ai/openapi.json
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

is_test = API_KEY.startswith("vt_test_")
payload = {
    "action_id": "quickstart_install_lodash",
    "text": "npm install lodash",
    "procedure": "package_exists",
    "on_null": "block",
}
if is_test:
    payload["mock_decision"] = "allow"
    print("TEST MODE: mock_decision=allow (no npm lookup, no quota)\n")
else:
    print("LIVE: package_exists against the public npm registry\n")

print(f'Attesting action_id="{payload["action_id"]}"\n')

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
    print(f"API error ({response.status_code}): {response.text}")
    sys.exit(1)

data = response.json()
decision = data.get("decision")
credential = data.get("credential") or {}

print(f"decision: {decision}")
print(f"procedure: {data.get('procedure')}")
print(f"HTTP 200 with decision=block is success (the gate refused the action).")
print()
print(f"credential.id:         {credential.get('id')}")
print(f"credential.verify_url: {credential.get('verify_url')}")
print()
print("Reconstruct without an API key:")
print(f"  GET {API_URL}/v1/credentials/{credential.get('id')}")
print("Public page: https://veritier.ai/c/<id> (400-day TTL)")
print("Issuer revoke: POST /v1/credentials/<id>/revoke")

if data.get("warnings"):
    print(f"\nWarnings: {'; '.join(data['warnings'])}")

print(
    f"\nRate limit: {response.headers.get('RateLimit-Remaining', '?')} "
    "requests remaining this minute"
)

# Other procedures (live, consume claims quota):
#   citation_exists  text="See Roe v. Wade, 410 U.S. 113 (1973)."
#   filing_exists    text="Accession 0000320193-24-000069."
#   statute_exists   text="See 26 U.S.C. § 501(c)(3)."
#   policy_ground    text="Install internal-tool@1.0.0" plus grounding_references
