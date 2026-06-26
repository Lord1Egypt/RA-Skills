\
#!/usr/bin/env python3
"""Agent-oriented helper for the official Resend CLI.

This helper does not replace the official CLI. It helps an agent:
- find the CLI and suggest install methods
- route tasks to the right commands
- inspect the bundled command catalogue
- scaffold sample files/commands
- statically lint emails batch JSON files
- explain likely failure causes
- execute the CLI with deterministic defaults and tolerant JSON parsing

Examples:
  python3 scripts/resend_cli.py probe
  python3 scripts/resend_cli.py catalog --resource emails
  python3 scripts/resend_cli.py info "emails send"
  python3 scripts/resend_cli.py recommend "send 70 different shipment notifications"
  python3 scripts/resend_cli.py scaffold batch-send --write-dir ./tmp
  python3 scripts/resend_cli.py lint-batch ./tmp/batch-emails.json
  python3 scripts/resend_cli.py doctor --command "emails send" --status 403 --message "1010 forbidden"
  python3 scripts/resend_cli.py run -- emails list --limit 5
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"


def _load_json(name: str) -> Any:
    return json.loads((ASSETS / name).read_text(encoding="utf-8"))


COMMAND_CATALOG = _load_json("command-catalog.json")
TASK_ROUTER = _load_json("task-router.json")
ERROR_MAP = _load_json("error-map.json")
GAPS = _load_json("coverage-gaps.json")
SUBPROCESS_CONTRACT = _load_json("subprocess-contract.json")
SCAFFOLDS = _load_json("scaffold-index.json")
SOURCE_MANIFEST = _load_json("source-manifest.json")


def emit(data: Any, code: int = 0) -> None:
    json.dump(data, sys.stdout, indent=2)
    sys.stdout.write("\n")
    raise SystemExit(code)


def normalise_command_name(name: str) -> str:
    return re.sub(r"\s+", " ", name.strip().lower())


def find_command(name: str) -> dict[str, Any] | None:
    target = normalise_command_name(name)
    for entry in COMMAND_CATALOG["commands"]:
        if normalise_command_name(entry["name"]) == target:
            return entry
    return None


def install_hints() -> list[dict[str, str]]:
    system = platform.system().lower()
    hints = [
        {"method": "curl", "command": "curl -fsSL https://resend.com/install.sh | bash"},
        {"method": "npm", "command": "npm install -g resend-cli"},
        {"method": "brew", "command": "brew install resend/cli/resend"},
        {"method": "powershell", "command": "irm https://resend.com/install.ps1 | iex"},
    ]
    if system == "windows":
        order = ["powershell", "npm", "curl", "brew"]
    elif system == "darwin":
        order = ["brew", "curl", "npm", "powershell"]
    else:
        order = ["curl", "npm", "brew", "powershell"]
    order_index = {name: i for i, name in enumerate(order)}
    return sorted(hints, key=lambda item: order_index[item["method"]])


def safe_env(extra: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ)
    env.setdefault("RESEND_NO_UPDATE_NOTIFIER", "1")
    if extra:
        env.update(extra)
    return env


def try_parse_json_blob(text: str) -> Any | None:
    stripped = text.strip()
    if not stripped:
        return None
    try:
        return json.loads(stripped)
    except Exception:
        return None


def try_parse_ndjson(text: str) -> list[Any] | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    parsed: list[Any] = []
    for line in lines:
        try:
            parsed.append(json.loads(line))
        except Exception:
            return None
    return parsed


def parse_structured(stdout: str, stderr: str) -> tuple[Any | None, str | None]:
    for channel_name, channel_text in (("stdout", stdout), ("stderr", stderr)):
        parsed = try_parse_json_blob(channel_text)
        if parsed is not None:
            return parsed, channel_name
        parsed_lines = try_parse_ndjson(channel_text)
        if parsed_lines is not None:
            return parsed_lines, f"{channel_name}_ndjson"
    return None, None


def probe_cli() -> dict[str, Any]:
    path = shutil.which("resend")
    result: dict[str, Any] = {
        "found": bool(path),
        "path": path,
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "python": platform.python_version(),
        },
        "env": {
            "RESEND_API_KEY_present": bool(os.environ.get("RESEND_API_KEY")),
            "RESEND_PROFILE": os.environ.get("RESEND_PROFILE"),
            "RESEND_NO_UPDATE_NOTIFIER": os.environ.get("RESEND_NO_UPDATE_NOTIFIER"),
        },
        "install_hints": install_hints(),
    }
    if path:
        try:
            proc = subprocess.run(
                [path, "--version"],
                capture_output=True,
                text=True,
                timeout=10,
                env=safe_env(),
            )
            version_text = (proc.stdout or proc.stderr).strip()
            result["version_probe"] = {
                "returncode": proc.returncode,
                "stdout": proc.stdout,
                "stderr": proc.stderr,
                "detected_version": version_text or None,
            }
        except Exception as exc:
            result["version_probe"] = {"error": str(exc)}
    return result


def cmd_probe(_: argparse.Namespace) -> None:
    emit(probe_cli())


def cmd_catalog(args: argparse.Namespace) -> None:
    entries = COMMAND_CATALOG["commands"]
    if args.resource:
        target = args.resource.strip().lower()
        entries = [e for e in entries if e["resource"].lower() == target]
    if args.category:
        target = args.category.strip().lower()
        entries = [e for e in entries if e["category"].lower() == target]
    if args.streaming:
        entries = [e for e in entries if e["streaming"]]
    if args.destructive:
        entries = [e for e in entries if e["destructive"]]
    emit(
        {
            "meta": COMMAND_CATALOG["meta"],
            "count": len(entries),
            "commands": entries,
        }
    )


def cmd_info(args: argparse.Namespace) -> None:
    entry = find_command(args.command_name)
    if not entry:
        emit(
            {
                "error": {
                    "message": f'Unknown command "{args.command_name}"',
                    "known_commands": sorted(e["name"] for e in COMMAND_CATALOG["commands"]),
                }
            },
            code=1,
        )
    related_gaps = [
        gap for gap in GAPS["gaps"]
        if any(normalise_command_name(name) in normalise_command_name(entry["name"]) or
               normalise_command_name(entry["name"]) in normalise_command_name(name)
               for name in gap["applies_to"])
    ]
    emit({"command": entry, "related_gaps": related_gaps})


def score_route(task: str, route: dict[str, Any]) -> int:
    text = task.lower()
    score = 0
    for kw in route.get("match_any", []):
        if kw.lower() in text:
            score += 2
    for kw in route.get("match_all", []):
        if kw.lower() in text:
            score += 1
        else:
            score -= 100
    for kw in route.get("match_none", []):
        if kw.lower() in text:
            score -= 4
    return score


def cmd_recommend(args: argparse.Namespace) -> None:
    task = args.task.strip()
    scored = []
    for route in TASK_ROUTER["routes"]:
        score = score_route(task, route)
        if score > 0:
            scored.append((score, route))
    scored.sort(key=lambda item: item[0], reverse=True)
    top = [route for _, route in scored[: args.top]]
    fallback = []
    text = task.lower()
    if "template" in text and ("send" in text or "deliver" in text):
        fallback.append("Hosted-template send may require MCP/API fallback; inspect templates-and-coverage-gaps.md.")
    if "receiving" in text and ("existing domain" in text or "enable" in text):
        fallback.append("Enabling receiving on an existing domain may require fallback if domains update still lacks the toggle.")
    if not top:
        top = [
            {
                "id": "generic",
                "preferred_surface": "cli",
                "recommended_sequence": ["resend --json -q doctor", "Load references/command-selection.md"],
                "notes": ["No high-confidence route matched. Start with diagnosis and explicit command selection."]
            }
        ]
    emit(
        {
            "task": task,
            "matches": top,
            "fallback_notes": fallback,
        }
    )


def cmd_scaffold(args: argparse.Namespace) -> None:
    spec = SCAFFOLDS.get(args.name)
    if not spec:
        emit(
            {
                "error": {
                    "message": f'Unknown scaffold "{args.name}"',
                    "available": sorted(SCAFFOLDS.keys()),
                }
            },
            code=1,
        )
    written: list[str] = []
    if args.write_dir:
        target_dir = Path(args.write_dir).resolve()
        target_dir.mkdir(parents=True, exist_ok=True)
        for file_name in spec.get("files", []):
            src = ASSETS / file_name
            dst = target_dir / file_name
            shutil.copyfile(src, dst)
            written.append(str(dst))
    emit(
        {
            "name": args.name,
            "description": spec["description"],
            "command": spec["command"],
            "files": spec.get("files", []),
            "written": written,
        }
    )


def lint_batch_file(path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []

    if not path.exists():
        return {
            "ok": False,
            "errors": [f"File does not exist: {path}"],
            "warnings": [],
            "suggestions": ["Create the file first or run scaffold batch-send."],
        }

    raw = path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return {
            "ok": False,
            "errors": [f"Invalid JSON: {exc}"],
            "warnings": [],
            "suggestions": ["The file must be a JSON array of email objects."],
        }

    if not isinstance(data, list):
        return {
            "ok": False,
            "errors": ["The root JSON value must be an array."],
            "warnings": [],
            "suggestions": ["Wrap the email objects in an array."],
        }

    count = len(data)
    if count == 0:
        warnings.append("The array is empty.")
    if count > 100:
        errors.append(f"Batch contains {count} items; the CLI/API batch limit is 100.")
        suggestions.append("Split the input into multiple files/chunks of 100 or fewer.")

    required_fields = ("from", "to", "subject")
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"Item {index} is not an object.")
            continue
        missing = [field for field in required_fields if field not in item]
        if missing:
            errors.append(f'Item {index} is missing required field(s): {", ".join(missing)}.')
        if "text" not in item and "html" not in item:
            errors.append(f'Item {index} must include "text" or "html".')
        if "attachments" in item:
            errors.append(f'Item {index} includes "attachments", which batch sends do not support.')
        if "scheduled_at" in item:
            errors.append(f'Item {index} includes "scheduled_at", which batch sends do not support.')
        to_value = item.get("to")
        if isinstance(to_value, list) and not to_value:
            warnings.append(f"Item {index} has an empty to list.")
        if isinstance(to_value, str):
            warnings.append(f'Item {index} uses a string for "to". Arrays are the documented batch-file shape.')
        if "from" in item and isinstance(item["from"], str) and "@resend.dev" in item["from"]:
            warnings.append(f"Item {index} uses resend.dev as the sender; that is testing-only.")
        if "html" in item and "text" in item:
            warnings.append(f'Item {index} contains both "html" and "text". That is allowed but make sure it is intentional.')

    if not suggestions and not errors:
        suggestions.append("The file shape looks compatible with emails batch.")
    return {
        "ok": not errors,
        "count": count,
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions,
    }


def cmd_lint_batch(args: argparse.Namespace) -> None:
    emit(lint_batch_file(Path(args.path)))


def cmd_doctor(args: argparse.Namespace) -> None:
    message = (args.message or "").lower()
    command = normalise_command_name(args.command or "")
    status = args.status

    checks: list[dict[str, Any]] = []
    if not command:
        checks.append(
            {
                "priority": 1,
                "check": "Start with doctor",
                "why": "This verifies CLI version, API key resolution, domains, and AI-agent detection.",
                "suggested_command": "resend --json -q doctor",
            }
        )

    if status in (401, 403) or "auth_error" in message or "forbidden" in message or "unauthor" in message:
        checks.extend([
            {
                "priority": 2,
                "check": "Verify auth resolution",
                "why": "The CLI may not be using the key or profile you expect.",
                "suggested_command": "resend --json -q doctor",
            },
            {
                "priority": 3,
                "check": "Check exact from-domain match",
                "why": "Resend commonly rejects sends when the sender does not match an exact verified domain/subdomain.",
            },
        ])
        if args.from_address and args.from_address.endswith("@resend.dev"):
            checks.append(
                {
                    "priority": 4,
                    "check": "Check resend.dev restriction",
                    "why": "resend.dev is testing-only and not meant for normal customer delivery.",
                }
            )
        checks.append(
            {
                "priority": 5,
                "check": "Only for raw REST fallback: verify User-Agent",
                "why": "The CLI sets RESEND_USER_AGENT automatically, but raw HTTP requests need a User-Agent header.",
            }
        )

    if command == "emails batch" or "batch" in message:
        checks.extend([
            {
                "priority": 10,
                "check": "Validate the batch file",
                "why": "Batch sends require a JSON array with 100 items or fewer.",
                "suggested_command": "python3 scripts/resend_cli.py lint-batch ./batch-emails.json",
            },
            {
                "priority": 11,
                "check": "Remove unsupported fields",
                "why": 'Batch sends do not support "attachments" or "scheduled_at".',
            },
        ])

    if "template" in message or command.startswith("templates") or ("send" in message and "template" in message):
        checks.append(
            {
                "priority": 20,
                "check": "Check whether the CLI surface actually exposes hosted-template sending",
                "why": "Template lifecycle is covered, but direct send-by-template is a known current gap/ambiguity.",
            }
        )

    if "receiving" in message or command.startswith("emails receiving"):
        checks.append(
            {
                "priority": 30,
                "check": "Confirm domain receiving is enabled",
                "why": "Inbound commands require a receiving-capable domain.",
            }
        )

    if "svix" in message or "signature" in message or command.startswith("webhooks"):
        checks.extend([
            {
                "priority": 40,
                "check": "Verify the raw request body, not parsed JSON",
                "why": "Svix verification depends on the exact original payload bytes.",
            },
            {
                "priority": 41,
                "check": "Dedupe on svix-id",
                "why": "Webhook delivery is at least once and can retry.",
            },
        ])

    if not checks:
        checks.append(
            {
                "priority": 1,
                "check": "Run doctor and inspect the parsed error payload",
                "why": "No specialised heuristic fired; start with general environment diagnosis.",
                "suggested_command": "resend --json -q doctor",
            }
        )

    checks.sort(key=lambda item: item["priority"])
    emit(
        {
            "inputs": {
                "command": args.command,
                "status": status,
                "message": args.message,
                "from_address": args.from_address,
                "to_address": args.to_address,
            },
            "checks": checks,
            "known_gaps": GAPS["gaps"],
        }
    )


def cmd_run(args: argparse.Namespace) -> None:
    probe = probe_cli()
    if not probe["found"]:
        emit(
            {
                "ok": False,
                "error": {
                    "message": 'The "resend" CLI was not found on PATH.',
                    "code": "cli_not_found",
                    "install_hints": probe["install_hints"],
                },
            },
            code=1,
        )

    tokens = list(args.command)
    if tokens and tokens[0] == "--":
        tokens = tokens[1:]
    if tokens and tokens[0] == "resend":
        tokens = tokens[1:]
    if not tokens:
        emit(
            {
                "ok": False,
                "error": {
                    "message": "No resend subcommand was provided.",
                    "code": "missing_subcommand",
                },
            },
            code=1,
        )

    cmd = [probe["path"]]
    if not args.raw:
        cmd.extend(SUBPROCESS_CONTRACT["default_global_flags"])
    cmd.extend(tokens)

    env = safe_env()
    if args.api_key:
        env["RESEND_API_KEY"] = args.api_key
    if args.profile:
        env["RESEND_PROFILE"] = args.profile

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=args.timeout,
            cwd=args.cwd,
            env=env,
        )
    except subprocess.TimeoutExpired as exc:
        emit(
            {
                "ok": False,
                "error": {
                    "message": f"Command timed out after {args.timeout} seconds.",
                    "code": "timeout",
                },
                "cmd": cmd,
                "stdout": exc.stdout,
                "stderr": exc.stderr,
            },
            code=1,
        )
    except Exception as exc:
        emit(
            {
                "ok": False,
                "error": {
                    "message": str(exc),
                    "code": "subprocess_error",
                },
                "cmd": cmd,
            },
            code=1,
        )

    parsed, parsed_from = parse_structured(proc.stdout, proc.stderr)
    output = {
        "ok": proc.returncode == 0,
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "parsed": parsed,
        "parsed_from": parsed_from,
        "contract_notes": [],
    }
    if parsed_from in {"stderr", "stderr_ndjson"}:
        output["contract_notes"].append(
            "Structured output was parsed from stderr. This is expected with current CLI JSON-error behaviour."
        )
    if not args.raw:
        output["contract_notes"].append("Wrapper prepended --json -q and set RESEND_NO_UPDATE_NOTIFIER=1.")
    emit(output, code=proc.returncode)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agent helper for the official Resend CLI.")
    sub = parser.add_subparsers(dest="subcommand", required=True)

    p_probe = sub.add_parser("probe", help="Find the CLI and report install/auth environment hints.")
    p_probe.set_defaults(func=cmd_probe)

    p_catalog = sub.add_parser("catalog", help="List commands from the bundled catalogue.")
    p_catalog.add_argument("--resource", help="Filter by resource.")
    p_catalog.add_argument("--category", help="Filter by category.")
    p_catalog.add_argument("--streaming", action="store_true", help="Only show streaming commands.")
    p_catalog.add_argument("--destructive", action="store_true", help="Only show destructive commands.")
    p_catalog.set_defaults(func=cmd_catalog)

    p_info = sub.add_parser("info", help="Show one command entry and related gaps.")
    p_info.add_argument("command_name", help='Command name, for example "emails send".')
    p_info.set_defaults(func=cmd_info)

    p_recommend = sub.add_parser("recommend", help="Route a free-text task to recommended CLI commands.")
    p_recommend.add_argument("task", help="Natural-language task description.")
    p_recommend.add_argument("--top", type=int, default=3, help="Maximum number of matching routes to return.")
    p_recommend.set_defaults(func=cmd_recommend)

    p_scaffold = sub.add_parser("scaffold", help="Return or materialise a sample scaffold.")
    p_scaffold.add_argument("name", help="Scaffold name.")
    p_scaffold.add_argument("--write-dir", help="Write scaffold files to this directory.")
    p_scaffold.set_defaults(func=cmd_scaffold)

    p_lint = sub.add_parser("lint-batch", help="Statically validate an emails batch JSON file.")
    p_lint.add_argument("path", help="Path to the JSON file.")
    p_lint.set_defaults(func=cmd_lint_batch)

    p_doctor = sub.add_parser("doctor", help="Explain likely causes of a failure using skill heuristics.")
    p_doctor.add_argument("--command", help='Relevant command, for example "emails send".')
    p_doctor.add_argument("--status", type=int, help="HTTP status code if known.")
    p_doctor.add_argument("--message", help="Relevant error message text.")
    p_doctor.add_argument("--from-address", help="Sender address if relevant.")
    p_doctor.add_argument("--to-address", help="Recipient address if relevant.")
    p_doctor.set_defaults(func=cmd_doctor)

    p_run = sub.add_parser("run", help="Execute the official CLI with deterministic defaults and tolerant parsing.")
    p_run.add_argument("--raw", action="store_true", help="Do not prepend --json -q.")
    p_run.add_argument("--timeout", type=int, default=60, help="Command timeout in seconds.")
    p_run.add_argument("--cwd", help="Optional working directory.")
    p_run.add_argument("--profile", help="Profile to export via RESEND_PROFILE for this run.")
    p_run.add_argument("--api-key", help="API key to export via RESEND_API_KEY for this run.")
    p_run.add_argument("command", nargs=argparse.REMAINDER, help='Subcommand tokens, for example: -- emails list --limit 5')
    p_run.set_defaults(func=cmd_run)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
