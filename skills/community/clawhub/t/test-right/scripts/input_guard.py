#!/usr/bin/env python3
"""Freeze and check declared experiment inputs. No model or network client."""

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import sys


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON field: {key}")
        result[key] = value
    return result


def read_json(path):
    def invalid_constant(value):
        raise ValueError(f"Invalid JSON constant: {value}")

    return json.loads(Path(path).read_text(encoding="utf-8"),
                      object_pairs_hook=unique_object,
                      parse_constant=invalid_constant)


def validate_source(source):
    if not isinstance(source, dict) or set(source) != {
        "request", "instructions", "files", "settings"
    }:
        raise ValueError("Source requires exactly request, instructions, files and settings")
    if not isinstance(source["request"], str) or not source["request"].strip():
        raise ValueError("request must be nonempty text")
    if not isinstance(source["instructions"], str):
        raise ValueError("instructions must be text")
    if not isinstance(source["settings"], dict):
        raise ValueError("settings must be an object")
    if not isinstance(source["files"], dict):
        raise ValueError("files must map relative paths to text")
    for name, content in source["files"].items():
        parts = name.split("/")
        if (not name or "\\" in name or "\x00" in name or ":" in name
                or PurePosixPath(name).is_absolute()
                or any(part in ("", ".", "..") for part in parts)):
            raise ValueError("Artifact paths must be portable relative file paths")
        if not isinstance(content, str):
            raise ValueError("Artifact contents must be text")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_private(path, content):
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as stream:
        stream.write(content)


def encode(value):
    return json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n"


def expected_packet(bundle, condition):
    if condition not in ("baseline", "treatment"):
        raise ValueError("condition must be baseline or treatment")
    bundle = Path(bundle)
    manifest = read_json(bundle / "manifest.json")
    if not isinstance(manifest, dict) or manifest.get("format") != 1:
        raise ValueError("Unsupported input bundle")
    if (digest(bundle / "source.json") != manifest.get("source_sha256")
            or digest(bundle / "intervention.md") != manifest.get("intervention_sha256")):
        raise ValueError("Frozen source or intervention changed; prepare a new version")
    source = read_json(bundle / "source.json")
    validate_source(source)
    packet = copy.deepcopy(source)
    packet["augmentation"] = (
        (bundle / "intervention.md").read_bytes().decode("utf-8")
        if condition == "treatment" else ""
    )
    return packet


def prepare(source_path, intervention_path, output):
    source_text = Path(source_path).read_bytes().decode("utf-8")
    source = read_json(source_path)
    validate_source(source)
    intervention = Path(intervention_path).read_bytes().decode("utf-8")
    if not intervention.strip():
        raise ValueError("intervention must be nonempty text")
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False, mode=0o700)
    write_private(output / "source.json", source_text)
    write_private(output / "intervention.md", intervention)
    write_private(output / "manifest.json", encode({
        "format": 1,
        "source_sha256": digest(output / "source.json"),
        "intervention_sha256": digest(output / "intervention.md"),
    }))
    for condition in ("baseline", "treatment"):
        write_private(output / f"{condition}.json", encode(expected_packet(output, condition)))


def check(bundle, condition, outgoing):
    expected = expected_packet(bundle, condition)
    actual = read_json(outgoing)
    if json.dumps(actual, sort_keys=True, allow_nan=False) != json.dumps(expected, sort_keys=True, allow_nan=False):
        raise ValueError("Outgoing inputs differ from the frozen condition; do not dispatch")
    return actual


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("prepare", help="Freeze source and prepare both conditions")
    build.add_argument("--source", required=True)
    build.add_argument("--intervention", required=True)
    build.add_argument("--out", required=True)
    verify = commands.add_parser("check", help="Check a complete outgoing input packet")
    verify.add_argument("--bundle", required=True)
    verify.add_argument("--condition", choices=["baseline", "treatment"], required=True)
    verify.add_argument("--request", required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            prepare(args.source, args.intervention, args.out)
        else:
            check(args.bundle, args.condition, args.request)
    except (OSError, ValueError, TypeError) as error:
        print(f"Input guard: {error}", file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "operation": args.command,
                      "boundary": "declared input packet; source fairness and runtime context need review"}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
