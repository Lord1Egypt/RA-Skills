#!/usr/bin/env python3
"""
x402Compute — Provision a new compute instance.

Handles the full x402 payment flow:
1. POST /compute/provision → get 402 challenge
2. Sign USDC TransferWithAuthorization locally
3. Resend with X-Payment header → instance provisioned

Usage:
  python provision.py <plan_id> <region> [--months N | --days N] [--os-id ID] [--label NAME] [--network base|solana] [--ssh-public-key KEY | --ssh-key-file PATH] [--model-id ID --mode private|grid]

Example:
  python provision.py vcg-a100-1c-2g-6gb lax --months 1 --label "my-gpu"
  python provision.py vc2-1c-1gb ewr --days 1 --label "test-daily"

AI Machine (one-click GPU running an LLM). Add --model-id and --mode:
  # Private OpenAI-compatible endpoint (returns endpoint URL + API key)
  python provision.py vcg-a100-1c-2g-6gb lax --days 1 --label "my-llm" \
      --model-id llama-3.2-3b --mode private
  # Join the grid & earn (serve as a node; requires 50k SGL staked to the wallet)
  python provision.py vcg-a100-1c-2g-6gb lax --months 1 --label "grid-node" \
      --model-id llama-3.2-3b --mode grid

AI Machines are the Standard tier (not confidential/TEE). See references/ai-machines.md.
"""

import argparse
import json
import os
import sys
from typing import Dict, Optional

import requests

import x402_wire
from solana_signing import create_solana_payment_header, ensure_solana_destination_ready
from wallet_signing import EVM_ASSETS, create_compute_auth_headers, load_compute_chain, load_payment_signer

BASE_URL = "https://compute.x402layer.cc"


def _find_accept_option(challenge: dict, requested_network: str) -> dict:
    # Exact network match (v1 name or exact-case CAIP-2). Unknown networks never match.
    for option in challenge.get("accepts", []):
        if x402_wire.network_name(option.get("network")) == requested_network:
            return option
    raise ValueError(f"No {requested_network} payment option found in 402 challenge")


MAX_SPEND_USD = float(os.getenv("COMPUTE_MAX_SPEND_USD", "500"))


