#!/usr/bin/env python3
import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import re
from pathlib import Path
from uuid import uuid4


DEFAULT_WATCH_INTERVAL = "1m"


class WatchSchedulingError(RuntimeError):
    pass


def _unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[str] = set()
    result: list[Path] = []
    for path in paths:
        try:
            key = str(path.resolve()).lower()
        except OSError:
            key = str(path).lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return result


def _candidate_install_dirs() -> list[Path]:
    candidates: list[Path] = []

    configured_install_dir = os.environ.get("OPENCLAW_INSTALL_DIR", "").strip()
    if configured_install_dir:
        candidates.append(Path(configured_install_dir))

    local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
    if local_app_data:
        candidates.append(Path(local_app_data) / "Programs" / "EasyClaw")

    for executable_name in ("openclaw.cmd", "openclaw", "EasyClaw.exe", "ClawX.exe"):
        resolved = shutil.which(executable_name)
        if not resolved:
            continue
        resolved_path = Path(resolved)
        if resolved_path.name.lower() in {"easyclaw.exe", "clawx.exe"}:
            candidates.append(resolved_path.parent)
            continue
        if resolved_path.name.lower() == "openclaw.cmd" and len(resolved_path.parents) >= 3:
            candidates.append(resolved_path.parents[2])

    return _unique_paths(candidates)


def _install_dir_command_candidates(install_dir: Path) -> list[tuple[list[str], dict[str, str]]]:
    candidates: list[tuple[list[str], dict[str, str]]] = []
    openclaw_mjs = install_dir / "resources" / "openclaw" / "openclaw.mjs"
    easyclaw_exe = install_dir / "EasyClaw.exe"
    clawx_exe = install_dir / "ClawX.exe"
    openclaw_cmd = install_dir / "resources" / "cli" / "openclaw.cmd"

    if openclaw_mjs.exists():
        if easyclaw_exe.exists():
            candidates.append(
                (
                    [str(easyclaw_exe), str(openclaw_mjs)],
                    {
                        "ELECTRON_RUN_AS_NODE": "1",
                        "OPENCLAW_EMBEDDED_IN": "EasyClaw",
                    },
                )
            )
        if clawx_exe.exists():
            candidates.append(
                (
                    [str(clawx_exe), str(openclaw_mjs)],
                    {
                        "ELECTRON_RUN_AS_NODE": "1",
                        "OPENCLAW_EMBEDDED_IN": "ClawX",
                    },
                )
            )
        candidates.append((["node", str(openclaw_mjs)], {}))
    if openclaw_cmd.exists():
        candidates.append(([str(openclaw_cmd)], {}))
    return candidates


def _openclaw_command_candidates() -> list[tuple[list[str], dict[str, str]]]:
    candidates: list[tuple[list[str], dict[str, str]]] = []
    raw = os.environ.get("OPENCLAW_BIN", "").strip()
    if raw:
        candidates.append((shlex.split(raw, posix=os.name != "nt"), {}))
    for install_dir in _candidate_install_dirs():
        candidates.extend(_install_dir_command_candidates(install_dir))
    candidates.append((["openclaw"], {}))
    return candidates


def _openclaw_base_command() -> list[str]:
    return _openclaw_command_candidates()[0][0]


def _looks_like_launcher_failure(result: subprocess.CompletedProcess[str]) -> bool:
    error_text = " ".join(part for part in ((result.stderr or "").strip(), (result.stdout or "").strip()) if part).lower()
    failure_tokens = (
        "enablecompilecache",
        "does not provide an export named",
        "is not recognized as an internal or external command",
        "operable program or batch file",
        "no such file or directory",
        "cannot find the file specified",
        "missing dist/entry",
    )
    return any(token in error_text for token in failure_tokens)


def _run_openclaw(args: list[str]) -> subprocess.CompletedProcess[str]:
    last_result: subprocess.CompletedProcess[str] | None = None
    for base_command, extra_env in _openclaw_command_candidates():
        command = [*base_command, *args]
        env = os.environ.copy()
        env.update(extra_env)
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=False, env=env)
        except OSError:
            continue
        if result.returncode == 0:
            return result
        last_result = result
        if not _looks_like_launcher_failure(result):
            return result
    if last_result is not None:
        return last_result
    raise WatchSchedulingError("OpenClaw CLI is unavailable on this machine.")


