#!/usr/bin/env python3
"""
Zero-Quota Integration Test - Veritier (Python)
================================================
Validates extract, verify, validate, attest, informational credentials,
reconstruct, JWKS, and revoke WITHOUT consuming monthly quota.

Usage:
  1. pip install httpx python-dotenv
  2. Create a test API key (vt_test_...) in your Veritier dashboard
  3. cp .env.example .env  and set VERITIER_TEST_KEY=vt_test_...
  4. python test_integration.py

See https://veritier.ai/docs#testing
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VERITIER_TEST_KEY") or os.getenv("VERITIER_API_KEY", "")
API_URL = "https://api.veritier.ai"

if not API_KEY:
    print("Error: VERITIER_TEST_KEY (or VERITIER_API_KEY) is not set.")
    print("  Create a test key (vt_test_...) at https://veritier.ai/dashboard")
    sys.exit(1)

if not API_KEY.startswith("vt_test_"):
    print("Warning: API key does not look like a test key (expected vt_test_... prefix).")
    print("  Using a production key here will consume your monthly quota.\n")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

SAMPLE_TEXT = (
    "Python was created by Guido van Rossum. "
    "The language was first released in 1991. "
    "Python is named after the British comedy group Monty Python."
)

failures = []
TOTAL = 10


def check(condition: bool, label: str, detail: str = ""):
    if condition:
        print(f"  OK {label}")
    else:
        msg = f"  FAIL {label}" + (f" - {detail}" if detail else "")
        print(msg)
        failures.append(label)


def run_test(step: int, name: str):
    print(f"\n[{step}/{TOTAL}] {name}")


print("========================================")
print("  Veritier Zero-Quota Integration Test")
print("========================================\n")
print(f"  API URL: {API_URL}")
print(f"  Key:     {API_KEY[:12]}... (length: {len(API_KEY)})\n")

run_test(1, "API connectivity check")
try:
    resp = httpx.get(f"{API_URL}/health", timeout=10.0)
    check(resp.status_code in (200, 404), "Server reachable", f"status={resp.status_code}")
except Exception as exc:
    check(False, "Server reachable", str(exc))

run_test(2, "Extract: mock_claims=3")
try:
    resp = httpx.post(
        f"{API_URL}/v1/extract",
        headers=HEADERS,
        json={"text": SAMPLE_TEXT, "mock_claims": 3},
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        check(len(data.get("claims", [])) == 3, "3 mock claims returned", f"got {len(data.get('claims', []))}")
        check(data.get("is_test") is True, "is_test=true")
        check(resp.headers.get("X-Veritier-Test-Mode") == "true", "X-Veritier-Test-Mode header")
except Exception as exc:
    check(False, "Extract request succeeded", str(exc))

run_test(3, "Extract: mock_claims=0")
try:
    resp = httpx.post(
        f"{API_URL}/v1/extract",
        headers=HEADERS,
        json={"text": SAMPLE_TEXT, "mock_claims": 0},
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        check(data.get("claims") == [], "claims=[]", f"got {data.get('claims')}")
        check(data.get("is_test") is True, "is_test=true")
except Exception as exc:
    check(False, "Extract empty-state request succeeded", str(exc))

run_test(4, "Verify: mock_verdict=true")
try:
    resp = httpx.post(
        f"{API_URL}/v1/verify",
        headers=HEADERS,
        json={"text": SAMPLE_TEXT, "mock_verdict": True},
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])
        check(len(results) == 3, "3 ClaimResult objects", f"got {len(results)}")
        check(all(r["verdict"] is True for r in results), "All verdicts true")
        check("credential" not in data or data.get("credential") is None, "no credential without action_id")
        check(data.get("is_test") is True, "is_test=true")
except Exception as exc:
    check(False, "Verify happy-path request succeeded", str(exc))

run_test(5, "Verify: mock_verdict=false")
try:
    resp = httpx.post(
        f"{API_URL}/v1/verify",
        headers=HEADERS,
        json={"text": SAMPLE_TEXT, "mock_verdict": False},
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        results = data.get("results", [])
        check(all(r["verdict"] is False for r in results), "All verdicts false")
        check(data.get("is_test") is True, "is_test=true")
except Exception as exc:
    check(False, "Verify error-path request succeeded", str(exc))

run_test(6, "Validate: mock_validation=true")
try:
    resp = httpx.post(
        f"{API_URL}/v1/validate",
        headers=HEADERS,
        json={
            "extracted_text": "Certificate of completion issued to Jane Doe.",
            "mock_validation": True,
        },
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        result = data.get("result") or {}
        check(result.get("verdict") == "authentic", "result.verdict=authentic", str(result)[:120])
        check(data.get("is_test") is True, "is_test=true")
except Exception as exc:
    check(False, "Validate request succeeded", str(exc))

run_test(7, "Verify action_id mints informational credential")
inform_id = None
try:
    resp = httpx.post(
        f"{API_URL}/v1/verify",
        headers=HEADERS,
        json={
            "text": SAMPLE_TEXT,
            "mock_verdict": True,
            "action_id": "onboard_inform",
        },
        timeout=30.0,
    )
    check(resp.status_code == 200, "HTTP 200 OK", f"got {resp.status_code}: {resp.text[:120]}")
    if resp.status_code == 200:
        data = resp.json()
        cred = data.get("credential") or {}
        inform_id = cred.get("id")
        check(str(inform_id or "").startswith("crc_"), "credential.id starts with crc_")
        check(data.get("is_test") is True, "is_test=true")
except Exception as exc:
    check(False, "Verify action_id request succeeded", str(exc))

run_test(8, "Attest: mock_decision=allow")
cred_id = None
try:
    resp = httpx.post(
        f"{API_URL}/v1/attest_action",
        headers=HEADERS,
        json={
            "action_id": "onboard_attest",
            "text": "npm install lodash",
            "procedure": "package_exists",
            "mock_decision": "allow",
        },
        timeout=30.0,
    )
    check(
        resp.status_code == 200,
        "HTTP 200 OK (block would also be 200)",
        f"got {resp.status_code}: {resp.text[:120]}",
    )
    if resp.status_code == 200:
        data = resp.json()
        check(data.get("decision") == "allow", "decision=allow")
        cred_id = (data.get("credential") or {}).get("id")
        check(str(cred_id or "").startswith("crc_"), "credential.id starts with crc_")
        check(data.get("is_test") is True, "is_test=true")
except Exception as exc:
    check(False, "Attest request succeeded", str(exc))

run_test(9, "Public reconstruct + JWKS")
try:
    jwk = httpx.get(f"{API_URL}/v1/credentials/.well-known/jwk", timeout=15.0)
    check(jwk.status_code == 200 and jwk.json().get("keys"), "JWKS returns keys")
    target = cred_id or inform_id
    if target:
        pub = httpx.get(f"{API_URL}/v1/credentials/{target}", timeout=15.0)
        check(
            pub.status_code == 200
            and pub.json().get("id") == target
            and pub.json().get("signature_valid") is True,
            "GET /v1/credentials/:id no auth",
            pub.text[:200],
        )
    else:
        check(False, "GET /v1/credentials/:id no auth", "no credential id from prior steps")
except Exception as exc:
    check(False, "Reconstruct/JWKS succeeded", str(exc))

run_test(10, "Issuer revoke")
try:
    target = inform_id or cred_id
    if not target:
        check(False, "revoke target", "no credential id")
    else:
        revoked = httpx.post(
            f"{API_URL}/v1/credentials/{target}/revoke",
            headers=HEADERS,
            timeout=15.0,
        )
        check(
            revoked.status_code == 200 and revoked.json().get("revoked") is True,
            "POST /v1/credentials/:id/revoke",
            f"{revoked.status_code} {revoked.text[:200]}",
        )
        pub = httpx.get(f"{API_URL}/v1/credentials/{target}", timeout=15.0)
        check(
            pub.status_code == 200 and pub.json().get("revoked") is True,
            "public GET still 200 with revoked=true",
            pub.text[:200],
        )
except Exception as exc:
    check(False, "Revoke succeeded", str(exc))

print()
if not failures:
    print("All integration checks passed.")
    print("  Zero quota was consumed. Switch to a production key for live fact-checking.")
    sys.exit(0)

print(f"{len(failures)} check(s) failed:")
for f in failures:
    print(f"  - {f}")
sys.exit(1)
