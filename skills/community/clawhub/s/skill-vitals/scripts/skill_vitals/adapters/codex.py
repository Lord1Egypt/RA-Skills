"""Codex app-server runtime probing and evidence reconciliation."""

import json
import os
import shutil
import subprocess
import sys
import threading
from pathlib import Path

from ..util import norm


def find_codex_executable(env=None):
    """Prefer the native binary because npm shims can detach redirected stdio."""
    environment = os.environ if env is None else env
    override = environment.get("SKILL_VITALS_CODEX_EXECUTABLE")
    if override:
        return override
    direct = shutil.which("codex.exe", path=environment.get("PATH"))
    if direct:
        return direct
    shim = (shutil.which("codex.cmd", path=environment.get("PATH")) or
            shutil.which("codex", path=environment.get("PATH")))
    if not shim:
        return None
    npm_root = Path(shim).parent
    candidates = list(npm_root.glob(
        "node_modules/@openai/codex/node_modules/@openai/codex-*/vendor/**/codex.exe"))
    return str(candidates[0]) if candidates else shim


def read_codex_runtime(cwd: Path, timeout=20, env=None, executable_finder=None):
    """Read Codex's authoritative Skill catalog through app-server skills/list."""
    state = {"available": False, "source": "codex app-server skills/list",
             "cwd": norm(cwd.resolve()), "skills": [], "errors": []}
    finder = executable_finder or find_codex_executable
    try:
        executable = finder(env=env)
    except TypeError:
        executable = finder()
    if not executable:
        state["errors"].append("codex executable not found")
        return state
    messages = [
        {"method": "initialize", "id": 1, "params": {"clientInfo": {
            "name": "skill-vitals", "title": "Skill Vitals", "version": "0.1.0"}}},
        {"method": "initialized", "params": {}},
        {"method": "skills/list", "id": 2, "params": {
            "cwds": [str(cwd.resolve())], "forceReload": True}},
    ]
    lines = []
    initialized_ready = threading.Event()
    response_ready = threading.Event()
    process = None
    try:
        command = ([sys.executable, executable]
                   if Path(executable).suffix.lower() == ".py" else [executable])
        process = subprocess.Popen(
            command + ["app-server", "--stdio"], stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            bufsize=1, cwd=str(cwd), env=env)

        def read_responses():
            for line in process.stdout:
                lines.append(line)
                try:
                    response_id = json.loads(line).get("id")
                    if response_id == 1:
                        initialized_ready.set()
                    elif response_id == 2:
                        response_ready.set()
                except json.JSONDecodeError:
                    pass

        reader = threading.Thread(target=read_responses, daemon=True)
        reader.start()
        process.stdin.write(json.dumps(messages[0], separators=(",", ":")) + "\n")
        process.stdin.flush()
        if not initialized_ready.wait(min(timeout, 5)):
            process.kill()
            process.wait(5)
            state["errors"].append("app-server initialize timed out")
            return state
        for message in messages[1:]:
            process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
            process.stdin.flush()
        response_ready.wait(timeout)
        process.terminate()
        try:
            process.wait(5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(5)
        reader.join(2)
    except (OSError, subprocess.SubprocessError) as exc:
        state["errors"].append(f"app-server failed: {exc}")
        return state

    response = None
    for line in lines:
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if message.get("id") == 2:
            response = message
            break
    if response is None:
        detail = (process.stderr.read().strip()[-500:] or
                  f"exit={process.returncode}, no skills/list response")
        state["errors"].append(detail)
        return state
    if response.get("error"):
        state["errors"].append(str(response["error"]))
        return state
    entries = response.get("result", {}).get("data", [])
    for entry in entries:
        if norm(entry.get("cwd", "")) != state["cwd"]:
            continue
        state["skills"].extend(entry.get("skills", []))
        state["errors"].extend(str(error) for error in entry.get("errors", []))
    state["available"] = True
    state["executable"] = norm(executable)
    return state


def apply_codex_runtime(skills, runtime, scan_skill):
    """Add runtime-only Skills and overlay authoritative metadata by path."""
    by_path = {(skill["host_family"], norm(Path(skill["path"]).resolve())): skill
               for skill in skills}
    for metadata in runtime.get("skills", []):
        skill_file = Path(metadata.get("path", ""))
        if not skill_file.is_file():
            continue
        key = ("codex", norm(skill_file.parent.resolve()))
        record = by_path.get(key)
        if record is None:
            record = scan_skill(skill_file.parent, "codex", set(), {}, False)
            if not record:
                continue
            skills.append(record)
            by_path[key] = record
        record.update({
            "name": metadata.get("name", record["name"]),
            "description": metadata.get("description", record["description"]),
            "description_chars": len(metadata.get("description", record["description"])),
            "loaded": bool(metadata.get("enabled", True)),
            "loaded_reason": ("codex-app-server-enabled"
                              if metadata.get("enabled", True)
                              else "codex-app-server-disabled"),
            "level": metadata.get("scope", record["level"]),
            "codex_scope": metadata.get("scope"),
            "codex_interface": metadata.get("interface"),
            "codex_dependencies": metadata.get("dependencies"),
            "runtime_verified": True,
        })
    return skills