def _extract_job_id(payload):
    if isinstance(payload, dict):
        for key in ("id", "jobId", "job_id"):
            value = payload.get(key)
            if value not in (None, ""):
                return str(value)
        for value in payload.values():
            found = _extract_job_id(value)
            if found:
                return found
    if isinstance(payload, list):
        for item in payload:
            found = _extract_job_id(item)
            if found:
                return found
    return None


def _parse_json_output(text: str):
    content = (text or "").strip()
    if not content:
        return None
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return None


def _find_job_id_by_name(name: str) -> str | None:
    result = _run_openclaw(["cron", "list", "--all", "--json"])
    if result.returncode != 0:
        return None
    payload = _parse_json_output(result.stdout)
    items = []
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        for key in ("items", "jobs", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                items = value
                break
    for item in items:
        if not isinstance(item, dict):
            continue
        if item.get("name") == name:
            job_id = item.get("jobId") or item.get("job_id") or item.get("id")
            if job_id not in (None, ""):
                return str(job_id)
    return None


def _duration_to_ms(value: str) -> int:
    raw = str(value or "").strip().lower()
    if not raw:
        raise WatchSchedulingError("Missing watcher interval.")
    match = re.fullmatch(r"(\d+)(ms|s|m|h|d)?", raw)
    if not match:
        raise WatchSchedulingError(f"Unsupported watcher interval: {value}")
    amount = int(match.group(1))
    unit = match.group(2) or "ms"
    multipliers = {
        "ms": 1,
        "s": 1000,
        "m": 60 * 1000,
        "h": 60 * 60 * 1000,
        "d": 24 * 60 * 60 * 1000,
    }
    return amount * multipliers[unit]


def _watcher_auth_args() -> list[str]:
    args: list[str] = []
    base_url = os.environ.get("CHANJING_PLATFORM_BASE_URL", "").strip()
    platform_token = os.environ.get("CHANJING_PLATFORM_API_TOKEN", "").strip()
    api_key = os.environ.get("CHANJING_PLATFORM_API_KEY", "").strip()
    api_secret = os.environ.get("CHANJING_PLATFORM_API_SECRET", "").strip()
    if base_url:
        args.extend(["--base-url", base_url])
    if platform_token:
        args.extend(["--api-token", platform_token])
        return args
    if api_key and api_secret:
        args.extend(["--api-key", api_key, "--api-secret", api_secret])
    return args


def _shell_command(script_path: Path, *, task_id: int, task_kind: str, label: str, watch_key: str, job_id: str | None) -> str:
    args = [
        sys.executable,
        str(script_path),
        "--task-id",
        str(task_id),
        "--task-kind",
        task_kind,
        "--watch-key",
        watch_key,
    ]
    if label:
        args.extend(["--label", label])
    if job_id:
        args.extend(["--job-id", job_id])
    args.extend(_watcher_auth_args())
    return " ".join(shlex.quote(part) for part in args)


def _build_prompt(script_path: Path, *, task_id: int, task_kind: str, label: str, watch_key: str, job_id: str | None) -> str:
    command = _shell_command(
        script_path,
        task_id=task_id,
        task_kind=task_kind,
        label=label,
        watch_key=watch_key,
        job_id=job_id,
    )
    return "\n".join(
        [
            "Check one async Chanjing platform task.",
            "Run this exact command in the terminal:",
            command,
            "If the command prints exactly NO_REPLY, reply with exactly NO_REPLY and nothing else.",
            "Otherwise reply with the command output verbatim and nothing else.",
        ]
    )


def build_watch_job_plan(*, task_id: int, task_kind: str, label: str = "", every: str = DEFAULT_WATCH_INTERVAL) -> dict:
    script_path = Path(__file__).with_name("cron_watch_task.py").resolve()
    if not script_path.exists():
        raise WatchSchedulingError(f"Watcher script not found: {script_path}")

    watch_key = uuid4().hex
    job_name = f"chanjing-watch-{task_kind}-{task_id}-{watch_key[:8]}"
    prompt = _build_prompt(
        script_path,
        task_id=task_id,
        task_kind=task_kind,
        label=label,
        watch_key=watch_key,
        job_id=None,
    )
    create_cli_args = [
        "cron",
        "create",
        "--name",
        job_name,
        "--every",
        every,
        "--session",
        "isolated",
        "--wake",
        "now",
        "--message",
        prompt,
        "--light-context",
        "--announce",
        "--channel",
        "last",
        "--json",
    ]
    return {
        "name": job_name,
        "watch_key": watch_key,
        "every": every,
        "every_ms": _duration_to_ms(every),
        "create_cli_args": create_cli_args,
        "legacy_cli_args": [
            "cron",
            "add",
            "--name",
            job_name,
            "--every",
            every,
            "--session",
            "isolated",
            "--message",
            prompt,
            "--announce",
            "--channel",
            "last",
            "--wake",
            "now",
            "--light-context",
            "--json",
        ],
        "tool_params": {
            "name": job_name,
            "schedule": {"kind": "every", "everyMs": _duration_to_ms(every)},
            "sessionTarget": "isolated",
            "wakeMode": "now",
            "payload": {
                "kind": "agentTurn",
                "message": prompt,
                "lightContext": True,
            },
            "delivery": {
                "mode": "announce",
                "channel": "last",
            },
        },
        "shell_command": " ".join(shlex.quote(part) for part in [*_openclaw_base_command(), *create_cli_args]),
    }


def schedule_task_watch(*, task_id: int, task_kind: str, label: str = "", every: str = DEFAULT_WATCH_INTERVAL) -> dict:
    plan = build_watch_job_plan(task_id=task_id, task_kind=task_kind, label=label, every=every)
    watch_key = plan["watch_key"]
    job_name = plan["name"]

    add_result = _run_openclaw(plan["create_cli_args"])
    creation_mode = "create"
    if add_result.returncode != 0:
        add_result = _run_openclaw(plan["legacy_cli_args"])
        creation_mode = "add"
        if add_result.returncode != 0:
            stderr = (add_result.stderr or add_result.stdout or "").strip()
            raise WatchSchedulingError(stderr or "Failed to create OpenClaw cron watch job.")

    payload = _parse_json_output(add_result.stdout)
    job_id = _extract_job_id(payload) or _find_job_id_by_name(job_name)
    if not job_id:
        raise WatchSchedulingError("Cron watcher creation could not be verified because no job id was returned.")

    edit_applied = False
    if job_id:
        script_path = Path(__file__).with_name("cron_watch_task.py").resolve()
        final_prompt = _build_prompt(
            script_path,
            task_id=task_id,
            task_kind=task_kind,
            label=label,
            watch_key=watch_key,
            job_id=job_id,
        )
        edit_result = _run_openclaw(
            [
                "cron",
                "edit",
                job_id,
                "--message",
                final_prompt,
                "--light-context",
                "--json",
            ]
        )
        edit_applied = edit_result.returncode == 0

    return {
        "name": job_name,
        "task_id": task_id,
        "task_kind": task_kind,
        "label": label,
        "watch_key": watch_key,
        "job_id": job_id,
        "schedule": every,
        "delivery": "announce",
        "delivery_channel": "last",
        "light_context": True,
        "creation_mode": creation_mode,
        "edit_applied": edit_applied,
    }


def remove_task_watch(job_id: str | None) -> bool:
    if not job_id:
        return False
    result = _run_openclaw(["cron", "remove", str(job_id)])
    return result.returncode == 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an OpenClaw cron watcher for an async platform task.")
    parser.add_argument("--task-id", type=int, required=True)
    parser.add_argument("--task-kind", required=True)
    parser.add_argument("--label", default="")
    parser.add_argument("--every", default=DEFAULT_WATCH_INTERVAL)
    args = parser.parse_args()

    result = schedule_task_watch(
        task_id=args.task_id,
        task_kind=args.task_kind,
        label=args.label,
        every=args.every,
    )
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2))
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
