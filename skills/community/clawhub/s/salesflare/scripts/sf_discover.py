#!/usr/bin/env python3
"""Salesflare OpenAPI endpoint discovery.

Examples:
  python3 scripts/sf_discover.py --contains opportunity
  python3 scripts/sf_discover.py --tag Accounts
  python3 scripts/sf_discover.py --method PATCH
  python3 scripts/sf_discover.py --format markdown > references/endpoints-generated.md
"""

from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

DEFAULT_OPENAPI_URL = "https://api.salesflare.com/openapi.json"


def load_spec(src: str) -> dict:
    if src.startswith("http://") or src.startswith("https://"):
        with urllib.request.urlopen(src, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    p = Path(src)
    return json.loads(p.read_text(encoding="utf-8"))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default=DEFAULT_OPENAPI_URL, help="OpenAPI JSON URL or local file path")
    ap.add_argument("--contains", default="", help="Case-insensitive substring filter over path/summary/tags")
    ap.add_argument("--tag", action="append", default=[], help="Tag filter (repeatable)")
    ap.add_argument("--method", action="append", default=[], help="HTTP method filter (GET/POST/...) repeatable")
    ap.add_argument("--format", choices=["table", "markdown", "json"], default="table")
    args = ap.parse_args()

    spec = load_spec(args.source)
    paths = spec.get("paths", {})

    wanted_methods = {m.upper() for m in args.method}
    wanted_tags = {t.lower() for t in args.tag}
    needle = args.contains.lower().strip()

    rows: list[dict] = []

    for path, ops in paths.items():
        if not isinstance(ops, dict):
            continue
        for method, op in ops.items():
            m = method.upper()
            if m not in {"GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"}:
                continue
            if wanted_methods and m not in wanted_methods:
                continue

            summary = (op.get("summary") or "").strip()
            operation_id = (op.get("operationId") or "").strip()
            tags = op.get("tags") or []
            tags_l = [str(t).lower() for t in tags]

            if wanted_tags and not any(t in wanted_tags for t in tags_l):
                continue

            hay = " ".join([path, summary, operation_id, " ".join(tags)]).lower()
            if needle and needle not in hay:
                continue

            rows.append(
                {
                    "method": m,
                    "path": path,
                    "summary": summary,
                    "operationId": operation_id,
                    "tags": tags,
                }
            )

    rows.sort(key=lambda r: (r["path"], r["method"]))

    if args.format == "json":
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return

    if args.format == "markdown":
        print("| Method | Path | Summary | Tags |")
        print("|---|---|---|---|")
        for r in rows:
            tags = ", ".join(r["tags"]) if r["tags"] else ""
            summary = (r["summary"] or "").replace("|", "\\|")
            print(f"| {r['method']} | `{r['path']}` | {summary} | {tags} |")
        return

    # table
    if not rows:
        print("No endpoints matched filters.")
        return

    w_method = max(len("METHOD"), max(len(r["method"]) for r in rows))
    w_path = max(len("PATH"), max(len(r["path"]) for r in rows))

    print(f"{'METHOD'.ljust(w_method)}  {'PATH'.ljust(w_path)}  SUMMARY")
    print(f"{'-'*w_method}  {'-'*w_path}  {'-'*40}")
    for r in rows:
        print(f"{r['method'].ljust(w_method)}  {r['path'].ljust(w_path)}  {r['summary']}")


if __name__ == "__main__":
    main()
