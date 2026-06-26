#!/usr/bin/env python3
"""Query Draft Script - Preview a VectCut draft's script content without rendering."""

import os
import sys
import json
import requests

BASE_URL = "https://open.vectcut.com"


def query_draft(draft_id, force_update=True):
    jwt_token = os.environ.get("VECTCUT_API_KEY")
    if not jwt_token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first, then retry querying."
        )

    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json",
    }

    payload = {"draft_id": draft_id, "force_update": force_update}

    resp = requests.post(
        f"{BASE_URL}/cut_jianying/query_script",
        headers=headers,
        json=payload,
        timeout=30,
    )
    body = resp.json()

    if resp.status_code != 200 or not body.get("success"):
        error = body.get("error") or str(body)
        raise RuntimeError(f"query_script failed: {error}")

    output_raw = body.get("output", "")

    # output is a JSON string, parse it
    if isinstance(output_raw, str):
        try:
            draft = json.loads(output_raw)
        except json.JSONDecodeError:
            draft = output_raw
    else:
        draft = output_raw

    return {"draft_id": draft_id, "success": True, "draft": draft}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python query_draft.py <draft_id> [--force-update]")
        sys.exit(1)

    draft_id = sys.argv[1]
    force_update = "--force-update" in sys.argv

    try:
        result = query_draft(draft_id, force_update=force_update)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
