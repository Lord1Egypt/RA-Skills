#!/usr/bin/env python3
"""
Coverage self-check for the DFA cut-set analysis (built into the skill).

Verifies that every No. (column A) of the source "Cut-Set List" sheet is found in
column A of the target "DFA Analysis-CutSet" sheet.

Key implementation detail
-------------------------
Target column A holds SEVERAL numbers per cut-set block, space-separated
(e.g. "1001 2001 3001 4001 50"), because rows of the same cut-set are merged
with `merge_values()`. Matching must therefore be **token-based**: split the
cell text on whitespace/commas and compare each numeric token against the set
of all tokens in the target column A. A naive substring match would give false
negatives (e.g. "100" matching inside "1001").

Scope
-----
By default only Order 2/3 rows are required to be covered, because the DFA
analysis is defined for 2nd/3rd-order minimal cut-sets. Out-of-scope orders are
reported separately for transparency, and reverse-orphans (target numbers no
longer present in the source) are reported to confirm they all belong to
struck-through (obsolete) blocks.

Usage:
    check_no_coverage.py [<excel_path>]
"""
import re
import sys
from collections import Counter

from openpyxl import load_workbook

SRC_KW = "Cut-Set List"
TGT_KW = "DFA Analysis-CutSet"
ORDERS = (2, 3)


def tokens(text):
    """Split a cell value into normalised numeric tokens.

    Handles: space / comma / newline separated lists, '_x000D_' CR artifacts,
    and float-ish values such as 1001.0.
    """
    if text is None:
        return []
    s = str(text).replace("_x000D_", " ").replace("\n", " ").replace("\r", " ")
    out = []
    for p in re.split(r"[\s,;，、]+", s):
        p = p.strip()
        if p.endswith(".0"):
            p = p[:-2]
        if re.fullmatch(r"\d+(\.\d+)?", p):
            out.append(p)
    return out


def is_red(cell):
    color = getattr(cell.font, "color", None)
    return color is not None and "FF0000" in str(color.rgb or "").upper()


def is_strike(cell):
    return getattr(cell.font, "strike", False)


def iter_blocks(ws, cut_col=4):
    """Yield (start_row, end_row, cutset_name) for merged 7-row blocks."""
    r = 2
    while r <= ws.max_row:
        d = ws.cell(r, cut_col).value
        if d is None or str(d).strip() == "":
            r += 1
            continue
        end = r
        for rng in ws.merged_cells.ranges:
            if rng.min_row == r and rng.min_col == cut_col and rng.max_col == cut_col:
                end = rng.max_row
        if end <= r:
            r += 1
            continue
        yield r, end, str(d).strip()
        r = end + 1


def pick_source_sheet(wb, keyword=SRC_KW):
    names = [n for n in wb.sheetnames if keyword.lower() in n.lower()]
    if not names:
        return None
    non_old = [n for n in names if "old" not in n.lower()]
    return (non_old or names)[0]


def pick_target_sheet(wb, keyword=TGT_KW):
    for n in wb.sheetnames:
        if keyword.lower() in n.lower():
            return wb[n]
    return None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else None
    if not path:
        print("usage: check_no_coverage.py <excel_path>", file=sys.stderr)
        return 2

    wb = load_workbook(path)
    src_name = pick_source_sheet(wb)
    if not src_name:
        print(f"[ERROR] no sheet containing '{SRC_KW}'", file=sys.stderr)
        return 1
    tgt = pick_target_sheet(wb)
    if tgt is None:
        print(f"[ERROR] no sheet containing '{TGT_KW}'", file=sys.stderr)
        return 1
    src = wb[src_name]

    # ---- target numbers, plus which block state owns each ----
    tgt_nums = set()
    num_owner = {}
    for s, e, _name in iter_blocks(tgt):
        state = ("red" if is_red(tgt.cell(s, 4))
                 else "strike" if is_strike(tgt.cell(s, 4))
                 else "normal")
        for rr in range(s, e + 1):
            for t in tokens(tgt.cell(rr, 1).value):
                tgt_nums.add(t)
                num_owner.setdefault(t, state)

    # ---- source rows ----
    src_rows = []
    for r in range(2, src.max_row + 1):
        a = src.cell(r, 1).value
        if a is None or str(a).strip() == "":
            continue
        try:
            order = int(src.cell(r, 5).value) if src.cell(r, 5).value is not None else None
        except (TypeError, ValueError):
            order = None
        src_rows.append((r, str(a).strip(), order))

    missing, non_numeric = [], []
    for r, a, o in src_rows:
        toks = tokens(a)
        if not toks:
            non_numeric.append((r, a))
            continue
        for t in toks:
            if t not in tgt_nums:
                missing.append((r, t, o))

    in_scope = [m for m in missing if m[2] in ORDERS]
    out_scope = [m for m in missing if m[2] not in ORDERS]

    print("=" * 74)
    print(f"COVERAGE CHECK  '{src_name}' column A  ->  '{tgt.title}' column A")
    print("=" * 74)
    print(f"source rows            : {len(src_rows)}")
    print(f"target distinct No.    : {len(tgt_nums)}")
    print(f"[1] Order 2/3 missing  : {len(in_scope)}")
    print(f"[2] out-of-scope missing: {len(out_scope)}")
    if out_scope:
        byorder = Counter(o for _r, _t, o in out_scope)
        print("      by Order: " + ", ".join(f"{o}:{n}" for o, n in sorted(byorder.items(), key=lambda kv: (kv[0] is None, kv[0]))))
    print(f"[3] non-numeric col-A rows: {len(non_numeric)}")
    for r, a in non_numeric[:10]:
        print(f"      row {r}: {a!r}")

    for r, t, o in in_scope[:30]:
        print(f"      MISSING row{r} No.={t!r} order={o}")

    # reverse check
    src_nums = set()
    for _r, a, _o in src_rows:
        src_nums.update(tokens(a))
    orphans = sorted(tgt_nums - src_nums, key=lambda x: int(x))
    nonstrike = [x for x in orphans if num_owner.get(x) != "strike"]
    print(f"[4] reverse orphans     : {len(orphans)} (not in strike blocks: {len(nonstrike)})")

    print("=" * 74)
    if len(in_scope) == 0:
        print("RESULT: PASS - every in-scope (Order 2/3) source No. is present in target column A.")
        return 0
    print(f"RESULT: FAIL - {len(in_scope)} in-scope source No. not found in target column A.")
    return 1


if __name__ == "__main__":
    sys.exit(main())