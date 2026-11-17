#!/usr/bin/env python3
"""Rebuild current worked outputs offline from their committed research inputs."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from universe_core import (  # noqa: E402
    build_universe,
    load_policy,
    read_json,
    write_artifacts,
)

EXAMPLES = (
    "cn-medium", "us-light", "us-medium", "us-heavy", "us-max",
    "crypto-medium", "hk-medium", "jp-medium", "kr-medium", "uk-medium",
)


def write(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    policy = load_policy()
    summary = []
    # Validate the complete set before replacing any committed output.
    with tempfile.TemporaryDirectory() as temporary:
        staging = Path(temporary)
        built = {}
        for name in EXAMPLES:
            folder = ROOT / "examples" / name
            market = name.split("-")[0]
            snapshot_folder = ROOT / "examples" / f"{market}-medium"
            universe, report = build_universe(
                read_json(folder / "build-spec.json"),
                read_json(snapshot_folder / "snapshot.json"),
                policy,
                built.get("us-heavy") if name == "us-max" else None,
            )
            if not report.get("qualified"):
                raise RuntimeError(f"{name}: worked examples must be fully qualified")
            built[name] = universe
            write_artifacts(universe, report, staging / name / "output")
            summary.append({
                "example": name,
                "entities": len(universe["members"]),
                "references": len(universe["coverage_plan"]["references"]),
                "qualified": report["qualified"],
                "version_hash": universe["version_hash"],
                "content_hash": universe["content_hash"],
                "warnings": report["warnings"],
            })
        for name in EXAMPLES:
            folder = ROOT / "examples" / name
            for output in (staging / name).iterdir():
                destination = folder / output.name
                if destination.is_dir():
                    shutil.rmtree(destination)
                elif destination.exists():
                    destination.unlink()
                shutil.move(str(output), str(destination))
        write(ROOT / "examples" / "build-summary.json", {"examples": summary})
    for item in summary:
        print(f"{item['example']}: {item['entities']} entities; qualified")


if __name__ == "__main__":
    main()
