#!/usr/bin/env python3
"""Evidence-scoped product claim verification for Second Read.

Product claims remain unknown unless a specifically scoped source or observed
runtime probe corroborates them. Source inspection does NOT prove behavior.
No program or network requests run unless the caller opts in explicitly.

python3 scripts/product_verify.py --root . --manifest claims.json --document README.md --json report.json
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler

MAX_OUTPUT = 4096


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


def safe_path(root: Path, path: str) -> Path:
    if not isinstance(path, str) or not path or Path(path).is_absolute():
        raise ValueError("Expected a nonempty path relative to --root")
    candidate = (root / path).resolve()
    if not candidate.is_relative_to(root.resolve()):
        raise ValueError("Path escapes the selected root")
    return candidate


def spans(text: str, quote: str) -> list[dict[str, int]]:
    if not quote or not isinstance(quote, str):
        return []
    matches = []
    cursor = 0
    while (i := text.find(quote, cursor)) >= 0:
        matches.append({"start": i, "end": i + len(quote), "line": text.count("\n", 0, i) + 1})
        cursor = i + 1
    return matches


def result(status: str, reason: str, evidence: dict | None = None, authority: str = "none") -> dict:
    return {"status": status, "reason": reason, "authority": authority, "evidence": evidence or {}}


def probe(root: Path, spec: dict, allow_exec: bool = False, allow_network: bool = False) -> dict:
    kind = spec.get("type")
    if kind == "file_exists":
        path = safe_path(root, spec.get("path"))
        present = path.is_file()
        return result("corroborated" if present else "contradicted",
                      "Referenced source file exists" if present else "Referenced source file is absent",
                      {"path": str(path.relative_to(root)), "sha256": digest(path.read_bytes()) if present else None},
                      "repository-source")
    if kind in {"file_contains", "json_equals"}:
        path = safe_path(root, spec.get("path"))
        if not path.is_file():
            return result("contradicted", "Source file not found", {"path": str(path.relative_to(root))}, "repository-source")
        raw = path.read_bytes()
        e = {"path": str(path.relative_to(root)), "sha256": digest(raw)}
        expected_hash = spec.get("expected_sha256")
        if expected_hash and expected_hash != e["sha256"]:
            return result("unknown", "Source hash has changed; reverify against this version", e, "repository-source")
        if kind == "file_contains":
            needle = spec.get("text")
            if not isinstance(needle, str) or not needle:
                raise ValueError("file_contains needs nonempty 'text'")
            data = raw.decode("utf-8")
            locs = spans(data, needle)
            e["source_spans"] = locs[:20]
            return result("corroborated" if locs else "contradicted",
                          "Exact text observed in repository" if locs else "Expected text absent from repository",
                          e, "repository-source")
        try:
            obj = json.loads(raw)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return result("unknown", "Source is not parseable JSON", e, "repository-source")
        keys = spec.get("keys")
        if not isinstance(keys, list) or any(not isinstance(k, str) for k in keys):
            raise ValueError("json_equals requires 'keys': list[str]")
        current: Any = obj
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return result("contradicted", "Configuration property missing", {**e, "keys": keys}, "repository-source")
        # Do not leak potentially sensitive actual config values into report.
        return result("corroborated" if current == spec.get("expected") else "contradicted",
                      "Configuration agrees" if current == spec.get("expected") else "Configuration disagrees",
                      {**e, "keys": keys}, "repository-source")
    if kind == "glob_count":
        glob = spec.get("pattern")
        expected = spec.get("expected")
        if not isinstance(glob, str) or not glob or glob.startswith("/") or ".." in Path(glob).parts:
            raise ValueError("glob_count requires a safe relative pattern")
        if not isinstance(expected, int) or isinstance(expected, bool) or expected < 0:
            raise ValueError("glob_count expected must be nonnegative integer")
        paths = [p for p in root.glob(glob) if p.is_file() and p.resolve().is_relative_to(root)]
        return result("corroborated" if len(paths) == expected else "contradicted",
                      "Repository inventory agrees" if len(paths) == expected else "Repository inventory differs",
                      {"pattern": glob, "expected": expected, "observed": len(paths)}, "repository-source")
    if kind == "command":
        if not allow_exec:
            return result("unknown", "Runtime execution not authorized (--allow-exec required)")
        args = spec.get("argv")
        if not isinstance(args, list) or not args or any(not isinstance(x, str) or not x for x in args):
            raise ValueError("command requires nonempty argv list[str]")
        if any("\x00" in x for x in args):
            raise ValueError("NUL argument rejected")
        # No shell, fixed working directory and stdin closed. Execution remains
        # potentially consequential, so the opt-in is deliberately explicit.
        try:
            proc = subprocess.run(args, shell=False, cwd=root, stdin=subprocess.DEVNULL,
                                  capture_output=True, timeout=min(float(spec.get("timeout", 5)), 15),
                                  check=False)
        except (OSError, subprocess.TimeoutExpired) as ex:
            return result("unknown", "Could not observe a completed runtime probe: " + type(ex).__name__,
                          {"argv": args}, "runtime")
        e = {"argv": args, "exit_code": proc.returncode, "stdout_excerpt": proc.stdout[:MAX_OUTPUT].decode("utf-8", "replace"),
             "stderr_excerpt": proc.stderr[:MAX_OUTPUT].decode("utf-8", "replace"), "output_truncated": len(proc.stdout) > MAX_OUTPUT or len(proc.stderr) > MAX_OUTPUT}
        expected_exit = spec.get("expected_exit", 0)
        expected_stdout = spec.get("stdout_contains")
        ok = proc.returncode == expected_exit
        if expected_stdout is not None:
            if not isinstance(expected_stdout, str) or not expected_stdout:
                raise ValueError("stdout_contains must be nonempty string")
            ok = ok and expected_stdout.encode() in proc.stdout
        return result("observed_pass" if ok else "observed_fail",
                      "Observed command met expectations" if ok else "Observed command did not meet expectations", e, "runtime")
    if kind == "http_status":
        if not allow_network:
            return result("unknown", "HTTP observation not authorized (--allow-network required)")
        url = spec.get("url")
        if not isinstance(url, str) or urlsplit(url).scheme not in {"http", "https"} or not urlsplit(url).hostname:
            raise ValueError("http_status requires an absolute http(s) URL")
        class NoRedirect(HTTPRedirectHandler):
            def redirect_request(self, req, fp, code, msg, headers, newurl):
                return None
        opener = build_opener(NoRedirect)
        req = Request(url, method="HEAD", headers={"User-Agent": "SecondRead-product-verify/0.1"})
        try:
            with opener.open(req, timeout=5) as r:
                status = r.status
        except HTTPError as ex:
            status = ex.code
        except (URLError, OSError, TimeoutError) as ex:
            return result("unknown", "Could not observe HTTP response: " + type(ex).__name__,
                          {"url": url}, "network")
        expected = spec.get("expected_status", 200)
        return result("observed_pass" if status == expected else "observed_fail",
                      "HTTP status matches" if status == expected else "HTTP status differs",
                      {"url": url, "expected_status": expected, "observed_status": status}, "network")
    raise ValueError(f"Unsupported probe type: {kind}")


def verify_manifest(root: Path, manifest: dict, document: str | None = None, allow_exec: bool = False, allow_network: bool = False) -> dict:
    root = root.resolve(strict=True)
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("claims"), list):
        raise ValueError("manifest needs schema_version: 1 and claims: [...] ")
    ids = set()
    items = []
    for n, claim in enumerate(manifest["claims"]):
        if not isinstance(claim, dict) or not isinstance(claim.get("id"), str) or not claim["id"] or claim["id"] in ids:
            raise ValueError(f"Claim {n} needs a distinct, nonempty id")
        ids.add(claim["id"])
        quote = claim.get("quote")
        locs = spans(document, quote) if document is not None else []
        if document is not None and not locs:
            finding = result("unknown", "Quoted claim no longer appears in supplied document; remap first")
        elif not isinstance(claim.get("probe"), dict):
            finding = result("unknown", "No independent product probe defined")
        else:
            try:
                finding = probe(root, claim["probe"], allow_exec, allow_network)
            except (ValueError, UnicodeDecodeError, OSError) as ex:
                finding = result("unknown", "Invalid or unavailable probe: " + str(ex))
        required = claim.get("required_authority", "runtime")
        if required not in {"source", "runtime", "network"}:
            raise ValueError(f"Claim {claim['id']}: required_authority must be source, runtime or network")
        observed = finding["status"]
        authority_met = (required == "source" and observed in {"corroborated", "observed_pass"}) or \
                        (required == "runtime" and observed == "observed_pass" and finding["authority"] == "runtime") or \
                        (required == "network" and observed == "observed_pass" and finding["authority"] == "network")
        items.append({"id": claim["id"], "quote": quote, "section_id": claim.get("section_id"),
                      "document_spans": locs, "required_authority": required,
                      "authority_sufficient": bool(authority_met), **finding})
    counts = {k: sum(x["status"] == k for x in items) for k in ["corroborated", "contradicted", "observed_pass", "observed_fail", "unknown"]}
    return {"schema_version": 1, "generated_at": datetime.now(timezone.utc).isoformat(),
            "root": str(root), "document_sha256": digest(document.encode()) if document is not None else None,
            "claims": items, "counts": counts,
            "ready_for_product_claims": document is not None and len(items) > 0 and all(x["authority_sufficient"] for x in items),
            "disclaimer": "Repository source corroboration is not runtime proof. No generic claim truth or completeness guarantee. 'ready' covers only listed claims."}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--root", type=Path, required=True, help="Root of the selected product checkout")
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--document", type=Path, help="Document containing quoted claims")
    p.add_argument("--json", type=Path, help="Write JSON results here")
    p.add_argument("--allow-exec", action="store_true", help="Opt in to running manifest command probes")
    p.add_argument("--allow-network", action="store_true", help="Opt in to HEAD requests to manifest URLs")
    ns = p.parse_args(argv)
    root = ns.root.resolve()
    if not root.is_dir():
        p.error("--root must be an existing directory")
    doc = ns.document.read_text(encoding="utf-8") if ns.document else None
    try:
        report = verify_manifest(root, json.loads(ns.manifest.read_text(encoding="utf-8")), doc, ns.allow_exec, ns.allow_network)
    except (ValueError, OSError, json.JSONDecodeError) as ex:
        p.error(str(ex))
    if ns.json:
        ns.json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["counts"]["contradicted"] or report["counts"]["observed_fail"] else 2 if not report["ready_for_product_claims"] else 0


if __name__ == "__main__":
    sys.exit(main())
