#!/usr/bin/env python3
"""
x402Compute — Resize an active compute instance in place.

Usage:
  python resize_instance.py <instance_id> <plan> [--confirm-disk-resize]

Examples:
  python resize_instance.py abc-123 vc2-2c-4gb
  python resize_instance.py abc-123 do:s-2vcpu-4gb --confirm-disk-resize
"""

import argparse
import json
import sys

import requests

from wallet_signing import create_compute_auth_headers

BASE_URL = "https://compute.x402layer.cc"


def resize_instance(instance_id: str, plan: str, confirm_disk_resize: bool = False) -> dict:
    """Resize a compute instance using compute auth or API key auth."""
    body = {
        "plan": plan,
        "confirm_disk_resize": confirm_disk_resize,
    }
    body_json = json.dumps(body, separators=(",", ":"))
    path = f"/compute/instances/{instance_id}/resize"
    auth_headers = create_compute_auth_headers("POST", path, body_json)

    response = requests.post(
        f"{BASE_URL}/compute/instances/{instance_id}/resize",
        data=body_json,
        headers={
            "Content-Type": "application/json",
            **auth_headers,
        },
        timeout=30,
    )

    if response.status_code != 200:
        return {"error": f"HTTP {response.status_code}", "response": response.text[:500]}

    return response.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resize a compute instance")
    parser.add_argument("instance_id", help="Instance ID to resize")
    parser.add_argument("plan", help="Target plan ID from /compute/plans")
    parser.add_argument(
        "--confirm-disk-resize",
        action="store_true",
        help="Required when the target resize increases disk size",
    )
    args = parser.parse_args()

    result = resize_instance(
        instance_id=args.instance_id,
        plan=args.plan,
        confirm_disk_resize=args.confirm_disk_resize,
    )
    if "error" in result:
        print(json.dumps(result, indent=2))
        sys.exit(1)

    print("Resize started:")
    print(f"  Provider:        {result.get('provider')}")
    print(f"  From Plan:       {result.get('from_plan')}")
    print(f"  To Plan:         {result.get('to_plan')}")
    print(f"  Old Expiry:      {result.get('old_expires_at')}")
    print(f"  New Expiry:      {result.get('new_expires_at')}")
    print(f"  Credit Preserved: ${result.get('remaining_credit', 0):.2f}")
    print(f"  Hours Before:    {result.get('remaining_hours_before')}")
    print(f"  Hours After:     {result.get('remaining_hours_after')}")
    if result.get("provider_action_id"):
        print(f"  Provider Action: {result.get('provider_action_id')}")
