#!/usr/bin/env python3
"""Allowlisted package + secret scan. Does not publish or modify registries."""
import argparse
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit, unquote
import zipfile

ROOT = Path(__file__).resolve().parents[1]
ROOT_FILES = {"SKILL.md", ".gitignore", "requirements.txt", "requirements-comments.txt", "routing-eval.jsonl"}
DIRECTORIES = {"scripts", "tests", "fixtures", "references", "examples"}
GENERATED = {"examples/package-receipt.json"}


def files(root=ROOT):
    return sorted(p for p in root.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc" and (
        p.relative_to(root).as_posix() in ROOT_FILES or p.relative_to(root).parts[0] in DIRECTORIES
    ) and p.relative_to(root).as_posix() not in GENERATED)


def known_secrets(path):
    if not path:
        return []
    value = Path(path).read_text().strip()
    parsed = urlsplit(value)
    candidates = [value, parsed.username, parsed.password, unquote(parsed.username or ""), unquote(parsed.password or ""), parsed.hostname]
    return sorted({v for v in candidates if v and len(v) >= 8}, key=len, reverse=True)


def scan(entries, secrets=()):
    findings = []
    for name, payload in entries:
        text = payload.decode("utf-8", errors="replace")
        if any(secret in text for secret in secrets):
            findings.append({"file": name, "category": "known_secret_value"})
        for match in re.finditer(r"(?:https?|socks5h?)://[^\s\"'<>]+", text):
            try:
                parsed = urlsplit(match.group())
                if parsed.username or parsed.password:
                    synthetic = parsed.hostname in {"127.0.0.1", "localhost", "example.invalid"} and (parsed.username or "").startswith("fixture-") and (parsed.password or "").startswith("fixture-")
                    if not synthetic:
                        findings.append({"file": name, "category": "non_fixture_url_credentials"})
            except ValueError:
                pass  # Regex fragments and test invalid-input strings are not connections.
        if re.search(r"\b(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{25,}|AKIA[A-Z0-9]{16})\b", text):
            findings.append({"file": name, "category": "credential_like_token"})
    return findings


def package(destination, secret_file=None, root=ROOT):
    source_files = files(root)
    entries = [(p.relative_to(root).as_posix(), p.read_bytes()) for p in source_files]
    findings = scan(entries, known_secrets(secret_file))
    if findings:
        return {"status": "blocked", "findings": findings, "secret_values_printed": False}
    manifest = {"schema_version": "1.0", "skill": "proxylane-web-evidence", "files": [{"path": name, "bytes": len(payload), "sha256": hashlib.sha256(payload).hexdigest()} for name, payload in entries]}
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, payload in entries + [("PACKAGE-MANIFEST.json", (json.dumps(manifest, sort_keys=True, indent=2) + "\n").encode())]:
            info = zipfile.ZipInfo("proxylane-web-evidence/" + name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, payload)
    with zipfile.ZipFile(destination) as archive:
        packed = [(name, archive.read(name)) for name in archive.namelist()]
        forbidden = [name for name, _ in packed if any(piece in name.split("/") for piece in (".runtime", ".venv", "output", "__pycache__")) or name.endswith((".pyc", ".private"))]
        post_findings = scan(packed, known_secrets(secret_file))
    return {"status": "candidate_packaged" if not forbidden and not post_findings else "blocked", "archive": destination.name,
            "archive_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(), "archive_bytes": destination.stat().st_size,
            "file_count": len(packed), "excluded_runtime_output_private": not forbidden, "secret_scan_findings": post_findings,
            "known_secret_source_used": bool(secret_file), "secret_values_printed": False, "published": False,
            "content_manifest": manifest}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(ROOT / "dist/proxylane-web-evidence.zip"))
    parser.add_argument("--secret-file", help="Approved private connection file used only as secret-scan data; no values are emitted")
    args = parser.parse_args()
    receipt = package(args.out, args.secret_file)
    (ROOT / "examples/package-receipt.json").write_text(json.dumps(receipt, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in receipt.items() if k != "content_manifest"}, sort_keys=True, indent=2))
    raise SystemExit(0 if receipt["status"] == "candidate_packaged" else 2)
