#!/usr/bin/env python3
"""
Re-crawl Tencent Docs links and compare with previous snapshots.
"""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


DEFAULT_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
)
BJ_TZ = dt.timezone(dt.timedelta(hours=8))


def now_bj_label() -> str:
    return dt.datetime.now(BJ_TZ).strftime("%Y%m%d_%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run_cmd(cmd: list[str], timeout: int) -> tuple[int, str]:
    p = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    err = (p.stderr or "").strip()
    return p.returncode, err


def parse_doc_id(url: str) -> str | None:
    p = urlparse(url)
    segs = [x for x in p.path.split("/") if x]
    if not segs:
        return None
    doc_id = segs[-1]
    if re.fullmatch(r"D[A-Za-z0-9_-]+", doc_id):
        return doc_id
    return None


def strip_query(url: str) -> str:
    p = urlparse(url)
    if not p.scheme or not p.netloc:
        return url
    return urlunparse((p.scheme, p.netloc, p.path, "", "", ""))


def redact_query_values(url: str | None, keep_keys: set[str] | None = None) -> str | None:
    if not url:
        return url
    p = urlparse(url)
    if not p.scheme or not p.netloc:
        return url

    keep_keys = keep_keys or set()
    pairs = parse_qsl(p.query, keep_blank_values=True)
    if not pairs:
        return strip_query(url)

    redacted_pairs = []
    for k, v in pairs:
        if k in keep_keys:
            redacted_pairs.append((k, v))
        else:
            redacted_pairs.append((k, "REDACTED"))
    redacted_query = urlencode(redacted_pairs, doseq=True)
    return urlunparse((p.scheme, p.netloc, p.path, p.params, redacted_query, ""))


def sanitize_name(name: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fff._-]+", "-", name).strip("-")
    return s or "doc"


def format_ms_bj(ms: int | None) -> str | None:
    if ms is None:
        return None
    try:
        t = dt.datetime.fromtimestamp(ms / 1000, tz=BJ_TZ)
        return t.strftime("%Y-%m-%d %H:%M:%S %z")
    except Exception:
        return None


def extract_opendoc_json(opendoc_path: Path) -> dict[str, Any] | None:
    if not opendoc_path.exists():
        return None
    raw = opendoc_path.read_text(encoding="utf-8", errors="ignore").strip()
    m = re.match(r"^[^(]+\((.*)\)\s*$", raw, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:
        return None


def extract_basic_client_vars(html_text: str) -> dict[str, Any] | None:
    m = re.search(r"atob\('([A-Za-z0-9+/=]+)'\)", html_text)
    if not m:
        return None
    try:
        decoded = base64.b64decode(m.group(1)).decode("utf-8", errors="ignore")
        return json.loads(decoded)
    except Exception:
        return None


def pick_last_modify(op_last: Any, basic_last: Any) -> int | None:
    if isinstance(op_last, int):
        return op_last
    if isinstance(basic_last, int):
        return basic_last
    return None


def fetch_one_doc(
    doc: dict[str, Any],
    idx: int,
    raw_dir: Path,
    timeout: int,
    user_agent: str,
    keep_raw: bool,
) -> dict[str, Any]:
    name = str(doc.get("name") or f"doc-{idx}")
    page_url = str(doc.get("url") or "").strip()
    doc_id = str(doc.get("id") or "").strip() or parse_doc_id(page_url)
    public_url = strip_query(page_url) if page_url else page_url
    doc_key = doc_id or public_url or name
    prefix = f"{idx:02d}_{sanitize_name(name)}"

    cookie_path = raw_dir / f"{prefix}.cookies.txt"
    html_path = raw_dir / f"{prefix}.html"
    opendoc_path = raw_dir / f"{prefix}.opendoc.js"
    header_path = raw_dir / f"{prefix}.opendoc.headers.txt"

    errors: list[str] = []
    warnings: list[str] = []

    if not page_url:
        return {
            "name": name,
            "url": public_url,
            "doc_key": doc_key,
            "id": doc_id,
            "fetch_ok": False,
            "errors": ["url is empty"],
        }

    code, err = run_cmd(
        [
            "curl",
            "-sSL",
            "-c",
            str(cookie_path),
            "-b",
            str(cookie_path),
            "-A",
            user_agent,
            page_url,
            "-o",
            str(html_path),
        ],
        timeout=timeout,
    )
    if code != 0:
        errors.append(f"fetch html failed: {err or f'curl exit {code}'}")

    html_text = ""
    if html_path.exists():
        html_text = html_path.read_text(encoding="utf-8", errors="ignore")

    opendoc_url = None
    m = re.search(r'href="(\/\/docs\.qq\.com\/dop-api\/opendoc\?[^"]+)"', html_text)
    if m:
        opendoc_url = "https:" + m.group(1)
    elif doc_id:
        opendoc_url = (
            "https://docs.qq.com/dop-api/opendoc"
            f"?u=&id={doc_id}&normal=1&outformat=1&noEscape=1&commandsFormat=1"
            "&doc_chunk_version=3&preview_token=&doc_chunk_flag=1"
            "&callback=clientVarsCallback&xsrf="
        )
        warnings.append("opendoc url not found in html, use fallback url")
    else:
        errors.append("cannot resolve opendoc url (missing html link and id)")

    if opendoc_url:
        code, err = run_cmd(
            [
                "curl",
                "-sSL",
                "-D",
                str(header_path),
                "-c",
                str(cookie_path),
                "-b",
                str(cookie_path),
                "-e",
                page_url,
                "-A",
                user_agent,
                opendoc_url,
                "-o",
                str(opendoc_path),
            ],
            timeout=timeout,
        )
        if code != 0:
            errors.append(f"fetch opendoc failed: {err or f'curl exit {code}'}")

    html_sha = sha256_file(html_path)
    opendoc_sha = sha256_file(opendoc_path)
    html_size = html_path.stat().st_size if html_path.exists() else 0
    opendoc_size = opendoc_path.stat().st_size if opendoc_path.exists() else 0

    op_json = extract_opendoc_json(opendoc_path)
    bcv = extract_basic_client_vars(html_text)

    cv = op_json.get("clientVars", {}) if isinstance(op_json, dict) else {}
    collab = cv.get("collab_client_vars", {}) if isinstance(cv, dict) else {}
    cgi_code = None
    if isinstance(op_json, dict):
        cgi_code = op_json.get("cgi_code")
    if cgi_code is None and isinstance(cv, dict):
        cgi_code = cv.get("cgicode")

    op_title = cv.get("padTitle") or cv.get("initialTitle")
    op_pad_type = cv.get("padType") or (op_json.get("padType") if isinstance(op_json, dict) else None)
    op_last = cv.get("lastModifyTime")
    rev = collab.get("rev") if isinstance(collab, dict) else None
    doc_status = cv.get("docStatus")

    basic_title = None
    basic_last = None
    basic_pad_type = None
    if isinstance(bcv, dict):
        doc_info = bcv.get("docInfo", {})
        if isinstance(doc_info, dict):
            pad_info = doc_info.get("padInfo", {})
            if isinstance(pad_info, dict):
                basic_title = pad_info.get("padTitle")
                basic_pad_type = pad_info.get("padType")
            basic_last = doc_info.get("lastModifyTime")

    last_modify_ms = pick_last_modify(op_last, basic_last)

    if op_json is None:
        warnings.append("cannot parse opendoc callback json")
    if cgi_code == 999:
        warnings.append("opendoc cgi_code=999, likely smartcanvas restricted payload")

    files: dict[str, str] = {}
    if keep_raw:
        files = {
            "html": str(html_path),
            "opendoc": str(opendoc_path),
            "headers": str(header_path),
            "cookies": str(cookie_path),
        }
    else:
        for p in [html_path, opendoc_path, header_path, cookie_path]:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass

    return {
        "name": name,
        "url": public_url,
        "doc_key": doc_key,
        "id": doc_id,
        "opendoc_url": redact_query_values(opendoc_url, keep_keys={"id"}),
        "title": op_title or basic_title or name,
        "pad_type": op_pad_type or basic_pad_type,
        "last_modify_ms": last_modify_ms,
        "last_modify_bj": format_ms_bj(last_modify_ms),
        "last_modify_ms_opendoc": op_last if isinstance(op_last, int) else None,
        "last_modify_ms_basic": basic_last if isinstance(basic_last, int) else None,
        "rev": rev if isinstance(rev, int) else None,
        "cgi_code": cgi_code,
        "doc_status": doc_status,
        "html_sha256": html_sha,
        "opendoc_sha256": opendoc_sha,
        "html_size": html_size,
        "opendoc_size": opendoc_size,
        "fetch_ok": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "files": files,
    }


def auto_find_baseline_manifest(workspace: Path, current_label: str) -> Path | None:
    root = workspace / "snapshots"
    if not root.exists():
        return None
    manifests: list[Path] = []
    for p in root.glob("*/manifest.json"):
        if p.parent.name == current_label:
            continue
        manifests.append(p)
    if not manifests:
        return None
    manifests.sort(key=lambda x: x.parent.name)
    return manifests[-1]


def compare_docs(
    current_docs: list[dict[str, Any]],
    baseline_docs: list[dict[str, Any]] | None,
) -> dict[str, Any]:
    by_key = {}
    added = 0
    changed = 0
    unchanged = 0
    removed = 0

    old_map = {}
    if baseline_docs:
        old_map = {
            str(d.get("doc_key") or d.get("url")): d
            for d in baseline_docs
            if d.get("doc_key") or d.get("url")
        }

    cur_keys = set()
    for d in current_docs:
        key = str(d.get("doc_key") or d.get("url"))
        cur_keys.add(key)
        old = old_map.get(key)
        if not baseline_docs:
            by_key[key] = {"status": "FIRST_RUN", "diff_fields": []}
            continue
        if old is None:
            added += 1
            by_key[key] = {"status": "NEW", "diff_fields": ["new_document"]}
            continue

        diff_fields = []
        check_keys = [
            "last_modify_ms",
            "rev",
            "cgi_code",
            "title",
            "pad_type",
        ]
        for k in check_keys:
            if d.get(k) != old.get(k):
                diff_fields.append(k)
        if diff_fields:
            changed += 1
            by_key[key] = {"status": "CHANGED", "diff_fields": diff_fields}
        else:
            unchanged += 1
            by_key[key] = {"status": "UNCHANGED", "diff_fields": []}

    if baseline_docs:
        for u in old_map:
            if u not in cur_keys:
                removed += 1

    summary = {
        "total": len(current_docs),
        "added": added,
        "changed": changed,
        "unchanged": unchanged,
        "removed_from_current": removed,
    }
    return {"by_key": by_key, "summary": summary}


def build_report(
    snapshot_label: str,
    generated_at: str,
    baseline_manifest: str | None,
    docs: list[dict[str, Any]],
    cmp_result: dict[str, Any],
) -> str:
    lines = []
    lines.append("# Tencent Docs Update Report")
    lines.append("")
    lines.append(f"- Snapshot: `{snapshot_label}`")
    lines.append(f"- Generated At (Asia/Shanghai): `{generated_at}`")
    lines.append(f"- Baseline Manifest: `{baseline_manifest or 'N/A (first run)'}`")
    lines.append("")

    summary = cmp_result.get("summary", {})
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total: `{summary.get('total', 0)}`")
    lines.append(f"- Added: `{summary.get('added', 0)}`")
    lines.append(f"- Changed: `{summary.get('changed', 0)}`")
    lines.append(f"- Unchanged: `{summary.get('unchanged', 0)}`")
    lines.append(f"- Removed From Current: `{summary.get('removed_from_current', 0)}`")
    lines.append("")

    lines.append("## Details")
    lines.append("")
    lines.append("| Name | Status | Last Modify (BJ) | Rev | CGI Code | Notes |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    by_key = cmp_result.get("by_key", {})
    for d in docs:
        key = str(d.get("doc_key") or d.get("url"))
        c = by_key.get(key, {"status": "UNKNOWN", "diff_fields": []})
        status = c.get("status", "UNKNOWN")
        diff = ",".join(c.get("diff_fields", [])) if c.get("diff_fields") else "-"
        warns = "; ".join(d.get("warnings", [])) if d.get("warnings") else ""
        errs = "; ".join(d.get("errors", [])) if d.get("errors") else ""
        notes = "; ".join(x for x in [diff, warns, errs] if x and x != "-") or "-"
        lines.append(
            "| {name} | {status} | {last} | {rev} | {cgi} | {notes} |".format(
                name=d.get("name") or "-",
                status=status,
                last=d.get("last_modify_bj") or "-",
                rev=d.get("rev") if d.get("rev") is not None else "-",
                cgi=d.get("cgi_code") if d.get("cgi_code") is not None else "-",
                notes=notes.replace("|", "/"),
            )
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Tencent Docs updates with snapshot comparison.")
    parser.add_argument("--config", required=True, help="Path to JSON config file.")
    parser.add_argument("--workspace", default="/tmp/tencent-doc-watch", help="Workspace for snapshots.")
    parser.add_argument("--label", default=now_bj_label(), help="Snapshot label, default is current time.")
    parser.add_argument("--compare", default="", help="Optional baseline manifest path.")
    parser.add_argument("--timeout", type=int, default=60, help="Timeout (seconds) for each curl command.")
    parser.add_argument("--user-agent", default=DEFAULT_UA, help="HTTP User-Agent for curl.")
    parser.add_argument(
        "--keep-raw",
        action="store_true",
        help="Keep raw HTML/opendoc/cookie files under snapshot/raw (disabled by default for privacy).",
    )
    args = parser.parse_args()

    config_path = Path(args.config).expanduser().resolve()
    workspace = Path(args.workspace).expanduser().resolve()
    snapshot_dir = workspace / "snapshots" / args.label
    raw_dir = snapshot_dir / "raw"
    manifest_path = snapshot_dir / "manifest.json"
    report_path = snapshot_dir / "report.md"

    if not config_path.exists():
        print(f"[ERROR] config not found: {config_path}", file=sys.stderr)
        return 2

    cfg = read_json(config_path)
    docs = cfg.get("docs")
    if not isinstance(docs, list) or not docs:
        print("[ERROR] config.docs must be a non-empty array", file=sys.stderr)
        return 2

    raw_dir.mkdir(parents=True, exist_ok=True)

    results = []
    for i, doc in enumerate(docs, start=1):
        if not isinstance(doc, dict):
            continue
        results.append(fetch_one_doc(doc, i, raw_dir, args.timeout, args.user_agent, args.keep_raw))

    if not args.keep_raw:
        shutil.rmtree(raw_dir, ignore_errors=True)

    baseline_manifest_path = None
    if args.compare:
        baseline_manifest_path = Path(args.compare).expanduser().resolve()
        if not baseline_manifest_path.exists():
            print(f"[WARN] baseline manifest not found: {baseline_manifest_path}")
            baseline_manifest_path = None
    else:
        baseline_manifest_path = auto_find_baseline_manifest(workspace, args.label)

    baseline_docs = None
    if baseline_manifest_path:
        try:
            baseline_docs = read_json(baseline_manifest_path).get("docs")
            if not isinstance(baseline_docs, list):
                baseline_docs = None
        except Exception:
            baseline_docs = None

    cmp_result = compare_docs(results, baseline_docs)
    generated_at = dt.datetime.now(BJ_TZ).strftime("%Y-%m-%d %H:%M:%S %z")

    manifest = {
        "generated_at_bj": generated_at,
        "snapshot_label": args.label,
        "config_path": str(config_path),
        "workspace": str(workspace),
        "baseline_manifest": str(baseline_manifest_path) if baseline_manifest_path else None,
        "docs": results,
        "comparison": cmp_result,
    }
    write_json(manifest_path, manifest)
    report_path.write_text(
        build_report(
            snapshot_label=args.label,
            generated_at=generated_at,
            baseline_manifest=str(baseline_manifest_path) if baseline_manifest_path else None,
            docs=results,
            cmp_result=cmp_result,
        ),
        encoding="utf-8",
    )

    summary = cmp_result.get("summary", {})
    print(f"[OK] Snapshot: {snapshot_dir}")
    print(f"[OK] Manifest: {manifest_path}")
    print(f"[OK] Report: {report_path}")
    print(
        "[OK] Summary: total={total}, added={added}, changed={changed}, unchanged={unchanged}, removed={removed}".format(
            total=summary.get("total", 0),
            added=summary.get("added", 0),
            changed=summary.get("changed", 0),
            unchanged=summary.get("unchanged", 0),
            removed=summary.get("removed_from_current", 0),
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
