#!/usr/bin/env python3
# Exit codes: 0=results, 1=no-results, 2=degraded/partial, 3=retrieval-stack-unavailable, 4=bad-args, 5=internal-error
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))
from super_memori_common import (
    diversify_results,
    grep_fallback,
    host_profile_status,
    lexical_index_stale,
    lexical_search,
    log_retrieval_event,
    read_state,
    reciprocal_rank_fuse,
    semantic_index_stale,
    semantic_runtime_status,
    semantic_search,
    skill_operational_decision,
    skill_operational_recall,
    skill_recall_gate,
    temporal_relational_rerank,
    build_hot_recovery_bundle,
    summarize_authority_surface,
)


class QueryMemoryArgError(Exception):
    pass


class QueryMemoryParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise QueryMemoryArgError(message)


def build_parser() -> QueryMemoryParser:
    p = QueryMemoryParser(description="Query local memory")
    p.add_argument("query")
    p.add_argument("--mode", default="auto", choices=["auto", "exact", "semantic", "hybrid", "recent", "learning"])
    p.add_argument("--type", dest="memory_type", default="all", choices=["episodic", "semantic", "procedural", "learning", "buffer", "all"])
    p.add_argument("--json", action="store_true")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--from", dest="date_from")
    p.add_argument("--to", dest="date_to")
    p.add_argument("--tags")
    p.add_argument("--reviewed-only", action="store_true")
    p.add_argument("--temporal", action="store_true")
    return p


def emit_error(message: str, *, as_json: bool = False) -> None:
    if as_json:
        print(json.dumps({"error": message}, ensure_ascii=False, indent=2))
    else:
        print(message, file=sys.stderr)


def apply_recent_filter(results: list[dict], date_from: str | None, date_to: str | None) -> list[dict]:
    if not date_from and not date_to:
        return results
    filtered = []
    for item in results:
        updated_at = item.get("updated_at") or ""
        date_part = updated_at[:10] if updated_at else ""
        if date_from and date_part and date_part < date_from:
            continue
        if date_to and date_part and date_part > date_to:
            continue
        filtered.append(item)
    return filtered


