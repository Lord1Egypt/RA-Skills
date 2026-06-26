#!/usr/bin/env python3
"""Create a machine-readable redacted manifest for a long external SOTA run."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from sota_public_safety import (
    is_absolute_like,
    sanitize_command_tokens,
    sanitize_path,
)


def parse_key_value(items: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for item in items:
        if "=" not in item:
            raise SystemExit(f"invalid key=value item: {item!r}")
        key, value = item.split("=", 1)
        out[key.strip()] = value.strip()
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="Path to the output JSON file.")
    parser.add_argument("--output-root", required=True, help="Run output root or shared storage path.")
    parser.add_argument("--model-family", required=True, help="Model family or trainer name.")
    parser.add_argument("--dataset-id", default="", help="Logical dataset identifier.")
    parser.add_argument("--dataset-manifest", default="", help="Dataset manifest path or id.")
    parser.add_argument("--gpu-type", default="", help="Requested or observed GPU type.")
    parser.add_argument("--repo", action="append", default=[], help="Repeatable role=name@commit or role=name.")
    parser.add_argument("--threshold", action="append", default=[], help="Repeatable key=value pair.")
    parser.add_argument(
        "--command",
        nargs=argparse.REMAINDER,
        default=[],
        help="Command tokens for the long run. Keep this flag last so trailing tokens are captured.",
    )
    args = parser.parse_args()

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    output_root = Path(args.output_root).expanduser().resolve()
    alias_roots = [(output_root, "$RUN_ROOT")]

    repos = []
    for item in args.repo:
        if "=" not in item:
            raise SystemExit(f"invalid --repo value: {item!r}, expected role=name[@commit]")
        role, ref = item.split("=", 1)
        name, _, commit = ref.partition("@")
        repos.append({"role": role.strip(), "name": name.strip(), "commit": commit.strip()})

    dataset_manifest = args.dataset_manifest.strip()
    if dataset_manifest and is_absolute_like(dataset_manifest):
        dataset_manifest = sanitize_path(
            dataset_manifest,
            alias_roots=alias_roots,
            allow_absolute_paths=False,
        )

    payload = {
        "schema_version": "1.0",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "output_root": sanitize_path(
            output_root,
            alias_roots=alias_roots,
            allow_absolute_paths=False,
        ),
        "model_family": args.model_family,
        "dataset": {
            "dataset_id": args.dataset_id,
            "manifest": dataset_manifest,
        },
        "source_control": repos,
        "runtime": {
            "gpu_type": args.gpu_type,
            "thresholds": parse_key_value(args.threshold),
            "command": sanitize_command_tokens(
                args.command,
                alias_roots=alias_roots,
                allow_absolute_paths=False,
                allow_raw=False,
            ),
        },
        "health": {
            "heartbeat_path": "",
            "log_path": "",
            "session_name": "",
            "supervisor": "",
        },
        "notes": [],
    }

    out_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
