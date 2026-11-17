#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
merge_vc.py — Sub-agent VC output merger for Parallel Dispatch (Workflow A)

Merges multiple per-batch VC markdown files (produced by `runSubagent` workers
spawned after `split_req.py`) into a single master VC document, then emits
statistics + coverage validation + tiered-review suggestions for the main agent.

What it does
------------
1. **Concatenate** all `vc-batch-*.md` files (in deterministic filename order)
   into one master document, dropping duplicate section dividers and normalizing
   headers.
2. **Parse** each VC block to extract:
   - VC ID, Linked Requirement ID, Verification Method
   - SMARTR-OC score (X/8)
   - Source Depth tags ([R]/[D]/[S]/[E]/[A]) and their counts
   - Gate compliance status (PASS / partial / BLOCKED)
   - VC-BLOCKED markers
3. **Validate coverage**: build a req_id → vc_id map from the merge inputs and
   cross-check against the `_index.json` produced by `split_req.py` (if present
   in the same parent directory). Reports UNCOVERED requirements and ORPHAN VCs.
4. **Emit tiered-review suggestions** per the main agent's review policy:
   - 8/8 → skip (low risk)
   - 6-7/8 → sample 20%
   - <6/8 → full re-review
   - any batch mean deviating >1.0 from global mean → full re-review

Input format
------------
Each batch file follows the sub-agent output contract (see
`references/vc-subagent-prompt.md`):

    # VC — {domain_name}

    ## VC-{REQ-ID} — {brief_title}

    | VC ID | Linked Requirement | Verification Method | ... |
    **SMARTR-OC**: **X/8**
    **Source Depth**:
    - {value} [R: BMS-XXXX]
    ...

Output layout
-------------
    {out_file}                          # merged master VC document
    {out_file}.stats.json               # machine-readable statistics
    stdout                              # human-readable summary for the main agent

Usage
-----
    python merge_vc.py <input_glob_or_dir> --out <merged.md>
                      [--index <_index.json>] [--encoding utf-8]

    # Merge all .md files in a directory:
    python merge_vc.py vc_batches/ --out VC_master.md

    # Merge a glob of batch files with coverage cross-check:
    python merge_vc.py "output/vc-batch-*.md" --out VC_master.md \
        --index vc_batches/_index.json

