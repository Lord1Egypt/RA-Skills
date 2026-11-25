"""recon-cli entry point - argparse + orchestration."""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from typing import List, Optional

from . import __version__
from .checks import ALL_CHECKS
from .config import Config
from .finding import CheckResult, Severity
from .report import open_report_file, print_report, write_markdown
from .util import strip_host

DEFAULT_REPORT_DIR = "reports"


def _epilog() -> str:
    checks = "\n".join(f"  {c.name:<17} {c.description}" for c in ALL_CHECKS)
    return (
        "examples:\n"
        "  python -m recon_cli example.com\n"
        "  python -m recon_cli example.com --only headers,tls\n"
        "  python -m recon_cli example.com --skip js_bundle,dns\n"
        "  python -m recon_cli example.com --md reports/example.md\n"
        "  python -m recon_cli example.com --json reports/example.json\n"
        "  python -m recon_cli example.com --show-false-positives\n"
        "  python -m recon_cli --help\n"
        "\nchecks:\n"
        f"{checks}\n"
        "\nSAFETY: active low-noise probing only - no brute force, no fuzzing, no DoS. "
        "You must be authorized to test the target. The tool makes outbound HTTP/HTTPS"
        "requests and DNS queries; it does NOT execute JS or run payloads. "
        "Exit code is 0 (clean), 1 (HIGH/CRIT finding), or 2 (bad arguments)."
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="recon-cli",
        description="Low-volume web configuration auditor with JS-bundle analysis.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=True,  # explicit: -h/--help are always available
        epilog=_epilog(),
    )
    p.add_argument("target", help="domain (example.de) or full URL (https://example.de)")
    p.add_argument("--json", metavar="FILE", help="write JSON report to FILE")
    p.add_argument("--md", "--out", metavar="FILE", dest="md",
                   help="write markdown report to FILE (default: reports/<host>.md)")
    p.add_argument("--no-report", action="store_true",
                   help="do not write the default markdown report")
    p.add_argument("--force", action="store_true",
                   help="replace an existing report file (exclusive creation is the default)")
    p.add_argument("--only", metavar="CHECKS",
                   help="run only named checks (comma-separated): " + ",".join(c.name for c in ALL_CHECKS))
    p.add_argument("--skip", metavar="CHECKS",
                   help="skip named checks (comma-separated): " + ",".join(c.name for c in ALL_CHECKS))
    p.add_argument("--timeout", type=float, default=10.0, help="per-request timeout (s), default 10")
    p.add_argument("--max-subdomains", type=int, default=25, help="max subdomain probes (default 25)")
    p.add_argument("--max-paths", type=int, default=15, help="max sensitive-path probes (default 15)")
    p.add_argument("--max-js-bundles", type=int, default=10,
                   help="max JS chunks to download and scan (default 10)")
    p.add_argument("--no-color", action="store_true", help="disable ANSI colors")
    p.add_argument("--show-false-positives", action="store_true",
                   help="include React/lib-internal hits in the report")
    noise = p.add_mutually_exclusive_group()
    noise.add_argument("--quiet", action="store_true", help="suppress per-check progress")
    noise.add_argument("--verbose", action="store_true", help="show per-check progress (default)")
    p.add_argument("--version", action="version", version=f"recon-cli {__version__}")
    return p


def _split_names(value: Optional[str]) -> set:
    if not value:
        return set()
    return {part.strip() for part in value.split(",") if part.strip()}


def _default_md_path(target: str) -> str:
    host = strip_host(target) or "target"
    safe = re.sub(r"[^A-Za-z0-9._-]+", "_", host)
    return os.path.join(DEFAULT_REPORT_DIR, f"{safe}.md")


def _ensure_parent(path: str) -> None:
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)


def _exit_code(results: List[CheckResult]) -> int:
    """1 when a HIGH/CRIT actionable finding is present, else 0."""
    worst = max(
        (f.severity for r in results for f in r.findings if not f.is_false_positive),
        default=None,
    )
    return 1 if worst is not None and worst >= Severity.HIGH else 0


def run(args: argparse.Namespace) -> int:
    cfg = Config(
        timeout=args.timeout,
        max_subdomains=args.max_subdomains,
        max_paths=args.max_paths,
        max_js_bundles=args.max_js_bundles,
        verbose=args.verbose,
        scratch_dir=f"/tmp/recon-cli-{os.getpid()}",
    )
    only = _split_names(args.only)
    skip = _split_names(args.skip)
    cfg.skip = skip

    known = {c.name for c in ALL_CHECKS}
    unknown = (only | skip) - known
    if unknown:
        print(
            f"error: unknown check(s): {', '.join(sorted(unknown))} "
            f"(available: {', '.join(c.name for c in ALL_CHECKS)})",
            file=sys.stderr,
        )
        return 2

    checks = [
        c() for c in ALL_CHECKS
        if (not only or c.name in only) and c.name not in skip
    ]
    if not checks:
        print(
            f"error: no checks selected (available: {', '.join(c.name for c in ALL_CHECKS)})",
            file=sys.stderr,
        )
        return 2

    quiet = args.quiet and not args.verbose
    results: List[CheckResult] = []
    t0 = time.time()
    for c in checks:
        if not quiet:
            print(f"  · running {c.name:<16} {c.description[:40]}…", end=" ", flush=True)
        try:
            r = c.run(args.target, cfg)
        except Exception as e:  # noqa: BLE001 - one check must not kill the run
            r = CheckResult(c.name, "error", error=f"{type(e).__name__}: {e}")
        results.append(r)
        if not quiet:
            print(f"({r.summary or r.status})")

    elapsed = time.time() - t0

    # terminal report
    color = not args.no_color and sys.stdout.isatty()
    print_report(args.target, results, color=color,
                 show_fp=args.show_false_positives)

    # optional files
    md_path = None if args.no_report else (args.md or _default_md_path(args.target))
    if md_path:
        try:
            _ensure_parent(md_path)
            p = write_markdown(args.target, results, md_path,
                               show_fp=args.show_false_positives,
                               overwrite=args.force)
            if p:
                print(f"  markdown report → {p}")
        except FileExistsError:
            print(f"  error: markdown report exists: {md_path} "
                  f"(rerun with --force to replace it)", file=sys.stderr)
        except OSError as e:
            print(f"  error: could not write markdown report: {e}", file=sys.stderr)
    if args.json:
        payload = {
            "target": args.target,
            "tool_version": __version__,
            "generated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "elapsed_s": round(elapsed, 2),
            "results": [
                {
                    "name": r.name,
                    "status": r.status,
                    "summary": r.summary,
                    "error": r.error,
                    "findings": [
                        {
                            "severity": f.severity.name,
                            "title": f.title,
                            "evidence": f.evidence,
                            "recommended_action": f.recommendation,
                            "false_positive": f.is_false_positive,
                        } for f in r.findings
                    ],
                } for r in results
            ],
        }
        try:
            _ensure_parent(args.json)
            with open_report_file(args.json, overwrite=args.force) as fh:
                json.dump(payload, fh, indent=2)
            print(f"  json report → {args.json}")
        except FileExistsError:
            print(f"  error: json report exists: {args.json} "
                  f"(rerun with --force to replace it)", file=sys.stderr)
        except OSError as e:
            print(f"  error: could not write JSON report: {e}", file=sys.stderr)

    # exit code: non-zero if any CRIT/HIGH actionable finding
    return _exit_code(results)


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return run(args)


if __name__ == "__main__":
    raise SystemExit(main())