def provision_instance(
    plan: str,
    region: str,
    months: int = 0,
    days: int = 0,
    os_id: int = 2284,
    label: str = "x402-instance",
    network: str = "base",
    ssh_public_key: Optional[str] = None,
    model_id: Optional[str] = None,
    mode: Optional[str] = None,
    skip_confirm: bool = False,
    hours: int = 0,
) -> dict:
    """Provision a compute instance with x402 payment.

    Pass model_id + mode to deploy an AI Machine (one-click GPU running an LLM):
      - mode="private": your own OpenAI-compatible endpoint (URL + API key returned).
                        Sent as the nested ai_machine object {model_id, mode:"private"}.
                        Requires an x402 wallet payment (credits are not accepted).
      - mode="grid":    serve on the grid and earn (requires 50k SGL staked to the wallet).
                        Sent as the nested deploy_node object {model_id}.
    ai_machine and deploy_node are mutually exclusive.
    """
    if hours > 0:
        # By the hour: only when GET /compute/plans shows "hourly": {"enabled": true}. Under 24
        # hours costs the hourly price +15% (machines) or +20% (GPUs); the 402 shows the total.
        prepaid_hours = hours
        duration_label = f"{hours} hour(s)"
    elif days > 0:
        prepaid_hours = days * 24
        duration_label = f"{days} day(s)"
    else:
        prepaid_hours = max(1, months) * 720
        duration_label = f"{max(1, months)} month(s)"
    body = {
        "plan": plan,
        "region": region,
        "os_id": os_id,
        "label": label,
        "prepaid_hours": prepaid_hours,
        "network": network,
    }
    if ssh_public_key:
        body["ssh_public_key"] = ssh_public_key.strip()
    # AI Machine: both model_id and mode are required together. The server takes a
    # NESTED object (not top-level model_id/mode):
    #   private -> ai_machine: {model_id, mode:"private"}   (x402 wallet payment; no credits)
    #   grid    -> deploy_node: {model_id}                  (self-installs a grid node)
    if model_id or mode:
        if not (model_id and mode):
            return {"error": "AI machine requires BOTH --model-id and --mode (private|grid)."}
        if mode.strip() == "private":
            body["ai_machine"] = {"model_id": model_id.strip(), "mode": "private"}
        else:  # grid
            body["deploy_node"] = {"model_id": model_id.strip()}
    body_json = json.dumps(body, separators=(",", ":"))
    auth_chain = load_compute_chain()

    print(f"Provisioning {plan} in {region} for {duration_label}...")

    # Step 1: Get 402 challenge
    path = "/compute/provision"
    auth_headers: Dict[str, str] = {}
    try:
        auth_headers = create_compute_auth_headers("POST", path, body_json, chain=auth_chain)
    except Exception as exc:
        return {"error": f"Failed to build auth headers: {exc}"}
    response = requests.post(
        f"{BASE_URL}/compute/provision",
        data=body_json,
        headers={
            "Content-Type": "application/json",
            **auth_headers,
        },
        timeout=30,
    )

    if response.status_code == 200:
        print("Instance provisioned (no payment required)")
        return response.json()

    if response.status_code != 402:
        return {"error": f"Unexpected status {response.status_code}", "response": response.text[:500]}

    # v2 PAYMENT-REQUIRED header first, v1 JSON body otherwise (x402_wire).
    challenge = x402_wire.read_challenge(response)

    option = _find_accept_option(challenge, network)
    pay_to = option["payTo"]
    amount = int(option["maxAmountRequired"])
    cost_usd = amount / 1_000_000

    if cost_usd > MAX_SPEND_USD:
        return {"error": f"Cost ${cost_usd:.2f} exceeds max spend limit ${MAX_SPEND_USD:.2f}. "
                f"Set COMPUTE_MAX_SPEND_USD to override."}

    print(f"\n--- Payment Confirmation ---")
    print(f"  Plan:        {plan}")
    print(f"  Region:      {region}")
    print(f"  Duration:    {duration_label}")
    if model_id and mode:
        print(f"  AI Machine:  {model_id} ({mode})")
    stablecoin = {"base": "USDC", "solana": "USDC", "robinhood": "USDG"}.get(network, "USDC")
    print(f"  Network:     {network}")
    print(f"  Cost:        ${cost_usd:.2f} {stablecoin}")
    print(f"  Pay to:      {pay_to}")

    if not skip_confirm:
        confirm = input("\nProceed with payment? [y/N] ").strip().lower()
        if confirm not in ("y", "yes"):
            return {"error": "Payment cancelled by user"}

    if network in EVM_ASSETS:
        # Both are EVM EIP-3009 transferWithAuthorization; only the EIP-712 domain differs.
        try:
            signer = load_payment_signer()
        except Exception as exc:
            return {"error": str(exc)}
        header_name, x_payment = signer.create_payment_header(challenge, option, network)
    else:
        ensure_solana_destination_ready(option)
        header_name, x_payment = create_solana_payment_header(challenge, option)

    # Step 2: Pay and provision
    # NOTE: Do NOT send compute auth headers here.
    # The x402 X-Payment header authenticates the payer via on-chain payment.
    # Sending auth headers causes 401 (nonce already consumed from step 1).
    # From here the payment is SENT. A timeout or 5xx is pending, never a reason to pay again.
    try:
        response = requests.post(
            f"{BASE_URL}/compute/provision",
            data=body_json,
            headers={
                "Content-Type": "application/json",
                header_name: x_payment,
            },
            timeout=120,
        )
    except requests.RequestException as exc:
        return x402_wire.pending_result(None, exc)

    print(f"Response: {response.status_code}")

    if response.status_code >= 500:
        print("Payment outcome unknown (server error after paying). Do NOT pay again.")
        return x402_wire.pending_result(response.status_code, response.text)

    if response.status_code == 202:
        # PAID, delivery not yet confirmed. The order exists and the machine is provisioning;
        # the body is the full order (incl. any one-time keys). Do NOT re-run provisioning:
        # that would buy a second machine. Poll the order instead.
        data = response.json()
        order = data.get("order", {})
        print("⏳ Payment accepted, delivery is being confirmed. Do NOT provision again.")
        print(f"   Order ID: {order.get('id', 'N/A')}")
        if data.get("pending_note"):
            print(f"   {data['pending_note']}")
        print(f"   Poll: python instance_details.py {order.get('id', '<id>')}")
        ai = order.get("ai") or (order.get("metadata") or {}).get("ai") or data.get("ai") or {}
        if ai.get("api_key"):
            print(f"   API Key:  {ai['api_key']}  (shown once — store it securely)")
        data["pending"] = True
        return data

    if response.status_code in (200, 201):
        data = response.json()
        order = data.get("order", {})
        print(f"✅ Instance provisioned!")
        print(f"   ID:      {order.get('id', 'N/A')}")
        print(f"   IP:      {order.get('ip_address', 'pending')}")
        print(f"   Plan:    {order.get('plan', plan)}")
        print(f"   Expires: {order.get('expires_at', 'N/A')}")
        # AI Machine (private mode): order.ai = {model_id, api_key, endpoint, ...}. `endpoint` is the
        # HTTPS base URL (already ending in /v1), e.g. https://ai.x402compute.cc/<order-id>/v1. Never
        # fall back to the raw box IP/port: that path is unencrypted.
        ai = order.get("ai") or (order.get("metadata") or {}).get("ai") or data.get("ai") or {}
        endpoint = ai.get("endpoint")
        api_key = ai.get("api_key")
        if endpoint:
            print(f"   Endpoint: {endpoint}  (HTTPS, OpenAI-compatible: /chat/completions, /models; auth: Authorization: Bearer <API_KEY>)")
        elif api_key:
            print(f"   Endpoint: https://ai.x402compute.cc/{order.get('id','<id>')}/v1  (HTTPS; answers 'warming up' until the machine boots)")
        if api_key:
            print(f"   API Key:  {api_key}  (shown once — store it securely)")
        if data.get("tx_hash"):
            print(f"   TX:      {data['tx_hash']}")
        return data

    if response.status_code == 409:
        try:
            body = response.json()
        except Exception:
            body = {}
        if "settlement_pending" in response.text:
            # The payment outcome is not known yet. It may have moved. Do NOT pay again: the
            # server checks the chain and either delivers or credits it back automatically.
            print("⏳ Payment outcome is being confirmed on-chain. Do NOT pay again.")
            return {"pending": True, "settlement_pending": True, "response": body or response.text[:2000]}

    return {"error": f"Provisioning failed: {response.status_code}", "response": response.text[:2000]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision a compute instance")
    parser.add_argument("plan", help="Plan ID (e.g. vcg-a100-1c-2g-6gb)")
    parser.add_argument("region", help="Region ID (e.g. lax)")
    duration = parser.add_mutually_exclusive_group()
    duration.add_argument("--months", type=int, default=0, help="Duration in months (default: 1 if --days not set)")
    duration.add_argument("--days", type=int, default=0, help="Duration in days (minimum: 1)")
    duration.add_argument("--hours", type=int, default=0, help="Duration in hours when hourly rentals are on: machines from 1, GPUs and AI machines from 2; under 24h costs +15%% machines / +20%% GPUs")
    parser.add_argument("--os-id", type=int, default=2284, help="OS image ID (default: 2284 = Ubuntu 24.04)")
    parser.add_argument("--label", default="x402-instance", help="Instance label")
    parser.add_argument("--network", default="base", choices=["base", "solana", "robinhood", "arc"], help="Payment network (base/solana/arc = USDC, robinhood = USDG; direct arc payments min $5)")
    parser.add_argument("--ssh-public-key", help="SSH public key contents (recommended)")
    parser.add_argument("--ssh-key-file", help="Path to SSH public key file (e.g. ~/.ssh/id_ed25519.pub)")
    parser.add_argument("--model-id", help="AI Machine: LLM to deploy (e.g. llama-3.2-3b). Requires --mode.")
    parser.add_argument("--mode", choices=["private", "grid"],
                        help="AI Machine mode: 'private' = your own OpenAI-compatible endpoint; "
                             "'grid' = join the grid & earn (needs 50k SGL staked). Requires --model-id.")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip payment confirmation prompt")
    parser.add_argument("--max-spend", type=float, help="Max USD spend limit (default: $500 or COMPUTE_MAX_SPEND_USD)")
    args = parser.parse_args()
    if args.max_spend is not None:
        MAX_SPEND_USD = args.max_spend
    if args.ssh_public_key and args.ssh_key_file:
        print("Error: provide either --ssh-public-key or --ssh-key-file, not both.")
        sys.exit(1)

    ssh_public_key = args.ssh_public_key
    if args.ssh_key_file:
        try:
            with open(args.ssh_key_file, "r", encoding="utf-8") as handle:
                ssh_public_key = handle.read().strip()
        except OSError as exc:
            print(f"Failed to read SSH key file: {exc}")
            sys.exit(1)

    # Default to 1 month if none of --hours, --days, --months is specified
    months = args.months if args.months > 0 else (0 if (args.days > 0 or args.hours > 0) else 1)
    days = args.days

    result = provision_instance(
        plan=args.plan,
        region=args.region,
        months=months,
        days=days,
        os_id=args.os_id,
        label=args.label,
        network=args.network,
        ssh_public_key=ssh_public_key,
        model_id=args.model_id,
        mode=args.mode,
        skip_confirm=args.yes,
        hours=args.hours,
    )
    if "error" in result:
        print(json.dumps(result, indent=2))
        sys.exit(1)
