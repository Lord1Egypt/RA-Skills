#!/usr/bin/env python3
"""
Reconstruct a Claim Credential - Veritier Quickstart (Python)
=============================================================
Public GET needs no API key. JWKS lists current and previous Ed25519 kids.
Issuer revoke is authenticated and does not delete the workpaper.

Usage:
  python reconstruct_credential.py crc_...
  python reconstruct_credential.py crc_... --revoke   # needs VERITIER_API_KEY

Docs: https://veritier.ai/docs#attestation
"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://api.veritier.ai"
API_KEY = os.getenv("VERITIER_API_KEY", "")

args = [a for a in sys.argv[1:] if a != "--revoke"]
do_revoke = "--revoke" in sys.argv[1:]
cred_id = args[0] if args else os.getenv("VERITIER_CREDENTIAL_ID", "")

if not cred_id:
    print("Usage: python reconstruct_credential.py crc_... [--revoke]")
    sys.exit(1)

jwk = httpx.get(f"{API_URL}/v1/credentials/.well-known/jwk", timeout=15.0)
if jwk.status_code != 200:
    print(f"JWKS error ({jwk.status_code}): {jwk.text}")
    sys.exit(1)
kids = [k.get("kid") for k in jwk.json().get("keys", [])]
print(f"JWKS kids: {kids}\n")

pub = httpx.get(f"{API_URL}/v1/credentials/{cred_id}", timeout=15.0)
if pub.status_code != 200:
    print(f"GET error ({pub.status_code}): {pub.text}")
    sys.exit(1)

data = pub.json()
print(f"id:              {data.get('id')}")
print(f"decision:        {data.get('decision')}")
print(f"procedure:       {data.get('procedure')}")
print(f"action_id:       {data.get('action_id')}")
print(f"engine_version:  {data.get('engine_version')}")
print(f"signature_valid: {data.get('signature_valid')}")
print(f"revoked:         {data.get('revoked')}")
print(f"as_of:           {data.get('as_of')}")
print(f"public page:     https://veritier.ai/c/{cred_id}")
print()
print("This is a workpaper, not a judicial finding.")

if data.get("revoked"):
    print("Issuer revoked this credential. Do not treat the decision as current.")

if do_revoke:
    if not API_KEY:
        print("\n--revoke requires VERITIER_API_KEY (same account that issued it).")
        sys.exit(1)
    revoked = httpx.post(
        f"{API_URL}/v1/credentials/{cred_id}/revoke",
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=15.0,
    )
    print(f"\nrevoke HTTP {revoked.status_code}: {revoked.text[:300]}")
