#!/usr/bin/env python3
"""Ensure local VoiceTrust model assets are present.

This script keeps the distributed skill bundle lightweight:
- the ClawHub package contains code + setup logic
- large SpeechBrain model checkpoints are downloaded on demand

Trust and provenance notes:
- this repository maintains the VoiceTrust code and packaging
- the underlying ECAPA speaker-recognition model originates from the SpeechBrain project
- the original upstream model page is https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb
- this downloader currently fetches the required runtime files from the VoiceTrust mirror path
- owner enrollment data remains local runtime state and is never downloaded by this script

Default behavior:
- check whether required local model files exist
- download missing files from the current VoiceTrust mirror path
- report exact status in human or JSON form
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import urllib.request
from pathlib import Path
from urllib.error import HTTPError, URLError

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
RUNTIME_ROOT = PACKAGE_ROOT / "runtime"
MODEL_DIR = RUNTIME_ROOT / "assets" / "models" / "ecapa_voxceleb"
CANONICAL_REPOSITORY = "https://github.com/ChuaKhunngan/VoiceTrust"
MODEL_UPSTREAM = "https://huggingface.co/speechbrain/spkrec-ecapa-voxceleb"
MODEL_MIRROR_NOTE = (
    "The current downloader uses the VoiceTrust mirror path for runtime convenience; "
    "the underlying model originates from the upstream SpeechBrain release above."
)
RAW_BASE_URL = (
    "https://raw.githubusercontent.com/ChuaKhunngan/VoiceTrust/main/"
    "assets/models/ecapa_voxceleb"
)

REQUIRED_FILES = [
    "hyperparams.yaml",
    "classifier.ckpt",
    "embedding_model.ckpt",
    "label_encoder.ckpt",
    "mean_var_norm_emb.ckpt",
]

EXPECTED_SHA256 = {
    "hyperparams.yaml": "6f78854fa04ba59e761437b76a2575d3aba5e5016de3e9b69f0c9a5077fb1a41",
    "classifier.ckpt": "fd9e3634fe68bd0a427c95e354c0c677374f62b3f434e45b78599950d860d535",
    "embedding_model.ckpt": "0575cb64845e6b9a10db9bcb74d5ac32b326b8dc90352671d345e2ee3d0126a2",
    "label_encoder.ckpt": "e13c3a167bb4112685670ee896d20e2b565af16b3a4ceeaa8689fa4d22adb8b9",
    "mean_var_norm_emb.ckpt": "cd70225b05b37be64fc5a95e24395d804231d43f74b2e1e5a513db7b69b34c33",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def file_report() -> dict:
    report = {}
    for name in REQUIRED_FILES:
        path = MODEL_DIR / name
        actual_sha256 = sha256_file(path) if path.exists() else None
        expected_sha256 = EXPECTED_SHA256.get(name)
        report[name] = {
            "present": path.exists(),
            "size_bytes": path.stat().st_size if path.exists() else 0,
            "sha256": actual_sha256,
            "expected_sha256": expected_sha256,
            "verified": bool(path.exists() and actual_sha256 == expected_sha256),
            "path": str(path),
            "url": f"{RAW_BASE_URL}/{name}",
            "model_upstream": MODEL_UPSTREAM,
        }
    return report


def missing_files() -> list[str]:
    return [name for name in REQUIRED_FILES if not (MODEL_DIR / name).exists()]


def verify_file(name: str, path: Path) -> dict:
    expected_sha256 = EXPECTED_SHA256[name]
    actual_sha256 = sha256_file(path)
    verified = actual_sha256 == expected_sha256
    return {
        "file": name,
        "path": str(path),
        "expected_sha256": expected_sha256,
        "sha256": actual_sha256,
        "verified": verified,
        "error": None if verified else "sha256_mismatch",
    }


def download_file(name: str, force: bool = False) -> dict:
    target = MODEL_DIR / name
    url = f"{RAW_BASE_URL}/{name}"
    if target.exists() and not force:
        verification = verify_file(name, target)
        return {
            "file": name,
            "status": "verified_existing" if verification["verified"] else "error",
            "path": str(target),
            "size_bytes": target.stat().st_size,
            "sha256": verification["sha256"],
            "expected_sha256": verification["expected_sha256"],
            "verified": verification["verified"],
            "url": url,
            **({"error": verification["error"]} if verification["error"] else {}),
        }

    tmp = target.with_suffix(target.suffix + ".part")
    try:
        with urllib.request.urlopen(url) as response, tmp.open("wb") as fh:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                fh.write(chunk)
        tmp.replace(target)
        verification = verify_file(name, target)
        if not verification["verified"]:
            target.unlink(missing_ok=True)
            return {
                "file": name,
                "status": "error",
                "path": str(target),
                "size_bytes": 0,
                "sha256": verification["sha256"],
                "expected_sha256": verification["expected_sha256"],
                "verified": False,
                "url": url,
                "error": verification["error"],
            }
        return {
            "file": name,
            "status": "downloaded",
            "path": str(target),
            "size_bytes": target.stat().st_size,
            "sha256": verification["sha256"],
            "expected_sha256": verification["expected_sha256"],
            "verified": True,
            "url": url,
        }
    except (HTTPError, URLError) as e:
        if tmp.exists():
            tmp.unlink()
        return {
            "file": name,
            "status": "error",
            "path": str(target),
            "url": url,
            "error": str(e),
        }


def ensure_models(force: bool = False) -> dict:
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    before_missing = missing_files()
    actions = []

    for name in REQUIRED_FILES:
        if force or name in before_missing:
            actions.append(download_file(name, force=force))

    after_missing = missing_files()
    verification_errors = [a for a in actions if a.get("status") == "error"]
    return {
        "ok": not after_missing and not verification_errors,
        "model_dir": str(MODEL_DIR),
        "canonical_repository": CANONICAL_REPOSITORY,
        "model_upstream": MODEL_UPSTREAM,
        "model_mirror_note": MODEL_MIRROR_NOTE,
        "raw_base_url": RAW_BASE_URL,
        "missing_before": before_missing,
        "missing_after": after_missing,
        "actions": actions,
        "verification_errors": verification_errors,
        "files": file_report(),
    }


def print_human_status(result: dict) -> int:
    if result["ok"]:
        print(f"VoiceTrust model assets ready: {result['model_dir']}")
        print(f"Canonical repository: {result['canonical_repository']}")
        print(f"Model upstream: {result['model_upstream']}")
        print(result["model_mirror_note"])
        if result["actions"]:
            print("Downloaded/checked files:")
            for action in result["actions"]:
                status = action["status"]
                suffix = " (sha256 verified)" if action.get("verified") else ""
                print(f"  - {action['file']}: {status}{suffix}")
        return 0

    print("VoiceTrust model assets are incomplete.")
    print(f"Model dir: {result['model_dir']}")
    print(f"Canonical repository: {result['canonical_repository']}")
    print(f"Model upstream: {result['model_upstream']}")
    print(result["model_mirror_note"])
    print(f"Source: {result['raw_base_url']}")
    print("Missing files after ensure:")
    for name in result["missing_after"]:
        print(f"  - {name}")
    errors = [a for a in result["actions"] if a.get("status") == "error"]
    if errors:
        print()
        print("Download / verification errors:")
        for action in errors:
            detail = action["error"]
            if action.get("expected_sha256"):
                detail += f" (expected {action['expected_sha256']}, got {action.get('sha256')})"
            print(f"  - {action['file']}: {detail}")
    return 2


def main() -> int:
    parser = argparse.ArgumentParser(description="Ensure local VoiceTrust model assets exist")
    parser.add_argument("--json", action="store_true", help="Output machine-readable status")
    parser.add_argument("--check-only", action="store_true", help="Only report status; do not download")
    parser.add_argument("--force", action="store_true", help="Re-download all required files")
    args = parser.parse_args()

    MODEL_DIR.mkdir(parents=True, exist_ok=True)

    if args.check_only:
        report = file_report()
        verified_ok = all(item["verified"] for item in report.values() if item["present"])
        result = {
            "ok": not missing_files() and verified_ok,
            "model_dir": str(MODEL_DIR),
            "canonical_repository": CANONICAL_REPOSITORY,
            "model_upstream": MODEL_UPSTREAM,
            "model_mirror_note": MODEL_MIRROR_NOTE,
            "raw_base_url": RAW_BASE_URL,
            "missing": missing_files(),
            "files": report,
        }
        if args.json:
            print(json.dumps(result, indent=2))
            return 0 if result["ok"] else 2
        if result["ok"]:
            print(f"VoiceTrust model assets ready: {result['model_dir']}")
            print(f"Canonical repository: {result['canonical_repository']}")
            print(f"Model upstream: {result['model_upstream']}")
            print(result["model_mirror_note"])
            return 0
        print("VoiceTrust model assets are missing or failed verification.")
        print(f"Model dir: {result['model_dir']}")
        print(f"Canonical repository: {result['canonical_repository']}")
        print(f"Model upstream: {result['model_upstream']}")
        print(result["model_mirror_note"])
        for name in result["missing"]:
            print(f"  - {name}")
        return 2

    result = ensure_models(force=args.force)
    if args.json:
        print(json.dumps(result, indent=2))
        return 0 if result["ok"] else 2
    return print_human_status(result)


if __name__ == "__main__":
    sys.exit(main())
