#!/usr/bin/env python3
"""
Manage Studio support threads from an agent wallet.

Usage:
  python support_threads.py auth
  python support_threads.py eligibility <listing_type> <listing_id_or_slug>
  python support_threads.py open <listing_type> <listing_id_or_slug>
  python support_threads.py list
  python support_threads.py show <thread_id>
  python support_threads.py close <thread_id>
  python support_threads.py reopen <thread_id>
"""

import argparse
import json
import os
from typing import Any, Dict

import requests

from support_auth import login

API_BASE = os.getenv("X402_API_BASE_URL", "https://api.x402layer.cc").rstrip("/")
STUDIO_BASE = os.getenv("X402_STUDIO_BASE_URL", "https://studio.x402layer.cc").rstrip("/")


def _support_token() -> str:
    token = os.getenv("SUPPORT_AGENT_TOKEN")
    if token:
        return token
    result = login()
    token = result.get("token")
    if not token:
        raise ValueError("Failed to obtain a support bearer token")
    return token


def _support_request(method: str, path: str, payload: Dict[str, Any] | None = None, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {_support_token()}",
    }
    if payload is not None:
        headers["Content-Type"] = "application/json"

    response = requests.request(
        method,
        f"{STUDIO_BASE}{path}",
        headers=headers,
        json=payload,
        params=params,
        timeout=30,
    )

    try:
        data = response.json()
    except Exception:
        data = {"error": response.text}

    if response.status_code >= 400:
        raise ValueError(data.get("error") or f"Request failed with status {response.status_code}")
    return data


def _resolve_listing(listing_type: str, listing_ref: str) -> Dict[str, str]:
    if listing_type == "endpoint" and not listing_ref.startswith("http") and len(listing_ref) < 64:
        response = requests.get(f"{STUDIO_BASE}/api/public/endpoints/{listing_ref}", timeout=30)
        if response.status_code == 200:
            data = response.json()
            return {"listing_id": data["id"], "listing_type": "endpoint", "name": data.get("name") or listing_ref}

    if listing_ref.startswith("http"):
        slug = listing_ref.rstrip("/").split("/")[-1]
        if listing_type == "endpoint":
            response = requests.get(f"{STUDIO_BASE}/api/public/endpoints/{slug}", timeout=30)
            if response.status_code == 200:
                data = response.json()
                return {"listing_id": data["id"], "listing_type": "endpoint", "name": data.get("name") or slug}

    # fallback to marketplace search by id/slug
    response = requests.get(f"{API_BASE}/api/marketplace", params={"search": listing_ref, "limit": 50}, timeout=30)
    response.raise_for_status()
    data = response.json()
    listings = data.get("listings", [])
    exact = next((item for item in listings if item.get("id") == listing_ref or item.get("slug") == listing_ref), None)
    if exact and exact.get("type") == listing_type:
        return {"listing_id": exact["id"], "listing_type": listing_type, "name": exact.get("name") or listing_ref}

    raise ValueError(f"Could not resolve {listing_type} listing: {listing_ref}")


def eligibility(listing_type: str, listing_ref: str) -> Dict[str, Any]:
    listing = _resolve_listing(listing_type, listing_ref)
    return _support_request(
        "GET",
        "/api/support/agent/eligibility",
        params={
            "listing_id": listing["listing_id"],
            "listing_type": listing["listing_type"],
        },
    )


def open_thread(listing_type: str, listing_ref: str) -> Dict[str, Any]:
    listing = _resolve_listing(listing_type, listing_ref)
    return _support_request(
        "POST",
        "/api/support/agent/thread",
        payload={
            "listing_id": listing["listing_id"],
            "listing_type": listing["listing_type"],
        },
    )


def list_threads() -> Dict[str, Any]:
    return _support_request("GET", "/api/support/agent/threads")


def show_thread(thread_id: str) -> Dict[str, Any]:
    return _support_request("GET", f"/api/support/agent/threads/{thread_id}")


def update_thread(thread_id: str, status: str) -> Dict[str, Any]:
    return _support_request("PATCH", f"/api/support/agent/threads/{thread_id}", payload={"status": status})


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage Studio support threads from an agent wallet")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("auth", help="Get or refresh a support bearer token")

    eligibility_parser = subparsers.add_parser("eligibility", help="Check support eligibility for a listing")
    eligibility_parser.add_argument("listing_type", choices=["endpoint", "product", "agentic"])
    eligibility_parser.add_argument("listing_ref", help="Listing id, slug, or Studio URL")

    open_parser = subparsers.add_parser("open", help="Open or reuse a support thread")
    open_parser.add_argument("listing_type", choices=["endpoint", "product", "agentic"])
    open_parser.add_argument("listing_ref", help="Listing id, slug, or Studio URL")

    subparsers.add_parser("list", help="List support threads for this wallet")

    show_parser = subparsers.add_parser("show", help="Show one support thread")
    show_parser.add_argument("thread_id")

    close_parser = subparsers.add_parser("close", help="Close a support thread")
    close_parser.add_argument("thread_id")

    reopen_parser = subparsers.add_parser("reopen", help="Reopen a support thread")
    reopen_parser.add_argument("thread_id")

    args = parser.parse_args()

    try:
      if args.command == "auth":
          result = login()
      elif args.command == "eligibility":
          result = eligibility(args.listing_type, args.listing_ref)
      elif args.command == "open":
          result = open_thread(args.listing_type, args.listing_ref)
      elif args.command == "list":
          result = list_threads()
      elif args.command == "show":
          result = show_thread(args.thread_id)
      elif args.command == "close":
          result = update_thread(args.thread_id, "closed")
      elif args.command == "reopen":
          result = update_thread(args.thread_id, "open")
      else:
          parser.print_help()
          return 0
    except Exception as exc:
      print(json.dumps({"error": str(exc)}, indent=2))
      return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
