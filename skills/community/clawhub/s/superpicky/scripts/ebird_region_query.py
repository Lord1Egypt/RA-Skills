#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fuzzy lookup for eBird-style country / region codes used by SuperPicky BirdID.

Data sources (under .upstream):
  - birdid/data/ebird_regions.json — names (EN/CN) for countries and subregions
  - birdid/avonet_filter.py — REGION_BOUNDS inline comments for codes not in JSON

Optional: pip install pypinyin (inside .venv) for Chinese-to-pinyin matching.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _skill_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _upstream() -> Path:
    return _skill_root() / ".upstream"


def _pinyin(s: str) -> str:
    if not s:
        return ""
    try:
        from pypinyin import lazy_pinyin, Style

        return "".join(lazy_pinyin(s, style=Style.NORMAL)).lower()
    except ImportError:
        return ""


def load_bounds_labels(avonet_py: Path) -> Dict[str, str]:
    """Parse REGION_BOUNDS lines: \"CODE\": (...),  # label"""
    labels: Dict[str, str] = {}
    if not avonet_py.is_file():
        return labels
    line_re = re.compile(
        r'^\s*"([A-Z]{2}(?:-[A-Z0-9]{1,12})*)"\s*:\s*\([^)]*\)\s*,\s*#\s*(.+?)\s*$'
    )
    for line in avonet_py.read_text(encoding="utf-8", errors="replace").splitlines():
        m = line_re.match(line)
        if m:
            labels[m.group(1)] = m.group(2).strip()
    return labels


def load_region_bounds_mod(up: Path) -> Dict[str, Tuple[float, float, float, float]]:
    sys.path.insert(0, str(up))
    try:
        from birdid.avonet_filter import REGION_BOUNDS

        return dict(REGION_BOUNDS)
    except Exception:
        return {}


def build_records(up: Path) -> List[Dict[str, Any]]:
    json_path = up / "birdid" / "data" / "ebird_regions.json"
    avonet_py = up / "birdid" / "avonet_filter.py"
    bounds_labels = load_bounds_labels(avonet_py)
    bounds = load_region_bounds_mod(up)

    records: List[Dict[str, Any]] = []
    seen: set[str] = set()

    if json_path.is_file():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        for c in data.get("countries") or []:
            code = c.get("code") or ""
            if code:
                seen.add(code)
                name = (c.get("name") or "").strip()
                name_cn = (c.get("name_cn") or "").strip()
                records.append(
                    {
                        "code": code,
                        "name": name or code,
                        "name_cn": name_cn,
                        "kind": "country",
                        "parent": "",
                        "pinyin": _pinyin(name_cn),
                    }
                )
            for r in c.get("regions") or []:
                rc = r.get("code") or ""
                if not rc:
                    continue
                seen.add(rc)
                rn = (r.get("name") or "").strip()
                rnc = (r.get("name_cn") or "").strip()
                records.append(
                    {
                        "code": rc,
                        "name": rn or rc,
                        "name_cn": rnc,
                        "kind": "region",
                        "parent": code,
                        "pinyin": _pinyin(rnc),
                    }
                )

    for bcode in sorted(bounds.keys()):
        if bcode in seen:
            continue
        label = bounds_labels.get(bcode, "")
        # Heuristic: if label has CJK, treat as Chinese primary
        has_cjk = bool(re.search(r"[\u4e00-\u9fff]", label))
        if has_cjk and label:
            records.append(
                {
                    "code": bcode,
                    "name": bcode,
                    "name_cn": label,
                    "kind": "bounds_only",
                    "parent": "",
                    "pinyin": _pinyin(label),
                }
            )
        else:
            records.append(
                {
                    "code": bcode,
                    "name": label or bcode,
                    "name_cn": "",
                    "kind": "bounds_only",
                    "parent": "",
                    "pinyin": _pinyin(label) if label else "",
                }
            )

    # Attach pinyin to English-only names for substring match (weak)
    for rec in records:
        if rec["pinyin"] == "" and rec["name"] and rec["name"] != rec["code"]:
            rec["pinyin"] = _pinyin(rec["name"])

    return records


