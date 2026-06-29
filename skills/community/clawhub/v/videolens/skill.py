from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib import error, request

import yaml

from occ.config import settings

REPO_URL = "https://github.com/shadoprizm/videolens.git"
DEFAULT_BRANCH = "main"
SPEND_ACTIONS = {"analyze"}
VALID_MODES = {"general", "bug", "meeting"}


def _json_safe(value: Any) -> Any:
    return json.loads(json.dumps(value, default=str))


def _state_root(spec: dict[str, Any]) -> Path:
    return Path(spec.get("state_dir") or (Path(settings.paths.data) / "videolens-video-intelligence")).resolve()


def _repo_dir(spec: dict[str, Any]) -> Path:
    return Path(spec.get("repo_dir") or (_state_root(spec) / "videolens")).resolve()


def _runs_dir(spec: dict[str, Any]) -> Path:
    return Path(spec.get("runs_dir") or (_state_root(spec) / "runs")).resolve()


def _task_api_url(context: dict[str, Any]) -> str:
    task_id = context.get("task_id")
    gateway_url = str(context.get("gateway_url") or f"http://127.0.0.1:{settings.server.port}").rstrip("/")
    return f"{gateway_url}/api/tasks/{task_id}"


def _fetch_task_payload(context: dict[str, Any]) -> dict[str, Any]:
    if context.get("pre_instructions") is not None:
        return {"pre_instructions": context.get("pre_instructions")}
    url = _task_api_url(context)
    with request.urlopen(url, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def _extract_structured_block(text: str) -> str:
    raw = (text or "").strip()
    if not raw:
        return ""
    if raw.startswith("```"):
        lines = raw.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            return "\n".join(lines[1:-1]).strip()
    for marker in ("```json", "```yaml", "```yml"):
        if marker in raw:
            start = raw.find(marker) + len(marker)
            end = raw.find("```", start)
            if end != -1:
                return raw[start:end].strip()
    return raw


def _parse_task_spec(pre_instructions: str) -> dict[str, Any]:
    payload = _extract_structured_block(pre_instructions)
    if not payload:
        return {"action": "preflight"}
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        loaded = yaml.safe_load(payload)
        if not isinstance(loaded, dict):
            raise ValueError("pre_instructions must be a JSON/YAML object for videolens-video-intelligence")
        data = loaded
    if not isinstance(data, dict):
        raise ValueError("pre_instructions must be a JSON/YAML object for videolens-video-intelligence")
    if not data.get("action"):
        data["action"] = "preflight"
    return data


def _run_command(command: list[str], *, env: dict[str, str] | None = None, cwd: Path | None = None, timeout: int = 300) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        env=env,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return {
        "command": command,
        "cwd": str(cwd) if cwd else None,
        "returncode": completed.returncode,
        "stdout": completed.stdout.strip(),
        "stderr": completed.stderr.strip(),
        "success": completed.returncode == 0,
    }


def _ensure_repo(spec: dict[str, Any]) -> dict[str, Any]:
    state_dir = _state_root(spec)
    repo_dir = _repo_dir(spec)
    state_dir.mkdir(parents=True, exist_ok=True)

    if not repo_dir.exists():
        return _run_command(
            ["git", "clone", "--depth", "1", "--branch", str(spec.get("branch") or DEFAULT_BRANCH), REPO_URL, str(repo_dir)],
            cwd=state_dir,
            timeout=int(spec.get("bootstrap_timeout_seconds") or 300),
        )

    if spec.get("update_repo"):
        return _run_command(
            ["git", "-C", str(repo_dir), "pull", "--ff-only"],
            timeout=int(spec.get("bootstrap_timeout_seconds") or 300),
        )

    return {"success": True, "command": ["git", "status"], "cwd": str(repo_dir), "stdout": "Repository already present.", "stderr": "", "returncode": 0}


def _uv_command() -> str | None:
    return shutil.which("uv")


def _venv_python(repo_dir: Path) -> Path:
    if os.name == "nt":
        return repo_dir / ".venv" / "Scripts" / "python.exe"
    return repo_dir / ".venv" / "bin" / "python"


def _ensure_runtime(spec: dict[str, Any]) -> dict[str, Any]:
    repo_dir = _repo_dir(spec)
    uv = _uv_command()
    timeout = int(spec.get("bootstrap_timeout_seconds") or 900)
    if uv:
        return _run_command([uv, "sync", "--extra", "ui"], cwd=repo_dir, timeout=timeout)
    return _run_command([sys.executable, "-m", "pip", "install", "-e", ".[ui]"], cwd=repo_dir, timeout=timeout)


def _collect_runtime_state(spec: dict[str, Any]) -> dict[str, Any]:
    repo_dir = _repo_dir(spec)
    venv_python = _venv_python(repo_dir)
    return {
        "state_dir": str(_state_root(spec)),
        "repo_dir": str(repo_dir),
        "runs_dir": str(_runs_dir(spec)),
        "repo_present": repo_dir.exists(),
        "pyproject_present": (repo_dir / "pyproject.toml").exists(),
        "uv_available": _uv_command() is not None,
        "git_available": shutil.which("git") is not None,
        "ffmpeg_available": shutil.which("ffmpeg") is not None,
        "ffprobe_available": shutil.which("ffprobe") is not None,
        "openai_api_key_present": bool(os.environ.get("OPENAI_API_KEY", "").strip()),
        "venv_python": str(venv_python),
        "venv_present": venv_python.exists(),
    }


def _build_preflight_report(spec: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    issues: list[str] = []
    if not state["git_available"]:
        issues.append("git is missing")
    if not state["ffmpeg_available"]:
        issues.append("ffmpeg is missing")
    if not state["ffprobe_available"]:
        issues.append("ffprobe is missing")
    if not state["repo_present"]:
        issues.append("VideoLens repo is not bootstrapped")
    if state["repo_present"] and not state["pyproject_present"]:
        issues.append("VideoLens pyproject.toml is missing")
    if state["repo_present"] and not state["venv_present"] and state["uv_available"]:
        issues.append("VideoLens runtime is not bootstrapped")
    if not state["openai_api_key_present"]:
        issues.append("OPENAI_API_KEY is missing for real analysis")

    next_steps: list[str] = []
    if not state["repo_present"] or (state["repo_present"] and not state["venv_present"]):
        next_steps.append("Run bootstrap action first")
    if not state["openai_api_key_present"]:
        next_steps.append("Provide OPENAI_API_KEY before analyze action")
    if not next_steps:
        next_steps.append("Wrapper is ready for manual VideoLens analysis")

    return {
        "success": len(issues) == 0,
        "summary": "VideoLens preflight passed" if not issues else f"VideoLens preflight found {len(issues)} issue(s)",
        "action": "preflight",
        "issues": issues,
        "next_steps": next_steps,
        "state": state,
        "requested_spec": spec,
        "readiness": {
            "bootstrap": state["git_available"],
            "analyze": state["repo_present"] and state["pyproject_present"] and state["ffmpeg_available"] and state["ffprobe_available"] and state["openai_api_key_present"],
        },
    }


def _require_fields(spec: dict[str, Any], *names: str) -> None:
    missing = [name for name in names if not str(spec.get(name) or "").strip()]
    if missing:
        raise ValueError(f"Missing required field(s) for action '{spec.get('action')}': {', '.join(missing)}")


def _new_run_dir(spec: dict[str, Any]) -> Path:
    explicit = spec.get("output_dir")
    if explicit:
        return Path(explicit).resolve()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = str(spec.get("run_id") or stamp).replace("/", "-").replace(" ", "-")
    return (_runs_dir(spec) / slug).resolve()


def _videolens_executable(repo_dir: Path) -> Path | None:
    bin_name = "videolens.exe" if os.name == "nt" else "videolens"
    candidate = repo_dir / ".venv" / ("Scripts" if os.name == "nt" else "bin") / bin_name
    return candidate if candidate.exists() else None


def _build_analyze_command(spec: dict[str, Any], output_dir: Path, repo_dir: Path | None = None) -> list[str]:
    _require_fields(spec, "source", "prompt")
    mode = str(spec.get("mode") or "general").strip()
    if mode not in VALID_MODES:
        raise ValueError(f"Unsupported mode: {mode}. Valid modes: {', '.join(sorted(VALID_MODES))}")
    repo_dir = repo_dir or _repo_dir(spec)
    executable = _videolens_executable(repo_dir)
    if executable:
        command = [str(executable), "analyze"]
    else:
        command = ["uv", "run", "videolens", "analyze"]
    command.extend([str(spec["source"]), "--mode", mode, "--prompt", str(spec["prompt"]), "--output-dir", str(output_dir), "--json"])
    if spec.get("max_frames") is not None:
        command.extend(["--max-frames", str(spec["max_frames"])])
    if spec.get("frame_interval") is not None:
        command.extend(["--frame-interval", str(spec["frame_interval"])])
    if spec.get("force"):
        command.append("--force")
    if spec.get("verbose"):
        command.append("--verbose")
    return command


def _run_analyze(spec: dict[str, Any], state: dict[str, Any]) -> dict[str, Any]:
    repo_dir = _repo_dir(spec)
    output_dir = _new_run_dir(spec)
    output_dir.mkdir(parents=True, exist_ok=True)
    command = _build_analyze_command(spec, output_dir)
    timeout = int(spec.get("command_timeout_seconds") or 1200)
    env = os.environ.copy()
    result = _run_command(command, env=env, cwd=repo_dir, timeout=timeout)
    report = output_dir / "report.md"
    analysis = output_dir / "analysis.json"
    return {
        "success": result["success"] and report.exists() and analysis.exists(),
        "summary": "VideoLens analysis completed" if result["success"] else "VideoLens analysis failed",
        "action": "analyze",
        "mode": str(spec.get("mode") or "general"),
        "source": str(spec.get("source") or ""),
        "output_dir": str(output_dir),
        "report_path": str(report) if report.exists() else None,
        "analysis_path": str(analysis) if analysis.exists() else None,
        "command": result["command"],
        "returncode": result["returncode"],
        "stdout": result["stdout"],
        "stderr": result["stderr"],
        "state": state,
    }


def run(context: dict[str, Any]) -> dict[str, Any]:
    try:
        task_payload = _fetch_task_payload(context)
        spec = _parse_task_spec(str(task_payload.get("pre_instructions") or ""))
        action = str(spec.get("action") or "preflight").strip()
        state = _collect_runtime_state(spec)

        if action == "preflight":
            return _build_preflight_report(spec, state)

        if action in SPEND_ACTIONS and not bool(spec.get("allow_credit_spend")):
            return {
                "success": False,
                "summary": f"Refusing {action} without allow_credit_spend=true",
                "action": action,
                "state": state,
                "requested_spec": spec,
                "error": "Set allow_credit_spend to true in pre_instructions to confirm you want a credit-spending VideoLens action.",
            }

        if action == "bootstrap":
            repo_result = _ensure_repo(spec)
            if not repo_result["success"]:
                return {"success": False, "summary": "Failed to bootstrap VideoLens repo", "action": action, "step": "git", "result": repo_result, "state": _collect_runtime_state(spec)}
            runtime_result = _ensure_runtime(spec)
            return {
                "success": runtime_result["success"],
                "summary": "VideoLens bootstrap completed" if runtime_result["success"] else "Failed to bootstrap VideoLens runtime",
                "action": action,
                "git": repo_result,
                "runtime": runtime_result,
                "state": _collect_runtime_state(spec),
            }

        if action == "analyze":
            repo_result = _ensure_repo(spec)
            if not repo_result["success"]:
                return {"success": False, "summary": "Failed to prepare VideoLens repo", "action": action, "step": "git", "result": repo_result, "state": _collect_runtime_state(spec)}
            runtime_result = _ensure_runtime(spec)
            if not runtime_result["success"]:
                return {"success": False, "summary": "Failed to prepare VideoLens runtime", "action": action, "step": "runtime", "result": runtime_result, "state": _collect_runtime_state(spec)}
            state = _collect_runtime_state(spec)
            if not state["openai_api_key_present"]:
                return {"success": False, "summary": "OPENAI_API_KEY is missing", "action": action, "state": state, "error": "Provide OPENAI_API_KEY before running VideoLens analysis."}
            return _run_analyze(spec, state)

        raise ValueError(f"Unsupported action: {action}")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return {"success": False, "summary": f"Failed to load task configuration: HTTP {exc.code}", "error": body or str(exc), "action": "preflight"}
    except Exception as exc:
        return {"success": False, "summary": f"VideoLens wrapper failed: {exc}", "error": str(exc), "context": _json_safe(context)}
