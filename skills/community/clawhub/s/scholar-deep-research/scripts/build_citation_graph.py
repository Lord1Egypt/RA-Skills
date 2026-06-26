#!/usr/bin/env python3
"""build_citation_graph.py — snowball search via OpenAlex citation links.

Two directions:
  - backward: papers that this paper *cites* (its references)
  - forward:  papers that cite *this* paper (downstream impact)

Reads the top-N selected (or score-ranked) papers from state, queries OpenAlex
for their refs / cited-by, normalizes the new candidates, and ingests them
back into state with discovered_via="citation_chase". Existing papers (matched
on DOI / OpenAlex ID) are skipped.

Re-running this script after changing --seed-top is safe — already-fetched
papers will be re-merged, not duplicated.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Any

# `httpx` is imported lazily inside network-calling helpers so that
# `--schema` introspection works on machines without httpx installed.

from _common import (
    EXIT_UPSTREAM, EXIT_VALIDATION, USER_AGENT, UpstreamError, command_signature,
    err, make_paper, make_payload, maybe_emit_schema, ok, read_cache, write_cache,
)
from research_state import apply_citation_chase, load_state, make_paper_id

WORKS = "https://api.openalex.org/works"


# Per-seed failure accumulator. Populated by the fetch_* helpers; surfaced
# in the envelope's `seed_failures` field so orchestrators can distinguish
# "no new papers" from "OpenAlex was failing." Reset at the start of main().
SEED_FAILURES: list[dict[str, Any]] = []


def _record_failure(seed_id: str | None, stage: str, exc: Exception) -> None:
    import httpx  # lazy (only to read the status code if present)
    status = None
    resp = getattr(exc, "response", None)
    if resp is not None:
        status = getattr(resp, "status_code", None)
    SEED_FAILURES.append({
        "seed_id": seed_id,
        "stage": stage,
        "status": status,
        "message": f"{type(exc).__name__}: {exc}",
    })
    sys.stderr.write(f"{stage} error for {seed_id}: {exc}\n")


def fetch_work(oa_id: str, email: str | None) -> dict | None:
    import httpx  # lazy
    headers = {"User-Agent": USER_AGENT}
    params = {}
    if email:
        params["mailto"] = email
        headers["From"] = email
    try:
        r = httpx.get(f"{WORKS}/{oa_id}", params=params,
                      headers=headers, timeout=30.0)
        r.raise_for_status()
        return r.json()
    except httpx.HTTPError as e:
        _record_failure(oa_id, "fetch_work", e)
        return None


def fetch_referenced(seed_id: str, oa_ids: list[str],
                     email: str | None) -> list[dict]:
    """Batch-fetch referenced works by OpenAlex IDs (limit 25 per request via filter)."""
    import httpx  # lazy
    out = []
    chunk = 25
    headers = {"User-Agent": USER_AGENT}
    for i in range(0, len(oa_ids), chunk):
        batch = oa_ids[i:i + chunk]
        params: dict[str, Any] = {
            "filter": "openalex_id:" + "|".join(batch),
            "per-page": chunk,
            "select": "id,doi,title,authorships,publication_year,host_venue,"
                      "primary_location,cited_by_count,abstract_inverted_index",
        }
        if email:
            params["mailto"] = email
        try:
            r = httpx.get(WORKS, params=params, headers=headers, timeout=30.0)
            r.raise_for_status()
            out.extend(r.json().get("results", []))
        except httpx.HTTPError as e:
            _record_failure(seed_id, "fetch_referenced", e)
        time.sleep(0.1)
    return out


def fetch_cited_by(oa_id: str, limit: int, email: str | None) -> list[dict]:
    import httpx  # lazy
    headers = {"User-Agent": USER_AGENT}
    params: dict[str, Any] = {
        "filter": f"cites:{oa_id}",
        "per-page": min(limit, 200),
        "select": "id,doi,title,authorships,publication_year,host_venue,"
                  "primary_location,cited_by_count,abstract_inverted_index",
    }
    if email:
        params["mailto"] = email
    try:
        r = httpx.get(WORKS, params=params, headers=headers, timeout=30.0)
        r.raise_for_status()
        return r.json().get("results", [])
    except httpx.HTTPError as e:
        _record_failure(oa_id, "fetch_cited_by", e)
        return []


def normalize(w: dict[str, Any]) -> dict[str, Any]:
    # Reuse the OpenAlex normalizer logic (kept inline to avoid cross-import).
    from search_openalex import _normalize  # local import for clarity
    return _normalize(w)


def main() -> None:
    p = argparse.ArgumentParser(description="Build citation graph from state.")
    p.add_argument(
        "--state",
        default=os.environ.get("SCHOLAR_STATE_PATH", "research_state.json"),
        help="State file path (env: SCHOLAR_STATE_PATH)",
    )
    p.add_argument("--seed-top", type=int, default=8,
                   help="Number of top-ranked papers to use as seeds")
    p.add_argument("--direction", choices=["forward", "backward", "both"],
                   default="both")
    p.add_argument("--depth", type=int, default=1,
                   help="Currently only depth=1 supported")
    p.add_argument("--cited-by-limit", type=int, default=50,
                   help="Max cited-by results per seed")
    p.add_argument("--email",
                   default=os.environ.get("SCHOLAR_MAILTO"),
                   help="Polite pool email (env: SCHOLAR_MAILTO)")
    p.add_argument("--dry-run", action="store_true",
                   help="Preview seeds and estimated request count, "
                        "without making any HTTP calls or mutating state")
    p.add_argument("--idempotency-key",
                   help="If set, a retried run with the same key returns "
                        "the cached response without re-hitting OpenAlex or "
                        "re-mutating state. Cache dir: .scholar_cache/ "
                        "(env: SCHOLAR_CACHE_DIR).")
    p.add_argument("--schema", action="store_true",
                   help="Print this command's parameter schema as JSON and exit")
    maybe_emit_schema(p, "build_citation_graph")
    args = p.parse_args()

    # Idempotency short-circuit: cache hit returns immediately, no network,
    # no state mutation. Signature check catches accidental key reuse with
    # different arguments — returns `idempotency_key_mismatch` rather than
    # silently serving stale data.
    if args.idempotency_key and not args.dry_run:
        sig = command_signature(args, exclude=("email",))
        cached = read_cache(args.idempotency_key)
        if cached is not None:
            if cached.get("signature") and cached["signature"] != sig:
                err("idempotency_key_mismatch",
                    f"Idempotency key '{args.idempotency_key}' was "
                    f"previously used with different arguments. Use a new "
                    f"key or flush the cache entry.",
                    retryable=False, exit_code=EXIT_VALIDATION,
                    key=args.idempotency_key,
                    cached_signature=cached["signature"],
                    current_signature=sig)
            ok(cached["response"], meta={
                "cache_hit": True,
                "idempotency_key": args.idempotency_key,
                "cached_at": cached.get("cached_at"),
            })
            return

    path = Path(args.state)
    state = load_state(path)

    # pick seeds: prefer .selected_ids, fall back to top-by-score
    if state.get("selected_ids"):
        seeds = [state["papers"][pid] for pid in state["selected_ids"]
                 if pid in state["papers"]][: args.seed_top]
    else:
        seeds = sorted(state["papers"].values(),
                       key=lambda x: x.get("score", 0),
                       reverse=True)[: args.seed_top]

    if not seeds:
        err("no_seeds",
            "No seed papers. Run rank_papers.py and `research_state.py "
            "select` first.",
            retryable=False, exit_code=EXIT_VALIDATION)

    seeds_with_oa = [s for s in seeds if s.get("openalex_id")]
    skipped_seeds = [s["id"] for s in seeds if not s.get("openalex_id")]

    if args.dry_run:
        # Each backward seed costs 1 metadata GET + ~1 batch GET per ~25 refs.
        # We don't know ref counts without fetching, so estimate 2 req/seed.
        # Each forward seed costs 1 cited-by page (--cited-by-limit).
        backward_req = 2 * len(seeds_with_oa) if args.direction in ("backward", "both") else 0
        forward_req = len(seeds_with_oa) if args.direction in ("forward", "both") else 0
        ok({
            "dry_run": True,
            "would_fetch": {
                "seeds": len(seeds_with_oa),
                "skipped_seeds_without_openalex_id": skipped_seeds,
                "direction": args.direction,
                "cited_by_limit": args.cited_by_limit,
                "estimated_requests": backward_req + forward_req,
                "breakdown": {
                    "backward_req_estimate": backward_req,
                    "forward_req_estimate": forward_req,
                },
                "seed_ids": [s["id"] for s in seeds_with_oa],
                "note": "Backward estimate assumes ~1 metadata GET + ~1 batch "
                        "GET per seed; actual count depends on reference counts.",
            },
        })
        return

    SEED_FAILURES.clear()
    new_records: list[dict[str, Any]] = []
    attempts = 0              # seed×direction fetch attempts
    seeds_any_success: set[str] = set()

    for seed in seeds_with_oa:
        oa_id = seed["openalex_id"]
        seed_success = False

        if args.direction in ("backward", "both"):
            attempts += 1
            full = fetch_work(oa_id, args.email)
            if full:
                refs = full.get("referenced_works", [])
                ref_ids = [r.rsplit("/", 1)[-1] for r in refs if r]
                if ref_ids:
                    works = fetch_referenced(oa_id, ref_ids, args.email)
                    for w in works:
                        new_records.append(normalize(w))
                seed_success = True

        if args.direction in ("forward", "both"):
            attempts += 1
            cited_by = fetch_cited_by(oa_id, args.cited_by_limit, args.email)
            if cited_by or not SEED_FAILURES or SEED_FAILURES[-1]["seed_id"] != oa_id:
                # Non-empty results, or no newly-recorded failure for this
                # seed in this direction: count as success for this direction.
                for w in cited_by:
                    new_records.append(normalize(w))
                seed_success = seed_success or True

        if seed_success:
            seeds_any_success.add(oa_id)

    seeds_attempted = len(seeds_with_oa)
    # "Wholly failed" = no seed got a successful fetch in any direction AND
    # we actually tried to fetch something (not just dry-run / zero seeds).
    wholly_failed = (
        seeds_attempted > 0
        and not seeds_any_success
        and SEED_FAILURES
    )

    if wholly_failed:
        err("upstream_error",
            "All citation-chase seeds failed. OpenAlex may be down or "
            "rate-limiting. Retry with the same --idempotency-key to resume.",
            retryable=True, exit_code=EXIT_UPSTREAM,
            seed_failures=SEED_FAILURES,
            seeds_attempted=seeds_attempted,
            seeds_with_success=0)

    # Merge + query-append runs under the state lock via apply_citation_chase.
    summary = apply_citation_chase(
        path,
        new_records,
        {
            "source": "openalex_citation_chase",
            "query": f"seeds={len(seeds)} direction={args.direction}",
        },
    )

    response = {
        "seeds": len(seeds),
        "seeds_used": seeds_attempted,
        "seeds_with_success": len(seeds_any_success),
        "skipped_seeds_without_openalex_id": skipped_seeds,
        "direction": args.direction,
        "fetched": len(new_records),
        "added": summary["added"],
        "merged": summary["merged"],
        "total_papers": summary["total_papers"],
        "partial_failure": bool(SEED_FAILURES),
        "seed_failures": list(SEED_FAILURES),
    }

    if args.idempotency_key:
        sig = command_signature(args, exclude=("email",))
        write_cache(args.idempotency_key, response, signature=sig)
        ok(response, meta={
            "cache_hit": False,
            "idempotency_key": args.idempotency_key,
        })
    else:
        ok(response)


if __name__ == "__main__":
    main()
