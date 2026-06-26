from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from .paths import LEGACY_SCRIPTS_ROOT, VENV_PYTHON, resolve_data_root


def _choose_python() -> str:
    if VENV_PYTHON.exists():
        return str(VENV_PYTHON)
    return sys.executable


def _run_python_script(script: Path, args: list[str]) -> int:
    cmd = [_choose_python(), str(script), *args]
    return subprocess.call(cmd)


def _read_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def _env_scoring_v2_enabled() -> bool:
    return os.getenv("RSS_BREW_SCORING_V2", "").strip().lower() in {"1", "true", "yes", "on"}


def cmd_run(ns: argparse.Namespace) -> int:
    script = LEGACY_SCRIPTS_ROOT / "run_pipeline_v2.py"
    argv = ["--data-root", str(resolve_data_root(ns.data_root))]
    if ns.debug:
        argv.append("--debug")
    if ns.mock:
        argv.append("--mock")
    if ns.scoring_v2 or _env_scoring_v2_enabled():
        argv.append("--scoring-v2")
    return _run_python_script(script, argv)


def cmd_dry_run(ns: argparse.Namespace) -> int:
    script = LEGACY_SCRIPTS_ROOT / "run_pipeline_v2.py"
    argv = ["--data-root", str(resolve_data_root(ns.data_root)), "--skip-core", "--mock"]
    if ns.debug:
        argv.append("--debug")
    if ns.scoring_v2 or _env_scoring_v2_enabled():
        argv.append("--scoring-v2")
    return _run_python_script(script, argv)


def cmd_inspect_latest(ns: argparse.Namespace) -> int:
    data_root = resolve_data_root(ns.data_root)
    latest_path = data_root / "run-records" / "latest-run.json"
    payload = _read_json(latest_path, {})
    if not payload:
        print(f"No latest run found at {latest_path}", file=sys.stderr)
        return 1
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def cmd_delivery_update(ns: argparse.Namespace) -> int:
    script = LEGACY_SCRIPTS_ROOT / "update_delivery_status.py"
    argv = [
        "--data-root",
        str(resolve_data_root(ns.data_root)),
        "--status",
        ns.status,
    ]
    if ns.message:
        argv.extend(["--message", ns.message])
    return _run_python_script(script, argv)


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="rss-brew", description="RSS-Brew app CLI (v1 compat)")
    ap_sub = ap.add_subparsers(dest="command", required=True)

    run = ap_sub.add_parser("run", help="Run full RSS-Brew pipeline")
    run.add_argument("--data-root", default=None)
    run.add_argument("--debug", action="store_true")
    run.add_argument("--mock", action="store_true")
    run.add_argument("--scoring-v2", action="store_true", help="Enable Scoring V2 path (or RSS_BREW_SCORING_V2=1)")
    run.set_defaults(handler=cmd_run)

    dry_run = ap_sub.add_parser("dry-run", help="Run dry-run path")
    dry_run.add_argument("--data-root", default=None)
    dry_run.add_argument("--debug", action="store_true")
    dry_run.add_argument("--mock", action="store_true")
    dry_run.add_argument("--scoring-v2", action="store_true", help="Enable Scoring V2 path (or RSS_BREW_SCORING_V2=1)")
    dry_run.set_defaults(handler=cmd_dry_run)

    inspect = ap_sub.add_parser("inspect", help="Inspect run state")
    inspect_sub = inspect.add_subparsers(dest="inspect_command", required=True)
    latest = inspect_sub.add_parser("latest", help="Print latest run manifest pointer")
    latest.add_argument("--data-root", default=None)
    latest.set_defaults(handler=cmd_inspect_latest)

    delivery = ap_sub.add_parser("delivery", help="Delivery state operations")
    delivery_sub = delivery.add_subparsers(dest="delivery_command", required=True)
    update = delivery_sub.add_parser("update", help="Update delivery status")
    update.add_argument("--data-root", default=None)
    update.add_argument("--status", required=True, choices=["sent", "failed", "pending"])
    update.add_argument("--message", default="")
    update.set_defaults(handler=cmd_delivery_update)

    return ap


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    ns = parser.parse_args(argv)
    return int(ns.handler(ns))


if __name__ == "__main__":
    raise SystemExit(main())