def match_score(query: str, rec: Dict[str, Any]) -> float:
    q_raw = query.strip()
    q = q_raw.lower()
    if not q:
        return 0.0

    cjk_q = bool(re.search(r"[\u4e00-\u9fff]", q_raw))
    code_l = rec["code"].lower()
    name_l = rec["name"].lower()
    cn = rec.get("name_cn") or ""
    cn_l = cn.lower()
    py = (rec.get("pinyin") or "").lower()

    if q == code_l:
        return 1.0
    if q in code_l:
        return 0.98

    if cjk_q:
        if py and q in py:
            return 0.88
        if cn:
            if q in cn_l:
                return 0.95
            r_cn = SequenceMatcher(None, q, cn_l).ratio()
            if r_cn >= 0.72:
                return r_cn
            return 0.0
        return 0.0

    if q in name_l:
        return 0.92
    if cn and q in cn_l:
        return 0.92
    if py and q in py:
        return 0.88

    best = 0.0
    hay_tokens: List[str] = []
    for part in (code_l, name_l, cn_l, py):
        if not part:
            continue
        hay_tokens.extend(part.replace("-", " ").split())

    for tok in hay_tokens:
        if len(tok) < 2 and len(q) > 1:
            continue
        r = SequenceMatcher(None, q, tok).ratio()
        if r > best:
            best = r
    for field in (code_l, name_l, cn_l, py):
        if len(field) >= 2:
            r = SequenceMatcher(None, q, field).ratio()
            if r > best:
                best = r

    return best


def search(
    records: List[Dict[str, Any]],
    query: str,
    *,
    limit: int,
    min_score: float,
) -> List[Tuple[float, Dict[str, Any]]]:
    if not query.strip():
        return [(1.0, r) for r in sorted(records, key=lambda x: x["code"])[:limit]]

    scored: List[Tuple[float, Dict[str, Any]]] = []
    for rec in records:
        s = match_score(query, rec)
        if s >= min_score:
            scored.append((s, rec))
    scored.sort(key=lambda x: (-x[0], x[1]["code"]))
    return scored[:limit]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fuzzy search eBird country/region codes (EN / CN / pinyin / code).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s shanghai
  %(prog)s 广东
  %(prog)s guangdong
  %(prog)s AU-SA
  %(prog)s texas --limit 5
  %(prog)s --list-countries --limit 80

Data: .upstream/birdid/data/ebird_regions.json + REGION_BOUNDS in avonet_filter.py
Optional: pip install pypinyin  (stronger Chinese romanization match)
""",
    )
    parser.add_argument(
        "query",
        nargs="?",
        default="",
        help="Search string (name, code, Chinese, or pinyin). Empty + --list-all lists codes (truncated).",
    )
    parser.add_argument("--limit", type=int, default=25, help="Max results (default: 25)")
    parser.add_argument(
        "--min-score",
        type=float,
        default=0.5,
        help="Minimum fuzzy score 0..1 (default: 0.5)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print JSON lines",
    )
    parser.add_argument(
        "--list-countries",
        action="store_true",
        help="Only country-level rows from JSON",
    )
    parser.add_argument(
        "--list-all",
        action="store_true",
        help="List records alphabetically by code (respects --limit)",
    )
    args = parser.parse_args()

    up = _upstream()
    if not (up / "birdid").is_dir():
        print(
            f"error: missing {up}/birdid — run scripts/install.sh from skill root",
            file=sys.stderr,
        )
        return 1

    records = build_records(up)
    if args.list_countries:
        records = [r for r in records if r.get("kind") == "country"]

    if args.list_all:
        query = ""
    elif not (args.query or "").strip():
        if args.list_countries:
            query = ""
        else:
            parser.print_help()
            return 1
    else:
        query = args.query

    results = search(records, query, limit=args.limit, min_score=args.min_score)

    if not results:
        print("No matches (try lower --min-score or different spelling).", file=sys.stderr)
        return 2

    if args.json:
        import json as _j

        for s, r in results:
            row = {"score": round(s, 4), **{k: r[k] for k in ("code", "name", "name_cn", "kind", "parent") if k in r}}
            print(_j.dumps(row, ensure_ascii=False))
        return 0

    for s, r in results:
        parent = f"  (parent {r['parent']})" if r.get("parent") else ""
        cn = f" | {r['name_cn']}" if r.get("name_cn") else ""
        print(f"{r['code']}\t{r['name']}{cn}\t[{r['kind']}, score={s:.2f}]{parent}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
