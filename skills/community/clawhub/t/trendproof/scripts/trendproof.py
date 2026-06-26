#!/usr/bin/env python3
"""TrendProof API CLI helper.

Reads API key from (in order):
1) --key flag
2) TRENDPROOF_API_KEY environment variable
3) Config file: ~/.config/clawdbot/trendproof.json  (key: "api_key")

Usage examples:
  python3 trendproof.py analyze "AI agents"
  python3 trendproof.py analyze "prompt engineering" --location 2826  # UK
  python3 trendproof.py analyze "rust programming" --json
  python3 trendproof.py batch "AI agents" "LLM fine-tuning" "RAG pipeline"
  python3 trendproof.py batch-file keywords.txt
  python3 trendproof.py configure --api-key tp_live_xxxx
  python3 trendproof.py configure --show

Notes:
- Uses only the Python standard library.
- Prints human-readable text by default; pass --json for machine-readable output.
- Base URL defaults to https://trendproof.dev; override with TRENDPROOF_BASE_URL.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path


# ── Config ─────────────────────────────────────────────────────────────────

CONFIG_PATH = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")) / "clawdbot" / "trendproof.json"
DEFAULT_BASE_URL = "https://trendproof.dev"


def _read_config() -> dict:
    try:
        return json.loads(CONFIG_PATH.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _write_config(data: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(data, indent=2))


def _get_api_key(cli_key: str | None = None) -> str | None:
    if cli_key:
        return cli_key
    env = os.environ.get("TRENDPROOF_API_KEY")
    if env:
        return env
    return _read_config().get("api_key")


def _get_base_url() -> str:
    return os.environ.get("TRENDPROOF_BASE_URL", DEFAULT_BASE_URL).rstrip("/")


# ── HTTP ────────────────────────────────────────────────────────────────────

def _post(endpoint: str, body: dict, api_key: str | None) -> dict:
    base = _get_base_url()
    url = f"{base}{endpoint}"
    data = json.dumps(body).encode()
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode(errors="replace")
        try:
            err = json.loads(body_text)
        except Exception:
            err = {"error": body_text}
        err["_http_status"] = e.code
        return err


# ── Formatting ───────────────────────────────────────────────────────────────

DIRECTION_EMOJI = {"rising": "🚀", "stable": "📊", "falling": "📉"}


def _direction_bar(score: float, width: int = 20) -> str:
    """ASCII bar: negative = red zone (←), positive = green zone (→)."""
    clamped = max(-100, min(200, score))
    if clamped >= 0:
        filled = int((clamped / 200) * width)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] +{clamped:.0f}"
    else:
        filled = int((abs(clamped) / 100) * width)
        bar = "░" * (width - filled) + "▓" * filled
        return f"[{bar}] {clamped:.0f}"


def _format_result(r: dict, verbose: bool = True) -> str:
    if "error" in r and "keyword" not in r:
        return f"❌  Error: {r.get('error', 'unknown')}"

    keyword = r.get("keyword", "?")
    score = r.get("velocity_score", 0)
    direction = r.get("trend_direction", "unknown")
    volume = r.get("volume", 0)
    cpc = r.get("cpc", 0)
    cpm = r.get("cpm", 0)
    competition = r.get("competition", 0)
    peak = r.get("peak_window", "N/A")
    hint = r.get("action_hint", "")
    cost = r.get("cost_usd", 0)
    cached = r.get("cached", False)
    elapsed = r.get("elapsed_ms", 0)

    emoji = DIRECTION_EMOJI.get(direction, "❓")
    bar = _direction_bar(score)

    lines = [
        f"",
        f"  Keyword      {keyword}",
        f"  Velocity     {bar}",
        f"  Direction    {emoji}  {direction.upper()}",
        f"  Volume       {volume:,} / mo",
        f"  CPC          ${cpc:.2f}   CPM ${cpm:.2f}",
        f"  Competition  {competition:.2f}",
        f"  Peak window  {peak}",
    ]
    if hint:
        lines.append(f"  Hint         {hint}")
    if verbose:
        cache_str = "✓ cached" if cached else f"live ({elapsed}ms)"
        lines.append(f"  Cost         ${cost:.4f}   [{cache_str}]")
    lines.append("")
    return "\n".join(lines)


def _format_batch_summary(results: list[dict]) -> str:
    """Sort results by velocity score descending and print a compact table."""
    sorted_r = sorted(
        [r for r in results if "keyword" in r],
        key=lambda x: x.get("velocity_score", 0),
        reverse=True,
    )
    errors = [r for r in results if "keyword" not in r]

    lines = ["", f"{'Keyword':<35} {'Score':>7}  {'Direction':<10}  {'Volume':>8}  {'CPC':>6}", "-" * 75]
    for r in sorted_r:
        emoji = DIRECTION_EMOJI.get(r.get("trend_direction", ""), "❓")
        lines.append(
            f"{r['keyword'][:34]:<35} {r.get('velocity_score', 0):>+7.0f}  "
            f"{emoji} {r.get('trend_direction', '?'):<8}  "
            f"{r.get('volume', 0):>8,}  "
            f"${r.get('cpc', 0):>5.2f}"
        )
    if errors:
        lines.append(f"\n  ❌ {len(errors)} error(s)")
    lines.append("")
    return "\n".join(lines)


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_configure(args: argparse.Namespace) -> None:
    if args.show:
        cfg = _read_config()
        key = cfg.get("api_key", "")
        if key:
            masked = key[:12] + "..." + key[-4:] if len(key) > 16 else key
            print(f"  api_key: {masked}")
            print(f"  config:  {CONFIG_PATH}")
        else:
            print("  No API key configured.")
            print(f"  Config:  {CONFIG_PATH}")
        return

    if not args.api_key:
        print("Usage: trendproof.py configure --api-key tp_live_xxxxx")
        sys.exit(1)

    cfg = _read_config()
    cfg["api_key"] = args.api_key
    _write_config(cfg)
    masked = args.api_key[:12] + "..." + args.api_key[-4:] if len(args.api_key) > 16 else args.api_key
    print(f"  ✓ API key saved ({masked})")
    print(f"  Config: {CONFIG_PATH}")


def cmd_analyze(args: argparse.Namespace) -> None:
    api_key = _get_api_key(getattr(args, "key", None))
    body: dict = {"keyword": args.keyword}
    if args.location:
        body["location_code"] = args.location
    if args.language:
        body["language_code"] = args.language

    result = _post("/api/analyze", body, api_key)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(_format_result(result, verbose=True))


def cmd_batch(args: argparse.Namespace) -> None:
    """Analyze multiple keywords sequentially and show ranked summary."""
    api_key = _get_api_key(getattr(args, "key", None))
    keywords = list(args.keywords)

    if getattr(args, "file", None):
        try:
            text = Path(args.file).read_text()
            file_kws = [line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")]
            keywords.extend(file_kws)
        except FileNotFoundError:
            print(f"❌  File not found: {args.file}", file=sys.stderr)
            sys.exit(1)

    if not keywords:
        print("❌  No keywords provided.", file=sys.stderr)
        sys.exit(1)

    results = []
    for kw in keywords:
        body: dict = {"keyword": kw}
        if args.location:
            body["location_code"] = args.location
        if args.language:
            body["language_code"] = args.language
        r = _post("/api/analyze", body, api_key)
        results.append(r)
        if not args.json and not args.quiet:
            emoji = DIRECTION_EMOJI.get(r.get("trend_direction", ""), "❓")
            score = r.get("velocity_score", 0)
            print(f"  {emoji}  {kw}: {score:+.0f}")

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(_format_batch_summary(results))

        total_cost = sum(r.get("cost_usd", 0) for r in results if "keyword" in r)
        print(f"  Total cost: ${total_cost:.4f}")


def cmd_batch_file(args: argparse.Namespace) -> None:
    """Read keywords from file and analyze."""
    args.keywords = []
    args.file = args.keywords_file
    cmd_batch(args)


def cmd_related(args: argparse.Namespace) -> None:
    """Get similar keywords for a seed keyword."""
    api_key = _get_api_key(args.key)
    if not api_key:
        print("❌  No API key. Run: trendproof configure --api-key TRND_xxx", file=sys.stderr)
        sys.exit(1)

    result = _post("/api/related", {"keyword": args.keyword}, api_key)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    if "error" in result:
        print(f"❌  {result['error']}", file=sys.stderr)
        sys.exit(1)

    items = result.get("related", [])
    if not items:
        print("No related keywords found.")
        return

    print(f"\n  Similar to: {args.keyword}\n")
    print(f"  {'Keyword':<35} {'Volume':>10}  {'CPC':>8}")
    print("  " + "─" * 57)
    for it in items:
        kw    = it.get("keyword", "")
        vol   = f"{it['volume']:,}" if it.get("volume") else "—"
        cpc   = f"${float(it['cpc']):.2f}" if it.get("cpc") else "—"
        print(f"  {kw:<35} {vol:>10}  {cpc:>8}")
    print()


# ── CLI entrypoint ────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="trendproof",
        description="TrendProof — Trend velocity intelligence for AI agents",
    )
    parser.add_argument("--key", help="TrendProof API key (overrides env/config)")
    sub = parser.add_subparsers(dest="command", required=True)

    # configure
    p_cfg = sub.add_parser("configure", help="Save API key to config")
    p_cfg.add_argument("--api-key", help="tp_live_xxx API key")
    p_cfg.add_argument("--show", action="store_true", help="Show current config")

    # analyze
    p_analyze = sub.add_parser("analyze", help="Analyze a single keyword")
    p_analyze.add_argument("keyword", help="Keyword to analyze")
    p_analyze.add_argument("--location", type=int, default=None, help="Location code (default: 2840 USA)")
    p_analyze.add_argument("--language", default=None, help="Language code (default: en)")
    p_analyze.add_argument("--json", action="store_true", help="Output raw JSON")

    # batch
    p_batch = sub.add_parser("batch", help="Analyze multiple keywords (ranked summary)")
    p_batch.add_argument("keywords", nargs="*", help="Keywords to analyze")
    p_batch.add_argument("--file", "-f", dest="file", default=None, help="Read additional keywords from file")
    p_batch.add_argument("--location", type=int, default=None)
    p_batch.add_argument("--language", default=None)
    p_batch.add_argument("--json", action="store_true")
    p_batch.add_argument("--quiet", "-q", action="store_true", help="No per-keyword progress")

    # batch-file (convenience alias)
    p_bf = sub.add_parser("batch-file", help="Analyze all keywords from a file")
    p_bf.add_argument("keywords_file", help="Path to newline-separated keywords file")
    p_bf.add_argument("--location", type=int, default=None)
    p_bf.add_argument("--language", default=None)
    p_bf.add_argument("--json", action="store_true")
    p_bf.add_argument("--quiet", "-q", action="store_true")

    # related
    p_rel = sub.add_parser("related", help="Get similar keywords for a seed keyword")
    p_rel.add_argument("keyword", help="Seed keyword")
    p_rel.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.command == "configure":
        cmd_configure(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "batch":
        cmd_batch(args)
    elif args.command == "batch-file":
        cmd_batch_file(args)
    elif args.command == "related":
        cmd_related(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
