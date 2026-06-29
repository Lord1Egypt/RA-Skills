#!/usr/bin/env python3
"""
merge_results.py — Merge rerun results into base results

Use case: after --rerun, overwrite base results with new results by id,
      keeping other pass/skip entries, outputting the full merged list.

Usage:
    python3 scripts/merge_results.py \
        --base   <previous full agent_results.json> \
        --patch  <new rerun agent_results.json> \
        --output <merged output path>
"""
import argparse
import json
import os
import sys


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--base",   required=True, help="Previous full results (base to merge into)")
    p.add_argument("--patch",  required=True, help="Rerun results (overrides base entries by id)")
    p.add_argument("--output", required=True, help="Output path for merged results")
    return p.parse_args()


def main():
    args = parse_args()

    # Load base
    try:
        with open(args.base, encoding="utf-8") as f:
            base_list = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read base: {e}", file=sys.stderr)
        sys.exit(1)

    # Load patch
    try:
        with open(args.patch, encoding="utf-8") as f:
            patch_list = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read patch: {e}", file=sys.stderr)
        sys.exit(1)

    # Build id -> patch index
    patch_map = {r["id"]: r for r in patch_list if r.get("id")}

    if not patch_map:
        print("⚠️  Patch empty, copying base as-is", file=sys.stderr)
        merged = base_list
    else:
        # Overwrite base entries with patch by id; keep others unchanged
        merged = []
        replaced = 0
        for r in base_list:
            rid = r.get("id", "")
            if rid in patch_map:
                merged.append(patch_map[rid])
                replaced += 1
            else:
                merged.append(r)

        # Append patch IDs not in base (defensive fallback)
        base_ids = {r.get("id") for r in base_list}
        extra = [r for r in patch_list if r.get("id") not in base_ids]
        if extra:
            merged.extend(extra)
            print(f"  ℹ️  Patch had {len(extra)} new IDs not in base, appended", file=sys.stderr)

        # Stats
        pass_c  = sum(1 for r in merged if r.get("status") == "pass")
        fail_c  = sum(1 for r in merged if r.get("status") == "fail")
        skip_c  = sum(1 for r in merged if r.get("status") == "skip")
        print(f"  Merge complete: {replaced} entries updated")
        print(f"  Summary: pass {pass_c} | fail {fail_c} | skip {skip_c} (total {len(merged)})")

    # Write output
    os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"  → Written: {args.output}")


if __name__ == "__main__":
    main()
