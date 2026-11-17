#!/usr/bin/env python3
"""Build, maintain and validate one ticker universe.

    python scripts/universe.py taxonomy --market M [--profile P | --check mine.json]
    python scripts/universe.py import   --watchlist W --market M --output snapshot.draft.json
    python scripts/universe.py measure  --prices P --benchmark B --source URL --output M
    python scripts/universe.py build    --spec S --snapshot N --output DIR [--seed universe.json]
    python scripts/universe.py maintain --universe U --changes C --output DIR
    python scripts/universe.py diff     before.json after.json
    python scripts/universe.py evaluate --universe U --prices P [--benchmark B]
    python scripts/universe.py validate universe.json

Build exits 0 when coverage is qualified (unused capacity allowed), 2 for blocked research,
and 3 for an explicit partial delivery. Checkpoints preserve attempts; invalid universes
are never published.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import evaluate_core  # noqa: E402
import measure_core  # noqa: E402
import provider_core  # noqa: E402
from build_run import run_build  # noqa: E402
from universe_core import (  # noqa: E402
    UniverseError,
    apply_change_set,
    check_taxonomy,
    diff_universes,
    load_policy,
    read_json,
    starter_taxonomy,
    validate_universe,
    watchlist_to_snapshot,
    write_artifacts,
)


def taxonomy(args: argparse.Namespace) -> int:
    if args.check:
        if args.target is not None and not args.profile:
            raise UniverseError("--target applies to one profile; pass --profile as well")
        report = check_taxonomy(
            read_json(args.check), args.market, load_policy(args.policy),
            args.target, args.profile,
        )
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["passed"] else 2
    themes = starter_taxonomy(args.market, args.profile)
    payload = json.dumps(
        {"schema_version": 1, "market": args.market, "taxonomy": themes},
        ensure_ascii=False, indent=2,
    ) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
        print(json.dumps({"status": "written", "output": args.output, "themes": len(themes)}))
    else:
        print(payload, end="")
    return 0


def import_watchlist(args: argparse.Namespace) -> int:
    try:
        text = Path(args.watchlist).read_text(encoding="utf-8")
    except OSError as exc:
        raise UniverseError(f"cannot read watchlist {args.watchlist}: {exc}") from exc
    draft = watchlist_to_snapshot(text, args.market, args.as_of or str(date.today()))
    Path(args.output).write_text(
        json.dumps(draft, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": "drafted",
        "output": args.output,
        "themes": len(draft["taxonomy"]),
        "candidates": len(draft["candidates"]),
        "notes": draft["notes"],
        "next": "research each candidate: role, metrics, evidence, eligibility, then build",
    }, ensure_ascii=False))
    return 0


def audit_core_command(args: argparse.Namespace) -> int:
    from coverage_core import audit_core
    report = audit_core(Path(args.watchlist).read_text(encoding="utf-8"),
                        read_json(args.universe) if args.universe else None)
    Path(args.output).write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                                encoding="utf-8")
    print(json.dumps({"status": report["status"], "original_count": report["original_count"],
                      "exact_retained": report["exact_retained"], "output": args.output}))
    return 0


def measure(args: argparse.Namespace) -> int:
    bundle = measure_core.measure(
        prices=args.prices,
        benchmarks=args.benchmark,
        source=args.source,
        window=args.window,
        liquidity_window=args.liquidity_window,
        as_of=args.as_of,
        benchmark_map=read_json(args.benchmark_map) if args.benchmark_map else None,
        factor_model=args.factor_model,
    )
    payload = bundle
    if args.into:
        payload = measure_core.merge_into_snapshot(read_json(args.into), bundle)
    Path(args.output).write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "status": "measured",
        "output": args.output,
        "as_of": bundle["as_of"],
        "tickers": len(bundle["metrics"]),
        "notes": bundle["notes"],
    }, ensure_ascii=False))
    return 0


def fetch(args: argparse.Namespace) -> int:
    included = set()
    if args.include_watchlist:
        from universe_core import parse_watchlist
        included = {t for _, tickers in parse_watchlist(
            Path(args.include_watchlist).read_text(encoding="utf-8")) for t in tickers}
    manifest = provider_core.fetch(
        market=args.market, output=args.output, cutoff=args.prices_until,
        limit=args.limit, workers=args.workers, include=included,
        crypto_scope=args.crypto_scope,
    )
    print(json.dumps({"status": "fetched" if manifest["complete"] else "partial",
                      "output": args.output, "received": manifest["received"],
                      "requested": manifest["requested"]}))
    return 0 if manifest["complete"] else 2


def build(args: argparse.Namespace) -> int:
    result, code = run_build(
        spec=args.spec, snapshot=args.snapshot, output=args.output, policy=args.policy,
        seed=args.seed, language=args.language, run_dir=args.run_dir, resume=args.resume,
        shortfall_action=args.shortfall_action,
    )
    print(json.dumps(result, ensure_ascii=False))
    return code


def maintain(args: argparse.Namespace) -> int:
    universe, report = apply_change_set(
        read_json(args.universe), read_json(args.changes), load_policy(args.policy)
    )
    artifacts = write_artifacts(universe, report, args.output, args.language)
    return _ok(universe, report, artifacts, report["maintenance"])


def evaluate(args: argparse.Namespace) -> int:
    report = evaluate_core.evaluate(
        universe=read_json(args.universe),
        prices=args.prices,
        benchmarks=args.benchmark,
        top=args.top,
    )
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
        print(json.dumps({
            "status": "evaluated",
            "output": args.output,
            "window": report["window"],
            "survival": report["survival"]["rate"],
            "coverage": {k: v["rate"] for k, v in report["coverage"]["top"].items()},
        }, ensure_ascii=False))
    else:
        print(payload, end="")
    return 0


def diff(args: argparse.Namespace) -> int:
    report = diff_universes(read_json(args.before), read_json(args.after))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def validate(args: argparse.Namespace) -> int:
    report = validate_universe(read_json(args.universe), load_policy(args.policy))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 2


def _paths(value: Any) -> Any:
    """Paths as strings; Markdown and HTML reports are language → path maps."""
    if isinstance(value, dict):
        return {key: str(path) for key, path in value.items()}
    return str(value)


def _ok(universe: dict, report: dict, artifacts: dict[str, Any], detail: dict) -> int:
    print(json.dumps({
        "status": "passed",
        "output": str(artifacts["directory"]),
        "artifacts": {
            name: _paths(value) for name, value in artifacts.items() if name != "directory"
        },
        "version_hash": universe["version_hash"],
        "warnings": report["warnings"],
        **detail,
    }, ensure_ascii=False))
    return 0


_LANGUAGE_HELP = (
    "the market-language report to write beside the English one; defaults to the market's own "
    "(cn is zh-Hans, us and crypto are en). English is always written — a universe is read "
    "both by the people who trade that market and by someone allocating across several"
)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(prog="universe.py", description=__doc__)
    value.add_argument(
        "--policy", help="policy JSON override (default: assets/default-policy.json)"
    )
    sub = value.add_subparsers(dest="command", required=True)

    themes = sub.add_parser("taxonomy", help="print the starter theme table for a market")
    themes.add_argument("--market", required=True, help="cn, us or crypto")
    themes.add_argument("--profile", help="cut to this profile's coverage level")
    themes.add_argument("--output", help="write to a file instead of stdout")
    themes.add_argument(
        "--check", metavar="FILE",
        help="check a hand-written theme table instead of printing the starter",
    )
    themes.add_argument(
        "--target", type=int,
        help="informational target for --profile; legacy policies also check size guidance",
    )
    themes.set_defaults(handler=taxonomy)

    draft = sub.add_parser("import", help="read an existing watchlist into a snapshot skeleton")
    draft.add_argument("--watchlist", required=True, help="TradingView .txt export")
    draft.add_argument("--market", required=True, help="cn, us or crypto")
    draft.add_argument("--as-of", help="defaults to today")
    draft.add_argument("--output", required=True, help="snapshot skeleton to write")
    draft.set_defaults(handler=import_watchlist)

    audit = sub.add_parser("audit-core", help="create an exact-code Core migration research queue")
    audit.add_argument("--watchlist", required=True)
    audit.add_argument("--universe")
    audit.add_argument("--output", required=True)
    audit.set_defaults(handler=audit_core_command)

    stats = sub.add_parser("measure", help="compute the window statistics from a price table")
    stats.add_argument("--prices", required=True, help="CSV of date,ticker,close[,volume|turnover]")
    stats.add_argument(
        "--benchmark", default=[], action="append",
        help="factor leg; repeat for an equal-weighted basket",
    )
    stats.add_argument("--source", required=True, help="http(s) URL the price table came from")
    stats.add_argument("--benchmark-map", help="per-theme gauges and optional fund comparisons")
    stats.add_argument("--factor-model", choices=("basket", "multivariate"), default="basket")
    stats.add_argument("--window", type=int, default=180, help="factor window in sessions")
    stats.add_argument(
        "--liquidity-window", type=int, default=30, help="turnover window in sessions"
    )
    stats.add_argument("--as-of", help="defaults to the last date in the table")
    stats.add_argument("--into", help="snapshot.json to fold the metrics into")
    stats.add_argument("--output", required=True, help="file to write")
    stats.set_defaults(handler=measure)

    network = sub.add_parser("fetch", help="optional public-data adapter; never selects members")
    network.add_argument("--market", required=True)
    network.add_argument("--prices-until", required=True, help="last completed session date")
    network.add_argument("--limit", type=int, default=500, help="size of the price research bench")
    network.add_argument("--workers", type=int, default=6)
    network.add_argument("--crypto-scope", choices=("spot-linked", "all-perpetuals"),
                         default="spot-linked", help="include classified perpetual-only assets")
    network.add_argument("--include-watchlist", help="also research these existing members")
    network.add_argument("--output", required=True)
    network.set_defaults(handler=fetch)

    new = sub.add_parser("build", help="build a universe from a researched snapshot")
    new.add_argument("--spec", help="build-spec.json")
    new.add_argument("--snapshot", help="researched snapshot.json")
    new.add_argument("--output", help="new, empty output directory")
    new.add_argument("--run-dir", help="checkpoint directory (default: OUTPUT.run)")
    new.add_argument("--resume", help="continue a checkpoint directory after repairing inputs")
    new.add_argument("--shortfall-action", choices=("auto", "deliver", "retry"),
                     help="Max: disclose/deliver count-only gaps within 5%%, or research/retry")
    new.add_argument(
        "--seed",
        help="existing base; coverage-first Max requires a qualified same-plan Heavy",
    )
    new.add_argument("--language", help=_LANGUAGE_HELP)
    new.set_defaults(handler=build)

    review = sub.add_parser("maintain", help="apply an evidence-backed change set")
    review.add_argument("--universe", required=True, help="existing universe.json")
    review.add_argument("--changes", required=True, help="changes.json")
    review.add_argument("--output", required=True, help="new, empty output directory")
    review.add_argument("--language", help=_LANGUAGE_HELP)
    review.set_defaults(handler=maintain)

    after = sub.add_parser(
        "evaluate", help="measure a universe against what the window actually did"
    )
    after.add_argument("--universe", required=True, help="the universe.json being evaluated")
    after.add_argument(
        "--prices", required=True,
        help="CSV of date,ticker,close covering the window, ideally wider than the universe",
    )
    after.add_argument(
        "--benchmark", action="append", default=[],
        help="factor leg for the independence check; repeat for a basket",
    )
    after.add_argument("--top", type=int, help="single cut for coverage (default: 10, 25, 50)")
    after.add_argument("--output", help="write to a file instead of stdout")
    after.set_defaults(handler=evaluate)

    compare = sub.add_parser("diff", help="compare two universe.json files")
    compare.add_argument("before", help="the earlier universe.json")
    compare.add_argument("after", help="the later universe.json")
    compare.set_defaults(handler=diff)

    check = sub.add_parser("validate", help="validate a standalone universe.json")
    check.add_argument("universe", help="universe.json")
    check.set_defaults(handler=validate)
    return value


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.handler(args)
    except (UniverseError, measure_core.MeasureError, evaluate_core.EvaluateError,
            provider_core.ProviderError) as exc:
        print(f"{args.command} failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
