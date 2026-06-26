# /// script
# dependencies = ["requests"]
# ///
"""
Discover and verify RunPod public endpoint IDs.

Modes:
  verify   — test all endpoints in the registry (default)
  probe    — probe a list of candidate slugs to find valid ones
  add      — probe candidates and auto-add confirmed ones to endpoints.json

Usage:
  discover_endpoints.py verify
  discover_endpoints.py probe --candidates "kokoro-tts,flux-dev,my-endpoint"
  discover_endpoints.py add --candidates "kokoro-tts,flux-dev"
"""

import sys
import json
import argparse
import pathlib
import requests
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from _utils import init_keys

REGISTRY_PATH = pathlib.Path(__file__).parent / "endpoints.json"
RUNPOD_BASE = "https://api.runpod.ai/v2"


def check_endpoint(endpoint_id: str, api_key: str) -> str:
    """Returns 'ok', 'not_found', or 'error:<msg>'"""
    try:
        # Use /health — instant response, no GPU spin-up
        resp = requests.get(
            f"{RUNPOD_BASE}/{endpoint_id}/health",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        if resp.status_code == 404:
            return "not_found"
        if resp.status_code in (200, 401, 403):
            return "ok"
        return f"http_{resp.status_code}"
    except Exception as e:
        return f"error:{e}"


def load_registry() -> dict:
    if not REGISTRY_PATH.exists():
        return {}
    return json.loads(REGISTRY_PATH.read_text())


def save_registry(data: dict):
    REGISTRY_PATH.write_text(json.dumps(data, indent=2))


def get_all_ids(registry: dict) -> list:
    ids = []
    for cat in registry.values():
        if isinstance(cat, dict):
            for eid, meta in cat.items():
                if isinstance(meta, dict) and "name" in meta:
                    ids.append((eid, meta))
    return ids


def main():
    parser = argparse.ArgumentParser(description="Discover and verify RunPod endpoint IDs")
    parser.add_argument("mode", nargs="?", default="verify",
                        choices=["verify", "probe", "add"],
                        help="Mode: verify (check registry), probe (test candidates), add (probe + save)")
    parser.add_argument("--candidates", help="Comma-separated endpoint IDs OR hub playground URLs to probe")
    args = parser.parse_args()

    api_key, _ = init_keys()
    registry = load_registry()

    if args.mode == "verify":
        print("Verifying all endpoints in registry...\n")
        all_ids = get_all_ids(registry)
        ok, broken = [], []
        for eid, meta in all_ids:
            status = check_endpoint(eid, api_key)
            icon = "✅" if status == "ok" else "❌"
            print(f"  {icon} {eid:<40} {meta.get('name','')}")
            (ok if status == "ok" else broken).append(eid)
        print(f"\n{len(ok)} OK, {len(broken)} not found: {broken}")

    elif args.mode in ("probe", "add"):
        if not args.candidates:
            print("--candidates required for probe/add mode", file=sys.stderr)
            sys.exit(1)

        # Accept full hub URLs like https://console.runpod.io/hub/playground/image/google-nano-banana-2-edit
        raw = [c.strip() for c in args.candidates.split(",")]
        candidates = []
        for c in raw:
            if "console.runpod.io/hub/playground/" in c:
                eid = c.rstrip("/").split("/")[-1]
                print(f"  Extracted from URL: {eid}")
                candidates.append(eid)
            else:
                candidates.append(c)
        print(f"Probing {len(candidates)} candidates...\n")
        found = []
        for eid in candidates:
            status = check_endpoint(eid, api_key)
            if status == "ok":
                print(f"  ✅ {eid}")
                found.append(eid)
            else:
                print(f"  ❌ {eid} ({status})")

        print(f"\nFound {len(found)}: {found}")

        if args.mode == "add" and found:
            # Add to registry under "unverified" category
            registry.setdefault("unverified", {})
            for eid in found:
                if eid not in registry.get("unverified", {}):
                    registry["unverified"][eid] = {
                        "name": eid,
                        "type": "unknown",
                        "mode": "sync",
                        "input": {},
                        "output_key": None,
                        "notes": "Auto-discovered — update type/input/output_key manually"
                    }
                    print(f"  Added to registry: {eid}")
            save_registry(registry)
            print(f"\nSaved to {REGISTRY_PATH}")


if __name__ == "__main__":
    main()
