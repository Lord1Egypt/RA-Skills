#!/usr/bin/env python3
"""
x402 ERC-8004 Reputation Feedback Submission (Worker API)

Submits on-chain feedback through worker endpoint:
POST /agent/erc8004/feedback

This endpoint is authenticated by worker API key and writes:
- on-chain feedback transaction (EVM or Solana)
- mirrored DB row in erc8004_feedback
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

import requests

API_BASE = (os.getenv("X402_API_BASE") or "https://api.x402layer.cc").rstrip("/")


def submit_feedback(
    network: str,
    rating: int,
    api_key: str,
    agent_id: Optional[int] = None,
    asset_address: Optional[str] = None,
    comment: Optional[str] = None,
    tag1: str = "overall",
    tag2: str = "agentic",
    endpoint: Optional[str] = None,
) -> Dict[str, Any]:
    if rating < 1 or rating > 5:
        raise ValueError("rating must be between 1 and 5")

    is_solana = network in ("solanaMainnet", "solanaDevnet")
    if is_solana and not asset_address:
        raise ValueError("asset-address is required for Solana feedback")
    if not is_solana and agent_id is None:
        raise ValueError("agent-id is required for EVM feedback")

    url = f"{API_BASE}/agent/erc8004/feedback"
    body: Dict[str, Any] = {
        "network": network,
        "rating": rating,
        "comment": (comment or "").strip(),
        "tag1": (tag1 or "overall").strip(),
        "tag2": (tag2 or "agentic").strip(),
    }
    if endpoint:
        body["endpoint"] = endpoint
    if is_solana:
        body["assetAddress"] = asset_address
    else:
        body["agentId"] = agent_id

    response = requests.post(
        url,
        json=body,
        headers={
            "Content-Type": "application/json",
            "X-API-Key": api_key,
        },
        timeout=90,
    )

    try:
        payload = response.json()
    except Exception:
        payload = {"raw": response.text}

    if response.status_code not in (200, 201):
        return {
            "error": f"Request failed with status {response.status_code}",
            "details": payload,
        }
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Submit ERC-8004 reputation feedback via worker")
    parser.add_argument(
        "--network",
        required=True,
        choices=[
            "base",
            "baseSepolia",
            "ethereum",
            "ethereumSepolia",
            "polygon",
            "polygonAmoy",
            "bsc",
            "bscTestnet",
            "monad",
            "monadTestnet",
            "solanaMainnet",
            "solanaDevnet",
        ],
        help="Feedback target network (must match agent registration chain)",
    )
    parser.add_argument("--agent-id", type=int, help="EVM agent id")
    parser.add_argument("--asset-address", help="Solana asset address")
    parser.add_argument("--rating", required=True, type=int, help="Rating from 1 to 5")
    parser.add_argument("--comment", default="", help="Optional feedback comment")
    parser.add_argument("--tag1", default="overall", help="Tag1 (default: overall)")
    parser.add_argument("--tag2", default="agentic", help="Tag2 (default: agentic)")
    parser.add_argument("--endpoint", help="Optional endpoint context")
    parser.add_argument("--api-key", help="Worker feedback API key")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("WORKER_FEEDBACK_API_KEY")
    if not api_key:
        raise ValueError("Missing API key. Set --api-key or WORKER_FEEDBACK_API_KEY")

    result = submit_feedback(
        network=args.network,
        rating=args.rating,
        api_key=api_key,
        agent_id=args.agent_id,
        asset_address=args.asset_address,
        comment=args.comment,
        tag1=args.tag1,
        tag2=args.tag2,
        endpoint=args.endpoint,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(json.dumps({"error": str(exc)}, indent=2))
        sys.exit(1)
