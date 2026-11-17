from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from preflight import inspect
from state import PLATFORMS, get_record, load, now, save, state_path
from adapters import ADAPTERS


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True))


def choose(platform: str) -> str:
    print(f"首次发现平台 {platform}。选择 enabled / disabled / deferred:", end=" ", flush=True)
    answer = input().strip().lower()
    return answer if answer in {"enabled", "disabled", "deferred"} else "deferred"


def get_version(record: dict[str, Any]) -> str:
    old = record.get("platforms", {}).get("clawhub", {}).get("publishedVersion")
    if not old:
        return "0.1.0"
    try:
        major, minor, patch = (int(x) for x in old.split("."))
        return f"{major}.{minor}.{patch + 1}"
    except (ValueError, AttributeError):
        return "0.1.0"


def preflight(skill_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    info = inspect(skill_dir)
    data = load()
    return info, data


def cmd_init(skill_dir: Path) -> int:
    info, data = preflight(skill_dir)
    if not info.get("sourceKey"):
        print_json(info)
        return 1
    record = get_record(data, info["sourceKey"])
    record["source"] = {"repo": info.get("gitRemote"), "path": str(skill_dir.resolve().relative_to(Path(info["repoRoot"]).resolve()))}
    for platform in PLATFORMS:
        record.setdefault("platforms", {}).setdefault(platform, {})
    save(data)
    print_json({"status": "initialized", "sourceKey": info["sourceKey"], "stateFile": str(state_path())})
    return 0


def cmd_status(skill_dir: Path) -> int:
    info, data = preflight(skill_dir)
    record = data.get("skills", {}).get(info.get("sourceKey", ""), {})
    print_json({"source": info, "state": record})
    return 0 if info.get("status") != "blocked" else 1


def cmd_reset(skill_dir: Path, platform: str | None, forget: bool = False) -> int:
    info, data = preflight(skill_dir)
    key = info.get("sourceKey")
    if not key or key not in data.get("skills", {}):
        return 1
    if forget:
        del data["skills"][key]
    elif platform:
        data["skills"][key].setdefault("platforms", {}).pop(platform, None)
    else:
        for value in data["skills"][key].setdefault("platforms", {}).values():
            value.pop("choice", None)
            value["status"] = "deferred"
    save(data)
    print_json({"status": "reset", "sourceKey": key, "platform": platform})
    return 0


def cmd_sync(args: argparse.Namespace) -> int:
    info, data = preflight(Path(args.skill_dir))
    if info.get("status") == "blocked":
        if args.json:
            print_json({"status": "blocked", "preflight": info})
        else:
            print_json({"preflight": info})
        return 1
    key = info["sourceKey"]
    record = get_record(data, key)
    record["source"] = {"repo": info.get("gitRemote"), "path": str(Path(info["skillDir"]).relative_to(Path(info["repoRoot"]))) }
    record["sourceHash"] = info["sourceHash"]
    selected = [x.strip() for x in args.platform.split(",")] if args.platform else list(PLATFORMS)
    unknown = set(selected) - set(PLATFORMS)
    if unknown:
        print(f"unknown platforms: {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2
    failures = 0
    results: list[dict[str, Any]] = []
    for platform in selected:
        item = record.setdefault("platforms", {}).setdefault(platform, {})
        choice = item.get("choice")
        if choice is None:
            if args.dry_run:
                choice = "deferred"
            else:
                choice = choose(platform)
            item["choice"] = choice
            if not args.dry_run:
                save(data)
        if choice != "enabled":
            item["status"] = "skipped"
            result_row = {"platform": platform, "status": "skipped", "choice": choice}
            results.append(result_row)
            if not args.json:
                print(f"[{platform}] skipped ({choice})")
            if not args.dry_run:
                save(data)
            continue
        if item.get("sourceHash") == info["sourceHash"] and item.get("status") in {"published", "indexed"} and not args.resume:
            results.append({"platform": platform, "status": "skipped", "reason": "unchanged source hash"})
            if not args.json:
                print(f"[{platform}] skipped (unchanged source hash)")
            if not args.dry_run:
                save(data)
            continue
        item["lastAttemptAt"] = now()
        info["version"] = args.version or get_version(record)
        result = ADAPTERS[platform](info, dry_run=args.dry_run, yes=args.yes)
        item["status"] = result.status
        item["error"] = result.message if result.status in {"failed", "blocked"} else None
        if result.values:
            item.update(result.values)
        if result.status in {"published", "indexed"}:
            item["sourceHash"] = info["sourceHash"]
            item["lastSuccessAt"] = now()
            if platform == "clawhub":
                item["publishedVersion"] = info["version"]
        else:
            failures += 1
        results.append({"platform": platform, "status": result.status, "message": result.message})
        if not args.json:
            print(f"[{platform}] {result.status}: {result.message}")
        if not args.dry_run:
            save(data)
    if not args.dry_run:
        save(data)
    report = {"status": "completed", "failures": failures, "sourceKey": key, "preflight": info, "results": results}
    if args.json:
        print_json(report)
    else:
        print_json({"status": "completed", "failures": failures, "sourceKey": key})
    return 1 if failures else 0


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="skill-sync")
    sub = root.add_subparsers(dest="command", required=True)
    for name in ("init", "preflight", "status"):
        p = sub.add_parser(name)
        p.add_argument("skill_dir")
    p = sub.add_parser("sync")
    p.add_argument("skill_dir")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--yes", action="store_true")
    p.add_argument("--resume", action="store_true")
    p.add_argument("--version")
    p.add_argument("--platform", default=None)
    p.add_argument("--json", action="store_true", help="emit one machine-readable JSON report")
    p = sub.add_parser("reset-choice")
    p.add_argument("skill_dir")
    p.add_argument("platform", choices=PLATFORMS)
    p = sub.add_parser("reset-all")
    p.add_argument("skill_dir")
    p = sub.add_parser("forget")
    p.add_argument("skill_dir")
    return root


def main() -> int:
    args = parser().parse_args()
    path = Path(args.skill_dir)
    if args.command == "init":
        return cmd_init(path)
    if args.command == "preflight":
        info, _ = preflight(path)
        print_json(info)
        return 0 if info.get("status") != "blocked" else 1
    if args.command == "status":
        return cmd_status(path)
    if args.command == "sync":
        return cmd_sync(args)
    if args.command == "reset-choice":
        return cmd_reset(path, args.platform)
    if args.command == "reset-all":
        return cmd_reset(path, None)
    if args.command == "forget":
        return cmd_reset(path, None, forget=True)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