Exit codes
----------
    0  success (even if UNCOVERED/ORPHAN warnings exist — they're reported, not fatal)
    2  no input files found / unreadable
    3  invalid CLI args
    4  no VC blocks parsed (all inputs malformed?)
"""

from __future__ import annotations

import argparse
import glob
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Regexes — kept module-level for clarity and to mirror split_req.py style.
# ---------------------------------------------------------------------------

# A VC block header: `## VC-{ID} — {title}` (em dash, hyphen, or colon separator).
# The ID must be a token WITHOUT internal spaces; the separator is the FIRST
# whitespace run followed by one of `—`, `-`, `:`. We require the separator to
# be preceded by whitespace so we don't mis-split IDs like `BMS-011`.
VC_HEADER_RE = re.compile(
    r"^##\s+VC-(\S+?)\s+[\u2014\-\u003a]\s*(.*)$",
    re.MULTILINE,
)

# SMARTR-OC score line: `**SMARTR-OC**: **X/8**`
SMARTR_RE = re.compile(
    r"\*\*SMARTR-OC\*\*:\s*\*?\*?(\d)\s*/\s*8\*?\*?",
    re.IGNORECASE,
)

# Source Depth tags anywhere in a VC block.
SOURCE_TAG_RE = re.compile(r"\[([RDSSEA])\b")

# Linked Requirement ID inside the VC table row: `| VC-X | BMS-123 | ... |`
# We capture the second column.
LINKED_REQ_RE = re.compile(
    r"^\|\s*VC-\S+\s*\|\s*([A-Za-z0-9\-]+)\s*\|",
    re.MULTILINE,
)

# VC-BLOCKED marker.
BLOCKED_RE = re.compile(r"VC-BLOCKED|🔴\s*VC-BLOCKED", re.IGNORECASE)

# Frontmatter splitter (same logic as split_req.py).
def split_frontmatter(text: str) -> Tuple[str, str]:
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            return text[: end + 4] + "\n", text[end + 5 :]
    return "", text


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Merge sub-agent VC batch files into a master document with stats + coverage."
    )
    p.add_argument(
        "input",
        help=(
            "Either a directory containing VC .md files, or a glob pattern "
            "(quote it on the shell) like 'output/vc-batch-*.md'."
        ),
    )
    p.add_argument(
        "--out",
        required=True,
        help="Output path for the merged master VC document (.md).",
    )
    p.add_argument(
        "--index",
        default=None,
        help=(
            "Path to the _index.json produced by split_req.py. When provided, "
            "the merger cross-checks coverage (UNCOVERED / ORPHAN detection)."
        ),
    )
    p.add_argument(
        "--encoding",
        default="utf-8",
        help="File encoding for read/write (default: utf-8).",
    )
    return p.parse_args()


# ---------------------------------------------------------------------------
# Input discovery
# ---------------------------------------------------------------------------

def discover_inputs(input_spec: str) -> List[Path]:
    """Resolve a directory or glob into a sorted list of .md files."""
    spec = Path(input_spec)
    if spec.is_dir():
        files = sorted(spec.glob("*.md"))
    else:
        # Treat as glob pattern (may contain wildcards).
        files = sorted(Path(x) for x in glob.glob(input_spec, recursive=True))
    return [f for f in files if f.is_file()]


# ---------------------------------------------------------------------------
# VC block parsing
# ---------------------------------------------------------------------------

def parse_vc_blocks(text: str) -> List[dict]:
    """
    Split a batch file into individual VC blocks and extract metadata.
    Returns a list of dicts with keys:
        vc_id, linked_req, title, method, smartr_score, source_tags (Counter),
        blocked (bool), raw (markdown text of the block).
    """
    from collections import Counter

    # Slice the file at each `## VC-` header. The block extends until the next
    # `## ` header or end of text.
    headers = list(VC_HEADER_RE.finditer(text))
    blocks: List[dict] = []

    for i, m in enumerate(headers):
        start = m.start()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        raw = text[start:end].rstrip() + "\n"
        vc_id = m.group(1).strip()
        title = m.group(2).strip()

        # SMARTR-OC score (default to None if absent — flagged in stats).
        smartr_m = SMARTR_RE.search(raw)
        smartr_score = int(smartr_m.group(1)) if smartr_m else None

        # Source Depth tag counts.
        tags = Counter(SOURCE_TAG_RE.findall(raw))

        # Linked requirement (first match in the table row).
        link_m = LINKED_REQ_RE.search(raw)
        linked_req = link_m.group(1).strip() if link_m else None

        blocked = bool(BLOCKED_RE.search(raw))

        # Method: pull the 3rd column of the VC table if present.
        method = None
        method_m = re.search(
            r"^\|\s*VC-\S+\s*\|\s*\S+\s*\|\s*([^|]+)\|",
            raw,
            re.MULTILINE,
        )
        if method_m:
            method = method_m.group(1).strip()

        blocks.append({
            "vc_id": vc_id,
            "linked_req": linked_req,
            "title": title,
            "method": method,
            "smartr_score": smartr_score,
            "source_tags": dict(tags),
            "blocked": blocked,
            "raw": raw,
        })

    return blocks


# ---------------------------------------------------------------------------
# Coverage cross-check
# ---------------------------------------------------------------------------

def cross_check_coverage(
    parsed: List[dict],
    index_path: Optional[Path],
) -> Dict:
    """
    Build req_id -> [vc_id] map from parsed VCs, then compare against the
    split_req _index.json (if provided) to report UNCOVERED / ORPHAN.
    """
    req_to_vcs: Dict[str, List[str]] = {}
    orphan_vcs: List[str] = []
    covered_reqs = set()

    for blk in parsed:
        vc_id = blk["vc_id"]
        req = blk["linked_req"]
        if req and re.match(r"^[A-Za-z]+-\d+", req):
            req_to_vcs.setdefault(req, []).append(vc_id)
            covered_reqs.add(req)
        else:
            # Linked requirement missing or malformed → potential ORPHAN.
            orphan_vcs.append(vc_id)

    expected_reqs: set = set()
    if index_path and index_path.is_file():
        try:
            idx = json.loads(index_path.read_text(encoding="utf-8"))
            # split_req.py _index.json schema:
            #   {"source":..., "heading_level":N, "file_count":N, "total_ids":N,
            #    "files": [{"file":..., "domain":..., "ids":[...], "count":N}]}
            files = idx.get("files", [])
            if isinstance(files, list):
                for entry in files:
                    if isinstance(entry, dict):
                        expected_reqs.update(entry.get("ids", []))
            else:
                # Backward-compat: legacy {file: {ids}} dict shape.
                for entry in idx.values():
                    if isinstance(entry, dict):
                        expected_reqs.update(entry.get("ids", []))
        except (json.JSONDecodeError, OSError):
            pass  # Index unreadable — report only what we parsed.

    uncovered = sorted(expected_reqs - covered_reqs) if expected_reqs else []

    return {
        "req_to_vcs": req_to_vcs,
        "covered_reqs": sorted(covered_reqs),
        "uncovered_reqs": uncovered,
        "orphan_vcs": orphan_vcs,
        "coverage_pct": (
            round(len(covered_reqs & expected_reqs) / len(expected_reqs) * 100, 1)
            if expected_reqs else None
        ),
    }


# ---------------------------------------------------------------------------
# Tiered review suggestions (main agent policy)
# ---------------------------------------------------------------------------

def tiered_review(parsed: List[dict]) -> Dict:
    """
    Apply the main agent's SMARTR-OC sampling policy to suggest review actions.

    Two-stage gating:
      1. SMARTR-OC score → full / sample / skip bucket.
      2. Gate 11 format spot-check on the skip bucket: a VC table row using
         ``; `` (semicolon+space) to separate conditions in the Test Conditions
         or Pass/Fail Criterion columns (instead of ``<br>``) is demoted from
         skip → sample, so the main agent re-inspects it. This closes the
         defense-in-depth gap where an 8/8 batch with a Gate 11 violation would
         otherwise be trusted-and-skipped (the sub-agent self-report is the
         sole enforcer otherwise). Mechanical, deterministic, no false negatives
         on the exact ``; `` separator pattern mandated by Gate 11.
    """
    scored = [b for b in parsed if b["smartr_score"] is not None]
    if not scored:
        return {
            "global_mean": None,
            "full_review_all": True,
            "note": "No SMARTR-OC scores parsed — full review required.",
        }

    global_mean = sum(b["smartr_score"] for b in scored) / len(scored)

    full_review: List[str] = []
    sample_review: List[str] = []
    skip_review: List[str] = []
    gate11_flags: List[Dict[str, str]] = []

    for b in scored:
        s = b["smartr_score"]
        vc_id = b["vc_id"]
        if s < 6:
            full_review.append(vc_id)
        elif s <= 7:
            sample_review.append(vc_id)
        else:
            # 8/8 candidate for skip — run Gate 11 spot-check before trusting.
            if _gate11_violation(b.get("raw", "")):
                sample_review.append(vc_id)
                gate11_flags.append({
                    "vc_id": vc_id,
                    "gate": "Gate 11",
                    "issue": "table cell uses '; ' separator instead of '<br>'",
                })
            else:
                skip_review.append(vc_id)

    result = {
        "global_mean": round(global_mean, 2),
        "skip_review_8_8": skip_review,
        "sample_review_6_7": sample_review,
        "full_review_lt_6": full_review,
        "policy": (
            "8/8 → skip (unless Gate 11 spot-check fails → sample); "
            "6-7/8 → sample 20%; <6/8 → full review; "
            "batch mean deviation >1.0 → full review"
        ),
    }
    if gate11_flags:
        result["gate11_spot_check_flags"] = gate11_flags
    return result


_GATE11_TABLE_ROW_RE = re.compile(
    r"^\|\s*VC-\S+\s*\|[^|]*\|[^|]*\|([^|]*)\|([^|]*)\|([^|]*)\|",
    re.MULTILINE,
)


def _gate11_violation(raw_vc_block: str) -> bool:
    """
    Detect Gate 11 violations in a parsed VC block's table rows.

    Gate 11 mandates ``<br>`` as the cell separator in the Test Conditions
    (4th col) and Pass/Fail Criterion (6th col). Returns True if any table
    row uses ``; `` (semicolon+space) to join ≥2 distinct conditions in those
    columns — the most common mechanical mistake that a ``<br>``-unaware
    sub-agent makes.
    """
    for m in _GATE11_TABLE_ROW_RE.finditer(raw_vc_block):
        test_cond, _meas_target, pass_fail = m.group(1), m.group(2), m.group(3)
        for cell in (test_cond, pass_fail):
            # Only flag when '; ' joins 2+ phrases (heuristic for stacked
            # conditions); a single '; ' inside one value is tolerated.
            parts = [p for p in cell.split("; ") if p.strip()]
            if len(parts) >= 2 and "<br>" not in cell:
                return True
    return False


# ---------------------------------------------------------------------------
# Master document assembly
# ---------------------------------------------------------------------------

def assemble_master(
    file_blocks: List[Tuple[Path, List[dict]]],
    encoding: str,
) -> str:
    """Concatenate parsed VC blocks into one master markdown document."""
    parts: List[str] = []
    parts.append("# VC Master Document (Parallel Dispatch Merge)\n")
    parts.append(
        f"> Auto-generated by `scripts/merge_vc.py` from "
        f"{len(file_blocks)} batch file(s). Do not edit by hand.\n\n"
    )

    for path, blocks in file_blocks:
        if not blocks:
            continue
        parts.append(f"\n---\n\n## Batch: {path.name}\n\n")
        for b in blocks:
            parts.append(b["raw"])
            parts.append("\n")

    return "".join(parts)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    args = parse_args()

    inputs = discover_inputs(args.input)
    if not inputs:
        print(f"ERROR: no .md input files found for '{args.input}'", file=sys.stderr)
        return 2

    file_blocks: List[Tuple[Path, List[dict]]] = []
    all_parsed: List[dict] = []

    for path in inputs:
        try:
            text = path.read_text(encoding=args.encoding)
        except OSError as e:
            print(f"WARN: skipping unreadable file {path}: {e}", file=sys.stderr)
            continue
        _, body = split_frontmatter(text)
        blocks = parse_vc_blocks(body)
        if blocks:
            file_blocks.append((path, blocks))
            all_parsed.extend(blocks)
        else:
            print(f"WARN: no VC blocks parsed from {path}", file=sys.stderr)

    if not all_parsed:
        print("ERROR: no VC blocks parsed from any input file.", file=sys.stderr)
        return 4

    # --- Merge master document ---
    master_md = assemble_master(file_blocks, args.encoding)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(master_md, encoding=args.encoding)

    # --- Statistics ---
    index_path = Path(args.index) if args.index else None
    coverage = cross_check_coverage(all_parsed, index_path)
    review = tiered_review(all_parsed)

    scored = [b for b in all_parsed if b["smartr_score"] is not None]
    smartr_dist = {}
    for b in scored:
        smartr_dist[b["smartr_score"]] = smartr_dist.get(b["smartr_score"], 0) + 1

    source_totals: Dict[str, int] = {}
    for b in all_parsed:
        for tag, n in b["source_tags"].items():
            source_totals[tag] = source_totals.get(tag, 0) + n

    stats = {
        "input_files": [str(p) for p in inputs],
        "total_vcs": len(all_parsed),
        "vcs_with_score": len(scored),
        "smartr_distribution": smartr_dist,
        "smartr_mean": review["global_mean"],
        "blocked_vcs": [b["vc_id"] for b in all_parsed if b["blocked"]],
        "source_tag_totals": source_totals,
        "coverage": coverage,
        "tiered_review": review,
    }
    stats_path = out_path.with_suffix(out_path.suffix + ".stats.json")
    stats_path.write_text(
        json.dumps(stats, indent=2, ensure_ascii=False),
        encoding=args.encoding,
    )

    # --- Human-readable summary on stdout (for the main agent) ---
    print(f"=== merge_vc.py summary ===")
    print(f"Inputs merged : {len(inputs)} file(s) → {out_path}")
    print(f"Total VCs     : {len(all_parsed)} ({len(scored)} with SMARTR-OC score)")
    if review["global_mean"] is not None:
        print(f"SMARTR-OC mean: {review['global_mean']}/8")
        print(f"  Distribution: {smartr_dist}")
    print(f"VC-BLOCKED    : {len(stats['blocked_vcs'])} {stats['blocked_vcs'][:10]}")
    print(f"Source tags   : {source_totals}")
    if coverage["coverage_pct"] is not None:
        print(f"Coverage      : {coverage['coverage_pct']}%")
        if coverage["uncovered_reqs"]:
            print(f"  UNCOVERED   : {len(coverage['uncovered_reqs'])} req(s) "
                  f"{coverage['uncovered_reqs'][:10]}")
        if coverage["orphan_vcs"]:
            print(f"  ORPHAN VC   : {len(coverage['orphan_vcs'])} {coverage['orphan_vcs'][:10]}")
    print(f"Tiered review :")
    print(f"  skip (8/8)  : {len(review.get('skip_review_8_8', []))}")
    print(f"  sample (6-7): {len(review.get('sample_review_6_7', []))}")
    print(f"  full (<6)   : {len(review.get('full_review_lt_6', []))}")
    print(f"Stats JSON    : {stats_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
