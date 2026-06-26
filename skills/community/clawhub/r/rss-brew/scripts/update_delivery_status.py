#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict


def read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Update RSS-Brew delivery state without mutating pipeline state")
    ap.add_argument("--data-root", default="/root/workplace/2 Areas/rss-brew-data")
    ap.add_argument("--status", required=True, choices=["sent", "failed", "pending"])
    ap.add_argument("--message", default="")
    args = ap.parse_args()

    data_root = Path(args.data_root)
    latest = read_json(data_root / "run-records" / "latest-run.json", {})
    manifest_path = Path(latest.get("manifest", "")) if isinstance(latest, dict) else Path("")
    if not manifest_path.exists():
        raise SystemExit("No latest manifest found")

    manifest: Dict[str, Any] = read_json(manifest_path, {})
    if not isinstance(manifest, dict):
        raise SystemExit("Invalid manifest")

    # Keep pipeline state unchanged; delivery is tracked separately.
    manifest["delivery_status"] = args.status
    manifest["delivery_updated_at"] = datetime.now(timezone.utc).isoformat()
    if args.message:
        manifest["delivery_note"] = args.message
    write_json(manifest_path, manifest)

    delivery_state_path = data_root / "run-records" / manifest.get("day", "unknown") / "delivery-state.json"
    write_json(
        delivery_state_path,
        {
            "day": manifest.get("day"),
            "run_id": manifest.get("run_id"),
            "pipeline_status": manifest.get("status"),
            "delivery_status": manifest.get("delivery_status"),
            "updated_at": manifest.get("delivery_updated_at"),
            "note": manifest.get("delivery_note", ""),
        },
    )

    print(f"[delivery] updated {manifest_path} -> {args.status}")


if __name__ == "__main__":
    main()
