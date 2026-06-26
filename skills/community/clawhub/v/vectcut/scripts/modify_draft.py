#!/usr/bin/env python3

import argparse
import json
import os
import sys

import requests

BASE_URL = "https://open.vectcut.com"


def modify_draft(draft_id, name=None, cover=None):
    token = os.environ.get("VECTCUT_API_KEY")
    if not token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first."
        )
    if not name and not cover:
        raise RuntimeError("At least one of --name or --cover is required.")

    payload = {"draft_id": draft_id}
    if name:
        payload["name"] = name
    if cover:
        payload["cover"] = cover

    resp = requests.post(
        f"{BASE_URL}/cut_jianying/modify_draft",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=30,
    )
    body = resp.json()
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(body.get("error") or str(body))

    output = body.get("output") or {}
    result = {
        "success": True,
        "draft_id": output.get("draft_id", draft_id),
        "draft_url": output.get("draft_url"),
    }
    if output.get("name") is not None:
        result["name"] = output.get("name")
    if output.get("cover") is not None:
        result["cover"] = output.get("cover")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("draft_id")
    parser.add_argument("--name")
    parser.add_argument("--cover")
    args = parser.parse_args()

    try:
        result = modify_draft(args.draft_id, name=args.name, cover=args.cover)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
