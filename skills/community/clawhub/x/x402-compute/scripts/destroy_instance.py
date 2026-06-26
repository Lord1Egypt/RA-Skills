#!/usr/bin/env python3
"""
x402Compute — Destroy a compute instance.

Usage:
  python destroy_instance.py <instance_id> [--yes]
"""

import argparse
import json
import sys

import requests

from wallet_signing import create_compute_auth_headers

BASE_URL = "https://compute.x402layer.cc"


def destroy_instance(instance_id: str, skip_confirm: bool = False) -> dict:
    """Destroy a compute instance after confirmation."""
    path = f"/compute/instances/{instance_id}"
    auth_headers = create_compute_auth_headers("GET", path)

    details_resp = requests.get(
        f"{BASE_URL}/compute/instances/{instance_id}",
        headers=auth_headers,
        timeout=15,
    )

    if details_resp.status_code == 200:
        info = details_resp.json().get("instance", details_resp.json())
        print(f"\n--- Instance Details ---")
        print(f"  ID:       {info.get('id', instance_id)}")
        print(f"  Label:    {info.get('label', 'N/A')}")
        print(f"  Plan:     {info.get('plan', 'N/A')}")
        print(f"  IP:       {info.get('ip_address', 'N/A')}")
        print(f"  Status:   {info.get('status', 'N/A')}")
        print(f"  Expires:  {info.get('expires_at', 'N/A')}")
    else:
        print(f"  Instance: {instance_id}")
        print(f"  (Could not fetch details: HTTP {details_resp.status_code})")

    if not skip_confirm:
        confirm = input("\n⚠️  This is irreversible. Destroy this instance? [y/N] ").strip().lower()
        if confirm not in ("y", "yes"):
            return {"error": "Destroy cancelled by user"}

    print(f"Destroying instance {instance_id}...")

    auth_headers = create_compute_auth_headers("DELETE", path)
    response = requests.delete(
        f"{BASE_URL}/compute/instances/{instance_id}",
        headers=auth_headers,
        timeout=30,
    )

    if response.status_code == 200:
        data = response.json()
        print("Instance destroyed successfully")
        return data

    return {"error": f"HTTP {response.status_code}", "response": response.text[:500]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Destroy a compute instance")
    parser.add_argument("instance_id", help="Instance ID to destroy")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt")
    args = parser.parse_args()

    result = destroy_instance(args.instance_id, skip_confirm=args.yes)
    if "error" in result:
        print(json.dumps(result, indent=2))
        sys.exit(1)