def main() -> int:
    parser = build_parser()
    try:
        args = parser.parse_args()
    except QueryMemoryArgError as e:
        emit_error(f"bad arguments: {e}")
        return 4

    try:
        warnings: list[str] = []
        degraded_reasons: list[str] = []
        state = read_state()
        profile = host_profile_status()
        skill_gate = skill_recall_gate(args.query)
        hot_query = any(token in args.query.casefold() for token in ["что только что изменилось", "только что изменилось", "что было недавно", "что не завершилось", "какие последние изменения не проверены", "recent changes", "just changed", "latest changes", "unfinished", "unverified"])
        hot_bundle = build_hot_recovery_bundle(query=args.query, limit=max(args.limit, 5)) if hot_query else None
        index_stale = lexical_index_stale(state)
        semantic_stale = semantic_index_stale(state)
        semantic_probe_needed = args.mode in {"auto", "semantic", "hybrid"}
        if semantic_probe_needed:
            semantic_status = semantic_runtime_status(state)
            semantic_ready = semantic_status["semantic_ready"]
            if not semantic_status["qdrant"]:
                warnings.append("semantic backend unavailable; lexical-only mode active")
            elif not semantic_status["deps"].get("sentence_transformers") or not semantic_status["deps"].get("numpy"):
                warnings.append("semantic dependencies missing; lexical-only mode active")
            elif not semantic_status["model_ready"]:
                warnings.append(f"local embedding model unavailable; lexical-only mode active ({semantic_status['model_error']})")
            elif not semantic_status["collection_present"]:
                warnings.append("semantic collection missing; lexical-only mode active")
            elif semantic_status["indexed_vectors"] <= 0:
                warnings.append("semantic collection has no indexed vectors; lexical-only mode active")
            elif semantic_stale:
                warnings.append("semantic index is stale; semantic retrieval may miss recent changes")
                degraded_reasons.append("semantic index is stale")
        else:
            semantic_status = {
                "deps": {"sentence_transformers": None, "numpy": None},
                "qdrant": None,
                "collection_present": None,
                "collection_info": None,
                "model_ready": None,
                "model_error": None,
                "indexed_vectors": int(state.get("semantic_indexed_vectors") or 0),
                "semantic_fresh": bool(state.get("semantic_last_indexed_at")) and not semantic_stale,
                "semantic_last_indexed_at": state.get("semantic_last_indexed_at"),
                "semantic_ready": False,
                "host_profile": profile,
            }
            semantic_ready = False

        mode_used = args.mode
        lexical_results: list[dict] = []
        semantic_results: list[dict] = []
        skill_candidates = skill_operational_recall(args.query, limit=3) if skill_gate.get("should_recall") else []
        lexical_error = None
        semantic_error = None
        fallback_error = None

        if args.mode == "auto":
            mode_used = "hybrid" if semantic_ready else "exact"
            if not semantic_ready:
                warnings.append("auto mode selected lexical search because semantic retrieval is unavailable")
                degraded_reasons.append("auto mode degraded to lexical search")
        elif args.mode in {"semantic", "hybrid"} and not semantic_ready:
            warnings.append(f"requested mode '{args.mode}' degraded to lexical search")
            degraded_reasons.append(f"requested mode '{args.mode}' degraded to lexical search")
            mode_used = "exact"
        elif args.mode == "learning":
            mode_used = "learning"
            if not semantic_ready:
                warnings.append("learning mode ran on lexical search on this host")

        if index_stale:
            warnings.append("lexical index is stale; results may miss recent changes")
            degraded_reasons.append("lexical index is stale")

        lexical_mode = mode_used in {"exact", "hybrid", "recent", "learning"}
        semantic_mode = mode_used in {"semantic", "hybrid"} and semantic_ready

        if lexical_mode:
            try:
                lexical_results = lexical_search(
                    args.query,
                    memory_type=("learning" if args.mode == "learning" else args.memory_type),
                    limit=max(args.limit * 4, 10),
                    reviewed_only=args.reviewed_only,
                )
            except Exception as e:
                lexical_error = str(e)
                warnings.append(f"lexical index unavailable: {e}")
                degraded_reasons.append("lexical index unavailable")

        if semantic_mode:
            try:
                semantic_results = semantic_search(
                    args.query,
                    memory_type=("learning" if args.mode == "learning" else args.memory_type),
                    limit=max(args.limit * int(profile["retrieval"]["fusion_multiplier"]), profile["retrieval"]["semantic_top_k"]),
                    reviewed_only=args.reviewed_only,
                )
                if not semantic_results:
                    warnings.append("semantic retrieval returned no candidates; using lexical path only")
                    degraded_reasons.append("semantic retrieval returned no candidates")
            except Exception as e:
                semantic_error = str(e)
                warnings.append(f"semantic retrieval unavailable: {e}")
                degraded_reasons.append("semantic retrieval unavailable")
                semantic_results = []

        if mode_used == "hybrid" and semantic_results:
            fused_results = reciprocal_rank_fuse(lexical_results, semantic_results, limit=max(args.limit * int(profile["retrieval"]["fusion_multiplier"]), profile["retrieval"]["rerank_limit"]))
        elif mode_used == "semantic" and semantic_results:
            fused_results = list(semantic_results)
        else:
            fused_results = list(lexical_results)

        fused_results = apply_recent_filter(fused_results, args.date_from, args.date_to)
        if fused_results and (mode_used in {"hybrid", "semantic"} or args.temporal):
            fused_results = temporal_relational_rerank(
                fused_results,
                query=args.query,
                limit=max(args.limit * int(profile["retrieval"]["fusion_multiplier"]), profile["retrieval"]["rerank_limit"]),
            )
        fused_results = diversify_results(fused_results, limit=max(args.limit, profile["retrieval"]["rerank_limit"]), per_source_cap=int(profile["retrieval"]["diversity_cap"]))

        if not fused_results and lexical_error is None:
            fallback_type = "learning" if args.mode == "learning" else args.memory_type
            try:
                fallback_results = grep_fallback(args.query, memory_type=fallback_type, limit=args.limit, reviewed_only=args.reviewed_only)
            except Exception as e:
                fallback_error = str(e)
                warnings.append(f"fallback retrieval unavailable: {e}")
            else:
                if fallback_results:
                    fused_results = fallback_results[: args.limit]
                    warnings.append("using grep fallback")
                    degraded_reasons.append("using grep fallback")

        degraded = bool(degraded_reasons)
        authority_surface = summarize_authority_surface(fused_results, query=args.query, mode_used=mode_used, degraded=degraded)
        fused_results = authority_surface["results"]
        if authority_surface["requires_low_authority_warning"]:
            warnings.append("low-authority matches only; results are heuristic/fallback and not confirmed memory truth")

        retrieval_stack_unavailable = lexical_error is not None and (fallback_error is not None or args.mode in {"exact", "recent", "learning"}) and (semantic_error is not None or args.mode in {"semantic", "hybrid"}) and not fused_results

        if retrieval_stack_unavailable:
            log_retrieval_event(
                'retrieval_stack_unavailable',
                query_text=args.query,
                mode_requested=args.mode,
                mode_used=mode_used,
                degraded=True,
                payload={'warnings': warnings},
            )
            payload = {
                "query": args.query,
                "mode_requested": args.mode,
                "mode_used": mode_used,
                "degraded": True,
                "warnings": warnings,
                "index_fresh": bool(state.get("lexical_last_indexed_at")) and not index_stale,
                "index_stale": index_stale,
                "semantic_fresh": bool(state.get("semantic_last_indexed_at")) and not semantic_stale,
                "semantic_stale": semantic_stale,
                "semantic_ready": semantic_ready,
                "host_profile": profile,
                "results": [],
                "error": "retrieval stack unavailable",
            }
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print(f"mode_requested: {payload['mode_requested']}")
                print(f"mode_used: {payload['mode_used']}")
                print("degraded: true")
                print("error: retrieval stack unavailable")
            return 3

        relation_hits = sum(1 for item in fused_results if item.get('relation_hits'))
        if not fused_results:
            log_retrieval_event(
                'retrieval_miss',
                query_text=args.query,
                mode_requested=args.mode,
                mode_used=mode_used,
                degraded=degraded,
                payload={'warnings': warnings},
            )
        else:
            if relation_hits:
                log_retrieval_event(
                    'relation_traversal_hit',
                    query_text=args.query,
                    mode_requested=args.mode,
                    mode_used=mode_used,
                    degraded=degraded,
                    payload={'hits': relation_hits},
                )
            if any((item.get('freshness_days') or 0) > 90 for item in fused_results):
                log_retrieval_event(
                    'stale_success',
                    query_text=args.query,
                    mode_requested=args.mode,
                    mode_used=mode_used,
                    degraded=degraded,
                    payload={'results': len(fused_results)},
                )
        payload = {
            "query": args.query,
            "mode_requested": args.mode,
            "mode_used": mode_used,
            "degraded": degraded,
            "warnings": warnings,
            "index_fresh": bool(state.get("lexical_last_indexed_at")) and not index_stale,
            "index_stale": index_stale,
            "semantic_fresh": bool(state.get("semantic_last_indexed_at")) and not semantic_stale,
            "semantic_stale": semantic_stale,
            "semantic_ready": semantic_ready,
            "host_profile": profile,
            "skill_recall_gate": skill_gate,
            "skill_candidates": skill_candidates,
            "authoritative_result_present": authority_surface["authoritative_result_present"] if fused_results else False,
            "low_authority_only": authority_surface["low_authority_only"] if fused_results else False,
            "results": fused_results[: args.limit],
            "hot_recovery": hot_bundle,
        }

        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"mode_requested: {payload['mode_requested']}")
            print(f"mode_used: {payload['mode_used']}")
            print(f"degraded: {str(payload['degraded']).lower()}")
            if warnings:
                print("warnings:")
                for w in warnings:
                    print(f"- {w}")
            print(f"authoritative_result_present: {str(payload['authoritative_result_present']).lower()}")
            print(f"low_authority_only: {str(payload['low_authority_only']).lower()}")
            if hot_bundle and hot_bundle.get("selected"):
                print("hot_recovery:")
                print(f"- truth_note: {hot_bundle.get('truth_note')}")
                for idx, item in enumerate(hot_bundle.get("selected", []), 1):
                    print(f"{idx}. [hot-change-buffer] {item.get('action_type','unknown')} :: {item.get('command_or_patch_summary','').strip()}")
            print("results:")
            for idx, item in enumerate(payload["results"], 1):
                print(f"{idx}. [{item.get('memory_type','unknown')}] {item.get('source_path','?')}")
                print(f"   authority: {item.get('match_authority','unknown')}")
                print(f"   {item.get('snippet','').strip()}")

        if hot_bundle and hot_bundle.get("selected"):
            return 2 if degraded else 0
        if payload["results"]:
            return 2 if degraded else 0
        if skill_candidates:
            return 2 if degraded else 0
        return 1
    except Exception as e:
        emit_error(f"internal error: {e}", as_json=("--json" in sys.argv))
        return 5


if __name__ == "__main__":
    raise SystemExit(main())
